"""Invented physical envelopes for the retained I/O/preparation boundary.

This helper reads no source or input file.  Its caller supplies an active
FreshTerminal, which already owns the finite pinned ordinary source graph.  The
same six historical fixture builders regenerate the complete metadata lineage
with genuine classifiers and unchanged acceptance predicates.  Only their
invented evidence inputs change to describe the new physical envelope.

The three returned protected-role sources are new doubles, never copies of the
protected capture/core/validator sources.  The core double decodes a deliberately
invented framing, performs no cryptography and invokes the genuine observer.
Actual source reads, descriptor hashing, rewind, stamps and close are left to
the exact retained IoAdapter and genuine ScopedCallbacks factory.  These inputs
are not firmware, constants from a device, or an executable actual bundle.
"""
import copy
import hashlib
import sys


MAGIC = b'SYNIO001'
PREFIX_BYTES = 272
BLOCK_BYTES = 1024
LOGICAL_PIECE_BYTES = 512
COMMON = b'invented-common!'
CANDIDATE = b'invented-candidate-not-a-key!!!!'
MODES = frozenset(('complete', 'capture_early_eof', 'decode_exception',
                   'measure_bad_hash'))


def _require(value):
    if not value:
        raise AssertionError('invented retained I/O boundary contract')


def _envelope(logical):
    _require(type(logical) is bytes and 512 <= len(logical) <= 1024**2)
    prefix = b'invented-physical-envelope-no-crypto'
    prefix += bytes(PREFIX_BYTES - len(prefix))
    pieces = [b'', b''] + [logical[n:n + LOGICAL_PIECE_BYTES]
        for n in range(0, len(logical), LOGICAL_PIECE_BYTES)]
    blocks = []
    for piece in pieces:
        blocks.append(len(piece).to_bytes(4, 'little') + piece +
                      bytes(BLOCK_BYTES - 4 - len(piece)))
    return MAGIC + prefix + b''.join(blocks), len(pieces)


def _constants():
    """Exactly fifteen prior-reference/bytes assignments accepted by the factory."""
    _require(len(COMMON) == 16 and len(CANDIDATE) == 32)
    rows = [('key_aes', COMMON), ('key_cxd90057_k8', CANDIDATE)]
    raw = ''.join(name + ' = ' + repr(value) + '\n' for name, value in rows)
    raw += ''.join('invented_alias_' + str(n) + ' = key_aes\n' for n in range(13))
    return raw.encode('ascii')


_READ = r'''
import copy
import hashlib

SYNTHETIC_PROTECTED_OBSERVATIONS = dict(role=_ROLE, mode=_MODE,
    calls=0, read_calls=0, bytes_returned=0, eof_probes=0,
    physical_source_invented=True, framing_invented=True,
    cryptography_performed=False, installed_dependency_used=False,
    actual_runtime_verified=False, feature_supported=False,
    recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def _require(value):
    if not value:
        raise AssertionError('invented protected source double contract')


def _read_all(reader, size):
    # A double can retain this small invented envelope. Production decoder
    # memory, crypto, framing and buffer behaviour are expressly unqualified.
    blocks = []
    remaining = size
    while remaining:
        block = reader.read(min(remaining, 1048576))
        SYNTHETIC_PROTECTED_OBSERVATIONS['read_calls'] += 1
        SYNTHETIC_PROTECTED_OBSERVATIONS['bytes_returned'] += len(block)
        _require(type(block) is bytes and 0 < len(block) <= remaining)
        blocks.append(block)
        remaining -= len(block)
    terminal = reader.read(1)
    SYNTHETIC_PROTECTED_OBSERVATIONS['read_calls'] += 1
    SYNTHETIC_PROTECTED_OBSERVATIONS['eof_probes'] += 1
    _require(terminal == b'')
    return b''.join(blocks)
'''


