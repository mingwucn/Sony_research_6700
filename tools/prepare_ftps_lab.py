"""Verify pinned host-lab artifacts and prepare a NEW private venv without pip.

Uses only the standard library. No downloads, package imports, build hooks,
certificate changes, sockets or server execution occur. No camera API exists.
"""

from __future__ import annotations

import argparse
import base64
import csv
from email.parser import BytesParser
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import sys
import tarfile
import venv
import zipfile


LOCK_PATH = Path(__file__).resolve().parents[1] / "references" / "host-lab.lock.json"
NAMES = {"pyftpdlib", "pyasynchat", "pyasyncore", "pyOpenSSL", "cryptography", "cffi", "pycparser"}


class LabError(ValueError):
    """Artifact, environment or host preconditions are not satisfied."""


def _object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise LabError("duplicate lock key")
        result[key] = value
    return result


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _name(value: str) -> str:
    if (not isinstance(value, str) or not value or len(value) > 512 or "\\" in value
            or any(c in value for c in '<>:"|?*') or any(ord(c) < 32 or ord(c) > 126 for c in value)
            or value.startswith("/") or any(p in {"", ".", ".."} for p in value.split("/"))):
        raise LabError("unsafe archive path")
    if any(p.endswith((".", " ")) for p in value.split("/")):
        raise LabError("ambiguous Windows archive path")
    for component in value.split("/"):
        device = component.split(".", 1)[0].upper()
        if device in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(r"(?:COM|LPT)[1-9]", device):
            raise LabError("reserved Windows archive path")
    if value.lower().endswith(".pth") or PurePosixPath(value).name.lower() in {"sitecustomize.py", "usercustomize.py"}:
        raise LabError("unreviewed Python startup hook")
    return value


def _plain(path: Path) -> None:
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        raise LabError("links and junctions are refused")


def _metadata(data: bytes, artifact: dict) -> None:
    metadata = BytesParser().parsebytes(data)
    normal = lambda value: re.sub(r"[-_.]+", "-", value).lower()
    if (normal(metadata.get("Name", "")) != normal(artifact["name"])
            or metadata.get("Version") != artifact["version"]
            or sorted(metadata.get_all("Requires-Dist", [])) != sorted(artifact["artifact_requires_dist"])):
        raise LabError("artifact metadata differs from reviewed lock")


def _wheel(data: bytes, artifact: dict, limits: dict) -> dict[str, bytes]:
    output: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        if len(infos) > limits["member_count"]:
            raise LabError("too many wheel members")
        names = [_name(info.filename) for info in infos]
        if len(names) != len(set(name.casefold() for name in names)):
            raise LabError("duplicate or case-colliding wheel member")
        if sum(info.file_size for info in infos) > limits["total_uncompressed_bytes"]:
            raise LabError("wheel expansion bound exceeded")
        for info, name in zip(infos, names):
            file_type = stat.S_IFMT(info.external_attr >> 16)
            if info.is_dir() or file_type not in {0, stat.S_IFREG} or info.flag_bits & 1:
                raise LabError("non-regular or encrypted wheel member")
            if not 0 <= info.file_size <= limits["member_bytes"]:
                raise LabError("wheel member size bound exceeded")
            if name.split("/", 1)[0] not in artifact["allowed_roots"]:
                raise LabError("unexpected wheel package root")
            content = archive.read(info)
            if len(content) != info.file_size:
                raise LabError("wheel member length mismatch")
            output[name] = content
        records = [name for name in names if name.endswith(".dist-info/RECORD")]
        if len(records) != 1:
            raise LabError("wheel must have exactly one RECORD")
        rows = list(csv.reader(io.StringIO(output[records[0]].decode("utf-8"))))
        if any(len(row) != 3 for row in rows):
            raise LabError("malformed wheel RECORD")
        if len(rows) != len({row[0] for row in rows}) or {row[0] for row in rows} != set(names):
            raise LabError("wheel RECORD does not cover exactly every member")
        for name, digest, size in rows:
            if name == records[0]:
                if digest or size:
                    raise LabError("unexpected self-hash in wheel RECORD")
                continue
            expected = "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(output[name]).digest()).rstrip(b"=").decode("ascii")
            if digest != expected or size != str(len(output[name])):
                raise LabError("wheel RECORD hash/size mismatch")
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise LabError("wheel must have exactly one METADATA")
        _metadata(output[metadata_names[0]], artifact)
        actual_native = sorted(name for name in names if name.lower().endswith((".pyd", ".dll", ".so")))
        if actual_native != sorted(artifact["native_files"]):
            raise LabError("native payload list differs from reviewed lock")
        for name in actual_native:
            content = output[name]
            if len(content) < 64 or content[:2] != b"MZ":
                raise LabError("unexpected native payload format")
            pe = int.from_bytes(content[60:64], "little")
            if (pe + 6 > len(content) or content[pe:pe + 4] != b"PE\0\0"
                    or int.from_bytes(content[pe + 4:pe + 6], "little") != 0x8664):
                raise LabError("native payload is not PE AMD64")
        if any(name not in output for name in artifact["license_files"]):
            raise LabError("reviewed wheel licence missing")
    return output


