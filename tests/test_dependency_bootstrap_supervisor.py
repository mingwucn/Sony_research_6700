"""Invented child programs and stream/process doubles; no device or native input."""
import io
from pathlib import Path
import subprocess
import sys
import threading
import time
import unittest
from unittest.mock import patch

from tools import dependency_bootstrap_supervisor as subject


def child(code):
    return [sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', code]


class _Process:
    def __init__(self, *, stdout=None, stderr=None, poll=None, wait=0):
        self.pid = 654321
        self.stdout = io.BytesIO(b'') if stdout is None else stdout
        self.stderr = io.BytesIO(b'') if stderr is None else stderr
        self.observed = poll
        self.reaped = wait
        self.kills = 0
        self.waits = 0
        self.kill_error = None

    def poll(self):
        return self.observed

    def kill(self):
        self.kills += 1
        if self.kill_error:
            raise self.kill_error

    def wait(self, timeout):
        self.waits += 1
        if isinstance(self.reaped, Exception):
            raise self.reaped
        return self.reaped


class _FaultStream(io.BytesIO):
    def read1(self, amount):
        raise OSError('invented sensitive detail must never be returned')


class _ReadSizes(io.BytesIO):
    def __init__(self, raw):
        super().__init__(raw)
        self.amounts = []

    def read1(self, amount):
        self.amounts.append(amount)
        return super().read1(amount)


class _BlockingStream(io.BytesIO):
    def __init__(self):
        super().__init__(b'')
        self.release = threading.Event()
        self.finished = threading.Event()

    def read1(self, amount):
        self.release.wait(5)
        self.finished.set()
        return b''


class _JoinThread:
    def __init__(self, end_on_join):
        self.ident = 987654
        self.end_on_join = end_on_join
        self.alive = True
        self.joins = []

    def start(self):
        pass

    def join(self, timeout):
        self.joins.append(timeout)
        if self.end_on_join:
            self.alive = False

    def is_alive(self):
        return self.alive


class _DoneDrain:
    end_on_join = False
    instances = []

    def __init__(self, stream, limit, wake):
        self.done = threading.Event()
        self.done.set()
        self.thread = _JoinThread(self.end_on_join)
        self.instances.append(self)

    def snapshot(self):
        return dict(data=b'', eof=True, overflow=False, error=None,
                    close_error=False, done=True)


class BootstrapSupervisorTests(unittest.TestCase):
    def invoke(self, code, **kwargs):
        return subject.run_once(child(code), **kwargs)

    def assert_bounded(self, result, stdout_limit=65536, stderr_limit=65536):
        self.assertLessEqual(len(result['stdout']), stdout_limit)
        self.assertLessEqual(len(result['stderr']), stderr_limit)
        self.assertFalse(result['automatic_retry'])

    def test_empty_zero_exit_requires_both_eof_and_observed_process_exit(self):
        result = self.invoke('pass')
        self.assertEqual((result['status'], result['returncode']), ('complete', 0))
        self.assertTrue(result['process_terminal'])
        self.assertTrue(result['stdout_eof'] and result['stderr_eof'])
        self.assertTrue(result['reader_threads_terminal'])
        self.assertEqual(result['read_errors'], {})
        self.assertFalse(result['cleanup']['attempted'])
        self.assert_bounded(result)

    def test_exact_limits_then_eof_are_complete(self):
        result = self.invoke('import os\nos.write(1,b"a"*8192)\nos.write(2,b"b"*4096)',
                             stdout_limit=8192, stderr_limit=4096)
        self.assertEqual((result['status'], result['returncode']), ('complete', 0))
        self.assertEqual(result['stdout'], b'a' * 8192)
        self.assertEqual(result['stderr'], b'b' * 4096)
        self.assertFalse(result['stdout_overflow'] or result['stderr_overflow'])

    def test_stdout_flood_stops_at_cap(self):
        result = self.invoke('import os\nwhile True: os.write(1,b"a"*4096)', stdout_limit=9000)
        self.assertEqual(result['status'], 'needs_review')
        self.assertTrue(result['stdout_overflow'])
        self.assertEqual(result['stdout'], b'a' * 9000)
        self.assertEqual(result['error_code'], 'stream_overflow')
        self.assertTrue(result['process_terminal'])
        self.assert_bounded(result, stdout_limit=9000)

    def test_stderr_flood_stops_at_cap(self):
        result = self.invoke('import os\nwhile True: os.write(2,b"b"*4096)', stderr_limit=5000)
        self.assertEqual(result['status'], 'needs_review')
        self.assertTrue(result['stderr_overflow'])
        self.assertEqual(result['stderr'], b'b' * 5000)
        self.assert_bounded(result, stderr_limit=5000)

    def test_both_streams_are_drained_while_child_lives(self):
        # A serial read-to-EOF deadlocks: stdout stays open while stderr fills.
        code = ('import os\n'
                'for i in range(8):\n'
                ' os.write(1,b"a"*4096)\n'
                ' os.write(2,b"b"*4096)\n')
        result = self.invoke(code, timeout=10)
        self.assertEqual((result['status'], result['returncode']), ('complete', 0))
        self.assertEqual(result['stdout'], b'a' * 32768)
        self.assertEqual(result['stderr'], b'b' * 32768)
        self.assertFalse(result['timed_out'])

    def test_nonzero_exit_is_not_complete_even_with_both_eof(self):
        result = self.invoke('import sys\nprint("ordinary")\nsys.exit(7)')
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 7))
        self.assertEqual(result['stdout'].strip(), b'ordinary')
        self.assertEqual(result['error_code'], 'nonzero_exit')
        self.assertTrue(result['stdout_eof'] and result['stderr_eof'])

    def test_timeout_kills_and_reaps_once_without_restart(self):
        start = time.monotonic()
        result = self.invoke('import time\ntime.sleep(10)', timeout=0.2)
        self.assertEqual(result['status'], 'needs_review')
        self.assertTrue(result['timed_out'])
        self.assertTrue(result['cleanup']['kill_attempted'])
        self.assertTrue(result['cleanup']['reap_attempted'])
        self.assertTrue(result['process_terminal'])
        self.assertLess(time.monotonic() - start, 5)
        self.assert_bounded(result)

    def test_overflow_remains_sticky_when_reap_reports_zero(self):
        process = _Process(stdout=io.BytesIO(b'ab'), wait=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process) as popen:
            result = subject.run_once(['invented'], stdout_limit=1)
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
        self.assertTrue(result['stdout_overflow'])
        self.assertEqual((process.kills, process.waits), (1, 1))
        popen.assert_called_once()

    def test_timeout_remains_sticky_when_reap_reports_zero(self):
        process = _Process(wait=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process) as popen:
            result = subject.run_once(['invented'], timeout=0.01)
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
        self.assertTrue(result['timed_out'])
        self.assertEqual((process.kills, process.waits), (1, 1))
        popen.assert_called_once()

    def test_read_exception_stays_sticky_at_zero_exit_and_is_sanitized(self):
        process = _Process(stdout=_FaultStream(), poll=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process):
            result = subject.run_once(['invented'])
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
        self.assertEqual(result['read_errors'], {'stdout': 'read_error'})
        self.assertNotIn('sensitive', repr(result))
        self.assertEqual((process.kills, process.waits), (0, 1))

    def test_unknown_kill_and_reap_preserve_pid_for_reconciliation(self):
        process = _Process(stdout=io.BytesIO(b'ab'), wait=OSError('invented unknown reap'))
        process.kill_error = OSError('invented unknown kill')
        with patch.object(subject.subprocess, 'Popen', return_value=process) as popen:
            result = subject.run_once(['invented'], stdout_limit=1)
        self.assertEqual(result['status'], 'needs_process_reconciliation')
        self.assertIsNone(result['returncode'])
        self.assertEqual(result['pid'], 654321)
        self.assertTrue(result['cleanup']['kill_error'] and result['cleanup']['reap_error'])
        self.assertEqual((process.kills, process.waits), (1, 1))
        popen.assert_called_once()

    def test_kill_error_is_sticky_but_successful_reap_establishes_terminal(self):
        process = _Process(stdout=io.BytesIO(b'ab'), wait=0)
        process.kill_error = OSError('invented kill error')
        with patch.object(subject.subprocess, 'Popen', return_value=process):
            result = subject.run_once(['invented'], stdout_limit=1)
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
        self.assertTrue(result['cleanup']['kill_error'])
        self.assertTrue(result['process_terminal'])

    def test_missing_eof_is_never_complete_and_cleanup_does_not_block_on_reader(self):
        stream = _BlockingStream()
        process = _Process(stdout=stream, poll=0)
        start = time.monotonic()
        try:
            with patch.object(subject.subprocess, 'Popen', return_value=process), \
                    patch.object(subject, 'CLEANUP_SECONDS', 0.03):
                result = subject.run_once(['invented'], timeout=0.01)
            self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
            self.assertTrue(result['timed_out'])
            self.assertFalse(result['stdout_eof'])
            self.assertFalse(result['reader_threads_terminal'])
            self.assertLess(time.monotonic() - start, 0.8)
        finally:
            stream.release.set()
            self.assertTrue(stream.finished.wait(1))

    def test_done_eof_but_live_reader_cannot_be_promoted_to_complete(self):
        process = _Process(poll=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process), \
                patch.object(subject, '_Drain', _DoneDrain), \
                patch.object(_DoneDrain, 'instances', []):
            result = subject.run_once(['invented'])
            readers = list(_DoneDrain.instances)
        self.assertEqual((result['status'], result['returncode']), ('needs_review', 0))
        self.assertEqual(result['error_code'], 'reader_cleanup_incomplete')
        self.assertTrue(result['stdout_eof'] and result['stderr_eof'])
        self.assertFalse(result['reader_threads_terminal'])
        self.assertEqual((process.kills, process.waits), (0, 1))
        self.assertEqual([len(reader.thread.joins) for reader in readers], [1, 1])
        first, second = [reader.thread.joins[0] for reader in readers]
        self.assertTrue(0 <= second <= first <= subject.CLEANUP_SECONDS)

    def test_normal_success_joins_done_readers_and_confirms_thread_termination(self):
        process = _Process(poll=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process), \
                patch.object(subject, '_Drain', _DoneDrain), \
                patch.object(_DoneDrain, 'end_on_join', True), \
                patch.object(_DoneDrain, 'instances', []):
            result = subject.run_once(['invented'])
            readers = list(_DoneDrain.instances)
        self.assertEqual((result['status'], result['returncode']), ('complete', 0))
        self.assertTrue(result['reader_threads_terminal'])
        self.assertEqual([len(reader.thread.joins) for reader in readers], [1, 1])
        self.assertTrue(all(not reader.thread.is_alive() for reader in readers))
        self.assertEqual((process.kills, process.waits), (0, 0))

    def test_read_sizes_are_remaining_plus_one_and_never_over_4096(self):
        stream = _ReadSizes(b'a' * 9001)
        process = _Process(stdout=stream, wait=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process):
            result = subject.run_once(['invented'], stdout_limit=9000)
        self.assertEqual(stream.amounts, [4096, 4096, 809])
        self.assertTrue(result['stdout_overflow'])
        self.assertEqual(len(result['stdout']), 9000)

    def test_exact_cap_requires_one_byte_probe_for_eof(self):
        stream = _ReadSizes(b'a' * 4096)
        process = _Process(stdout=stream, poll=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process):
            result = subject.run_once(['invented'], stdout_limit=4096)
        self.assertEqual(stream.amounts, [4096, 1])
        self.assertEqual(result['status'], 'complete')

    def test_spawn_is_once_no_shell_no_stdin_and_environment_is_not_replaced(self):
        argv = ['invented', 'argument']
        process = _Process(poll=0)
        with patch.object(subject.subprocess, 'Popen', return_value=process) as popen:
            result = subject.run_once(argv)
        self.assertEqual(result['status'], 'complete')
        popen.assert_called_once_with(argv, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     shell=False)
        self.assertEqual(argv, ['invented', 'argument'])

    def test_spawn_failure_returns_fixed_sanitized_code_without_retry(self):
        with patch.object(subject.subprocess, 'Popen', side_effect=OSError('invented secret path')) as popen:
            result = subject.run_once(['invented'])
        self.assertEqual(result['status'], 'needs_review')
        self.assertEqual(result['error_code'], 'spawn_error')
        self.assertIsNone(result['pid'])
        self.assertIsNone(result['returncode'])
        self.assertNotIn('secret', repr(result))
        popen.assert_called_once()

    def test_invalid_argv_refuses_before_spawn(self):
        for argv in (None, 'invented', (), [], [''], [True], ['a\x00b'], ['a', 1]):
            with self.subTest(argv=argv), patch.object(subject.subprocess, 'Popen') as popen:
                with self.assertRaisesRegex(ValueError, '^argv_contract$'):
                    subject.run_once(argv)
                popen.assert_not_called()

    def test_invalid_timeout_refuses_before_spawn(self):
        for timeout in (False, True, 0, -1, 31, 10**1000, float('inf'), float('nan'), '1', None):
            with self.subTest(timeout=timeout), patch.object(subject.subprocess, 'Popen') as popen:
                with self.assertRaisesRegex(ValueError, '^timeout_bound$'):
                    subject.run_once(['invented'], timeout=timeout)
                popen.assert_not_called()

    def test_invalid_caps_refuse_before_spawn(self):
        for key in ('stdout_limit', 'stderr_limit'):
            for cap in (False, True, 0, -1, 65537, 1.0, '1', None):
                with self.subTest(key=key, cap=cap), patch.object(subject.subprocess, 'Popen') as popen:
                    with self.assertRaisesRegex(ValueError, '^stream_bound$'):
                        subject.run_once(['invented'], **{key: cap})
                    popen.assert_not_called()

    def test_ordinary_cli_refuses(self):
        result = subprocess.run(child('import runpy\nrunpy.run_path(' +
                                repr(str(Path(subject.__file__).resolve())) + ',run_name="__main__")'),
                                stdin=subprocess.DEVNULL, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((result.stdout, result.stderr), (b'', b''))


if __name__ == '__main__':
    unittest.main()
