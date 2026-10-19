"""Invented Windows metadata and transcripts; no dependency, file or socket I/O."""
import copy
import hashlib
import json
import stat
import unittest
from unittest.mock import patch

from tools import dependency_evidence as subject


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def receipt(path, index, size):
    stamp = dict(device=7, inode=index + 1, mode=stat.S_IFREG | 0o600,
        nlink=1, size=size, mtime_ns=1234, ctime_ns=5678, file_attributes=0)
    return dict(path=path, sha256=digest(['invented file', index]), size=size,
        opened_read_only=True, **{key:dict(stamp) for key in
        ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after')})


def transcripts(data):
    p, o = data['expectation'], data['observation']
    o['expectation_sha256'] = digest(p)
    events = []

    def event(name, payload):
        events.append(dict(sequence=len(events) + 1, event=name, data=payload))

    event('expectation_bound', dict(sha256=digest(p)))
    event('bootstrap_complete', dict(sha256=digest(o['startup'])))
    event('guard_installed', dict(backend='ctypes'))
    for alias, row in o['python_origins'].items():
        event('python_import', dict(alias=alias, receipt_sha256=digest(row)))
    for name, load in o['native_loads'].items():
        for kind, key in [('native_intent','intent'), ('native_audit','audit'), ('native_complete','after')]:
            event(kind, dict(name=name, sha256=digest(load[key])))
    event('vectors_complete', o['vectors'])
    event('guard_finished', dict(native_names=sorted(o['native_loads'])))
    raw = dict(schema='dependency_guard_transcript_v1', operation_id=p['operation_id'],
        expectation_sha256=digest(p), events=copy.deepcopy(events),
        **{key:o[key] for key in ('startup','python_origins','trusted_origins','native_loads','vectors')})
    data['raw_receipt_json'] = canonical(raw).decode('ascii') + '\n'
    o['raw_receipt_sha256'] = hashlib.sha256(data['raw_receipt_json'].encode()).hexdigest()
    anchor = dict(raw_receipt_sha256=o['raw_receipt_sha256'], operation_id=p['operation_id'])
    for kind in ('raw_written','raw_flushed','raw_fsynced','raw_closed','raw_reverified','callback_claimed'):
        event(kind, dict(anchor))
    event('callback_returned', dict(success=True))
    event('cleanup_complete', dict(aliases_released=True,finder_removed=True,native_wrapper_removed=True))
    o['events'] = events
    data['journal_jsonl'] = ''.join(canonical(row).decode('ascii') + '\n' for row in events)
    o['journal_sha256'] = hashlib.sha256(data['journal_jsonl'].encode()).hexdigest()


def fixture():
    paths = [f'FakePkg/module{i:02}.py' for i in range(11)]
    paths += [f'FakePkg/native/{name}.pyd' for name in ('cpu','aes','aesni','ecb','cbc')]
    paths += [f'FakePkg/data/item{i:03}.bin' for i in range(335)]
    rows = {path:receipt(path,i,(i % 13)+1) for i,path in enumerate(paths)}
    files = {path:{k:row[k] for k in ('sha256','size')} for path,row in rows.items()}
    flags = dict(execution_authorized=False,actual_runtime_verified=False,actual_binding_ready=False,camera_commands=[])
    manifest = dict(schema='activation_wheel_manifest_v1',status='wheel_buffer_manifest_validated',
        version='3.24.1',wheel_sha256=digest('wheel'),record_sha256=digest('RECORD'),
        files=files,roster_sha256=digest(files),record_rows=351,archive_entries=352,**flags)
    proof = dict(schema='activation_installed_proof_v1',status='installed_receipt_set_validated',
        roster_sha256=manifest['roster_sha256'],record_sha256=manifest['record_sha256'],
        files={path:dict(files[path],open_identity_sha256=digest(row)) for path,row in rows.items()},**flags)
    package = dict(manifest=manifest,installed_receipts=rows,installed_proof=proof)

    def origin(row, root):
        return dict(root=root,relative_path=row['path'],sha256=row['sha256'],size=row['size'],
            identity={k:row['lstat_before'][k] for k in ('device','inode','mode','size','mtime_ns')})

    python = {f'FakePkg.module{i:02}':origin(rows[paths[i]],'package') for i in range(11)}
    native = {f'native_{i}':origin(rows[paths[11+i]],'package') for i in range(5)}
    trusted_rows = {f'trusted{i}':receipt(path,1000+i,5) for i,path in enumerate(
        ['Lib/ctypes/__init__.py','DLLs/_ctypes.pyd','Lib/platform.py','Lib/ctypes/util.py','Lib/ctypes/_endian.py'])}
    trusted = {name:origin(row,'runtime') for name,row in trusted_rows.items()}
    p = dict(schema='dependency_expectation_v1',operation_id='invented-act-001',platform='windows',
        backend='ctypes',extension_suffix='.pyd',
        roots=dict(package=dict(path='X:/fixtures/package',identity_sha256=digest('package root')),
                   runtime=dict(path='Y:/fixtures/runtime',identity_sha256=digest('runtime root'))),
        python_origins=python,native_libraries=native,trusted_origins=trusted,
        source_sha256=dict(runtime=digest('source runtime'),guard=digest('source guard')),
        config_sha256=digest('config'),cache_sha256=digest('cache'),manifest_sha256=digest(manifest),
        installed_proof_sha256=digest(proof),vector_plan_sha256=digest('public-vector plan'),
        loader_kwargs={},no_fallback=True,bootstrap_boundary=['interpreter','stdlib','_ctypes','os_loader'])

    def observed(row, root):
        row=copy.deepcopy(row);row['path']=p['roots'][root]['path']+'/'+row['path'];return row

    loads = {}
    for name, expected in native.items():
        before=observed(rows[expected['relative_path']],'package')
        loads[name]=dict(intent=dict(api='ctypes.CDLL',arguments=[before['path'].replace('/','\\')],
            keyword_arguments={},before=before),audit=dict(api='ctypes.dlopen',argument=before['path']),after=copy.deepcopy(before))
    o = dict(schema='dependency_observation_v1',evidence_mode='invented',operation_id=p['operation_id'],
        expectation_sha256=digest(p),source_sha256=dict(p['source_sha256']),config_sha256=p['config_sha256'],
        cache_sha256=p['cache_sha256'],root_identities={k:v['identity_sha256'] for k,v in p['roots'].items()},
        startup=dict(isolated=True,no_site=True,no_user_site=True,no_bytecode=True,preloaded_package_aliases=[],bootstrap_boundary=list(p['bootstrap_boundary'])),
        python_origins={name:observed(rows[row['relative_path']],'package') for name,row in python.items()},
        trusted_origins={name:observed(row,'runtime') for name,row in trusted_rows.items()},
        native_loads=loads,vectors=dict(plan_sha256=p['vector_plan_sha256'],cases=12,comparisons=24,passed=True),
        raw_receipt_sha256='',journal_sha256='',events=[],transitive_os_dependencies_attested=False)
    data=dict(expectation=p,observation=o,package=package)
    transcripts(data)
    return data


BASE = fixture()


def event(data,name):
    return next(row for row in data['observation']['events'] if row['event']==name)


def renumber(data):
    for number,row in enumerate(data['observation']['events'],1):row['sequence']=number


class DependencyEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data=copy.deepcopy(BASE)

    def refused(self,code=None):
        with self.assertRaises(subject.EvidenceError) as caught:
            subject.validate_dependency_records(**self.data)
        if code:self.assertEqual(str(caught.exception),code)

    def test_complete_invented_contract_keeps_all_authority_false(self):
        before=copy.deepcopy(self.data)
        result=subject.validate_dependency_records(**self.data)
        self.assertEqual(result['payload_files'],351)
        self.assertEqual((result['python_origins'],result['native_loads'],result['trusted_origins']),(11,5,5))
        for key in ['complete_before_any_cipher_use','historical_events_authenticated','fresh_observation_performed',
                    'execution_authorized','operational_acceptance','feature_supported','recovery_proven','device_write_gate_passed']:
            self.assertIs(result[key],False)
        self.assertEqual(result['camera_commands'],[])
        self.assertEqual(self.data,before)

    def test_saved_mode_is_still_only_consistency(self):
        self.data['observation']['evidence_mode']='saved_records'
        result=subject.validate_dependency_records(**self.data)
        self.assertIs(result['historical_events_authenticated'],False)

    def test_raw_loader_spellings_preserved_while_normalized_target_matches(self):
        first=subject.validate_dependency_records(**self.data)
        self.data['observation']['native_loads']['native_0']['intent']['arguments'][0]='x:/fixtures/package/FakePkg/native/../native/cpu.pyd'
        transcripts(self.data)
        second=subject.validate_dependency_records(**self.data)
        self.assertNotEqual(first['observation_sha256'],second['observation_sha256'])

    def test_explicit_zero_winmode_is_not_false(self):
        self.data['expectation']['loader_kwargs']={'winmode':0}
        for row in self.data['observation']['native_loads'].values():row['intent']['keyword_arguments']={'winmode':False}
        transcripts(self.data);self.refused('loader_arguments')

    def test_admitted_explicit_winmode_remains_unattested(self):
        self.data['expectation']['loader_kwargs']={'winmode':8}
        for row in self.data['observation']['native_loads'].values():row['intent']['keyword_arguments']={'winmode':8}
        transcripts(self.data)
        self.assertIs(subject.validate_dependency_records(**self.data)['execution_authorized'],False)

    def test_same_api_ctime_may_differ_between_apis(self):
        row=self.data['observation']['python_origins']['FakePkg.module00']
        row['fstat_before']['ctime_ns']=row['fstat_after']['ctime_ns']=9999
        transcripts(self.data)
        self.assertEqual(subject.validate_dependency_records(**self.data)['status'],'dependency_record_contract_consistent')

    def test_same_api_file_change_is_refused(self):
        self.data['observation']['python_origins']['FakePkg.module00']['fstat_after']['ctime_ns']+=1
        self.refused('file_changed')

    def test_native_completion_without_expected_identity(self):
        row=self.data['observation']['native_loads']['native_0']['after']
        for key in ('lstat_before','fstat_before','fstat_after','lstat_after'):row[key]['inode']+=1
        self.refused('expected_identity')

    def test_durable_receipt_hash_mismatch(self):
        self.data['raw_receipt_json']+=' '
        self.refused('transcript_hash')

    def test_journal_hash_mismatch(self):
        self.data['journal_jsonl']+='\n'
        self.refused('journal_lines')

    def test_journal_other_events_with_valid_hash_refused(self):
        rows=[json.loads(line) for line in self.data['journal_jsonl'].splitlines()]
        rows[-1]['data']['aliases_released']=False
        text=''.join(canonical(row).decode()+'\n' for row in rows)
        self.data['journal_jsonl']=text
        self.data['observation']['journal_sha256']=hashlib.sha256(text.encode()).hexdigest()
        self.refused('journal_projection')

    def test_raw_other_origin_with_valid_hash_refused(self):
        raw=json.loads(self.data['raw_receipt_json']);raw['trusted_origins']['trusted0']['sha256']=digest('substitute')
        text=canonical(raw).decode()+'\n';self.data['raw_receipt_json']=text
        o=self.data['observation'];o['raw_receipt_sha256']=hashlib.sha256(text.encode()).hexdigest()
        for row in o['events']:
            if 'raw_receipt_sha256' in row['data']:row['data']['raw_receipt_sha256']=o['raw_receipt_sha256']
        self.data['journal_jsonl']=''.join(canonical(row).decode()+'\n' for row in o['events'])
        o['journal_sha256']=hashlib.sha256(self.data['journal_jsonl'].encode()).hexdigest()
        self.refused('raw_projection')

    def test_duplicate_json_keys_refused(self):
        self.data['raw_receipt_json']='{"schema":"one","schema":"two"}'
        self.refused('duplicate_key')

    def test_float_or_nonfinite_json_refused(self):
        for number in ['1.0','NaN','Infinity']:
            with self.subTest(number=number):
                self.data['raw_receipt_json']='{"x":'+number+'}'
                self.refused('json_number')

    def test_transcript_utf8_byte_bound_before_encoding_whole_text(self):
        self.data['raw_receipt_json']='\U0001f600'*(1024**2+1)
        self.refused('transcript_bound')

    def test_aggregate_escaped_strings_refused_before_container_serialization(self):
        value=[['\U0001f600'*2048]*2000]*2
        original=subject._canonical
        def scalar_only(value):
            self.assertNotIsInstance(value,(dict,list))
            return original(value)
        with patch.object(subject,'_canonical',side_effect=scalar_only):
            with self.assertRaisesRegex(subject.EvidenceError,'^bound$'):subject._bounded_copy(value)

    def test_aggregate_escaped_keys_refused_before_container_serialization(self):
        value=[{('\u0001'*1000)+str(i):None for i in range(2000)}]
        original=subject._canonical
        def scalar_only(value):
            self.assertNotIsInstance(value,(dict,list))
            return original(value)
        with patch.object(subject,'_canonical',side_effect=scalar_only):
            with self.assertRaisesRegex(subject.EvidenceError,'^bound$'):subject._bounded_copy(value)

    def test_exception_does_not_echo_private_input(self):
        self.data['expectation']['roots']['runtime']['path']='PRIVATE-INPUT-secret'
        with self.assertRaises(subject.EvidenceError) as caught:subject.validate_dependency_records(**self.data)
        self.assertNotIn('PRIVATE',str(caught.exception))


def mutation_test(mutator, code):
    def run(self):
        mutator(self.data)
        # Bind the changed expectation to ensure policy-specific negatives do
        # not pass merely because a generic digest mismatch was noticed first.
        self.data['observation']['expectation_sha256']=digest(self.data['expectation'])
        event(self.data,'expectation_bound')['data']['sha256']=digest(self.data['expectation'])
        self.refused(code)
    return run


def put(where, key, value):
    return lambda data:where(data).__setitem__(key,value)


MUTATIONS = {
    'unknown_policy_field':(put(lambda d:d['expectation'],'execution_authorized',True),'shape'),
    'unsupported_policy_version':(put(lambda d:d['expectation'],'schema','dependency_expectation_v99'),'policy_schema'),
    'unsupported_backend':(put(lambda d:d['expectation'],'backend','cffi'),'policy_schema'),
    'fallback_enabled':(put(lambda d:d['expectation'],'no_fallback',False),'policy_schema'),
    'unsupported_platform':(put(lambda d:d['expectation'],'platform','posix'),'policy_schema'),
    'blank_operation':(put(lambda d:d['expectation'],'operation_id',''),'operation'),
    'missing_native_roster':(put(lambda d:d['expectation'],'native_libraries',{}),'origin_roster'),
    'manifest_authorized':(put(lambda d:d['package']['manifest'],'execution_authorized',True),'authority'),
    'manifest_numeric_false':(put(lambda d:d['package']['manifest'],'execution_authorized',0),'authority'),
    'proof_numeric_false':(put(lambda d:d['package']['installed_proof'],'execution_authorized',0),'installed_proof'),
    'wrong_manifest_binding':(put(lambda d:d['expectation'],'manifest_sha256','0'*64),'package_binding'),
    'wrong_proof_binding':(put(lambda d:d['expectation'],'installed_proof_sha256','0'*64),'package_binding'),
    'wrong_record_binding':(put(lambda d:d['package']['installed_proof'],'record_sha256','0'*64),'installed_proof'),
    'wrong_roster_digest':(put(lambda d:d['package']['manifest'],'roster_sha256','0'*64),'roster'),
    'wrong_roster_count':(put(lambda d:d['package']['manifest'],'record_rows',350),'roster'),
    'boolean_roster_count':(put(lambda d:d['package']['manifest'],'record_rows',True),'integer'),
    'missing_installed_receipt':(lambda d:d['package']['installed_receipts'].pop('FakePkg/module00.py'),'shape'),
    'wrong_installed_token':(put(lambda d:d['package']['installed_proof']['files']['FakePkg/module00.py'],'open_identity_sha256','0'*64),'installed_proof'),
    'package_domain_replaced':(put(lambda d:d['expectation']['python_origins']['FakePkg.module00'],'root','runtime'),'origin_domain'),
    'trusted_domain_replaced':(put(lambda d:d['expectation']['trusted_origins']['trusted0'],'root','package'),'origin_domain'),
    'expected_package_hash_changed':(put(lambda d:d['expectation']['python_origins']['FakePkg.module00'],'sha256','0'*64),'package_origin'),
    'expected_package_inode_changed':(put(lambda d:d['expectation']['python_origins']['FakePkg.module00']['identity'],'inode',9999),'expected_identity'),
    'root_replaced':(put(lambda d:d['observation']['root_identities'],'runtime','0'*64),'root_identity'),
    'source_replaced':(put(lambda d:d['observation']['source_sha256'],'runtime','0'*64),'source_binding'),
    'config_replaced':(put(lambda d:d['observation'],'config_sha256','0'*64),'source_binding'),
    'operation_replaced':(put(lambda d:d['observation'],'operation_id','another-act'),'expectation_binding'),
    'site_enabled':(put(lambda d:d['observation']['startup'],'no_site',False),'startup'),
    'numeric_startup_true':(put(lambda d:d['observation']['startup'],'isolated',1),'startup'),
    'preloaded_package':(put(lambda d:d['observation']['startup'],'preloaded_package_aliases',['FakePkg']),'startup'),
    'bootstrap_boundary_removed':(put(lambda d:d['expectation'],'bootstrap_boundary',[]),'bootstrap'),
    'transitive_os_claim':(put(lambda d:d['observation'],'transitive_os_dependencies_attested',True),'unsupported_attestation'),
    'cipher_before_receipt_claim':(put(lambda d:d['observation'],'complete_before_cipher_use',True),'shape'),
    'failed_vectors':(put(lambda d:d['observation']['vectors'],'passed',False),'vectors'),
    'missing_comparisons':(put(lambda d:d['observation']['vectors'],'comparisons',23),'vectors'),
    'boolean_case_count':(put(lambda d:d['observation']['vectors'],'cases',True),'integer'),
    'wrong_vector_plan':(put(lambda d:d['observation']['vectors'],'plan_sha256','0'*64),'vectors'),
    'missing_python_origin':(lambda d:d['observation']['python_origins'].pop('FakePkg.module00'),'shape'),
    'missing_native_completion':(lambda d:d['observation']['native_loads']['native_0'].pop('after'),'shape'),
    'unexpected_native_load':(put(lambda d:d['observation']['native_loads'],'unexpected',{}),'shape'),
    'audit_wrong_api':(put(lambda d:d['observation']['native_loads']['native_0']['audit'],'api','ctypes.CDLL'),'loader_api'),
    'intent_wrong_api':(put(lambda d:d['observation']['native_loads']['native_0']['intent'],'api','cffi.FFI.dlopen'),'loader_api'),
    'unexpected_loader_kwarg':(put(lambda d:d['observation']['native_loads']['native_0']['intent'],'keyword_arguments',{'handle':1}),'loader_arguments'),
    'extra_loader_argument':(put(lambda d:d['observation']['native_loads']['native_0']['intent'],'arguments',['X:/fixtures/package/FakePkg/native/cpu.pyd','unexpected']),'loader_arguments'),
    'wrong_loader_target':(put(lambda d:d['observation']['native_loads']['native_0']['audit'],'argument','X:/elsewhere/cpu.pyd'),'loader_target'),
    'unc_loader_target':(put(lambda d:d['observation']['native_loads']['native_0']['audit'],'argument','\\\\server\\share\\cpu.pyd'),'loader_path'),
    'relative_loader_target':(put(lambda d:d['observation']['native_loads']['native_0']['audit'],'argument','cpu.pyd'),'loader_path'),
    'missing_guard_event':(lambda d:d['observation']['events'].remove(event(d,'guard_installed')),'event_order'),
    'native_audit_without_intent':(lambda d:d['observation']['events'].remove(event(d,'native_intent')),'native_event'),
    'native_completion_before_audit':(put(lambda d:event(d,'native_audit'),'event','native_complete'),'native_event'),
    'wrong_event_receipt_hash':(put(lambda d:event(d,'native_intent')['data'],'sha256','0'*64),'event_order'),
    'missing_fsync':(lambda d:d['observation']['events'].remove(event(d,'raw_fsynced')),'event_order'),
    'callback_before_durable_close':(put(lambda d:event(d,'raw_closed'),'event','callback_claimed'),'event_order'),
    'wrong_durable_receipt_hash':(put(lambda d:event(d,'raw_fsynced')['data'],'raw_receipt_sha256','0'*64),'event_order'),
    'callback_failed':(put(lambda d:event(d,'callback_returned')['data'],'success',False),'event_order'),
    'cleanup_incomplete':(put(lambda d:event(d,'cleanup_complete')['data'],'finder_removed',False),'event_order'),
    'extra_callback_event':(lambda d:d['observation']['events'].append(copy.deepcopy(event(d,'callback_claimed'))),'extra_event'),
    'missing_reverification':(lambda d:d['observation']['events'].remove(event(d,'raw_reverified')),'event_order'),
    'duplicate_python_import':(lambda d:d['observation']['events'].insert(4,copy.deepcopy(event(d,'python_import'))),'python_event'),
    'guard_reinstalled_midstream':(put(lambda d:event(d,'native_intent'),'event','guard_installed'),'incomplete_loads'),
    'missing_expected_native':(lambda d:d['observation']['native_loads'].pop('native_0'),'shape'),
    'unsafe_trusted_reparse':(put(lambda d:d['observation']['trusted_origins']['trusted0']['lstat_before'],'file_attributes',0x400),'file_kind'),
    'package_hardlink':(put(lambda d:d['package']['installed_receipts']['FakePkg/module00.py']['fstat_before'],'nlink',2),'file_kind'),
    'opened_writable_package':(put(lambda d:d['package']['installed_receipts']['FakePkg/module00.py'],'opened_read_only',False),'receipt_binding'),
    'cross_api_mode_drift':(put(lambda d:d['observation']['trusted_origins']['trusted0']['fstat_before'],'mode',stat.S_IFREG|0o700),'file_changed'),
    'extra_cleanup_field':(put(lambda d:event(d,'cleanup_complete')['data'],'private_diagnostic','must-not-publish'),'event_order'),
    'boolean_sequence':(put(lambda d:event(d,'expectation_bound'),'sequence',True),'integer'),
    'policy_loader_boolean':(put(lambda d:d['expectation'],'loader_kwargs',{'winmode':True}),'integer'),
}

for name,(mutator,code) in MUTATIONS.items():
    setattr(DependencyEvidenceTests,'test_refuses_'+name,mutation_test(mutator,code))


class PathPolicyTests(unittest.TestCase):
    def test_relative_path_traversal_absolute_reserved_and_aliases_refused(self):
        for path in ['../x.py','a/../x.py','/x.py','C:/x.py','a\\x.py','a//x.py',
                     'CON.py','COM¹.txt','x.','x ','a:*','e\u0301.py','a/./x.py']:
            with self.subTest(path=path):
                with self.assertRaises(subject.EvidenceError):subject._relative(path)

    def test_overlapping_and_case_equivalent_roots_refused(self):
        for root in ['X:/fixtures/package','X:/fixtures/package/nested','X:/fixtures','x:/fixtures/package']:
            with self.subTest(root=root):
                data=copy.deepcopy(BASE);data['expectation']['roots']['runtime']['path']=root
                with self.assertRaises(subject.EvidenceError):subject.validate_dependency_records(**data)

    def test_package_file_casefold_duplicate_refused(self):
        data=copy.deepcopy(BASE)
        files=data['package']['manifest']['files'];files['fakepkg/MODULE00.py']=files.pop('FakePkg/data/item000.bin')
        with self.assertRaisesRegex(subject.EvidenceError,'^duplicate_path$'):subject.validate_dependency_records(**data)

    def test_closed_origin_roster_rejects_trusted_package_alias_collision(self):
        data=copy.deepcopy(BASE);rows=data['expectation']['trusted_origins']
        rows['FakePkg.module00']=rows.pop('trusted0')
        with self.assertRaisesRegex(subject.EvidenceError,'^duplicate_alias$'):subject.validate_dependency_records(**data)


if __name__=='__main__':unittest.main(verbosity=2)
