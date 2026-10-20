"""Source-captured disabled outer child; no fixture or activation selector.

Private seams are capable APIs, not authorization. The public CLI refuses.
Interpreter, stdlib and initial bootstrap remain trusted assumptions.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import base64
import hashlib
import json
from pathlib import Path
import sys
import time
import types

RETAINED = ('acceptance','link_acceptance','member_acceptance','metadata_preflight',
    'expanded_gate','ext_superblock','ext_preflight','ext_read_planner','ext_gate',
    'gdt_preflight','gdt_cleanup','gdt_gate','gdt_adapter','gdt_runner','prefix',
    'offline_inventory','artifact_probe','classifier','tar_inventory','metadata_tar',
    'member_prefix','header_candidates','io_adapter','validator','capture','core')
DEPENDENCIES = ('dependency_evidence','dependency_producer','dependency_package_preflight',
    'dependency_execution','dependency_controller','dependency_parent')
OUTER = dict(dependency_operational_metadata='operational_metadata',
    dependency_host_entry='host_entry',dependency_operational_entry='operational_entry',
    dependency_successor_wiring='successor_wiring',dependency_successor_sources='namespace',
    dependency_adapter_sources='adapter_loader',retained_gate='retained_gate',
    ordinary_io='ordinary_io',dependency_operational_preparation='operational_preparation',
    parent_verifier='dependency.dependency_parent')
ROSTER = frozenset({'bound.role:'+n for n in RETAINED} |
    {'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'} |
    {'dependency.'+n for n in DEPENDENCIES} |
    {'adapter','adapter_scope','adapter_comparison','namespace','successor_wiring',
     'host_entry','retained_gate','ordinary_io','operational_metadata','operational_entry',
     'operational_preparation','adapter_loader','outer_loader','process_child'})
PACKET_FIELDS = frozenset(('schema','documents','reference_pins','seal_sha256',
    'request_bytes','request_sha256','checked','original_receipts','ordinary',
    'ordinary_receipts','repository_root'))
TERMINAL_FIELDS=frozenset(('schema','operation_id','status','preflight_sha256','request_sha256',
    'evidence','preparation_closed','helpers_closed','adapter_closed','callback_closed',
    'execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','camera_commands'))
EVIDENCE_FIELDS=frozenset(('dependency_sha256','bridge_sha256','stdout_sha256'))
DEPENDENCY_ARTIFACTS=frozenset(('started.json','collection.json','transition.json','verification.json',
    'completion.json','producer/expectation.json','producer/binding.json','producer/journal.jsonl',
    'producer/raw.json','producer/audit-acknowledgement.json','producer/result.json'))

def need(ok, code):
    if not ok:raise ValueError(code)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def strict(raw):
    def pairs(rows):
        result={}
        for k,v in rows:
            need(k not in result,'operational_process_duplicate');result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda _:need(False,'operational_process_nonfinite'))

def unbytes(text):
    need(type(text) is str,'operational_process_bytes')
    raw=base64.b64decode(text,validate=True)
    need(0<len(raw)<=2*1024**2,'operational_process_bytes')
    return raw

def module(name,raw):
    result=types.ModuleType(name)
    exec(compile(raw,'<checked-process:'+name+'>','exec',dont_inherit=True,optimize=0),vars(result))
    return result

def owners(buffers):
    loader=module('_checked_operational_sources',buffers['outer_loader'])
    need(set(loader.ROSTER)==set(OUTER),'operational_process_outer_roster')
    texts={n:buffers[k] for n,k in OUTER.items()}
    outer=loader.OuterSources(buffers=texts,hashes={n:sha(b) for n,b in texts.items()}).load()
    adapter=None
    try:
        source=outer.modules['dependency_adapter_sources']
        texts={n:buffers[k] for n,k in source.BUFFER_KEYS.items()}
        adapter=source.AdapterSources(buffers=texts,hashes={n:sha(b) for n,b in texts.items()}).load()
        return outer,adapter
    except BaseException as primary:
        try:outer.close()
        except BaseException as cleanup:raise primary from cleanup
        raise

def project(adapter,buffers,rows,repository_root):
    return adapter.project(process_sources=rows,process_buffers=buffers,repository_root=repository_root)

def migration_record(value, *, wire=False):
    fields={'context_bytes','expected_context_sha256','ancestry_proof_bytes',
            'expected_ancestry_proof_sha256'}
    need(type(value) is dict and set(value)==fields,'operational_process_migration_shape')
    result={}
    for name,limit in (('context',16384),('ancestry_proof',65536)):
        raw=unbytes(value[name+'_bytes']) if wire else value[name+'_bytes']
        pin=value['expected_'+name+'_sha256']
        need(type(raw) is bytes and 0<len(raw)<=limit and type(pin) is str and
            len(pin)==64 and all(c in '0123456789abcdef' for c in pin) and sha(raw)==pin,
            'operational_process_migration_anchor')
        result[name+'_bytes']=raw
        result['expected_'+name+'_sha256']=pin
    return result


def packet_migration(packet):
    need(type(packet) is dict,'operational_process_packet')
    v2=packet.get('schema')=='pending_operational_outer_packet_v2'
    need(packet.get('schema') in ('pending_operational_outer_packet_v1',
         'pending_operational_outer_packet_v2') and
         set(packet)==(PACKET_FIELDS|{'historical_migration'} if v2 else PACKET_FIELDS),
         'operational_process_packet')
    return migration_record(packet['historical_migration'],wire=True) if v2 else None


def decode_packet(packet):
    packet_migration(packet)
    docs=packet['documents']
    need(type(docs) is dict and set(docs)=={'candidate','review','decision','seal','inputs'},'operational_process_documents')
    documents={n:unbytes(docs[n]) for n in ('candidate','review','decision','seal')}
    documents['inputs']={n:unbytes(b) for n,b in docs['inputs'].items()}
    raw=unbytes(packet['request_bytes'])
    need(sha(raw)==packet['request_sha256'],'operational_process_request')
    request=strict(raw)
    return documents,raw,request,{n:unbytes(b) for n,b in packet['checked'].items()}, {n:unbytes(b) for n,b in packet['ordinary'].items()}

def check_packet(packet,buffers,rows,adapter):
    docs,raw,request,checked,ordinary=decode_packet(packet)
    sources,projected=project(adapter,buffers,rows,packet['repository_root'])
    need(projected==checked and encoded(sources)==encoded(request['sources']),
        'operational_process_projection')
    binding=adapter.modules['dependency_adapter_binding']
    binding.validate_request(request,expected_request_sha256=packet['request_sha256'],checked_sources=checked)
    return docs,raw,request,checked,ordinary

def helper_owner(outer,buffers,rows,mode):
    namespace=outer.modules['dependency_successor_sources']
    order=namespace.CHILD_ORDER if mode=='child' else namespace.PARENT_ORDER
    owner=namespace.HelperSources(mode=mode,buffers={n:buffers['dependency.'+n] for n in order},
        origins={n:rows['dependency.'+n]['path'] for n in order},
        hashes={n:sha(buffers['dependency.'+n]) for n in order})
    owner.load()
    return owner

def preflight_arguments(packet,decoded,outer,adapter,validated):
    docs,raw,request,checked,ordinary=decoded
    arguments=dict(documents=docs,original_receipts=packet['original_receipts'],validated=validated,
        request_bytes=raw,request_sha256=packet['request_sha256'],checked_sources=checked,
        adapter_owner=adapter,ordinary=ordinary,ordinary_receipts=packet['ordinary_receipts'],
        outer_source_receipts=outer.receipts(),prepared_repository_root=packet['repository_root'])
    migration=packet_migration(packet)
    if migration is not None:arguments['historical_migration']=migration
    return arguments


def validate_gate(packet,decoded,outer):
    docs,raw,request,checked,ordinary=decoded
    gate=outer.modules['retained_gate'];migration=packet_migration(packet)
    if migration is None:
        return gate.validate_bundle(docs,expected_seal_sha256=packet['seal_sha256'],
            reference_pins=packet['reference_pins'])
    need(sha(raw)==packet['request_sha256'],'operational_process_request')
    return gate.validate_bundle_v6(docs,expected_seal_sha256=packet['seal_sha256'],
        reference_pins=packet['reference_pins'],expected_operation_id=request['operation_id'],
        **migration)


def refuse_v6_execution(packet):
    need(packet_migration(packet) is None,'operational_process_v6_execution_pending')

def runtime_wiring(outer):
    return outer.modules['dependency_successor_wiring']

def close_owned(items,primary=None):
    cleanup=None
    for item in items:
        if item is not None and not item.closed:
            try:item.close()
            except BaseException as error:
                if cleanup is None:cleanup=error
    if primary is not None:
        if cleanup is not None:raise primary from cleanup
        raise primary
    if cleanup is not None:raise cleanup

def child(request,packet,buffers,rows):
    need(set(buffers)==set(rows)==ROSTER,'operational_process_roster')
    need(not any(n=='tools' or n.startswith('tools.') or n.split('.')[0] in
        ('ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend') for n in sys.modules),
        'operational_process_startup')
    outer=adapter=helpers=prep=None;primary=None;stdout=None
    try:
        outer,adapter=owners(buffers)
        decoded=check_packet(packet,buffers,rows,adapter)
        docs,raw,prepared,checked,ordinary=decoded
        need(Path(prepared['folder'])==Path(request['folder'])/'composition',
            'operational_process_folder')
        gate=outer.modules['retained_gate'];io=outer.modules['ordinary_io']
        validated=validate_gate(packet,decoded,outer)
        need(validated['candidate']['operation_id']==request['operation_id']==prepared['operation_id'],
            'operational_process_operation')
        if packet_migration(packet) is not None:
            outer.modules['dependency_operational_metadata'].validate_pending(
                **preflight_arguments(packet,decoded,outer,adapter,validated))
            refuse_v6_execution(packet)
        helpers=helper_owner(outer,buffers,rows,'child')
        source_buffers={n:buffers['dependency.'+n] for n in helpers.order}
        source_buffers['closure_manifest']=encoded(prepared['sources'])
        prep=outer.modules['dependency_operational_preparation'].Preparation(
            source_owner=outer,adapter_owner=adapter,request_bytes=raw,
            request_sha256=packet['request_sha256'],checked_sources=checked,documents=docs,
            original_receipts=packet['original_receipts'],ordinary=ordinary,
            ordinary_receipts=packet['ordinary_receipts'],legacy_seal_sha256=packet['seal_sha256'],
            reference_pins=packet['reference_pins'],prepared_repository_root=packet['repository_root'],
            **({'historical_migration':packet_migration(packet)} if packet_migration(packet) is not None else {}))
        context=outer.modules['dependency_host_entry'].make_context(validated)
        context['child_argv']=request['argv_prefix']+sys.argv[1:]
        result=outer.modules['dependency_operational_entry']._continue_child(
            request=prepared,request_sha256=packet['request_sha256'],checked_sources=checked,
            adapter_owner=adapter,helpers=helpers,dependency_source_buffers=source_buffers,
            runtime_wiring=runtime_wiring(outer),preparation=prep,context=context,
            identity=dict(operation_id=prepared['operation_id'],isolated=True,optimized=False,camera_commands=[]))
        evidence=dict(result['completion_evidence']);stdout=evidence.pop('stdout')
        need(type(stdout) is bytes and 0<len(stdout)<=16384 and sha(stdout)==evidence['stdout_sha256'],
            'operational_process_stdout')
        need(all(item.closed for item in (prep,helpers,adapter)) and prep.callback_lease.closed,
            'operational_process_cleanup')
        preflight_receipt=io.write_new(Path(request['folder'])/'pending-preflight.json',prep.preflight)
        terminal=dict(schema='disabled_operational_outer_child_v1',operation_id=prepared['operation_id'],
            status='complete_pending_composition',preflight_sha256=preflight_receipt['sha256'],
            request_sha256=packet['request_sha256'],evidence=evidence,
            preparation_closed=True,helpers_closed=True,adapter_closed=True,callback_closed=True,
            execution_authorized=False,feature_supported=False,recovery_proven=False,
            device_write_gate_passed=False,camera_commands=[])
        outer.intact()
        io.write_new(Path(request['folder'])/'outer-child.json',terminal)
    except BaseException as error:primary=error
    close_owned((prep,helpers,adapter,outer),primary)
    sys.stdout.buffer.write(stdout);sys.stdout.buffer.flush()
    return 0

def run_runtime(**kwargs):raise ValueError('real_activation_pending')
