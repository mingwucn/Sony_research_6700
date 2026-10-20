"""Pure historical-byte comparison for a pending successor proposal.

No historical act decision is created, required or inherited. Caller-selected
digests check bytes; they do not authenticate authority or current host state.
This module is deliberately disconnected from launch/activation paths.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import base64
import hashlib
import json
import math
from pathlib import PurePosixPath, PureWindowsPath

FIXED = frozenset(('parent_evidence','q_old_result','q_old_seal',
    'q_integration_result','q_integration_review','q_snapshot_result',
    'q_snapshot_log','source_cache','source_receipts','basis','source_manifest',
    'prerequisites','binding_plan','q_old_review','role_authority','binding_schema',
    'historical_scope','historical_rights','repair_overlay','q_repair_result',
    'q_repair_review','factory_evidence'))
HISTORICAL = FIXED | {'dependency_config','q_outer_result','q_outer_review'}
RETAINED = frozenset(('basis','source_manifest','prerequisites','binding_plan',
    'role_authority','binding_schema'))
ORDINARY = RETAINED | {'authored_source_manifest','authored_source_receipts',
    'dependency_packet','dependency_fixed','activity_scope','activity_rights',
    'historical_evidence_index','qualification_index'}
DECISIONS = frozenset(('accepted_contract_interaction','accompanying_component_terms',
    'constants_provenance','narrow_research_hypothesis_scope',
    'distinct_operational_act_decision'))
MAX_BYTES = 4*1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),
                      ensure_ascii=True,allow_nan=False).encode('ascii')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value, size=64):
    need(type(value) is str and len(value)==size and
         all(c in '0123456789abcdef' for c in value),'legacy_digest')


def receipt(raw):
    need(type(raw) is bytes and 0<len(raw)<=MAX_BYTES,'legacy_buffer')
    return dict(bytes=len(raw),sha256=sha(raw))


def shape(value, fields):
    need(type(value) is dict and set(value)==set(fields),'legacy_shape')


def decode(raw):
    receipt(raw)
    def pairs(rows):
        result={}
        for k,v in rows:
            need(k not in result,'legacy_duplicate_key');result[k]=v
        return result
    def invalid(_):
        raise ValueError('legacy_nonfinite')
    try:
        value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=invalid)
        stack=[(value,0)];count=0
        while stack:
            item,depth=stack.pop();count+=1
            need(depth<=32 and count<=500000,'legacy_json_bound')
            if type(item) is float:need(math.isfinite(item),'legacy_nonfinite')
            if type(item) is dict:stack.extend((v,depth+1) for v in item.values())
            elif type(item) is list:stack.extend((v,depth+1) for v in item)
        return value
    except (UnicodeError,RecursionError) as error:
        raise ValueError('legacy_json_encoding_depth') from error


def relative(path):
    need(type(path) is str and 0<len(path)<=4096 and
         all(ord(c)>=32 for c in path) and '\\' not in path and ':' not in path,
         'legacy_path')
    p=PurePosixPath(path)
    need(not p.is_absolute() and '..' not in p.parts and str(p)==path and
         len(p.parts)>=3 and p.parts[:2]==('private','sessions') and
         p.suffix in ('.json','.log'),'legacy_path')


def _compare(*, historical_buffers, reference_map_bytes,
        expected_reference_map_sha256, proposal_bytes, expected_proposal_sha256,
        request_bytes, expected_request_sha256, ordinary_buffers,
        retained_source_buffers):
    """Compare all 25 saved reference inputs with a distinct pending proposal.

    This verifies metadata edges/cache bytes and the 29 retained source copies.
    It does not run historical gate semantics, execute cache text, authenticate
    a source roster, inspect installed payloads, or qualify an operational path.
    """
    for raw,pin in ((reference_map_bytes,expected_reference_map_sha256),
                    (proposal_bytes,expected_proposal_sha256),
                    (request_bytes,expected_request_sha256)):
        digest(pin);receipt(raw);need(sha(raw)==pin,'legacy_selected_anchor')
    shape(historical_buffers,HISTORICAL);shape(ordinary_buffers,ORDINARY)
    for group in (historical_buffers,ordinary_buffers):
        for b in group.values():receipt(b)
    need(sum(map(len,historical_buffers.values()))+
         sum(map(len,ordinary_buffers.values()))<=32*1024**2,'legacy_total_bound')
    mapping=decode(reference_map_bytes)
    shape(mapping,('references','reference_pins','dependency_profile_sha256',
        'raw_fixed_references','ordinary_input_documents','execution_authorized','camera_commands'))
    shape(mapping['references'],HISTORICAL)
    shape(mapping['reference_pins'],FIXED|{'dependency_profile'})
    need(type(mapping['raw_fixed_references']) is int and mapping['raw_fixed_references']==22
         and type(mapping['ordinary_input_documents']) is int and mapping['ordinary_input_documents']==25
         and mapping['execution_authorized'] is False and mapping['camera_commands']==[],
         'legacy_map_mode')
    paths=set()
    for role,row in mapping['references'].items():
        shape(row,('path','bytes','sha256'));relative(row['path'])
        need(row['path'].casefold() not in paths,'legacy_path_alias');paths.add(row['path'].casefold())
        need(type(row['bytes']) is int and row['bytes']>0,'legacy_size')
        digest(row['sha256']);need({k:row[k] for k in ('bytes','sha256')}==receipt(historical_buffers[role]),'legacy_original_bytes')
        if role in FIXED:need(mapping['reference_pins'][role]==row['sha256'],'legacy_fixed_reference')
    for pin in mapping['reference_pins'].values():digest(pin)
    old={n:decode(b) for n,b in historical_buffers.items() if n!='q_snapshot_log'}
    config=old['dependency_config'];historical_operation=config['operation_id'];digest(historical_operation,32)
    profile=sha(encoded({k:v for k,v in config.items() if k!='operation_id'}))
    need(profile==mapping['dependency_profile_sha256']==mapping['reference_pins']['dependency_profile'],
         'legacy_dependency_profile')
    request=decode(request_bytes);proposal=decode(proposal_bytes)
    digest(request['operation_id'],32)
    need(request['schema']=='gdt_observation_request_core_v1' and
         proposal['schema']=='gdt_observation_proposal_v1' and
         proposal['operation_id']==request['operation_id'] and
         proposal['request_sha256']==sha(request_bytes) and proposal['camera_commands']==[],
         'legacy_proposal_binding')
    need(proposal['ordinary']=={n:receipt(b) for n,b in ordinary_buffers.items()},'legacy_proposal_originals')
    for role in RETAINED:need(ordinary_buffers[role]==historical_buffers[role],'legacy_retained_bytes')
    rights=decode(ordinary_buffers['activity_rights'])
    need(rights['schema']=='gdt_observation_activity_dispositions_v1' and
         rights['operation_id']==request['operation_id'] and rights['camera_commands']==[],
         'legacy_rights_mode')
    shape(rights['decisions'],DECISIONS)
    need(all(row==dict(disposition='pending',evidence=[]) for row in rights['decisions'].values()),
         'legacy_pending_only')
    need(rights['scope_sha256']==sha(ordinary_buffers['activity_scope']),'legacy_rights_binding')
    cache=old['source_cache'];shape(cache,('schema','sources'))
    need(cache['schema']=='ordinary_python_source_cache_v1','legacy_cache_mode')
    roles=old['role_authority']['roles'];need(type(roles) is dict and len(roles)==26,'legacy_role_roster')
    expected={'role:'+n for n in roles}|{'bootstrap:'+n for n in ('activation_gate','activation_binding','io_entry')}
    expected|={'integration:'+n for n in ('runtime_entry','gdt_wiring','prospective_child')}
    expected|={'dependency:'+n for n in config['source_rows']}
    expected|={'trusted:'+n for n,r in config['trusted_origins'].items() if PureWindowsPath(r['path']).suffix=='.py'}
    need(len(expected)==47,'legacy_cache_roster');shape(cache['sources'],expected)
    retained={'bound.role:'+n for n in roles}|{'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'}
    shape(retained_source_buffers,retained)
    for b in retained_source_buffers.values():receipt(b)
    need(sum(map(len,retained_source_buffers.values()))<=16*1024**2,'legacy_source_total')
    source_paths=set();decoded={};total=0
    for role,row in cache['sources'].items():
        shape(row,('path','bytes','sha256','base64'));digest(row['sha256'])
        need(type(row['bytes']) is int and 0<row['bytes']<=MAX_BYTES and
             type(row['base64']) is str and len(row['base64'])<=2*MAX_BYTES,'legacy_cache_bound')
        need(type(row['path']) is str and all(ord(c)>=32 for c in row['path']) and
             len(row['path'])<=4096 and PureWindowsPath(row['path']).is_absolute() and
             '..' not in PureWindowsPath(row['path']).parts and
             PureWindowsPath(row['path']).suffix=='.py' and PureWindowsPath(row['path']).as_posix().casefold() not in source_paths,
             'legacy_source_path')
        source_paths.add(PureWindowsPath(row['path']).as_posix().casefold())
        try:b=base64.b64decode(row['base64'],validate=True)
        except (ValueError,TypeError) as error:raise ValueError('legacy_cache_encoding') from error
        total+=len(b);need(total<=16*1024**2 and receipt(b)=={k:row[k] for k in ('bytes','sha256')},'legacy_cache_hash')
        decoded[role]=b
    for role,b in retained_source_buffers.items():
        receipt(b);need(b==decoded[role.removeprefix('bound.')],'legacy_retained_source')
    identity=proposal['protected_identities'];manifest=old['source_manifest']
    need(identity['firmware_package']=={k:manifest[k] for k in ('bytes','sha256')} and
         identity['operational_constants']['sha256']==old['prerequisites']['constants_sha256'],
         'legacy_protected_metadata')
    return dict(schema='pending_successor_legacy_comparison_v1',
        historical_operation_id=historical_operation,proposed_operation_id=request['operation_id'],
        operation_ids_differ=historical_operation!=request['operation_id'],
        reference_map_sha256=sha(reference_map_bytes),proposal_sha256=sha(proposal_bytes),
        request_sha256=sha(request_bytes),historical_receipts={n:receipt(b) for n,b in historical_buffers.items()},
        compared_inputs=25,retained_originals=6,compared_cache_sources=47,retained_source_copies=29,
        full_legacy_gate_semantics_validated=False,full_proposal_semantics_validated=False,
        historical_authority_promoted=False,operational_path_qualified=False,
        current_payload_freshness_verified=False,execution_authorized=False,
        feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def compare(**arguments):
    """Return comparison evidence or refuse malformed/inconsistent buffers."""
    try:
        return _compare(**arguments)
    except (KeyError,TypeError,OverflowError) as error:
        raise ValueError('legacy_malformed') from error
