"""Invented old-format records only. No private files, crypto or native loads."""
import copy
import hashlib
import json
import ntpath
import stat
import unittest

from tools import dependency_legacy as subject
from tools.dependency_evidence import EvidenceError


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def win(path):
    return path.replace('/', '\\')


def fixture():
    aliases = ['Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Cipher.AES',
        'Cryptodome.Cipher._mode_ecb', 'Cryptodome.Cipher._mode_cbc', 'Cryptodome.Random',
        'Cryptodome.Util', 'Cryptodome.Util._raw_api', 'Cryptodome.Util._cpu_features',
        'Cryptodome.Util._file_system', 'Cryptodome.Util.py3compat']
    packages = ['Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Random', 'Cryptodome.Util']
    py = {n:n.replace('.', '/') + ('/__init__.py' if n in packages else '.py') for n in aliases}
    native = {'cpuid':'Cryptodome/Util/_cpuid_c.pyd', 'aes':'Cryptodome/Cipher/_raw_aes.pyd',
        'aesni':'Cryptodome/Cipher/_raw_aesni.pyd', 'ecb':'Cryptodome/Cipher/_raw_ecb.pyd', 'cbc':'Cryptodome/Cipher/_raw_cbc.pyd'}
    trusted = {'ctypes':'Lib/ctypes/__init__.py', '_ctypes':'DLLs/_ctypes.pyd',
        'ctypes.util':'Lib/ctypes/util.py', 'ctypes._endian':'Lib/ctypes/_endian.py', 'platform':'Lib/platform.py'}
    package_root = 'X:/fixtures/venv/Lib/site-packages'
    base = 'Y:/fixtures/runtime'
    def receipt(path, index):
        stamp = dict(device=7, inode=index, mode=stat.S_IFREG | 0o600, nlink=1,
            size=7, mtime_ns=1234, ctime_ns=5678, file_attributes=0)
        return dict(path=path, size=7, sha256=digest(['invented', index]), opened_read_only=True,
            **{k:dict(stamp) for k in ['lstat_before','fstat_before','fstat_after','lstat_after']})
    paths = list(py.values()) + list(native.values()) + [f'Cryptodome/data/item{i:03}.bin' for i in range(335)]
    receipts = {p:receipt(p,i+1) for i,p in enumerate(paths)}
    files = {p:{k:row[k] for k in ('sha256','size')} for p,row in receipts.items()}
    flags = dict(execution_authorized=False, actual_runtime_verified=False, actual_binding_ready=False, camera_commands=[])
    manifest = dict(schema='activation_wheel_manifest_v1', status='wheel_buffer_manifest_validated', version='3.24.1',
        wheel_sha256=digest('wheel'), record_sha256=digest('record'), files=files,
        roster_sha256=digest(files), record_rows=351, archive_entries=352, **flags)
    proof = dict(schema='activation_installed_proof_v1',status='installed_receipt_set_validated',
        roster_sha256=manifest['roster_sha256'],record_sha256=manifest['record_sha256'],
        files={p:dict(files[p],open_identity_sha256=digest(row)) for p,row in receipts.items()},**flags)
    def origin(row, domain):
        return dict(root=domain,relative_path=row['path'],size=row['size'],sha256=row['sha256'],
            identity={k:row['lstat_before'][k] for k in ['device','inode','mode','size','mtime_ns']})
    trusted_receipts = {n:receipt(p,i+1000) for i,(n,p) in enumerate(trusted.items())}
    policy = dict(schema='dependency_expectation_v1', operation_id='a'*32, platform='windows',backend='ctypes',extension_suffix='.pyd',
        roots=dict(package=dict(path=package_root,identity_sha256=digest('package root')),
                   runtime=dict(path=base,identity_sha256=digest('runtime root'))),
        python_origins={n:origin(receipts[p],'package') for n,p in py.items()},
        native_libraries={n:origin(receipts[p],'package') for n,p in native.items()},
        trusted_origins={n:origin(row,'runtime') for n,row in trusted_receipts.items()},
        source_sha256=dict(runtime=digest('authored runtime source'), continuation=digest('authored continuation source')),
        config_sha256='',cache_sha256=digest('source cache'),manifest_sha256=digest(manifest),
        installed_proof_sha256=digest(proof),vector_plan_sha256='',loader_kwargs={},no_fallback=True,
        bootstrap_boundary=['interpreter','stdlib','_ctypes','os_loader'])
    def triple(row, root):
        return dict(path=win(root+'/'+row['path']),bytes=row['size'],sha256=row['sha256'])
    def legacy(row, root):
        return dict(triple(row,root),**{k:copy.deepcopy(row[k]) for k in ['lstat_before','fstat_before','fstat_after','lstat_after']},
            read_calls=2,eof_probes=1,closed=True)
    # Public known-answer metadata, not private keys or an executed cipher.
    vectors = [{'id': 'ECB-128', 'mode': 'ECB', 'key_bits': 128, 'key_hex': '2b7e151628aed2a6abf7158809cf4f3c', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': None, 'ciphertext_hex': '3ad77bb40d7a3660a89ecaf32466ef97f5d3d58503b9699de785895a96fdbaaf43b1cd7f598ece23881b00e3ed0306887b0c785e27e8ad3f8223207104725dd4'}, {'id': 'ECB-192', 'mode': 'ECB', 'key_bits': 192, 'key_hex': '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': None, 'ciphertext_hex': 'bd334f1d6e45f25ff712a214571fa5cc974104846d0ad3ad7734ecb3ecee4eefef7afd2270e2e60adce0ba2face6444e9a4b41ba738d6c72fb16691603c18e0e'}, {'id': 'ECB-256', 'mode': 'ECB', 'key_bits': 256, 'key_hex': '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': None, 'ciphertext_hex': 'f3eed1bdb5d2a03c064b5a7e3db181f8591ccb10d410ed26dc5ba74a31362870b6ed21b99ca6f4f9f153e7b1beafed1d23304b7a39f9f3ff067d8d8f9e24ecc7'}, {'id': 'CBC-128', 'mode': 'CBC', 'key_bits': 128, 'key_hex': '2b7e151628aed2a6abf7158809cf4f3c', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': '000102030405060708090a0b0c0d0e0f', 'ciphertext_hex': '7649abac8119b246cee98e9b12e9197d5086cb9b507219ee95db113a917678b273bed6b8e3c1743b7116e69e222295163ff1caa1681fac09120eca307586e1a7'}, {'id': 'CBC-192', 'mode': 'CBC', 'key_bits': 192, 'key_hex': '8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': '000102030405060708090a0b0c0d0e0f', 'ciphertext_hex': '4f021db243bc633d7178183a9fa071e8b4d9ada9ad7dedf4e5e738763f69145a571b242012fb7ae07fa9baac3df102e008b0e27988598881d920a9e64f5615cd'}, {'id': 'CBC-256', 'mode': 'CBC', 'key_bits': 256, 'key_hex': '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4', 'plaintext_hex': '6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710', 'iv_hex': '000102030405060708090a0b0c0d0e0f', 'ciphertext_hex': 'f58c4c04d6e5f1ba779eabfb5f7bfbd69cfc4e967edb808d679f777bc6702c7d39f23369a9d9bacfa530e26304231461b2eb05e2c39be9fcda6c19078c6a9d1b'}]
    config = dict(schema='dependency_probe_config_v1',operation_id=policy['operation_id'],
        package_root=win(package_root+'/Cryptodome'),source_rows={n:triple(receipts[p],package_root) for n,p in py.items()},
        native_rows={n:triple(receipts[p],package_root) for n,p in native.items()},
        trusted_origins={n:triple(row,base) for n,row in trusted_receipts.items()},vectors=vectors)
    policy['config_sha256']=hashlib.sha256(encoded(config)+b'\n').hexdigest();policy['vector_plan_sha256']=digest(vectors)
    startup=dict(implementation='cpython',version=[3,13,12],platform='win32',os_name='nt',maxsize=2**63-1,
        isolated=1,no_site=1,dont_write_bytecode=True,optimize=0,executable=win('X:/fixtures/venv/Scripts/python.exe'),
        base_executable=win(base+'/python.exe'),prefix=win(base),base_prefix=win(base),
        path=[win(base+'/'+p) for p in ['python313.zip','DLLs','Lib']]+[win(base)])
    probe = {k:copy.deepcopy(startup[k]) for k in ['executable','base_executable','prefix','base_prefix','path','isolated','no_site','dont_write_bytecode']}
    probe.update(version='3.13.12 invented interpreter', normalized_path=[ntpath.normcase(ntpath.normpath(p)) for p in startup['path']],
        pre_guard_modules=['abc','os','sys'],pre_guard_ctypes_loaded=False)
    trusted_observed={n:legacy(row,base) for n,row in trusted_receipts.items()}
    events=[]
    def emit(name,data):events.append(dict(sequence=len(events)+1,event=name,data=copy.deepcopy(data)))
    emit('probe_started',dict(operation_id=config['operation_id'],test_injection_used=False,startup=probe))
    emit('trusted_bootstrap_native',dict(argument=None,guarded_file_origin=False))
    emit('trusted_bootstrap_native',dict(argument='kernel32',guarded_file_origin=False))
    emit('trusted_backend_initialized',dict(origins=trusted_observed,guarded_initialization=False))
    # Nested source execution is intentional; completion order is LIFO.
    for n,row in config['source_rows'].items():emit('source_execute_intent',dict(alias=n,path=row['path'],sha256=row['sha256']))
    for n,row in reversed(list(config['source_rows'].items())):emit('source_execute_complete',dict(alias=n,path=row['path'],sha256=row['sha256']))
    intents=[]; completions=[]
    for index,(name,path) in enumerate(native.items(),1):
        row=legacy(receipts[path],package_root)
        intent=dict(logical=name,path=row['path'],sha256=row['sha256'],bytes=row['bytes'],api='ctypes.CDLL',
            arguments=[row['path']],keyword_arguments={},before=row,audit_seen=True,audit_argument=row['path'])
        complete=dict(logical=name,intent_sequence=index,after=copy.deepcopy(row),audit_seen=True)
        emit('native_intent',dict(intent,audit_seen=False,audit_argument=None))
        emit('native_audit',dict(logical=name,raw_request=row['path'],audit_argument=row['path'],effective_winmode_observed=False))
        emit('native_completion',complete);intents.append(intent);completions.append(complete)
    cases=[dict(id=row['id'],branch_request=branch,encrypt=True,decrypt=True) for row in vectors for branch in ['default','generic']]
    for case in cases:emit('vector_case',case)
    emit('computation_complete',dict(cases=12,checks=24,native_completions=5))
    raw=dict(schema='dependency_probe_raw_result_v1',status='complete_dependency_vectors',operation_id=config['operation_id'],
        evidence_class='runtime-observed',test_injection_used=False,config_sha256=policy['config_sha256'],cache_sha256=policy['cache_sha256'],
        source_origins=copy.deepcopy(config['source_rows']),trusted_origins=trusted_observed,
        native_receipt=dict(schema='dependency_probe_native_receipt_v1',backend='ctypes',intents=intents,completions=completions,
            aesni_loaded=True,failures=[],audit_required=True,transitive_os_dependencies_attested=False),cases=cases,checks=24,events=events,
        gdt_execution_authorized=False,actual_gdt_entry_ready=False,feature_supported=False,camera_commands=[],
        limitations=['Trusted stdlib and _ctypes initialization are not package guarded-load proof.',
            'Pre/post path hashes do not attest the OS-mapped bytes or all transitive DLLs.',
            'This -I -S startup does not qualify a legacy -I GDT entry.'])
    completion=dict(schema='gdt_dependency_continuation_result_v1',status='protected_callback_returned',
        callback_result=dict(status='public_vectors_during_live_continuation',checks=24,durable_receipt_verified_before_callback=True,
            camera_commands=[],gdt_execution_authorized=False,feature_supported=False),provenance={},test_injection_used=False,
        evidence_class='runtime-observed',actual_gdt_entry_ready=False,gdt_execution_authorized=False,feature_supported=False,camera_commands=[],
        fresh_source_receipts={n:legacy(receipts[p],package_root) for n,p in py.items()},
        source_finder_and_alias_cleanup_verified=True,runtime_source_sha256=policy['source_sha256']['runtime'])
    data=dict(expectation=policy,package=dict(manifest=manifest,installed_receipts=receipts,installed_proof=proof),
        config=config,completion=completion,raw_receipt_json='',journal_jsonl='')
    journal=[dict(sequence=1,event='integrated_entry_started',data=dict(startup=startup,test_injection_used=False,
        actual_gdt_entry_ready=False,gdt_execution_authorized=False))]+[dict(row,sequence=row['sequence']+1) for row in events]
    for name,payload in [('native_provenance_persisted',{}),('protected_callback_claimed',{}),('protected_callback_returned',dict(attempt=1))]:
        journal.append(dict(sequence=len(journal)+1,event=name,data=payload))
    rebind(data,raw,journal)
    return data