_CAPTURE = r'''
def capture_stream(reader, size, digest, payload_offset, payload_bytes):
    observation = SYNTHETIC_PROTECTED_OBSERVATIONS
    observation['calls'] += 1
    _require(size == _SIZE and digest == _DIGEST and payload_offset == 8 and
             payload_bytes == _CHUNKS[0]['payload_bytes'])
    if _MODE == 'capture_early_eof':
        # Return otherwise plausible metadata after only a short read. The
        # retained facade must reject the absent EOF/full-byte/hash proof.
        block = reader.read(17)
        observation['read_calls'] += 1
        observation['bytes_returned'] += len(block)
        first, iv = bytes(1024), bytes(16)
    else:
        raw = _read_all(reader, size)
        first = raw[8 + 272:8 + 272 + 1024]
        iv = raw[8:24]
    capture = dict(bytes=size, sha256=digest, chunks=copy.deepcopy(_CHUNKS),
        retained_source_bytes=1040, transient_read_limit=1048576,
        managed_source_buffer_budget_bytes=3 * 1048576,
        whole_process_memory_capped=False, ciphertext_blocks=_BLOCK_COUNT,
        address_type='package_file_offset', raw_contents_output=False)
    return first, iv, capture
'''


_CORE = r'''
def measure_parent(reader, size, digest, chunks, iv, common, candidate, *, observer):
    observation = SYNTHETIC_PROTECTED_OBSERVATIONS
    observation['calls'] += 1
    _require(size == _SIZE and digest == _DIGEST and chunks == _CHUNKS and
        type(iv) is bytes and len(iv) == 16 and common == _COMMON and
        candidate == _CANDIDATE and callable(observer))
    if _MODE == 'decode_exception':
        block = reader.read(19)
        observation['read_calls'] += 1
        observation['bytes_returned'] += len(block)
        raise RuntimeError('invented protected decoder interruption')
    raw = _read_all(reader, size)
    _require(raw[:8] == b'SYNIO001' and len(raw) == 8 + 272 + 1024 * _BLOCK_COUNT)
    pieces, cursor = [], 0
    for number in range(_BLOCK_COUNT):
        start = 8 + 272 + number * 1024
        block = raw[start:start + 1024]
        length = int.from_bytes(block[:4], 'little')
        _require(length <= 512 and not any(block[4 + length:]) and
                 ((number < 2 and length == 0) or (number >= 2 and length > 0)))
        piece = block[4:4 + length]
        observer(cursor, piece)
        cursor += length
        pieces.append(piece)
    logical = b''.join(pieces)
    _require(len(logical) == _MEASUREMENT['logical_decoded_bytes_measured'] and
        hashlib.sha256(logical).hexdigest() == _MEASUREMENT['logical_decoded_sha256'])
    observation['observer_calls'] = observation.get('observer_calls', 0) + _BLOCK_COUNT
    observation['logical_bytes_returned'] = observation.get('logical_bytes_returned', 0) + len(logical)
    measurement = copy.deepcopy(_MEASUREMENT)
    if _MODE == 'measure_bad_hash':
        measurement['actual_decoding_pass_parent_sha256'] = '0' * 64
    return logical[:512], measurement
'''


_VALIDATOR = r'''
def validate_header(header, total):
    observation = SYNTHETIC_PROTECTED_OBSERVATIONS
    observation['calls'] += 1
    _require(type(header) is bytes and len(header) == 512 and
        hashlib.sha256(header).hexdigest() == _HEADER_DIGEST and
        total == _VALIDATION['decoded_bytes'])
    return copy.deepcopy(_VALIDATION)
'''