def _source(data: bytes, artifact: dict, limits: dict) -> dict[str, bytes]:
    output: dict[str, bytes] = {}
    exports = artifact["source_exports"]
    prefix = "pyftpdlib-2.2.0/"
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        if len(members) > limits["member_count"] or sum(m.size for m in members) > limits["total_uncompressed_bytes"]:
            raise LabError("source archive expansion bound exceeded")
        seen: set[str] = set()
        found: set[str] = set()
        runtime_members: set[str] = set()
        for member in members:
            name = _name(member.name.rstrip("/"))
            if name.casefold() in seen or not (name == prefix.rstrip("/") or name.startswith(prefix)):
                raise LabError("duplicate or unexpected source archive member")
            seen.add(name.casefold())
            if not member.isfile() and not member.isdir():
                raise LabError("source archive links/devices are refused")
            if not 0 <= member.size <= limits["member_bytes"]:
                raise LabError("source member size bound exceeded")
            if member.isfile() and name.startswith(prefix + "pyftpdlib/"):
                runtime_members.add(name)
            if name not in exports:
                continue
            if not member.isfile():
                raise LabError("source export must be a regular file")
            stream = archive.extractfile(member)
            if stream is None:
                raise LabError("missing source export")
            with stream:
                content = stream.read(limits["member_bytes"] + 1)
            if len(content) != exports[name]["size"] or _digest(content) != exports[name]["sha256"]:
                raise LabError("source export differs from reviewed Git-matching bytes")
            relative = name[len(prefix):]
            if not relative.startswith("pyftpdlib/"):
                relative = "pyftpdlib-2.2.0.hostlab-info/" + relative
            output[_name(relative)] = content
            found.add(name)
        if found != set(exports) or runtime_members != {name for name in exports if name.startswith(prefix + "pyftpdlib/")}:
            raise LabError("source export set differs from reviewed lock")
        _metadata(output["pyftpdlib-2.2.0.hostlab-info/PKG-INFO"], artifact)
    return output


