"""Invented event/file qualification; no bootstrap or dependency activation."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import dependency_bootstrap_journal as subject


class Explosive:
    def __repr__(self):
        raise AssertionError('repr must not be called')

    def __str__(self):
        raise AssertionError('str must not be called')

    def __iter__(self):
        raise AssertionError('iteration must not be called')


class ExplosiveList(list):
    def __iter__(self):
        raise AssertionError('subclass iteration must not be called')


class ExplosiveDict(dict):
    def __iter__(self):
        raise AssertionError('subclass iteration must not be called')

    def items(self):
        raise AssertionError('subclass items must not be called')


class JournalTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / 'invented-events.jsonl'
        self.journals = []
        self.addCleanup(self.cleanup_journals)

    def cleanup_journals(self):
        for journal in self.journals:
            if not journal._close_attempted:
                journal.close()

    def journal(self, **kwargs):
        journal = subject.Journal(self.path, **kwargs)
        self.journals.append(journal)
        return journal

    def assert_refused(self, code, function, *args, **kwargs):
        with self.assertRaises(ValueError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.args, (code,))

    @staticmethod
    def line(event='import', args=None, sequence=1):
        row = {'sequence': sequence, 'event': event, 'arguments': subject.encode_value(args)}
        return json.dumps(row, sort_keys=True, separators=(',', ':'),
                          ensure_ascii=True, allow_nan=False).encode('ascii') + b'\n'

    def test_typed_encoding_preserves_scalar_and_container_distinctions(self):
        value = (None, False, 1, '1', b'1', [1], {'z': 1, 'a': None})
        encoded = subject.encode_value(value)
        self.assertEqual(encoded, {'type': 'tuple', 'items': [
            {'type': 'none'}, {'type': 'bool', 'value': False},
            {'type': 'int', 'value': '1'}, {'type': 'str', 'value': '1'},
            {'type': 'bytes', 'hex': '31'},
            {'type': 'list', 'items': [{'type': 'int', 'value': '1'}]},
            {'type': 'dict', 'items': [['a', {'type': 'none'}],
                                     ['z', {'type': 'int', 'value': '1'}]]}]})

    def test_integer_exact_boundaries_and_one_beyond(self):
        limit = 2**128 - 1
        for value in (-limit, 0, limit):
            self.assertEqual(subject.encode_value(value), {'type': 'int', 'value': str(value)})
        for value in (-limit-1, limit+1):
            self.assert_refused('bootstrap_journal_value_bound', subject.encode_value, value)

    def test_string_bytes_and_dictionary_key_bounds(self):
        for value in ('x'*512, b'x'*256, {'k'*128: None}):
            self.assertIsInstance(subject.encode_value(value), dict)
        for value in ('x'*513, b'x'*257, {'k'*129: None}):
            self.assert_refused('bootstrap_journal_value_bound', subject.encode_value, value)

    def test_unsupported_objects_subclasses_and_nonstring_keys_do_not_call_methods(self):
        class ExplosiveInt(int):
            def __str__(self):
                raise AssertionError('subclass int str must not be called')
        class ExplosiveString(str):
            def __lt__(self, other):
                raise AssertionError('subclass key comparison must not be called')
        for value in (Explosive(), ExplosiveList([1]), ExplosiveDict(a=1),
                      ExplosiveInt(1), {ExplosiveString('a'): None}, {1: None},
                      1.0, bytearray(b'a'), set()):
            self.assert_refused('bootstrap_journal_value_type', subject.encode_value, value)

    def test_depth_boundary_and_cyclic_structure_refuse_boundedly(self):
        value = None
        for _ in range(6):
            value = [value]
        self.assertIsInstance(subject.encode_value(value), dict)
        self.assert_refused('bootstrap_journal_depth', subject.encode_value, [value])
        cyclic = []
        cyclic.append(cyclic)
        self.assert_refused('bootstrap_journal_depth', subject.encode_value, cyclic)

    def test_node_boundary_includes_containers_and_dictionary_keys(self):
        self.assertEqual(len(subject.encode_value([None]*127)['items']), 127)
        self.assert_refused('bootstrap_journal_nodes', subject.encode_value, [None]*128)
        self.assertEqual(len(subject.encode_value({str(i): None for i in range(63)})['items']), 63)
        self.assert_refused('bootstrap_journal_nodes', subject.encode_value,
                            {str(i): None for i in range(64)})

    def test_invalid_limits_refuse_before_open(self):
        for name, ceiling in (('event_limit', 256), ('event_bytes_limit', 4096),
                              ('bytes_limit', 262144)):
            for value in (0, -1, True, 1.0, ceiling+1):
                with self.subTest(name=name, value=value), patch.object(subject.os, 'open') as opening:
                    self.assert_refused('bootstrap_journal_limit', subject.Journal,
                                        self.path, **{name: value})
                    opening.assert_not_called()
        self.assertFalse(self.path.exists())

    def test_existing_file_is_preserved_and_never_reopened(self):
        self.path.write_bytes(b'prior evidence\n')
        self.assert_refused('bootstrap_journal_open', subject.Journal, self.path)
        self.assertEqual(self.path.read_bytes(), b'prior evidence\n')

    def test_normal_lines_canonical_durable_and_sequential(self):
        journal = self.journal()
        original_write, original_fsync = os.write, os.fsync
        with patch.object(subject.os, 'write', wraps=original_write) as write, \
             patch.object(subject.os, 'fsync', wraps=original_fsync) as sync:
            first = journal.emit('bootstrap.start', (b'\x00', True))
            second = journal.emit('bootstrap.stop', {'status': 'synthetic'})
        journal.close()
        self.assertEqual(first['sequence'], 1)
        self.assertEqual(second['sequence'], 2)
        self.assertEqual(write.call_count, 2)
        self.assertEqual(sync.call_count, 2)
        raw = self.path.read_bytes()
        self.assertEqual(raw, self.line('bootstrap.start', (b'\x00', True)) +
                         self.line('bootstrap.stop', {'status': 'synthetic'}, 2))
        self.assertEqual(journal.event_count, 2)
        self.assertEqual(journal.bytes_written, len(raw))
        self.assertEqual(journal.state, 'closed')

    def test_exact_event_bytes_boundary_passes_one_byte_less_refuses_without_write(self):
        limit = len(self.line())
        journal = self.journal(event_bytes_limit=limit)
        journal.emit('import', None)
        journal.close()
        second_path = self.path.with_name('smaller.jsonl')
        second = subject.Journal(second_path, event_bytes_limit=limit-1)
        self.journals.append(second)
        with patch.object(subject.os, 'write') as write:
            self.assert_refused('bootstrap_journal_event_bytes', second.emit, 'import', None)
            write.assert_not_called()
        self.assertEqual(second_path.read_bytes(), b'')
        self.assertEqual(second.state, 'needs_review')

    def test_exact_aggregate_bound_passes_next_line_refuses_preserving_prior(self):
        first = self.line()
        second = self.line(sequence=2)
        journal = self.journal(bytes_limit=len(first)+len(second))
        journal.emit('import', None)
        journal.emit('import', None)
        with patch.object(subject.os, 'write') as write:
            self.assert_refused('bootstrap_journal_bytes', journal.emit, 'import', None)
            write.assert_not_called()
        self.assertEqual(self.path.read_bytes(), first+second)
        self.assertEqual(journal.event_count, 2)
        self.assertEqual(journal.failure_code, 'bootstrap_journal_bytes')

    def test_event_count_bound_and_sticky_refusal(self):
        journal = self.journal(event_limit=1)
        journal.emit('import', None)
        self.assert_refused('bootstrap_journal_event_limit', journal.emit, 'import', None)
        with patch.object(subject.os, 'write') as write:
            self.assert_refused('bootstrap_journal_needs_review', journal.emit, 'import', None)
            write.assert_not_called()
        self.assertEqual(journal.failure_code, 'bootstrap_journal_event_limit')
        journal.close()
        self.assertEqual(journal.state, 'needs_review')

    def test_bad_event_or_value_is_sticky_before_any_write(self):
        for index, (event, args, code) in enumerate((
                ('', None, 'bootstrap_journal_event'),
                ('a'*129, None, 'bootstrap_journal_event'),
                ('bad\nevent', None, 'bootstrap_journal_event'),
                ('bad event', None, 'bootstrap_journal_event'),
                ('\u03b1', None, 'bootstrap_journal_event'),
                (Explosive(), None, 'bootstrap_journal_event'),
                ('import', Explosive(), 'bootstrap_journal_value_type'))):
            with self.subTest(index=index):
                path = self.path.with_name(str(index)+'.jsonl')
                journal = subject.Journal(path)
                self.journals.append(journal)
                with patch.object(subject.os, 'write') as write:
                    self.assert_refused(code, journal.emit, event, args)
                    write.assert_not_called()
                self.assertEqual(journal.state, 'needs_review')
                self.assertEqual(journal.failure_code, code)
                self.assertEqual(path.read_bytes(), b'')

    def test_canonical_serialization_failure_is_sticky_without_write(self):
        journal = self.journal()
        with patch.object(subject, '_canonical', side_effect=MemoryError), \
             patch.object(subject.os, 'write') as write:
            self.assert_refused('bootstrap_journal_serialization', journal.emit, 'import', None)
            write.assert_not_called()
        self.assertEqual(journal.state, 'needs_review')

    def test_single_short_write_preserves_partial_file_and_never_syncs_or_retries(self):
        journal = self.journal()
        original_write = os.write
        def short(fd, raw):
            return original_write(fd, raw[:5])
        with patch.object(subject.os, 'write', side_effect=short) as write, \
             patch.object(subject.os, 'fsync') as sync:
            self.assert_refused('bootstrap_journal_write', journal.emit, 'import', None)
            self.assertEqual(write.call_count, 1)
            sync.assert_not_called()
            self.assert_refused('bootstrap_journal_needs_review', journal.emit, 'import', None)
            self.assertEqual(write.call_count, 1)
        self.assertEqual(self.path.read_bytes(), self.line()[:5])
        self.assertEqual(journal.event_count, 0)
        self.assertEqual(journal.bytes_written, 0)

    def test_write_exception_has_fixed_code_and_no_retry(self):
        journal = self.journal()
        with patch.object(subject.os, 'write', side_effect=OSError('invented private text')) as write, \
             patch.object(subject.os, 'fsync') as sync:
            self.assert_refused('bootstrap_journal_write', journal.emit, 'import', None)
            self.assertEqual(write.call_count, 1)
            sync.assert_not_called()
        self.assertEqual(journal.state, 'needs_review')
        self.assertEqual(self.path.read_bytes(), b'')

    def test_fsync_failure_preserves_written_line_but_no_acceptance_or_retry(self):
        journal = self.journal()
        with patch.object(subject.os, 'fsync', side_effect=OSError('invented')) as sync:
            self.assert_refused('bootstrap_journal_fsync', journal.emit, 'import', None)
            self.assert_refused('bootstrap_journal_needs_review', journal.emit, 'import', None)
            self.assertEqual(sync.call_count, 1)
        self.assertEqual(self.path.read_bytes(), self.line())
        self.assertEqual(journal.event_count, 0)
        self.assertEqual(journal.bytes_written, 0)

    def test_close_once_then_emit_refuses_without_io(self):
        journal = self.journal()
        journal.close()
        with patch.object(subject.os, 'close') as close, patch.object(subject.os, 'write') as write:
            self.assert_refused('bootstrap_journal_close_once', journal.close)
            self.assert_refused('bootstrap_journal_closed', journal.emit, 'import', None)
            close.assert_not_called()
            write.assert_not_called()

    def test_close_failure_has_no_retry_and_preserves_file(self):
        journal = self.journal()
        journal.emit('import', None)
        original_close = os.close
        def uncertain_close(fd):
            original_close(fd)
            raise OSError('invented uncertain completion')
        with patch.object(subject.os, 'close', side_effect=uncertain_close) as close:
            self.assert_refused('bootstrap_journal_close', journal.close)
            self.assert_refused('bootstrap_journal_close_once', journal.close)
            self.assertEqual(close.call_count, 1)
        self.assertEqual(journal.state, 'needs_review')
        self.assertEqual(journal.failure_code, 'bootstrap_journal_close')
        self.assertEqual(self.path.read_bytes(), self.line())

    def test_secondary_close_error_does_not_mask_primary_failure(self):
        journal = self.journal()
        self.assert_refused('bootstrap_journal_value_type', journal.emit, 'import', Explosive())
        original_close = os.close
        def uncertain_close(fd):
            original_close(fd)
            raise OSError('invented close after completion')
        with patch.object(subject.os, 'close', side_effect=uncertain_close) as close:
            journal.close()
            self.assertEqual(close.call_count, 1)
        self.assertEqual(journal.failure_code, 'bootstrap_journal_value_type')
        self.assertEqual(journal.close_failure_code, 'bootstrap_journal_close')
        self.assertEqual(journal.state, 'needs_review')
        self.assertEqual(self.path.read_bytes(), b'')


if __name__ == '__main__':
    unittest.main()
