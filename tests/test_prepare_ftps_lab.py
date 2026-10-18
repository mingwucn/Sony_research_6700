"""Synthetic archive/preparation guards; no dependencies, sockets or venv run."""

import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from tools import prepare_ftps_lab as subject


LIMITS = {"member_count": 100, "member_bytes": 4096, "total_uncompressed_bytes": 65536}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def wheel_fixture(*, name="demo", root="demo", files=(), native=(), record_change=None):
    """Build invented wheel bytes with complete, correctly hashed RECORD rows."""
    info = name + "-1.0.dist-info"
    members = [(root + "/__init__.py", b"# invented fixture; never imported\n"),
               (info + "/METADATA", ("Name: " + name + "\nVersion: 1.0\n\n").encode()),
               (info + "/LICENSE", b"Authored synthetic fixture text only\n"), *files]
    record_name = info + "/RECORD"
    rows = [[path, "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode(), str(len(data))]
            for path, data in members]
    rows.append([record_name, "", ""])
    if record_change:
        record_change(rows)
    stream = io.StringIO(newline="")
    csv.writer(stream, lineterminator="\n").writerows(rows)
    members.append((record_name, stream.getvalue().encode()))
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, data in members:
            entry = zipfile.ZipInfo(path)
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o600) << 16
            archive.writestr(entry, data)
    artifact = {"name": name, "version": "1.0", "artifact_requires_dist": [],
                "allowed_roots": [root, info], "native_files": list(native),
                "license_files": [info + "/LICENSE"]}
    return output.getvalue(), artifact


def source_fixture(*, extra=(), excluded_export=None, corrupt_export=None):
    prefix = "pyftpdlib-2.2.0/"
    regular = [(prefix + "pyftpdlib/__init__.py", b"# invented source fixture\n"),
               (prefix + "PKG-INFO", b"Name: pyftpdlib\nVersion: 2.2.0\n\n")]
    exports = {path: {"size": len(data), "sha256": digest(data)} for path, data in regular}
    if excluded_export:
        regular = [(path, data) for path, data in regular if path != prefix + excluded_export]
    if corrupt_export:
        regular = [(path, b"changed" if path == prefix + corrupt_export else data) for path, data in regular]
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:gz") as archive:
        for path, data in regular:
            member = tarfile.TarInfo(path)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
        for path, kind, data in extra:
            member = tarfile.TarInfo(path)
            member.type = kind
            if kind == tarfile.REGTYPE:
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
            else:
                member.linkname = "outside"
                archive.addfile(member)
    artifact = {"name": "pyftpdlib", "version": "2.2.0", "artifact_requires_dist": [],
                "source_exports": exports}
    return output.getvalue(), artifact


def synthetic_pe(machine=0x8664):
    data = bytearray(128)
    data[:2] = b"MZ"
    data[60:64] = (80).to_bytes(4, "little")
    data[80:84] = b"PE\0\0"
    data[84:86] = machine.to_bytes(2, "little")
    return bytes(data)  # Header fixture only; never loaded or executed.