def verify(artifact_dir: Path) -> tuple[dict, dict[str, bytes], str]:
    """Return fully verified extraction bytes; no files or processes are created."""
    raw_lock = LOCK_PATH.read_bytes()
    lock = json.loads(raw_lock, object_pairs_hook=_object)
    runtime = lock["runtime"]
    if (lock["schema_version"] != 1 or sys.implementation.name != runtime["implementation"]
            or tuple(sys.version_info[:3]) != tuple(runtime["python_version"])
            or os.name != runtime["os_name"] or platform.machine().upper() != runtime["machine"]
            or runtime["include_system_site_packages"] is not False or runtime["pip"] is not False):
        raise LabError("this lock requires CPython 3.13.12 on Windows AMD64")
    artifacts = lock["artifacts"]
    if len(artifacts) != 7 or {item["name"] for item in artifacts} != NAMES:
        raise LabError("unexpected host-lab artifact set")
    _plain(artifact_dir)
    if not artifact_dir.is_dir():
        raise LabError("artifact directory is unavailable")
    output: dict[str, bytes] = {}
    folded: set[str] = set()
    for artifact in artifacts:
        filename = _name(artifact["filename"])
        if "/" in filename:
            raise LabError("artifact filename must be a basename")
        path = artifact_dir / filename
        _plain(path)
        if not path.is_file() or path.stat().st_size != artifact["size"]:
            raise LabError("locked artifact missing or wrong length")
        with path.open("rb") as stream:
            data = stream.read(artifact["size"] + 1)
        if len(data) != artifact["size"] or _digest(data) != artifact["sha256"]:
            raise LabError("locked whole-artifact SHA-256 mismatch")
        extracted = _wheel(data, artifact, lock["limits"]) if filename.endswith(".whl") else _source(data, artifact, lock["limits"])
        for name, content in extracted.items():
            if name.casefold() in folded:
                raise LabError("package extraction paths collide")
            folded.add(name.casefold())
            output[name] = content
    if sum(map(len, output.values())) > lock["limits"]["total_uncompressed_bytes"]:
        raise LabError("total extraction bound exceeded")
    # A file must not be another member's containing directory.
    if any(parent.as_posix().casefold() in folded for name in output for parent in PurePosixPath(name).parents if str(parent) != "."):
        raise LabError("file/directory extraction collision")
    return lock, output, _digest(raw_lock)


def prepare(artifact_dir: Path, environment: Path) -> dict:
    lock, output, lock_hash = verify(artifact_dir)
    environment = Path(os.path.abspath(environment))
    if environment.exists() or environment.is_symlink():
        raise LabError("refuse to overwrite an existing environment")
    _plain(environment.parent)
    if not environment.parent.is_dir():
        raise LabError("environment parent must already exist")
    # Exclusively reserve the new directory before venv writes its own files.
    environment.mkdir(exist_ok=False)
    venv.EnvBuilder(system_site_packages=False, clear=False, symlinks=False,
                    with_pip=False, upgrade_deps=False).create(environment)
    packages = environment / "Lib" / "site-packages"
    for name, content in sorted(output.items()):
        destination = packages.joinpath(*PurePosixPath(_name(name)).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(content)
    record = {
        "schema_version": 1, "host_lab_lock_sha256": lock_hash,
        "python": sys.version.splitlines()[0], "extracted_files": len(output),
        "artifacts": [{key: item[key] for key in ("name", "version", "filename", "sha256")} for item in lock["artifacts"]],
        "third_party_package_imported": False, "build_or_setup_hook_executed": False,
        "pip_or_global_install_performed": False, "server_or_socket_started": False,
        "camera_commands": [], "publication_rights_complete": False,
    }
    with (environment / "host-lab-preparation.json").open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--environment", type=Path, help="NEW directory; its parent must already exist")
    parser.add_argument("--verify-only", action="store_true", help="verify archives without creating an environment")
    args = parser.parse_args()
    if args.verify_only == (args.environment is not None):
        parser.error("choose --verify-only or --environment, exclusively")
    try:
        if args.verify_only:
            lock, files, lock_hash = verify(args.artifact_dir)
            print(json.dumps({"verified_artifacts": len(lock["artifacts"]), "verified_extraction_files": len(files), "lock_sha256": lock_hash}))
        else:
            print(json.dumps(prepare(args.artifact_dir, args.environment)))
    except (LabError, OSError, KeyError, TypeError, zipfile.BadZipFile, tarfile.TarError, json.JSONDecodeError) as error:
        # Fixed error categories keep private locations and archive text out of output.
        print("Host lab preparation refused: " + type(error).__name__, file=sys.stderr)
        print("Any new partial environment is retained for local review; it is never reused automatically.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
