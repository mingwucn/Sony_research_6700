"""Invented source manifest/receipt consistency and composed offline preflight.

No file reads or dependency activation. Receipt claims are not observations.
Caller-selected external anchors bind bytes, not consent or independent review.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_authority_grammar as envelope
from tools import dependency_basis_links as links
from tools import dependency_basis_recompute as basis
from tools import dependency_evidence as evidence
from tools import dependency_input_semantics as dependency

SOURCE_INPUTS = frozenset(('authored_source_manifest','authored_source_receipts'))
CHECKED = SOURCE_INPUTS | links.INPUTS | dependency.CHECKED_ROLES
MANIFEST_FIELDS = ('schema','invented','operation_id','root_path','sources','camera_commands')


def _operation(value):
    envelope.need(type(value) is str and 1 <= len(value) <= 96 and
        all(c.isascii() and (c.isalnum() or c in '_-') for c in value), 'source_operation')


def validate_invented_source_roles(documents, *, external_seal_sha256, scope_bytes,
        source_buffers, ordinary_buffers, historical_buffers, source_anchor_bytes,
        external_source_anchor_sha256, dependency_anchor_bytes):
    """Check two roles against an external original-byte anchor, without I/O."""
    envelope.validate_invented_chain(documents, external_seal_sha256=external_seal_sha256,
        scope_bytes=scope_bytes, source_buffers=source_buffers,
        ordinary_buffers=ordinary_buffers, historical_buffers=historical_buffers)
    envelope.digest(external_source_anchor_sha256)
    anchor = envelope.decode(source_anchor_bytes)
    dep_anchor = envelope.decode(dependency_anchor_bytes)
    envelope.need(envelope.sha(source_anchor_bytes) == external_source_anchor_sha256, 'source_external_anchor')
    envelope.shape(anchor, ('schema','invented','operation_id','manifest_file_sha256',
        'receipts_file_sha256','dependency_anchor_file_sha256'), 'source_anchor_shape')
    envelope.need(anchor['schema']=='invented_authored_source_anchor_v1' and anchor['invented'] is True,
        'source_anchor_mode')
    _operation(anchor['operation_id'])
    for field in ('manifest_file_sha256','receipts_file_sha256','dependency_anchor_file_sha256'):
        envelope.digest(anchor[field])
        envelope.need(anchor[field] not in {envelope.sha(v) for v in documents.values()}, 'source_anchor_cycle')
    manifest_raw = ordinary_buffers['authored_source_manifest']
    receipts_raw = ordinary_buffers['authored_source_receipts']
    envelope.need(envelope.sha(manifest_raw)==anchor['manifest_file_sha256'] and
        envelope.sha(receipts_raw)==anchor['receipts_file_sha256'] and
        envelope.sha(dependency_anchor_bytes)==anchor['dependency_anchor_file_sha256'], 'source_original_bytes')
    manifest = envelope.decode(manifest_raw); receipts = envelope.decode(receipts_raw)
    envelope.shape(manifest, MANIFEST_FIELDS, 'source_manifest_shape')
    envelope.shape(receipts, ('schema','invented','operation_id','manifest_file_sha256','rows','camera_commands'),
        'source_receipts_shape')
    envelope.need(manifest['schema']=='invented_authored_source_manifest_v1' and manifest['invented'] is True and
        receipts['schema']=='invented_authored_source_receipts_v1' and receipts['invented'] is True and
        manifest['camera_commands']==receipts['camera_commands']==[], 'source_record_mode')
    envelope.need(type(dep_anchor) is dict and dep_anchor.get('operation_id')==anchor['operation_id'] and
        manifest['operation_id']==receipts['operation_id']==anchor['operation_id'], 'source_cross_operation')
    envelope.need(receipts['manifest_file_sha256']==envelope.sha(manifest_raw), 'source_receipt_manifest')
    root = evidence._absolute(manifest['root_path'])
    envelope.need(not root.endswith('/'), 'source_root_label')
    envelope.shape(manifest['sources'], envelope.SOURCE_ROLES, 'source_manifest_roster')
    envelope.shape(receipts['rows'], envelope.SOURCE_ROLES, 'source_receipt_roster')
    prerequisites = envelope.decode(ordinary_buffers['prerequisites'])
    envelope.need(type(prerequisites) is dict and {'qualified_roles','constants_relative_path',
        'crypto_python_relative_path'} <= set(prerequisites), 'source_prerequisites')
    envelope.shape(prerequisites['qualified_roles'], links.ROLES, 'source_role_roster')
    protected = envelope.decode(ordinary_buffers['source_manifest'])
    envelope.need(type(protected) is dict and 'relative_path' in protected, 'source_protected_label')
    paths = set()
    for value in (protected['relative_path'],prerequisites['constants_relative_path'],
                  prerequisites['crypto_python_relative_path']):
        links.private_path(value); paths.add(value.casefold())
    identities = set(); total = 0
    for role, row in manifest['sources'].items():
        envelope.shape(row, ('path','bytes','sha256','identity'), 'authored_source_shape')
        links.private_path(row['path']); evidence._relative(row['path'])
        envelope.need(row['path'].endswith('.py') and row['path'].casefold() not in paths, 'source_path_alias')
        paths.add(row['path'].casefold())
        envelope.need(type(row['bytes']) is int and 0 < row['bytes'] <= envelope.MAX_BYTES, 'source_size')
        total += row['bytes']; envelope.need(total <= 32*1024**2, 'source_total_bound')
        envelope.digest(row['sha256'])
        envelope.need(envelope.receipt(source_buffers[role]) == dict(bytes=row['bytes'],sha256=row['sha256']),
            'source_buffer_identity')
        evidence._shape(row['identity'], evidence.CROSS)
        for value in row['identity'].values(): evidence._integer(value)
        identity = row['identity']; pair = identity['device'],identity['inode']
        envelope.need(pair not in identities, 'source_identity_alias'); identities.add(pair)
        item = receipts['rows'][role]
        envelope.shape(item, ('receipt','close_attempts','eof_probes','read_calls','closed'), 'source_read_shape')
        envelope.need(item['closed'] is True and all(type(item[k]) is int and item[k]==1
            for k in ('close_attempts','eof_probes')) and type(item['read_calls']) is int and
            2 <= item['read_calls'] <= row['bytes']+1, 'source_read_completion')
        evidence._receipt(item['receipt'], root+'/'+row['path'], row['sha256'], row['bytes'], identity)
        if role.startswith('bound.role:'):
            qualified = prerequisites['qualified_roles'][role.split(':',1)[1]]
            envelope.shape(qualified, ('path','sha256'), 'source_qualified_shape')
            envelope.need(links.equal(qualified,dict(path=row['path'],sha256=row['sha256'])), 'source_qualified_binding')
    return dict(schema='invented_authored_source_consistency_v1', checked_roles=sorted(SOURCE_INPUTS),
        operation_id=anchor['operation_id'], source_roles_checked=len(envelope.SOURCE_ROLES),
        manifest_file_sha256=envelope.sha(manifest_raw),receipts_file_sha256=envelope.sha(receipts_raw),
        source_anchor_file_sha256=external_source_anchor_sha256, source_reads_observed=False,
        source_origin_authenticated=False,source_freshness_verified=False,
        actual_inputs_accessed=False,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def validate_invented_composed_inputs(documents, *, external_seal_sha256, scope_bytes,
        source_buffers, ordinary_buffers, historical_buffers, source_anchor_bytes,
        external_source_anchor_sha256, dependency_anchor_bytes, external_dependency_anchor_sha256):
    """Run source, dependency and retained basis validators on the same buffers.

    This checks ten role contracts. The legacy dependency-plan bridge, freshness,
    actual namespace/startup and candidate-to-operation authority remain pending.
    """
    common = dict(external_seal_sha256=external_seal_sha256,scope_bytes=scope_bytes,
        source_buffers=source_buffers,ordinary_buffers=ordinary_buffers,historical_buffers=historical_buffers)
    sources = validate_invented_source_roles(documents, **common,
        source_anchor_bytes=source_anchor_bytes,external_source_anchor_sha256=external_source_anchor_sha256,
        dependency_anchor_bytes=dependency_anchor_bytes)
    dep = dependency.validate_invented_dependency_roles(documents, **common,
        dependency_anchor_bytes=dependency_anchor_bytes,external_dependency_anchor_sha256=external_dependency_anchor_sha256)
    retained = basis.validate_invented_basis_roles(documents, **common)
    return dict(schema='invented_composed_metadata_contracts_v1',operation_id=sources['operation_id'],
        checked_roles=sorted(CHECKED),pending_ordinary_roles=sorted(envelope.policy.ORDINARY_INPUTS-CHECKED),
        source_result=sources,dependency_result=dep,basis_result=retained,
        source_reads_observed=False,source_freshness_verified=False,dependency_bridge_verified=False,
        complete_basis_semantics_verified=False,actual_startup_verified=False,current_candidate_operation_bound=False,
        actual_inputs_accessed=False,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