def rebind(data,raw=None,journal=None):
    if raw is None:raw=json.loads(data['raw_receipt_json'])
    if journal is None:journal=[json.loads(line) for line in data['journal_jsonl'].splitlines()]
    text=encoded(raw).decode()+'\n';data['raw_receipt_json']=text
    anchor=dict(path=win('Z:/invented-output/provenance.json'),sha256=hashlib.sha256(text.encode()).hexdigest(),bytes=len(text.encode()))
    data['completion']['provenance']=anchor
    journal[-3]['data']=copy.deepcopy(anchor);journal[-2]['data']=dict(provenance=copy.deepcopy(anchor),attempt=1)
    data['journal_jsonl']=''.join(encoded(row).decode()+'\n' for row in journal)


def rebuild(data,raw):
    journal=[json.loads(row) for row in data['journal_jsonl'].splitlines()]
    for i,row in enumerate(raw['events'],1):row['sequence']=i
    journal=journal[:1]+[dict(row,sequence=row['sequence']+1) for row in raw['events']]+journal[-3:]
    for i,row in enumerate(journal,1):row['sequence']=i
    rebind(data,raw,journal)


def resize_source(data,alias,size):
    raw=json.loads(data['raw_receipt_json'])
    p=data['expectation']; row=p['python_origins'][alias];path=row['relative_path']
    row['size']=size;row['identity']['size']=size
    data['config']['source_rows'][alias]['bytes']=size;raw['source_origins'][alias]['bytes']=size
    installed=data['package']['installed_receipts'][path];installed['size']=size
    fresh=data['completion']['fresh_source_receipts'][alias];fresh['bytes']=size
    for receipt in [installed,fresh]:
        for key in ['lstat_before','fstat_before','fstat_after','lstat_after']:receipt[key]['size']=size
    fresh['read_calls']=(size+1024**2-1)//1024**2+1
    m=data['package']['manifest'];m['files'][path]['size']=size;m['roster_sha256']=digest(m['files'])
    proof=data['package']['installed_proof'];proof['roster_sha256']=m['roster_sha256']
    proof['files'][path]=dict(m['files'][path],open_identity_sha256=digest(installed))
    p['manifest_sha256']=digest(m);p['installed_proof_sha256']=digest(proof)
    p['config_sha256']=hashlib.sha256(encoded(data['config'])+b'\n').hexdigest();raw['config_sha256']=p['config_sha256']
    rebind(data,raw)


