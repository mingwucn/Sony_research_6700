"""Bounded host-only subprocess supervision for authored synthetic children.

This helper does not authorize an argv, authenticate its executable or sources,
or establish any camera, native-dependency or feature capability.  The ordinary
CLI refuses.  Callers must review and bind their synthetic command separately.
"""
import math
import os
import subprocess
import threading
import time


CLEANUP_SECONDS = 2.0
READ_BYTES = 4096


class _Drain:
    """One bounded stream, with snapshots independent of a blocked reader."""

    def __init__(self, stream, limit, wake):
        self.stream = stream
        self.limit = limit
        self.wake = wake
        self.lock = threading.Lock()
        self.data = bytearray()
        self.eof = False
        self.overflow = False
        self.error = None
        self.close_error = False
        self.done = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        try:
            while True:
                with self.lock:
                    remaining = self.limit - len(self.data)
                # One byte beyond the remaining allowance detects overflow;
                # no read or retained buffer can grow with the child's output.
                amount = min(READ_BYTES, remaining + 1)
                read1 = getattr(self.stream, 'read1', None)
                chunk = read1(amount) if callable(read1) else os.read(self.stream.fileno(), amount)
                if type(chunk) is not bytes or len(chunk) > amount:
                    with self.lock:
                        self.error = 'read_contract_error'
                    break
                with self.lock:
                    if not chunk:
                        self.eof = True
                        break
                    self.data.extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        self.overflow = True
                        break
        except Exception:
            with self.lock:
                self.error = 'read_error'
        finally:
            try:
                self.stream.close()
            except Exception:
                with self.lock:
                    self.close_error = True
            self.done.set()
            self.wake.set()

    def snapshot(self):
        with self.lock:
            return dict(data=bytes(self.data), eof=self.eof,
                        overflow=self.overflow, error=self.error,
                        close_error=self.close_error, done=self.done.is_set())


def _arguments(argv, timeout, stdout_limit, stderr_limit):
    if type(argv) is not list or not argv or any(type(arg) is not str or not arg or '\x00' in arg for arg in argv):
        raise ValueError('argv_contract')
    if type(timeout) not in (int, float) or not 0 < timeout <= 30 or not math.isfinite(timeout):
        raise ValueError('timeout_bound')
    for cap in (stdout_limit, stderr_limit):
        if type(cap) is not int or not 1 <= cap <= 65536:
            raise ValueError('stream_bound')


def run_once(argv, *, timeout=30, stdout_limit=65536, stderr_limit=65536):
    """Launch once, drain both pipes concurrently and return bounded facts.

    A timeout, overflow or read/cleanup error is sticky even when the child
    subsequently exits zero.  Success needs a genuinely observed zero exit and
    EOF and actual thread termination on both readers.  Normal completion joins
    both readers.  Failure allows one kill and one bounded reap attempt, with
    at most two further seconds shared by all joins and reaping.  A
    still-blocked reader is left daemonized, never forcibly closed from another
    thread; its incomplete cleanup is reported.  This is a process/pipe bound,
    not an operating-system memory, descendant-process or native-code sandbox.
    """
    _arguments(argv, timeout, stdout_limit, stderr_limit)
    result = dict(status='needs_review', returncode=None, pid=None,
                  stdout=b'', stderr=b'', timed_out=False,
                  stdout_overflow=False, stderr_overflow=False,
                  read_errors={}, close_errors=[], stdout_eof=False,
                  stderr_eof=False, reader_threads_terminal=False,
                  process_terminal=False, error_code=None,
                  cleanup=dict(attempted=False, kill_attempted=False,
                               kill_error=False, reap_attempted=False,
                               reap_error=False, bound_seconds=CLEANUP_SECONDS),
                  automatic_retry=False)
    start = time.monotonic()
    try:
        process = subprocess.Popen(list(argv), stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=False)
    except Exception:
        result['error_code'] = 'spawn_error'
        return result
    result['pid'] = process.pid
    wake = threading.Event()
    readers = {}
    terminal = None
    failure = None
    try:
        readers = {'stdout': _Drain(process.stdout, stdout_limit, wake),
                   'stderr': _Drain(process.stderr, stderr_limit, wake)}
        for reader in readers.values():
            reader.thread.start()
        deadline = start + timeout
        while True:
            try:
                observed = process.poll()
                if observed is not None:
                    if type(observed) is not int:
                        failure = 'process_poll_error'
                        break
                    terminal = observed
            except Exception:
                failure = 'process_poll_error'
                break
            current = {name: reader.snapshot() for name, reader in readers.items()}
            if any(row['overflow'] for row in current.values()):
                failure = 'stream_overflow'
                break
            if any(row['error'] or row['close_error'] for row in current.values()):
                failure = 'stream_read_error'
                break
            if any(row['done'] and not row['eof'] for row in current.values()):
                failure = 'stream_incomplete'
                break
            if terminal is not None and all(row['eof'] and row['done'] for row in current.values()):
                if terminal != 0:
                    failure = 'nonzero_exit'
                break
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result['timed_out'] = True
                failure = 'timeout'
                break
            wake.wait(min(0.01, remaining))
            wake.clear()
    except Exception:
        failure = 'reader_start_error'

    cleanup_deadline = time.monotonic() + CLEANUP_SECONDS
    joined = False
    if failure is None:
        joined = True
        try:
            for reader in readers.values():
                if reader.thread.ident is not None:
                    reader.thread.join(max(0, cleanup_deadline - time.monotonic()))
            if any(reader.thread.is_alive() for reader in readers.values()):
                failure = 'reader_cleanup_incomplete'
        except Exception:
            failure = 'reader_join_error'
    if failure:
        cleanup = result['cleanup']
        cleanup['attempted'] = True
        if terminal is None:
            cleanup['kill_attempted'] = True
            try:
                process.kill()
            except Exception:
                cleanup['kill_error'] = True
        cleanup['reap_attempted'] = True
        try:
            observed = process.wait(timeout=max(0, cleanup_deadline - time.monotonic()))
            if type(observed) is int:
                terminal = observed
            else:
                cleanup['reap_error'] = True
        except Exception:
            cleanup['reap_error'] = True
        if not joined:
            try:
                for reader in readers.values():
                    if reader.thread.ident is not None:
                        reader.thread.join(max(0, cleanup_deadline - time.monotonic()))
            except Exception:
                # The original failure remains sticky; a join failure cannot
                # establish terminal readers or justify an automatic retry.
                failure = 'reader_join_error'

    snapshots = {name: reader.snapshot() for name, reader in readers.items()}
    for name, row in snapshots.items():
        result[name] = row['data']
        result[name + '_eof'] = row['eof']
        result[name + '_overflow'] = row['overflow']
        if row['error']:
            result['read_errors'][name] = row['error']
        if row['close_error']:
            result['close_errors'].append(name)
    result['reader_threads_terminal'] = len(readers) == 2 and all(
        reader.done.is_set() and not reader.thread.is_alive() for reader in readers.values())
    result['returncode'] = terminal
    result['process_terminal'] = terminal is not None
    result['error_code'] = failure
    if terminal is None:
        result['status'] = 'needs_process_reconciliation'
    elif failure is None and terminal == 0 and result['reader_threads_terminal'] and all(
            row['eof'] and not row['error'] and not row['overflow'] and not row['close_error']
            for row in snapshots.values()):
        result['status'] = 'complete'
    return result


if __name__ == '__main__':
    raise SystemExit(2)
