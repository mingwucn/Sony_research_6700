from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.offline_inventory import InventoryError, build_inventory, hash_artifact, main


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

    def test_known_sha_and_length(self):
        result = hash_artifact(self.source)
        self.assertEqual(result["bytes"], 16)
        self.assertEqual(result["sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())

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

    def test_symlink_refused(self):
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