BASE=fixture()


class LegacyAdapterTests(unittest.TestCase):
    def setUp(self):self.data=copy.deepcopy(BASE)
    def refused(self,code=None):
        with self.assertRaises(EvidenceError) as caught:subject.adapt_legacy_dependency_records(**self.data)
        if code:self.assertEqual(str(caught.exception),code)

    def test_lossless_envelope_remains_blocked(self):
        before=copy.deepcopy(self.data);out=subject.adapt_legacy_dependency_records(**self.data)
        self.assertEqual(self.data,before)
        self.assertEqual(out['original_raw_receipt_json'],self.data['raw_receipt_json'])
        self.assertEqual(out['original_journal_jsonl'],self.data['journal_jsonl'])
        self.assertEqual((out['python_origins'],out['native_loads'],out['trusted_origins']),(11,5,5))
        self.assertIn('individual_durability_steps_not_journaled',out['blockers'])
        for key in ['successor_contract_applied','actual_records_observed','historical_events_authenticated','execution_authorized',
                    'operational_acceptance','feature_supported','recovery_proven','device_write_gate_passed']:
            self.assertIs(out[key],False)
        self.assertEqual(out['camera_commands'],[])

    def test_detached_envelope_does_not_alias_mutable_input(self):
        out=subject.adapt_legacy_dependency_records(**self.data)
        out['config']['source_rows'].clear();self.assertEqual(len(self.data['config']['source_rows']),11)

    def test_exact_whitespace_preserved_when_anchor_rebound(self):
        text=json.dumps(json.loads(self.data['raw_receipt_json']),indent=2)+'\n\n'
        self.data['raw_receipt_json']=text
        anchor=self.data['completion']['provenance'];anchor.update(sha256=hashlib.sha256(text.encode()).hexdigest(),bytes=len(text.encode()))
        journal=[json.loads(row) for row in self.data['journal_jsonl'].splitlines()]
        journal[-3]['data']=dict(anchor);journal[-2]['data']['provenance']=dict(anchor)
        self.data['journal_jsonl']='\n'.join(json.dumps(row,indent=None) for row in journal)+'\n'
        out=subject.adapt_legacy_dependency_records(**self.data)
        self.assertEqual(out['original_raw_receipt_json'],text)

    def test_raw_changed_without_anchor_refused(self):
        self.data['raw_receipt_json']+=' ';self.refused('legacy_raw_hash')

    def test_unknown_raw_field_is_refused_even_with_new_hash(self):
        raw=json.loads(self.data['raw_receipt_json']);raw['unknown']='do not discard';rebind(self.data,raw)
        self.refused('shape')

    def test_duplicate_key_refused(self):
        self.data['raw_receipt_json']='{"schema":1,"schema":2}';self.refused('duplicate_key')

    def test_missing_event_refused_even_when_reindexed_and_rehashed(self):
        raw=json.loads(self.data['raw_receipt_json']);raw['events'].pop(3)
        for i,row in enumerate(raw['events'],1):row['sequence']=i
        rebind(self.data,raw);self.refused('legacy_events')

    def test_raw_journal_projection_mismatch_refused(self):
        rows=[json.loads(row) for row in self.data['journal_jsonl'].splitlines()];rows[1]['data']['test_injection_used']=True
        self.data['journal_jsonl']=''.join(encoded(row).decode()+'\n' for row in rows);self.refused('legacy_journal')

    def test_source_import_stack_mismatch_refused(self):
        raw=json.loads(self.data['raw_receipt_json']);completes=[r for r in raw['events'] if r['event']=='source_execute_complete']
        completes[0]['data'],completes[1]['data']=completes[1]['data'],completes[0]['data']
        rebind(self.data,raw);self.refused('legacy_import')

    def test_vector_during_unfinished_source_execution_refused_fully_rebound(self):
        raw=json.loads(self.data['raw_receipt_json']);rows=raw['events']
        imports=[r for r in rows if r['event']=='source_execute_intent']
        completes=[r for r in rows if r['event']=='source_execute_complete']
        native=[r for r in rows if r['event'].startswith('native_')]
        vectors=[r for r in rows if r['event']=='vector_case']
        raw['events']=rows[:4]+imports+native+vectors+completes+rows[-1:]
        rebuild(self.data,raw);self.refused('legacy_import')

    def test_ctypes_module_flag_contradiction_refused_fully_rebound(self):
        raw=json.loads(self.data['raw_receipt_json'])
        startup=raw['events'][0]['data']['startup'];startup['pre_guard_modules']=sorted(startup['pre_guard_modules']+['_ctypes'])
        rebuild(self.data,raw);self.refused('legacy_startup')

    def test_native_loads_after_vectors_refused_fully_rebound(self):
        raw=json.loads(self.data['raw_receipt_json']);rows=raw['events']
        early=[r for r in rows[:-1] if not r['event'].startswith('native_')]
        native=[r for r in rows if r['event'].startswith('native_')]
        raw['events']=early+native+rows[-1:]
        rebuild(self.data,raw);self.refused('legacy_native_order')

    def test_oversized_producer_event_refused_fully_rebound(self):
        raw=json.loads(self.data['raw_receipt_json'])
        raw['events'][0]['data']['startup']['pre_guard_modules']=[f'harmless{i:04}_'+('x'*80) for i in range(1000)]
        rebuild(self.data,raw);self.refused('legacy_event_bound')

    def test_oversized_canonical_publication_refused_before_shape(self):
        raw=json.loads(self.data['raw_receipt_json']);raw['padding']={str(i):'x'*2048 for i in range(1050)}
        rebind(self.data,raw);self.refused('legacy_publication_bound')

    def test_oversized_journal_entry_refused(self):
        rows=[json.loads(row) for row in self.data['journal_jsonl'].splitlines()]
        rows[0]['data']['startup']['path']=['x'*80 for _ in range(1000)]
        self.data['journal_jsonl']=''.join(encoded(row).decode()+'\n' for row in rows);self.refused('legacy_event_bound')

    def test_public_vector_substitution_refused_despite_all_hashes_rebound(self):
        for key in ['key_hex','plaintext_hex','ciphertext_hex','iv_hex']:
            with self.subTest(key=key):
                self.data=copy.deepcopy(BASE);config=self.data['config'];config['vectors'][3][key]='0'*len(config['vectors'][3][key])
                p=self.data['expectation'];p['config_sha256']=hashlib.sha256(encoded(config)+b'\n').hexdigest();p['vector_plan_sha256']=digest(config['vectors'])
                raw=json.loads(self.data['raw_receipt_json']);raw['config_sha256']=p['config_sha256'];rebind(self.data,raw)
                self.refused('legacy_vector_plan')

    def test_oversized_source_refused_despite_all_metadata_rebound(self):
        resize_source(self.data,'Cryptodome',1024**2+1);self.refused('integer')

    def test_aggregate_sources_refused_despite_all_metadata_rebound(self):
        for alias in list(self.data['config']['source_rows'])[:5]:resize_source(self.data,alias,1024**2)
        self.refused('legacy_source_budget')

    def test_lazy_cbc_import_and_native_load_between_vector_cases_accepted(self):
        raw=json.loads(self.data['raw_receipt_json']);rows=raw['events'];alias='Cryptodome.Cipher._mode_cbc'
        pairs=[]
        for name,row in self.data['config']['source_rows'].items():
            if name!=alias:
                data=dict(alias=name,path=row['path'],sha256=row['sha256'])
                pairs.extend([dict(event='source_execute_intent',data=data),dict(event='source_execute_complete',data=data)])
        native=[r for r in rows if r['event'].startswith('native_')]
        early=[r for r in native if r['data']['logical']!='cbc'];late=[r for r in native if r['data']['logical']=='cbc']
        vectors=[r for r in rows if r['event']=='vector_case'];source=self.data['config']['source_rows'][alias]
        data=dict(alias=alias,path=source['path'],sha256=source['sha256'])
        raw['events']=rows[:4]+pairs+early+vectors[:6]+[dict(event='source_execute_intent',data=data)]+late+[dict(event='source_execute_complete',data=data)]+vectors[6:]+rows[-1:]
        rebuild(self.data,raw)
        self.assertEqual(subject.adapt_legacy_dependency_records(**self.data)['native_loads'],5)

    def test_exception_does_not_echo_private_text(self):
        self.data['config']['package_root']='PRIVATE-secret-path'
        with self.assertRaises(EvidenceError) as caught:subject.adapt_legacy_dependency_records(**self.data)
        self.assertNotIn('PRIVATE',str(caught.exception))