class PrepareLabArchiveTests(unittest.TestCase):
    def test_synthetic_wheel_accepts_exact_bytes_record_metadata_and_licence(self):
        data, artifact = wheel_fixture()
        result = subject._wheel(data, artifact, LIMITS)
        self.assertEqual(result["demo/__init__.py"], b"# invented fixture; never imported\n")
        self.assertEqual(len(result), 4)

    def test_wheel_traversal_ads_windows_devices_and_startup_hooks_refused(self):
        paths = ("../escape.py", "demo/../escape.py", "/absolute.py", "demo\\escape.py",
                 "demo/file:stream", "demo/CON.txt", "demo/NUL", "demo/COM1.bin",
                 "demo/LPT9.txt", "demo/trailing.", "demo/trailing ", "demo/trigger.pth",
                 "demo/SITECUSTOMIZE.PY", "demo/usercustomize.py")
        for path in paths:
            with self.subTest(path=path), self.assertRaises(subject.LabError):
                data, artifact = wheel_fixture(files=((path, b"invented"),))
                subject._wheel(data, artifact, LIMITS)

    def test_wheel_case_collisions_refused_before_extraction(self):
        data, artifact = wheel_fixture(files=(("demo/Upper.py", b"one"), ("demo/upper.py", b"two")))
        with self.assertRaisesRegex(subject.LabError, "case-colliding"):
            subject._wheel(data, artifact, LIMITS)

    def test_wheel_record_hash_size_coverage_duplicate_and_shape_refused(self):
        mutations = (lambda rows: rows[0].__setitem__(1, "sha256=wrong"),
                     lambda rows: rows[0].__setitem__(2, "999"),
                     lambda rows: rows.pop(0),
                     lambda rows: rows.append(list(rows[0])),
                     lambda rows: rows[-1].__setitem__(1, "sha256=self"),
                     lambda rows: rows[0].append("extra"))
        for index, mutation in enumerate(mutations):
            with self.subTest(case=index), self.assertRaisesRegex(subject.LabError, "RECORD"):
                data, artifact = wheel_fixture(record_change=mutation)
                subject._wheel(data, artifact, LIMITS)

    def test_wheel_metadata_and_missing_locked_licence_refused(self):
        data, artifact = wheel_fixture()
        artifact["version"] = "2.0"
        with self.assertRaisesRegex(subject.LabError, "metadata"):
            subject._wheel(data, artifact, LIMITS)
        artifact["version"] = "1.0"
        artifact["license_files"].append("demo-1.0.dist-info/MISSING")
        with self.assertRaisesRegex(subject.LabError, "licence missing"):
            subject._wheel(data, artifact, LIMITS)

    def test_locked_native_payload_must_exist_and_have_amd64_pe_header(self):
        path = "demo/native.pyd"
        data, artifact = wheel_fixture(native=(path,))
        with self.assertRaisesRegex(subject.LabError, "native payload list"):
            subject._wheel(data, artifact, LIMITS)
        for payload in (b"not a PE", synthetic_pe(0x14C), b"MZ" + b"\0" * 126):
            with self.subTest(payload=payload[:2]), self.assertRaises(subject.LabError):
                data, artifact = wheel_fixture(files=((path, payload),), native=(path,))
                subject._wheel(data, artifact, LIMITS)
        data, artifact = wheel_fixture(files=((path, synthetic_pe()),), native=(path,))
        self.assertEqual(subject._wheel(data, artifact, LIMITS)[path], synthetic_pe())

    def test_unlisted_native_payload_and_archive_expansion_refused(self):
        data, artifact = wheel_fixture(files=(("demo/native.pyd", synthetic_pe()),))
        with self.assertRaisesRegex(subject.LabError, "native payload list"):
            subject._wheel(data, artifact, LIMITS)
        data, artifact = wheel_fixture()
        for limits in (dict(LIMITS, member_count=1), dict(LIMITS, member_bytes=1),
                       dict(LIMITS, total_uncompressed_bytes=1)):
            with self.subTest(limits=limits), self.assertRaises(subject.LabError):
                subject._wheel(data, artifact, limits)

    def test_source_exports_are_exact_authored_bytes(self):
        data, artifact = source_fixture()
        result = subject._source(data, artifact, LIMITS)
        self.assertEqual(result["pyftpdlib/__init__.py"], b"# invented source fixture\n")
        self.assertIn("pyftpdlib-2.2.0.hostlab-info/PKG-INFO", result)

    def test_source_traversal_ads_devices_startup_hooks_and_case_collision_refused(self):
        prefix = "pyftpdlib-2.2.0/"
        for name in (prefix + "../escape", prefix + "file:stream", prefix + "AUX.txt",
                     prefix + "startup.pth", prefix + "sitecustomize.py", prefix + "PYFTPDLIB/__INIT__.PY"):
            with self.subTest(name=name), self.assertRaises(subject.LabError):
                data, artifact = source_fixture(extra=((name, tarfile.REGTYPE, b"fixture"),))
                subject._source(data, artifact, LIMITS)

    def test_source_links_devices_unlocked_runtime_and_incomplete_exports_refused(self):
        prefix = "pyftpdlib-2.2.0/"
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE, tarfile.FIFOTYPE):
            with self.subTest(kind=kind), self.assertRaisesRegex(subject.LabError, "links/devices"):
                data, artifact = source_fixture(extra=((prefix + "link", kind, b""),))
                subject._source(data, artifact, LIMITS)
        data, artifact = source_fixture(extra=((prefix + "pyftpdlib/unreviewed.py", tarfile.REGTYPE, b"fixture"),))
        with self.assertRaisesRegex(subject.LabError, "export set"):
            subject._source(data, artifact, LIMITS)
        data, artifact = source_fixture(excluded_export="pyftpdlib/__init__.py")
        with self.assertRaisesRegex(subject.LabError, "export set"):
            subject._source(data, artifact, LIMITS)
        data, artifact = source_fixture(corrupt_export="pyftpdlib/__init__.py")
        with self.assertRaisesRegex(subject.LabError, "reviewed Git-matching bytes"):
            subject._source(data, artifact, LIMITS)


class PrepareLabBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifacts = self.root / "synthetic-artifacts"
        self.artifacts.mkdir()
        self.lock_path = self.root / "synthetic-lock.json"
        self.lock = {"schema_version": 1, "limits": dict(LIMITS), "runtime": {
            "implementation": sys.implementation.name, "python_version": list(sys.version_info[:3]),
            "os_name": os.name, "machine": platform.machine().upper(),
            "include_system_site_packages": False, "pip": False}, "artifacts": []}
        for index, name in enumerate(sorted(subject.NAMES)):
            data, artifact = wheel_fixture(name=name, root=f"invented{index}")
            artifact.update(filename=f"invented{index}.whl", size=len(data), sha256=digest(data))
            self.lock["artifacts"].append(artifact)
            (self.artifacts / artifact["filename"]).write_bytes(data)
        self.save_lock()
        self.lock_patch = patch.object(subject, "LOCK_PATH", self.lock_path)
        self.lock_patch.start()
        self.addCleanup(self.lock_patch.stop)
        self.venv_patch = patch.object(subject.venv, "EnvBuilder", side_effect=AssertionError("tests must not create a venv"))
        self.builder = self.venv_patch.start()
        self.addCleanup(self.venv_patch.stop)

    def save_lock(self):
        self.lock_path.write_text(json.dumps(self.lock), encoding="utf-8")

    def test_verify_returns_only_exact_synthetic_bytes_without_environment_creation(self):
        lock, output, lock_hash = subject.verify(self.artifacts)
        self.assertEqual(len(lock["artifacts"]), 7)
        self.assertEqual(len(output), 28)
        self.assertEqual(lock_hash, digest(self.lock_path.read_bytes()))
        self.builder.assert_not_called()
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["synthetic-artifacts", "synthetic-lock.json"])

    def test_whole_archive_hash_missing_file_and_runtime_mismatch_refused(self):
        first = self.artifacts / self.lock["artifacts"][0]["filename"]
        original = first.read_bytes()
        first.write_bytes(b"X" + original[1:])
        with self.assertRaisesRegex(subject.LabError, "whole-artifact SHA-256"):
            subject.verify(self.artifacts)
        first.unlink()
        with self.assertRaisesRegex(subject.LabError, "missing or wrong length"):
            subject.verify(self.artifacts)
        self.lock["runtime"]["machine"] = "MISMATCHED-SYNTHETIC-HOST"
        self.save_lock()
        with self.assertRaisesRegex(subject.LabError, "lock requires"):
            subject.verify(self.artifacts)
        self.builder.assert_not_called()

    def test_cross_package_case_collision_refused_even_with_valid_archive_hashes(self):
        last = self.lock["artifacts"][-1]
        data, replacement = wheel_fixture(name=last["name"], root="INVENTED0")
        replacement.update(filename=last["filename"], size=len(data), sha256=digest(data))
        self.lock["artifacts"][-1] = replacement
        (self.artifacts / replacement["filename"]).write_bytes(data)
        self.save_lock()
        with self.assertRaisesRegex(subject.LabError, "paths collide"):
            subject.verify(self.artifacts)

    def test_file_cannot_also_be_an_extraction_parent_directory(self):
        last = self.lock["artifacts"][-1]
        data, replacement = wheel_fixture(name=last["name"], root="invented6", files=(
            ("invented6/parent", b"ordinary file"), ("invented6/parent/child.py", b"invented child")))
        replacement.update(filename=last["filename"], size=len(data), sha256=digest(data))
        self.lock["artifacts"][-1] = replacement
        (self.artifacts / replacement["filename"]).write_bytes(data)
        self.save_lock()
        with self.assertRaisesRegex(subject.LabError, "file/directory extraction collision"):
            subject.verify(self.artifacts)

    def test_existing_environment_directory_and_file_preserved_before_venv_call(self):
        existing_dir = self.root / "existing-dir"
        existing_dir.mkdir()
        marker = existing_dir / "evidence.txt"
        marker.write_bytes(b"preserve existing evidence")
        existing_file = self.root / "existing-file"
        existing_file.write_bytes(b"preserve existing file")
        with patch.object(subject, "verify", return_value=({}, {}, "a" * 64)):
            for destination in (existing_dir, existing_file):
                with self.subTest(destination=destination.name), self.assertRaisesRegex(subject.LabError, "overwrite"):
                    subject.prepare(self.artifacts, destination)
        self.assertEqual(marker.read_bytes(), b"preserve existing evidence")
        self.assertEqual(existing_file.read_bytes(), b"preserve existing file")
        self.builder.assert_not_called()

    def test_exclusive_directory_reservation_race_refused_before_venv_call(self):
        destination = self.root / "never-created"
        with patch.object(subject, "verify", return_value=({}, {}, "a" * 64)), \
                patch.object(Path, "mkdir", side_effect=FileExistsError("synthetic concurrent creator")) as mkdir:
            with self.assertRaises(FileExistsError):
                subject.prepare(self.artifacts, destination)
        mkdir.assert_called_once_with(exist_ok=False)
        self.builder.assert_not_called()
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
