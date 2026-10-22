"""Bounded, typed private journal for disposable synthetic bootstrap trials.

This module neither imports dependency packages nor starts a child.  The caller
owns path/root authentication.  A successful record means one unbuffered write
and one fsync completed; it does not authenticate the event or its producer.
No failed write, close, or ambiguous outcome is retried, reopened, or removed.
"""
import json
import os
from pathlib import Path


EVENT_LIMIT = 256
EVENT_BYTES_LIMIT = 4096
BYTES_LIMIT = 262144
INTEGER_LIMIT = 2**128 - 1
_PATH_TYPE = type(Path())
_EVENT_CHARS = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:-')


def _fail(code):
    raise ValueError(code)


def encode_value(value):
    """Return closed, explicitly typed JSON data without calling input methods.

    Root depth is zero; at most six nested edges and 128 nodes are allowed.
    Dictionary keys also count as nodes.  Only exact built-in types are accepted
    so subclasses cannot supply iterators, representations, or conversions.
    Integer values use decimal strings, preserving the bounded 128-bit domain
    through JSON readers whose native number types might otherwise round them.
    """
    nodes = 0

    def visit(item, depth):
        nonlocal nodes
        if depth > 6:
            _fail('bootstrap_journal_depth')
        nodes += 1
        if nodes > 128:
            _fail('bootstrap_journal_nodes')
        kind = type(item)
        if item is None:
            return {'type': 'none'}
        if kind is bool:
            return {'type': 'bool', 'value': item}
        if kind is int:
            if not -INTEGER_LIMIT <= item <= INTEGER_LIMIT:
                _fail('bootstrap_journal_value_bound')
            return {'type': 'int', 'value': str(item)}
        if kind is str:
            if len(item) > 512:
                _fail('bootstrap_journal_value_bound')
            return {'type': 'str', 'value': item}
        if kind is bytes:
            if len(item) > 256:
                _fail('bootstrap_journal_value_bound')
            return {'type': 'bytes', 'hex': item.hex()}
        if kind is list or kind is tuple:
            if len(item) > 128 - nodes:
                _fail('bootstrap_journal_nodes')
            return {'type': 'list' if kind is list else 'tuple',
                    'items': [visit(child, depth + 1) for child in item]}
        if kind is dict:
            if len(item) * 2 > 128 - nodes:
                _fail('bootstrap_journal_nodes')
            # Check exact key types before sorting: heterogeneous keys and
            # subclasses must never trigger comparison or conversion methods.
            for key in item:
                if type(key) is not str:
                    _fail('bootstrap_journal_value_type')
                if len(key) > 128:
                    _fail('bootstrap_journal_value_bound')
            pairs = []
            for key in sorted(item):
                nodes += 1
                if nodes > 128:
                    _fail('bootstrap_journal_nodes')
                pairs.append([key, visit(item[key], depth + 1)])
            return {'type': 'dict', 'items': pairs}
        _fail('bootstrap_journal_value_type')

    return visit(value, 0)


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


class Journal:
    """Exclusive, no-retry JSONL writer with sticky ``needs_review`` state.

    Caps count the complete ASCII JSONL line, including its newline.  Counters
    advance only after a full write and fsync, so partial files are evidence of
    uncertain outcomes rather than accepted events.  There is no user-space
    output buffer to flush.  ``close`` attempts descriptor close at most once;
    a secondary close error is retained without masking a primary emit failure.
    """

    def __init__(self, path, *, event_limit=EVENT_LIMIT,
                 event_bytes_limit=EVENT_BYTES_LIMIT, bytes_limit=BYTES_LIMIT):
        for value, ceiling in ((event_limit, EVENT_LIMIT),
                               (event_bytes_limit, EVENT_BYTES_LIMIT),
                               (bytes_limit, BYTES_LIMIT)):
            if type(value) is not int or not 1 <= value <= ceiling:
                _fail('bootstrap_journal_limit')
        if type(path) is not str and type(path) is not _PATH_TYPE:
            _fail('bootstrap_journal_path')
        if type(path) is str and (not path or '\x00' in path):
            _fail('bootstrap_journal_path')
        self.event_limit = event_limit
        self.event_bytes_limit = event_bytes_limit
        self.bytes_limit = bytes_limit
        self.event_count = 0
        self.bytes_written = 0
        self.state = 'open'
        self.failure_code = None
        self.close_failure_code = None
        self._close_attempted = False
        self._fd = None
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0)
        flags |= getattr(os, 'O_NOFOLLOW', 0)
        try:
            self._fd = os.open(path, flags, 0o600)
        except BaseException:
            self.state = 'needs_review'
            self.failure_code = 'bootstrap_journal_open'
            raise ValueError(self.failure_code) from None

    def _record_failure(self, code):
        self.state = 'needs_review'
        if self.failure_code is None:
            self.failure_code = code

    def emit(self, event, args):
        if self.state == 'needs_review':
            _fail('bootstrap_journal_needs_review')
        if self.state != 'open' or self._fd is None or self._close_attempted:
            _fail('bootstrap_journal_closed')
        try:
            if (type(event) is not str or not 1 <= len(event) <= 128 or
                    any(char not in _EVENT_CHARS for char in event)):
                _fail('bootstrap_journal_event')
            if self.event_count >= self.event_limit:
                _fail('bootstrap_journal_event_limit')
            row = {'sequence': self.event_count + 1, 'event': event,
                   'arguments': encode_value(args)}
            raw = _canonical(row) + b'\n'
            if len(raw) > self.event_bytes_limit:
                _fail('bootstrap_journal_event_bytes')
            if self.bytes_written + len(raw) > self.bytes_limit:
                _fail('bootstrap_journal_bytes')
        except ValueError as exc:
            # All intentional refusal messages above and in encode_value are
            # fixed literals.  Never render a supplied object or exception.
            code = exc.args[0] if len(exc.args) == 1 and type(exc.args[0]) is str else ''
            if not code.startswith('bootstrap_journal_'):
                code = 'bootstrap_journal_serialization'
            self._record_failure(code)
            raise ValueError(self.failure_code) from None
        except BaseException:
            self._record_failure('bootstrap_journal_serialization')
            raise ValueError(self.failure_code) from None
        try:
            written = os.write(self._fd, raw)
            if type(written) is not int or written != len(raw):
                self._record_failure('bootstrap_journal_write')
                raise ValueError(self.failure_code)
        except BaseException:
            self._record_failure('bootstrap_journal_write')
            raise ValueError(self.failure_code) from None
        try:
            os.fsync(self._fd)
        except BaseException:
            self._record_failure('bootstrap_journal_fsync')
            raise ValueError(self.failure_code) from None
        self.event_count += 1
        self.bytes_written += len(raw)
        return row

    def close(self):
        if self._close_attempted:
            _fail('bootstrap_journal_close_once')
        self._close_attempted = True
        descriptor = self._fd
        self._fd = None
        if descriptor is None:
            if self.state != 'needs_review':
                self.state = 'closed'
            return
        try:
            os.close(descriptor)
        except BaseException:
            self.close_failure_code = 'bootstrap_journal_close'
            had_primary = self.failure_code is not None
            self._record_failure(self.close_failure_code)
            if not had_primary:
                raise ValueError(self.failure_code) from None
            return
        if self.state != 'needs_review':
            self.state = 'closed'