def raw_test(mutator,code=None):
    def run(self):
        raw=json.loads(self.data['raw_receipt_json']);mutator(raw);rebind(self.data,raw);self.refused(code)
    return run


RAW_MUTATIONS={
    'wrong_schema':(lambda r:r.update(schema='newer'),'legacy_raw'),
    'injected':(lambda r:r.update(test_injection_used=True),'legacy_raw'),
    'wrong_evidence':(lambda r:r.update(evidence_class='offline-tested'),'legacy_raw'),
    'wrong_operation':(lambda r:r.update(operation_id='b'*32),'legacy_raw'),
    'wrong_config_hash':(lambda r:r.update(config_sha256='0'*64),'legacy_binding'),
    'wrong_cache_hash':(lambda r:r.update(cache_sha256='0'*64),'legacy_binding'),
    'true_authority':(lambda r:r.update(gdt_execution_authorized=True),'authority'),
    'numeric_false':(lambda r:r.update(feature_supported=0),'authority'),
    'changed_limitations':(lambda r:r.update(limitations=['unlimited']*3),'legacy_limitations'),
    'missing_source':(lambda r:r['source_origins'].pop('Cryptodome'),'shape'),
    'source_path_traversal':(lambda r:r['source_origins']['Cryptodome'].update(path='X:\\fixtures\\..\\other.py'),'legacy_origin'),
    'unclosed_trusted':(lambda r:r['trusted_origins']['ctypes'].update(closed=False),'legacy_read'),
    'impossible_read_calls':(lambda r:r['trusted_origins']['ctypes'].update(read_calls=999),'legacy_read'),
    'boolean_eof':(lambda r:r['trusted_origins']['ctypes'].update(eof_probes=True),'integer'),
    'unobserved_audit':(lambda r:r['native_receipt'].update(audit_required=False),'legacy_native'),
    'transitive_claim':(lambda r:r['native_receipt'].update(transitive_os_dependencies_attested=True),'legacy_native'),
    'failed_load':(lambda r:r['native_receipt'].update(failures=['aes']),'legacy_native'),
    'missing_completion':(lambda r:r['native_receipt']['completions'].pop(),'legacy_native'),
    'missing_aesni':(lambda r:r['native_receipt'].update(aesni_loaded=False),'legacy_native'),
    'wrong_loader':(lambda r:r['native_receipt']['intents'][0].update(api='cffi.dlopen'),'legacy_loader'),
    'extra_loader_keyword':(lambda r:r['native_receipt']['intents'][0].update(keyword_arguments={'winmode':0}),'legacy_loader'),
    'mismatched_audit_target':(lambda r:r['native_receipt']['intents'][0].update(audit_argument='X:\\elsewhere\\cpuid.pyd'),'legacy_loader'),
    'boolean_completion_sequence':(lambda r:r['native_receipt']['completions'][0].update(intent_sequence=True),'integer'),
    'renamed_logical_completion':(lambda r:r['native_receipt']['completions'][0].update(logical='aes'),'legacy_native'),
    'changed_vector_result':(lambda r:r['cases'][0].update(decrypt=False),'legacy_vectors'),
    'boolean_checks':(lambda r:r.update(checks=True),'integer'),
    'startup_boolean_flag':(lambda r:r['events'][0]['data']['startup'].update(isolated=True),'legacy_startup'),
    'startup_preloaded_alias':(lambda r:r['events'][0]['data']['startup']['pre_guard_modules'].append('Cryptodome'),'legacy_startup'),
    'unknown_event':(lambda r:r['events'][4].update(event='raw_fsynced'),'legacy_events'),
    'boolean_event_sequence':(lambda r:r['events'][0].update(sequence=True),'integer'),
}
for name,(mutator,code) in RAW_MUTATIONS.items():setattr(LegacyAdapterTests,'test_refuses_'+name,raw_test(mutator,code))


