"""Run reviewed opt-in synthetic FTPS tests on literal 127.0.0.1 only.

Use the newly prepared private venv's python with -I. No host, camera, source
spool or credential argument exists. All fixtures/results remain in a NEW
private directory. This starts local listeners and loads reviewed native TLS
dependencies; it is intentionally outside ordinary tests/ and CI discovery.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True, help="NEW directory below repository private/")
    args = parser.parse_args()
    if not sys.flags.isolated or sys.prefix == sys.base_prefix:
        parser.error("use prepared private environment Python with -I")
    sys.path.insert(0, str(ROOT))  # Only this reviewed repository is added.
    from tools.prepare_ftps_lab import verify

    lock, expected, lock_hash = verify(args.artifact_dir)
    environment = Path(sys.prefix).resolve()
    preparation = json.loads((environment / "host-lab-preparation.json").read_text(encoding="utf-8"))
    if preparation["host_lab_lock_sha256"] != lock_hash:
        raise RuntimeError("environment was prepared with a different lock")
    packages = environment / "Lib" / "site-packages"
    for name, content in expected.items():
        actual = packages.joinpath(*name.split("/"))
        if actual.is_symlink() or actual.read_bytes() != content:
            raise RuntimeError("prepared package bytes changed")
    workspace = Path(os.path.abspath(args.workspace))
    private = (ROOT / "private").resolve()
    # These are trusted owner-controlled directories, not an attacker sandbox.
    if (workspace == private or not workspace.resolve().is_relative_to(private)
            or workspace.exists() or workspace.is_symlink() or not workspace.parent.is_dir()):
        parser.error("workspace must be a NEW directory below private/ with an existing parent")
    workspace.mkdir(exist_ok=False)
    journal = workspace / "journal.jsonl"
    with journal.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"event": "prepared", "utc": datetime.now(timezone.utc).isoformat(),
            "lock_sha256": lock_hash, "python": sys.version.splitlines()[0], "isolation": True,
            "endpoint": "127.0.0.1 only, ephemeral ports", "camera_commands": [],
            "synthetic_only": True}) + "\n")
    from lab_tests import test_ftps_lab
    test_ftps_lab.WORKSPACE = workspace
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_ftps_lab)
    with (workspace / "unittest.txt").open("x", encoding="utf-8") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, failfast=True).run(suite)
    live = sum(server._thread is not None and server._thread.is_alive()
               for server in test_ftps_lab.SERVERS)
    listeners = sum(server._server.socket is not None and server._server.socket.fileno() != -1
                    for server in test_ftps_lab.SERVERS)
    success = result.wasSuccessful() and live == 0 and listeners == 0
    outcome = {"event": "result", "utc": datetime.now(timezone.utc).isoformat(),
               "total": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
               "skipped": len(result.skipped), "exit_code": 0 if success else 1,
               "lab_servers_started": len(test_ftps_lab.SERVERS),
               "live_lab_threads": live, "open_lab_control_listeners": listeners,
               "camera_commands": [], "native_ftp_or_bridge_validated": False}
    with journal.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(outcome) + "\n")
    print(json.dumps(outcome))
    if not success:
        print("Inspect retained private unittest.txt and fixtures before another new run.", file=sys.stderr)
    return outcome["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
