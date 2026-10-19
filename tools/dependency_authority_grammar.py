"""Pure invented-document qualification. No I/O, execution or permission API."""
import hashlib
import json
import math

if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_operational_scope as policy

DOCUMENTS = frozenset(('candidate', 'review', 'decision', 'seal'))
SOURCE_ROLES = policy.SOURCE_ROLES | {'host_parent_adapter'}
HISTORY_ROLES = frozenset(n for n in policy.LEGACY_INPUTS if n not in {
    'basis', 'source_manifest', 'prerequisites', 'binding_plan', 'role_authority',
    'binding_schema', 'dependency_config', 'source_cache', 'source_receipts',
    'activity_scope', 'activity_rights'})
PROTECTED = frozenset(('firmware_package', 'operational_constants'))
MAX_BYTES = 2 * 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def duplicate_free(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate_json_key')
        result[key] = value
    return result


def decode(raw):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'raw_document_bound')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=duplicate_free,
                          parse_float=finite_float,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
    except (UnicodeError, RecursionError) as exc:
        raise ValueError('json_encoding_or_depth') from exc


def finite_float(text):
    value = float(text)
    need(math.isfinite(value), 'nonfinite_json')
    return value


def shape(value, fields, code):
    need(type(value) is dict and set(value) == set(fields), code)


def digest(value):
    need(type(value) is str and len(value) == 64 and
         all(c in '0123456789abcdef' for c in value), 'digest_shape')


def receipt(raw):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'buffer_bound')
    return dict(bytes=len(raw), sha256=sha(raw))


def receipts(rows, buffers, roles):
    shape(rows, roles, 'receipt_roster')
    shape(buffers, roles, 'buffer_roster')
    for role in roles:
        shape(rows[role], ('bytes', 'sha256'), 'receipt_shape')
        need(type(rows[role]['bytes']) is int, 'receipt_size_type')
        digest(rows[role]['sha256'])
        need(rows[role] == receipt(buffers[role]), 'original_bytes_mismatch')


def validate_invented_chain(documents, *, external_seal_sha256, scope_bytes,
                            source_buffers, ordinary_buffers, historical_buffers):
    """Compare supplied invented byte buffers only; return no activation authority.

    external_seal_sha256 must arrive outside these four documents. Matching it
    proves consistency with the caller's anchor, never reviewer identity/consent.
    No protected buffers or actual path arguments are accepted by this API.
    Ordinary buffers except the historical index are opaque. Their receipt
    equality does not establish role semantics, freshness or provenance.
    """
    shape(documents, DOCUMENTS, 'document_roster')
    digest(external_seal_sha256)
    parsed = {name: decode(raw) for name, raw in documents.items()}
    need(sha(documents['seal']) == external_seal_sha256, 'external_anchor_mismatch')
    for name, value in parsed.items():
        need(type(value) is dict and value.get('schema') == 'invented_authority_' + name + '_v1'
             and value.get('invented') is True, 'invented_document_required')
    candidate, review, decision, seal = (parsed[n] for n in ('candidate', 'review', 'decision', 'seal'))
    shape(candidate, ('schema', 'invented', 'phase', 'scope_file_sha256', 'sources', 'ordinary',
                      'protected', 'historical_blockers', 'rights_uncertainties', 'runtime'), 'candidate_shape')
    need(candidate['phase'] in ('prepared', 'operational_shape'), 'candidate_phase')
    policy.validate_review_packet(decode(scope_bytes))
    need(candidate['scope_file_sha256'] == sha(scope_bytes), 'scope_original_bytes')
    receipts(candidate['sources'], source_buffers, SOURCE_ROLES)
    receipts(candidate['ordinary'], ordinary_buffers, policy.ORDINARY_INPUTS)
    shape(candidate['protected'], PROTECTED, 'protected_roster')
    for row in candidate['protected'].values():
        shape(row, ('bytes', 'sha256', 'read_authorized'), 'protected_shape')
        need(type(row['bytes']) is int and row['bytes'] > 0 and row['read_authorized'] is False,
             'protected_read_disabled')
        digest(row['sha256'])
    need(candidate['historical_blockers'] == list(policy.HISTORY), 'historical_blockers')
    need(candidate['rights_uncertainties'] == sorted(policy.RIGHTS), 'rights_uncertainties')
    history = decode(ordinary_buffers['historical_evidence_index'])
    shape(history, ('schema', 'invented', 'purpose', 'receipts'), 'history_shape')
    need(history['schema'] == 'invented_historical_index_v1' and history['invented'] is True
         and history['purpose'] == 'comparison_only', 'history_authority')
    receipts(history['receipts'], historical_buffers, HISTORY_ROLES)
    runtime = candidate['runtime']
    shape(runtime, ('interpreter_identity', 'argv'), 'runtime_shape')
    need(type(runtime['interpreter_identity']) is str and
         0 < len(runtime['interpreter_identity']) <= 256, 'interpreter_identity')
    need(type(runtime['argv']) is list and len(runtime['argv']) == 8 and
         all(type(v) is str and 0 < len(v) <= 8192 for v in runtime['argv']) and
         runtime['argv'][0] == runtime['interpreter_identity'] and
         runtime['argv'][1:7] == ['-I', '-S', '-B', '-X', 'utf8', '-c'], 'runtime_argv')
    # Strict forward DAG: candidate <- review <- decision <- seal.
    shape(review, ('schema', 'invented', 'candidate_sha256', 'outcome'), 'review_shape')
    need(review['candidate_sha256'] == sha(documents['candidate']) and
         review['outcome'] in ('accepted_shape', 'refused_shape'), 'review_binding')
    shape(decision, ('schema', 'invented', 'candidate_sha256', 'review_sha256', 'outcome'), 'decision_shape')
    need(decision['candidate_sha256'] == sha(documents['candidate']) and
         decision['review_sha256'] == sha(documents['review']), 'decision_binding')
    expected = 'pending' if candidate['phase'] == 'prepared' else 'accepted_shape'
    need(decision['outcome'] == expected and review['outcome'] == 'accepted_shape', 'decision_refused_or_phase')
    shape(seal, ('schema', 'invented', 'candidate_sha256', 'review_sha256', 'decision_sha256'), 'seal_shape')
    for name in ('candidate', 'review', 'decision'):
        need(seal[name + '_sha256'] == sha(documents[name]), 'seal_binding')
    return dict(schema='invented_authority_consistency_v1', phase=candidate['phase'],
                external_anchor_sha256=external_seal_sha256, execution_authorized=False,
                runtime_qualified=False, protected_inputs_read=False,
                feature_supported=False, recovery_proven=False,
                device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