def input_test(mutator,code=None):
    def run(self):mutator(self.data);self.refused(code)
    return run


INPUT_MUTATIONS={
    'wrong_expected_native_set':(lambda d:d['expectation']['native_libraries'].pop('aesni'),'shape'),
    'extra_config_field':(lambda d:d['config'].update(unknown='preserve or refuse'),'shape'),
    'config_alias_substitution':(lambda d:d['config']['source_rows']['Cryptodome'].update(sha256='0'*64),'legacy_origin'),
    'wrong_source_authority_hash':(lambda d:d['completion'].update(runtime_source_sha256='0'*64),'legacy_source'),
    'wrong_completion_shape':(lambda d:d['completion'].update(extra='unknown'),'shape'),
    'wrong_callback':(lambda d:d['completion']['callback_result'].update(checks=23),'legacy_callback'),
    'wrong_cleanup':(lambda d:d['completion'].update(source_finder_and_alias_cleanup_verified=False),'legacy_completion'),
    'changed_fresh_identity':(lambda d:d['completion']['fresh_source_receipts']['Cryptodome']['fstat_before'].update(inode=55),'legacy_read'),
    'wrong_anchor_hash':(lambda d:d['completion']['provenance'].update(sha256='0'*64),'legacy_raw_hash'),
    'oversized_transcript':(lambda d:d.update(raw_receipt_json='x'*(4*1024**2+1)),'transcript_bound'),
}
for name,(mutator,code) in INPUT_MUTATIONS.items():setattr(LegacyAdapterTests,'test_refuses_'+name,input_test(mutator,code))


if __name__=='__main__':unittest.main(verbosity=2)
