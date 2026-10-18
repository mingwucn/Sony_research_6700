from contextlib import contextmanager, redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.offline_inventory import (
    InventoryError, build_inventory, hash_artifact, inspect_artifact, main,
)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "private-body-serial.bin"
        self.source.write_bytes(b"synthetic-only\x00\x01")

    def report(self, entries=None):
        return build_inventory("ILCE-6700", "UNKNOWN", "body-01",
                               entries or [("ap", self.source)], "synthetic")

    @staticmethod
    def file_stat(**changes):
        fields = dict(st_mode=stat.S_IFREG | 0o600, st_dev=1, st_ino=23,
                      st_size=3, st_mtime_ns=100, st_ctime_ns=200)
        fields.update(changes)
        return SimpleNamespace(**fields)

    @contextmanager
    def mocked_file(self, *, initial=None, before=None, after=None,
                    named_after=None, chunks=None):
        initial = initial or self.file_stat()
        before = before or self.file_stat()
        after = after or before
        named_after = named_after or initial
        with (patch("tools.offline_inventory.Path.lstat",
                    side_effect=[initial, named_after]),
              patch("tools.offline_inventory.os.open", return_value=321) as opened,
              patch("tools.offline_inventory.os.fstat", side_effect=[before, after]),
              patch("tools.offline_inventory.os.read",
                    side_effect=chunks or [b"abc", b""]) as read,
              patch("tools.offline_inventory.os.close") as closed):
            yield opened, read, closed

    def test_known_sha_and_length(self):
        result = hash_artifact(self.source)
        self.assertEqual(result["bytes"], 16)
        self.assertEqual(result["sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())

    def test_inspection_returns_prefix_from_same_hashed_read(self):
        with self.mocked_file(chunks=[b"a", b"bc", b""]) as (opened, read, closed):
            result, prefix = inspect_artifact(self.source, prefix_limit=2)
        self.assertEqual(result, {"bytes": 3,
                                 "sha256": hashlib.sha256(b"abc").hexdigest()})
        self.assertEqual(prefix, b"ab")
        self.assertEqual(opened.call_count, 1)
        self.assertEqual(read.call_count, 3)
        closed.assert_called_once_with(321)

    def test_inspection_default_prefix_is_bounded(self):
        content = b"synthetic" * 1024
        self.source.write_bytes(content)
        result, prefix = inspect_artifact(self.source)
        self.assertEqual(prefix, content[:4096])
        self.assertEqual(len(prefix), 4096)
        self.assertEqual(result, {"bytes": len(content),
                                 "sha256": hashlib.sha256(content).hexdigest()})

    def test_inspection_short_and_zero_prefixes(self):
        for limit, expected in [(0, b""), (4096, b"abc")]:
            with self.subTest(limit=limit), self.mocked_file():
                result, prefix = inspect_artifact(self.source, prefix_limit=limit)
            self.assertEqual(prefix, expected)
            self.assertEqual(result["bytes"], 3)

    def test_invalid_prefix_limits_refused_before_open(self):
        for limit in [-1, 4097, 1.5, "3", True, None]:
            with (self.subTest(limit=limit),
                  patch("tools.offline_inventory.os.open") as opened):
                with self.assertRaises(InventoryError):
                    inspect_artifact(self.source, prefix_limit=limit)
                opened.assert_not_called()

    def test_cross_api_ctime_difference_is_allowed_for_unchanged_file(self):
        path_stat = self.file_stat(st_ctime_ns=200)
        descriptor_stat = self.file_stat(st_ctime_ns=999)
        with self.mocked_file(initial=path_stat, before=descriptor_stat,
                              after=descriptor_stat, named_after=path_stat):
            result = hash_artifact(self.source)
        self.assertEqual(result, {"bytes": 3,
                                 "sha256": hashlib.sha256(b"abc").hexdigest()})

    def test_same_api_ctime_change_refused_despite_cross_api_difference(self):
        for api in ["path", "descriptor"]:
            with self.subTest(api=api):
                initial = self.file_stat(st_ctime_ns=200)
                before = self.file_stat(st_ctime_ns=999)
                named_after = self.file_stat(st_ctime_ns=201) if api == "path" else initial
                after = self.file_stat(st_ctime_ns=1000) if api == "descriptor" else before
                with self.mocked_file(initial=initial, before=before, after=after,
                                      named_after=named_after):
                    with self.assertRaisesRegex(InventoryError, "during reading"):
                        hash_artifact(self.source)

    def test_replacement_or_change_before_open_refused(self):
        changes = [dict(st_dev=2), dict(st_ino=24), dict(st_size=4),
                   dict(st_mtime_ns=101), dict(st_mode=stat.S_IFDIR | 0o700)]
        for changed in changes:
            with self.subTest(changed=changed), self.mocked_file(
                    before=self.file_stat(**changed)) as (_, _, closed):
                with self.assertRaisesRegex(InventoryError, "before reading"):
                    hash_artifact(self.source)
            closed.assert_called_once_with(321)

    def test_descriptor_mutations_during_read_refused(self):
        # Includes equal-size content changes with restored mtime but changed ctime.
        changes = [dict(st_dev=2), dict(st_ino=24), dict(st_size=4),
                   dict(st_mtime_ns=101), dict(st_ctime_ns=201)]
        for changed in changes:
            with self.subTest(changed=changed), self.mocked_file(
                    after=self.file_stat(**changed)):
                with self.assertRaisesRegex(InventoryError, "during reading"):
                    hash_artifact(self.source)

    def test_path_replacement_or_mutation_after_open_refused(self):
        changes = [dict(st_dev=2), dict(st_ino=24), dict(st_size=4),
                   dict(st_mtime_ns=101), dict(st_ctime_ns=201),
                   dict(st_mode=stat.S_IFLNK | 0o777)]
        for changed in changes:
            with self.subTest(changed=changed), self.mocked_file(
                    named_after=self.file_stat(**changed)):
                with self.assertRaisesRegex(InventoryError, "during reading"):
                    hash_artifact(self.source)

    def test_short_read_refused_even_when_metadata_is_unchanged(self):
        with self.mocked_file(chunks=[b"ab", b""]):
            with self.assertRaisesRegex(InventoryError, "during reading"):
                hash_artifact(self.source)

    def test_read_error_is_sanitized_and_descriptor_is_closed(self):
        with self.mocked_file(chunks=[OSError("private-serial-and-path")]) as (_, _, closed):
            with self.assertRaises(InventoryError) as caught:
                inspect_artifact(self.source)
        self.assertNotIn("private", str(caught.exception))
        closed.assert_called_once_with(321)

    def test_deterministic_sorted_output(self):
        self.assertEqual(self.report([("cp", self.source), ("ap", self.source)]),
                         self.report([("ap", self.source), ("cp", self.source)]))

    def test_no_paths_or_filename_in_report(self):
        text = json.dumps(self.report())
        self.assertNotIn(str(self.root), text)
        self.assertNotIn(self.source.name, text)

    def test_never_claims_compatibility(self):
        result = self.report()
        self.assertEqual(result["compatibility"], "UNVERIFIED")
        self.assertFalse(result["camera_access_performed"])

    def test_does_not_modify_source(self):
        before = self.source.read_bytes()
        self.report()
        self.assertEqual(before, self.source.read_bytes())

    def test_duplicate_labels_refused(self):
        with self.assertRaises(InventoryError):
            self.report([("ap", self.source), ("ap", self.source)])

    def test_empty_file_refused(self):
        self.source.write_bytes(b"")
        with self.assertRaises(InventoryError):
            self.report()

    def test_directory_refused(self):
        with self.assertRaises(InventoryError):
            self.report([("ap", self.root)])

    def test_missing_file_refused_without_path_leak(self):
        with self.assertRaises(InventoryError) as caught:
            hash_artifact(self.root / "secret-missing.bin")
        self.assertNotIn("secret", str(caught.exception))

    def test_symlink_refused_without_privilege_or_open(self):
        with self.mocked_file(initial=self.file_stat(
                st_mode=stat.S_IFLNK | 0o777)) as (opened, _, closed):
            with self.assertRaisesRegex(InventoryError, "not a symlink or device"):
                hash_artifact(self.source)
        opened.assert_not_called()
        closed.assert_not_called()

    def test_real_symlink_refused_when_available(self):
        link = self.root / "link.bin"
        try:
            link.symlink_to(self.source)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable")
        with self.assertRaises(InventoryError):
            hash_artifact(link)

    def test_mutation_during_read_refused(self):
        real_read = os.read
        changed = False

        def mutate(fd, size):
            nonlocal changed
            data = real_read(fd, size)
            if not changed:
                changed = True
                with self.source.open("ab") as out:
                    out.write(b"changed")
            return data

        with patch("tools.offline_inventory.os.read", side_effect=mutate):
            with self.assertRaises(InventoryError):
                hash_artifact(self.source)

    def test_real_same_size_mutation_during_read_refused(self):
        initial = self.source.stat()
        real_read = os.read
        changed = False

        def mutate(fd, size):
            nonlocal changed
            data = real_read(fd, size)
            if not changed:
                changed = True
                self.source.write_bytes(b"X" * initial.st_size)
                # Make the fixture independent of the host timestamp resolution.
                os.utime(self.source, ns=(initial.st_atime_ns,
                                         initial.st_mtime_ns + 1_000_000_000))
            return data

        with patch("tools.offline_inventory.os.read", side_effect=mutate):
            with self.assertRaisesRegex(InventoryError, "during reading"):
                hash_artifact(self.source)
        self.assertEqual(self.source.stat().st_size, initial.st_size)

    def test_invalid_label_refused(self):
        with self.assertRaises(InventoryError):
            self.report([("../../private", self.source)])

    def test_no_artifacts_refused(self):
        with self.assertRaises(InventoryError):
            build_inventory("ILCE-6700", "UNKNOWN", "body-01", [])

    def test_cli_success(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--model", "ILCE-6700", "--firmware", "UNKNOWN",
                         "--alias", "body-01", "--kind", "synthetic",
                         "--artifact", "ap=" + str(self.source)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["artifacts"][0]["label"], "ap")

    def test_cli_failure_has_no_partial_report(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(["--model", "ILCE-6700", "--firmware", "UNKNOWN",
                         "--alias", "body-01", "--artifact", "ap=" + str(self.source),
                         "--artifact", "cp=" + str(self.root / "missing.bin")])
        self.assertEqual(code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("inventory refused", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
