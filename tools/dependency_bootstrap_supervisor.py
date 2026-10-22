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
        self.interrupted = False
        self.interruption_stages = []
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
        except BaseException as error:
            with self.lock:
                self.error = 'read_error'
                if not isinstance(error, Exception):
                    self.interrupted = True
                    self.interruption_stages.append('read')
        finally:
            try:
                self.stream.close()
            except BaseException as error:
                with self.lock:
                    self.close_error = True
                    if not isinstance(error, Exception):
                        self.interrupted = True
                        self.interruption_stages.append('close')
            self.done.set()
            self.wake.set()

    def snapshot(self):
        with self.lock:
            return dict(data=bytes(self.data), eof=self.eof,
                        overflow=self.overflow, error=self.error,
                        close_error=self.close_error, done=self.done.is_set(),
                        interrupted=self.interrupted,
                        interruption_stages=list(self.interruption_stages))


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
    Recoverable BaseException interruptions are swallowed only to return facts
    the caller can persist.  They never permit success or automatic retry.  An
    exception before Popen returns leaves spawn outcome unknown, without a PID.
    Repeated asynchronous interruption, abrupt termination, and OS call latency
    cannot be given a hard wall-clock guarantee by this cooperative helper.
    """
    _arguments(argv, timeout, stdout_limit, stderr_limit)
    result = dict(status='needs_review', returncode=None, pid=None,
                  stdout=b'', stderr=b'', timed_out=False,
                  stdout_overflow=False, stderr_overflow=False,
                  read_errors={}, close_errors=[], stdout_eof=False,
                  stderr_eof=False, reader_threads_terminal=False,
                  process_terminal=False, error_code=None,
                  spawn_attempted=False, spawn_outcome_unknown=False,
                  interrupted=False, interruption_stages=[],
                  reader_start_attempted=[],
                  cleanup=dict(attempted=False, kill_attempted=False,
                               kill_error=False, reap_attempted=False,
                               reap_error=False, reader_join_attempted=[],
                               reader_join_errors=[], bound_seconds=CLEANUP_SECONDS),
                  automatic_retry=False)
    failure = None

    def fail(code, stage=None, error=None):
        nonlocal failure
        if failure is None:
            failure = code
        if error is not None and not isinstance(error, Exception):
            result['interrupted'] = True
            if stage not in result['interruption_stages']:
                result['interruption_stages'].append(stage)

    start = time.monotonic()
    result['spawn_attempted'] = True
    try:
        process = subprocess.Popen(list(argv), stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=False)
    except BaseException as error:
        fail('spawn_outcome_unknown', 'spawn', error)
        result['status'] = 'needs_process_reconciliation'
        result['spawn_outcome_unknown'] = True
        result['error_code'] = failure
        return result
    readers = {}
    last_snapshots = {}
    terminal = None
    stage = 'pid'
    try:
        result['pid'] = process.pid
        stage = 'reader_create'
        wake = threading.Event()
        for name, cap in (('stdout', stdout_limit), ('stderr', stderr_limit)):
            readers[name] = _Drain(getattr(process, name), cap, wake)
        stage = 'reader_start'
        for name, reader in readers.items():
            result['reader_start_attempted'].append(name)
            reader.thread.start()
        deadline = start + timeout
        while True:
            stage = 'poll'
            try:
                observed = process.poll()
                if observed is not None:
                    if type(observed) is not int:
                        fail('process_poll_error')
                        break
                    terminal = observed
            except BaseException as error:
                fail('process_poll_error', stage, error)
                break
            stage = 'snapshot'
            current = {name: reader.snapshot() for name, reader in readers.items()}
            last_snapshots.update(current)
            if any(row['overflow'] for row in current.values()):
                fail('stream_overflow')
                break
            if any(row['error'] or row['close_error'] for row in current.values()):
                fail('stream_read_error')
                break
            if any(row['done'] and not row['eof'] for row in current.values()):
                fail('stream_incomplete')
                break
            if terminal is not None and all(row['eof'] and row['done'] for row in current.values()):
                if terminal != 0:
                    fail('nonzero_exit')
                break
            stage = 'wait'
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result['timed_out'] = True
                fail('timeout')
                break
            wake.wait(min(0.01, remaining))
            wake.clear()
    except BaseException as error:
        code = 'reader_start_error' if stage in ('reader_create', 'reader_start') else 'supervision_error'
        fail(code, stage, error)

    cleanup = result['cleanup']
    try:
        cleanup_deadline = time.monotonic() + CLEANUP_SECONDS
    except BaseException as error:
        cleanup_deadline = None
        fail('cleanup_clock_error', 'cleanup_clock', error)

    def cleanup_remaining():
        if cleanup_deadline is None:
            return 0
        try:
            return max(0, cleanup_deadline - time.monotonic())
        except BaseException as error:
            fail('cleanup_clock_error', 'cleanup_clock', error)
            return 0

    def join_readers():
        for name, reader in readers.items():
            if name in cleanup['reader_join_attempted']:
                continue
            try:
                if reader.thread.ident is not None:
                    # Mark before the call: an interrupted join is not retried.
                    cleanup['reader_join_attempted'].append(name)
                    reader.thread.join(cleanup_remaining())
            except BaseException as error:
                cleanup['reader_join_errors'].append(name)
                fail('reader_join_error', 'join', error)

    if failure is None:
        join_readers()
        try:
            if any(reader.thread.is_alive() for reader in readers.values()):
                fail('reader_cleanup_incomplete')
        except BaseException as error:
            fail('reader_state_error', 'reader_state', error)
    if failure:
        cleanup['attempted'] = True
        if terminal is None and not cleanup['kill_attempted']:
            cleanup['kill_attempted'] = True
            try:
                process.kill()
            except BaseException as error:
                cleanup['kill_error'] = True
                fail('process_kill_error', 'kill', error)
        if not cleanup['reap_attempted']:
            cleanup['reap_attempted'] = True
            try:
                observed = process.wait(timeout=cleanup_remaining())
                if type(observed) is int:
                    terminal = observed
                else:
                    cleanup['reap_error'] = True
                    fail('process_reap_error')
            except BaseException as error:
                cleanup['reap_error'] = True
                fail('process_reap_error', 'reap', error)
        join_readers()

    snapshots = {}
    for name, reader in readers.items():
        try:
            row = reader.snapshot()
        except BaseException as error:
            fail('reader_snapshot_error', 'reader_snapshot', error)
            row = dict(last_snapshots.get(name, dict(data=b'', eof=False,
                overflow=False, close_error=False, done=False)))
            row['error'] = 'snapshot_error'
        snapshots[name] = row
        result[name] = row['data']
        result[name + '_eof'] = row['eof']
        result[name + '_overflow'] = row['overflow']
        if row['error']:
            result['read_errors'][name] = row['error']
        if row['close_error']:
            result['close_errors'].append(name)
        if row.get('interrupted'):
            result['interrupted'] = True
            for item in row.get('interruption_stages', []):
                label = name + '.' + item
                if label not in result['interruption_stages']:
                    result['interruption_stages'].append(label)
    try:
        result['reader_threads_terminal'] = len(readers) == 2 and all(
            reader.done.is_set() and not reader.thread.is_alive() for reader in readers.values())
    except BaseException as error:
        fail('reader_state_error', 'reader_state', error)
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