def invented_boundary(terminal, mode='complete'):
    """Generate only invented inputs; retain all ordinary roles unchanged.

    Call inside ``with FreshTerminal(genuine_classifier=True)`` and close that
    scope before installing the parent validation finder. Returned role sources
    override only the protected capture/core/validator roles. The caller owns
    writing new invented files, readonly attributes, all file-operation tracing
    and subsequent cleanup; this helper performs none of those operations.
    """
    if mode not in MODES:
        raise ValueError('unsupported invented retained I/O mode')
    _require(terminal.active and terminal.genuine_classifier and
             terminal.harness is not None)
    logical = terminal.harness.fixture.logical
    source, count = _envelope(logical)
    digest = hashlib.sha256(source).hexdigest()
    chunks = [dict(type_hex='46444154', payload_file_offset=8,
                   payload_bytes=len(source) - 8)]
    builder = sys.modules['test_gdt_runner']
    fixtures = builder.old.fixtures
    original_evidence, original_classifier = fixtures.evidence, fixtures.classifier
    classifier = sys.modules['classifier'].classify

    def evidence(*args, **kwargs):
        measured, prior, spans = original_evidence(*args, **kwargs)
        _require(measured['stream_measurement']['logical_decoded_bytes_measured'] == len(logical))
        measured.update(source_read_limit_bytes=1048576,
            managed_io_crypto_buffer_budget_bytes=5 * 1048576,
            whole_process_memory_capped=False)
        measured['stream_measurement'].update(actual_decoding_pass_parent_bytes=len(source),
            actual_decoding_pass_parent_sha256=digest, physical_blocks_checked=count,
            chunks=copy.deepcopy(chunks))
        prior.update(input_package_bytes=len(source), input_package_sha256=digest,
                     physical_blocks_checked=count)
        return measured, prior, spans

    fixtures.evidence = evidence
    fixtures.classifier = classifier
    primary = None
    harness = None
    try:
        harness = builder.Harness()
    except BaseException as error:
        primary = error
    finally:
        # Preserve foreign replacements and release our other temporary binding
        # independently. This is an owned trusted fixture scope, not a sandbox.
        changed = []
        for name, owned, original in (('evidence', evidence, original_evidence),
                                    ('classifier', classifier, original_classifier)):
            if getattr(fixtures, name) is owned:
                setattr(fixtures, name, original)
            else:
                changed.append(name)
        if changed:
            cleanup = AssertionError('invented fixture binding ownership changed: ' + ','.join(changed))
            if primary is not None:
                raise primary from cleanup
            raise cleanup
    if primary is not None:
        raise primary
    _require(harness is not None and harness.fixture.logical == logical)
    basis = copy.deepcopy(harness.fixture.basis)
    sys.modules['gdt_preflight'].freeze_basis(**basis)
    measured = basis['prior_measured']
    _require(measured == harness.fixture.measured and
        measured['stream_measurement']['chunks'] == chunks and
        measured['stream_measurement']['physical_blocks_checked'] == count)
    shared = dict(_MODE=mode, _SIZE=len(source), _DIGEST=digest, _CHUNKS=chunks,
        _BLOCK_COUNT=count, _COMMON=COMMON, _CANDIDATE=CANDIDATE,
        _MEASUREMENT=measured['stream_measurement'],
        _HEADER_DIGEST=measured['header_sha256'],
        _VALIDATION=measured['decoded_header_validation'])
    roles = {}
    for role, body in (('capture', _CAPTURE), ('core', _CORE), ('validator', _VALIDATOR)):
        values = dict(shared, _ROLE=role)
        prefix = ''.join(name + ' = ' + repr(value) + '\n' for name, value in values.items())
        raw = (prefix + _READ + body).encode('ascii')
        _require(0 < len(raw) <= 2 * 1024**2)
        roles[role] = raw
    return dict(basis=basis, source_manifest=dict(bytes=len(source), sha256=digest),
        role_sources=roles, constants_raw=_constants(), source_raw=source,
        summary=dict(schema='invented_io_boundary_inputs_v1', mode=mode,
            physical_bytes=len(source), logical_bytes=len(logical),
            physical_blocks=count, source_framing='SYNIO001_invented_only',
            complete_lineage_regenerated=True, genuine_classifier_used=True,
            ordinary_roles_changed=[], actual_protected_sources_read=False,
            actual_runtime_verified=False, feature_supported=False,
            recovery_proven=False, device_write_gate_passed=False, camera_commands=[]))
