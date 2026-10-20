"""Entirely invented documents/source rows; no saved/private artifact reads."""
import base64
import copy
import hashlib
import json
from pathlib import Path
import stat

INPUTS = ('basis','source_manifest','prerequisites','binding_plan','dependency_config',
          'source_cache','source_receipts','role_authority','binding_schema','historical_scope',
          'historical_rights','activity_scope','activity_rights','q_old_result','q_old_seal',
          'q_old_review','q_integration_result','q_integration_review','q_snapshot_result',
          'q_snapshot_log','q_outer_result','q_outer_review','repair_overlay','q_repair_result','q_repair_review','factory_evidence','parent_evidence')
PURPOSE='one_private_two_phase_primary_gdt_metadata_observation'
UNCERTAINTIES=sorted(('accepted_contract_interaction','accompanying_component_terms',
    'constants_provenance','narrow_research_hypothesis_scope','distinct_operational_act_decision'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
enc=lambda value:json.dumps(value,sort_keys=True,separators=(',',':')).encode('utf-8')


class Fixture:
    def __init__(self, root, role_names=None):
        root=Path(root);self.root=root;legacy='private/sessions/invented-legacy';session='private/sessions/invented-new'
        op='1'*32;self.p={k:{} for k in INPUTS};p=self.p
        p['parent_evidence']=copy.deepcopy(PARENT_EVIDENCE_POLICY)
        source={};receipts={};old_sources={};roles={};integration={}
        def add(key,path):
            raw=('raise AssertionError("never execute invented source") # '+key+'\n').encode()
            row={'path':str(path),'bytes':len(raw),'sha256':sha(raw),'base64':base64.b64encode(raw).decode()}
            source[key]=row
            stamp={'st_dev':1,'st_ino':len(source),'st_mode':stat.S_IFREG|0o666,'st_nlink':1,
                   'st_size':len(raw),'st_mtime_ns':1,'st_ctime_ns':1,'st_file_attributes':0}
            receipts[key]={**{k:row[k] for k in ('path','bytes','sha256')},'close_attempts':1,
                           'eof_probes':1,'closed':True,**{k:copy.deepcopy(stamp) for k in ('lstat_before','lstat_after','fstat_before','fstat_after')}}
            return row
        for n in range(26):
            name=(role_names[n] if role_names is not None else 'gdt_gate' if n==0 else 'ext_read_planner' if n==1 else 'role'+str(n));path=legacy+'/'+name+'.py';row=add('role:'+name,root/path)
            roles[name]={'path':path,'sha256':row['sha256']};old_sources[name+'.py']=row['sha256']
        for name in ('activation_gate','activation_binding','io_entry'):
            row=add('bootstrap:'+name,root/legacy/(name+'.py'));old_sources[name+'.py']=row['sha256']
        for name in ('runtime_entry','gdt_wiring','prospective_child'):
            row=add('integration:'+name,root/'private/sessions/invented-integration'/(name+'.py'))
            integration[name+'.py']=row['sha256']
        venv=root/'private/invented-venv';base=root/'invented-base';package=venv/'Lib/site-packages/Cryptodome'
        p['dependency_config']={'schema':'dependency_probe_config_v1','operation_id':op,'package_root':str(package),
                                'source_rows':{},'native_rows':{},'trusted_origins':{},'vectors':[]}
        for n in range(11):
            alias='invented'+str(n);row=add('dependency:'+alias,package/(alias+'.py'))
            p['dependency_config']['source_rows'][alias]={k:row[k] for k in ('path','bytes','sha256')}
        for alias,path in [('ctypes',base/'Lib/ctypes/__init__.py'),('ctypes.util',base/'Lib/ctypes/util.py'),
                           ('ctypes._endian',base/'Lib/ctypes/_endian.py'),('platform',base/'Lib/platform.py')]:
            row=add('trusted:'+alias,path)
            p['dependency_config']['trusted_origins'][alias]={k:row[k] for k in ('path','bytes','sha256')}
        for name in ('cpuid','aes','aesni','ecb','cbc'):
            p['dependency_config']['native_rows'][name]={'path':str(package/(name+'.pyd')),'bytes':8,'sha256':'b'*64}
        p['dependency_config']['trusted_origins']['_ctypes']={'path':str(base/'DLLs/_ctypes.pyd'),'bytes':8,'sha256':'c'*64}
        p['repair_overlay']={'schema':'gdt_source_repair_overlay_v1','repairs':{},'execution_authorized':False,'camera_commands':[]}
        for key in ('role:gdt_gate','role:ext_read_planner','bootstrap:io_entry'):
            row=source[key];name=Path(row['path']).name;prior='9'*64
            old_sources[name]=prior
            p['repair_overlay']['repairs'][key]={'path':legacy+'/'+name,'old_sha256':prior,'new_sha256':row['sha256']}
        p['q_repair_result']={'status':'qualified_invented_outer_gate_v2','tests_run':162,'passed':162,
            'child_exit_code':0,'skipped':0,'sources_stable':True,'timed_out':False,'execution_authorized':False,
            'actual_entry_ready':False,'test_ids':list(REQUIRED_REPAIR_TEST_IDS),'source_sha256':dict(REQUIRED_REPAIR_SOURCE_PINS)}
        p['q_repair_review']={'schema':'gdt_scoped_repair_review_v1','status':'three_source_reviews_accept_scoped_repairs',
            'result_sha256':'0'*64,'source_sha256':dict(REQUIRED_REPAIR_SOURCE_PINS),
            'review_artifact_sha256':{'gate':'1'*64,'runtime':'2'*64,'io':'3'*64},
            'operational_acceptance':False,'execution_authorized':False,'camera_commands':[]}
        p['source_cache']={'schema':'ordinary_python_source_cache_v1','sources':source}
        p['source_receipts']={'schema':'ordinary_python_source_receipts_v1','receipts':receipts,'metadata_reads':{}}
        p['role_authority']={'roles':roles}
        p['binding_schema']={'aliases':{key:key for key in roles},'load_order':list(roles)[:23],'protected_order':list(roles)[23:]}
        p['source_manifest']={'schema':'gdt_io_source_manifest_v1','relative_path':'private/invented-source.dat',
                              'bytes':100,'sha256':'d'*64,'readonly_required':True,'existing_private_acquisition':True,
                              'no_acquisition_or_download':True,'camera_commands':[]}
        p['basis']={name:{} for name in ('prior_stream','prior_prefix','prior_directory','prior_member_identification',
            'prior_selection','prior_measured','prior_accepted_inventory','lead_plan','prior_ext_superblock_observation')}
        p['basis']['prior_stream']={'input_package_bytes':100,'input_package_sha256':'d'*64}
        p['prerequisites']={'qualified_roles':roles,'binding_input':{'roles':roles,'dependency':{}},
            'constants_relative_path':'private/invented-constants.py','constants_sha256':'e'*64,
            'constants_assignment_count':15,'selected_literal_lengths':{'common':16,'candidate':32},
            'crypto_python_relative_path':(venv/'Scripts/python.exe').relative_to(root).as_posix()}
        old_sources.update({f'invented_extra_{n}.py':'f'*64 for n in range(66)})
        old_ids=[f'old.case{n}' for n in range(811)]
        p['q_old_result']={'status':'qualified_invented_activation_preparation_only','passed':811,'tests_run':811,
            'child_exit_code':0,'skipped':0,'sources_stable':True,'timed_out':False,'sources_sha256':old_sources,
            'summary':{'test_ids':old_ids,'was_successful':True,'failures':0,'errors':0,'skipped':0,'expected_failures':0,'unexpected_successes':0}}
        p['q_old_seal']={'test_ids':old_ids,'sources_sha256':old_sources}
        p['q_old_review']={'status':'passed','sources_sha256':old_sources}
        integration.update({f'invented_integration_extra_{n}.py':'a'*64 for n in range(9)})
        ids=[f'integration.case{n}' for n in range(51)]
        p['q_integration_result']={'passed':51,'tests_run':51,'skipped':0,'child_exit_code':0,
            'sources_and_predecessors_stable':True,'timed_out':False,'test_ids':ids,
            'observed_pass_ids':ids,'source_sha256':integration}
        p['q_integration_review']={'status':'accepted_preparation_only_invented_core_composition_and_source_reviewed_factory',
                                  'qualified_source_sha256':integration}
        p['q_snapshot_log']=('\n'.join(f'test_{n:02} (__main__.Invented.test_{n:02}) ... ok' for n in range(20))
                             +'\n\nRan 20 tests in 0.001s\n\nOK\n').encode()
        p['q_snapshot_result']={'exit_code':0,'source_stable':True,'timed_out':False}
        bootstrap={name:{'path':session+'/'+name+'.py','bytes':8,'sha256':sha(name.encode())}
                   for name in ('outer_gate','ordinary_io','entry_v2')}
        p['q_outer_result']={'status':'qualified_invented_outer_gate_v5','tests_run':40,'passed':40,
            'child_exit_code':0,'skipped':0,'timed_out':False,'sources_stable':True,'execution_authorized':False,
            'actual_entry_ready':False,'test_ids':[f'outer.case{n}' for n in range(40)],
            'source_sha256':{name+'.py':row['sha256'] for name,row in bootstrap.items()}}
        # Test-only policy receipt model; values are supplied by the test harness.
        p['q_outer_result'].update(tests_run=len(REQUIRED_OUTER_TEST_IDS),passed=len(REQUIRED_OUTER_TEST_IDS),
            test_ids=list(REQUIRED_OUTER_TEST_IDS))
        p['q_outer_result']['source_sha256'].update({name:'b'*64 for name in REQUIRED_OUTER_SOURCE_NAMES
            if name not in p['q_outer_result']['source_sha256']})
        p['q_outer_result']['source_sha256'].update(REQUIRED_OUTER_SOURCE_PINS)
        p['q_outer_review']={'status' :'reviewed_invented_outer_gate_v5','source_sha256':p['q_outer_result']['source_sha256']}
        startup={'implementation':'cpython','version':[3,13,12],'platform':'win32','os_name':'nt','maxsize':2**63-1,
                 'isolated':1,'no_site':1,'dont_write_bytecode':True,'optimize':0,
                 'executable':str(venv/'Scripts/python.exe'),'base_executable':str(base/'python.exe'),
                 'prefix':str(base),'base_prefix':str(base),
                 'path':[str(base/'python313.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)]}
        self.c={'schema':'gdt_outer_candidate_v5','operation_id':op,'repository_root':str(root),'session':session,
                'legacy_session':legacy,'base_commit':'0'*40,'purpose':PURPOSE,'author':'invented-author',
                'child_argv_prefix':[startup['executable'],'-I','-S','-B','-X','utf8',str(root/session/'entry_v2.py')],
                'startup':startup,'bootstrap':bootstrap,'inputs':{},'camera_commands':[]}
        p['activity_scope']={'schema':'gdt_outer_scope_v5','operation_id':op,'purpose':PURPOSE,'risk':'R0','camera_commands':[]}
        p['activity_rights']={'schema':'gdt_outer_rights_v5','owner_facts':{'country':'China','personal':True,'noncommercial':True,
            'existing_inspection_rights':'No / unknown','download_consent_alone_clears_inspection':False},
            'preserved_uncertainties':UNCERTAINTIES,'camera_commands':[]}
        self.d={'schema':'gdt_outer_decision_v5','operation_id':op,'status':'accepted_one_frozen_host_metadata_act',
                'execution_authorized':True,'assessor':'invented-assessor','preserved_uncertainties':UNCERTAINTIES,'camera_commands':[]}
        self.r={'schema':'gdt_outer_review_v5','operation_id':op,'status':'reviewed_one_frozen_host_metadata_act',
                'reviewer':'invented-reviewer','findings':[],'camera_commands':[]}
        self.s={'schema':'gdt_outer_seal_v5','operation_id':op,'execution_authorized':True,'camera_commands':[]}

        # Distinct invented successor factory, preserving the51-case old source pin.
        row=source['integration:prospective_child'];old_factory=row['sha256']
        raw=base64.b64decode(row['base64'])+b'# invented reviewed repair\n'
        row.update(bytes=len(raw),sha256=sha(raw),base64=base64.b64encode(raw).decode())
        receipt=receipts['integration:prospective_child']
        receipt.update(bytes=len(raw),sha256=row['sha256'])
        for field in ('lstat_before','lstat_after','fstat_before','fstat_after'):receipt[field]['st_size']=len(raw)
        contract={'prospective_child.py':row['sha256'],'gdt_wiring.py':integration['gdt_wiring.py'],
                  'test_factory.py':'a'*64,'qualify.py':'a'*64}
        composition={'roles/'+name+'.py':value['sha256'] for name,value in roles.items()}
        composition.update({name:'a'*64 for name in ('prospective_child.py','gdt_wiring.py','io_entry.py',
            'runtime_entry.py','dependency_fixture.py','test_composition.py','prepare_fixture.py','prepare_fixture_v2.py','qualify.py')})
        composition.update({'prospective_child.py':row['sha256'],'gdt_wiring.py':integration['gdt_wiring.py'],
            'runtime_entry.py':integration['runtime_entry.py'],'io_entry.py':source['bootstrap:io_entry']['sha256']})
        def qualification(ids,pins,reviews):
            return {'test_ids':list(ids),'source_sha256':pins,'result_sha256':'1'*64,'stderr_sha256':'2'*64,
                    'review_artifact_sha256':{name:'3'*64 for name in reviews},'child_exit_code':0,
                    'skipped':0,'sources_stable':True,'operational_acceptance':False}
        p['factory_evidence']={'schema':'gdt_reviewed_factory_migration_v1','old_factory_sha256':old_factory,
            'new_factory_sha256':row['sha256'],'contract':qualification(REQUIRED_FACTORY_TEST_IDS,contract,
                ('runtime-rereview-29.json','io-rereview-29.json')),
            'composition':qualification(REQUIRED_CHILD_TEST_IDS,composition,('runtime-rereview-8.json','io-review-8.json')),
            'execution_authorized':False,'operational_acceptance':False,'camera_commands':[]}

    def pack(self):
        p=self.p;c=self.c
        raw={k:(v if type(v) is bytes else enc(v)) for k,v in p.items()}
        p['q_repair_review']['result_sha256']=sha(raw['q_repair_result'])
        p['q_old_review'].update(tests_result_sha256=sha(raw['q_old_result']),qualification_seal_sha256=sha(raw['q_old_seal']))
        p['q_integration_review']['qualification_result_sha256']=sha(raw['q_integration_result'])
        p['q_snapshot_result']['stderr_sha256']=sha(raw['q_snapshot_log'])
        p['q_outer_review']['result_sha256']=sha(raw['q_outer_result'])
        p['activity_scope'].update(basis_sha256=sha(raw['basis']),source_manifest_sha256=sha(raw['source_manifest']),
                                   historical_scope_sha256=sha(raw['historical_scope']))
        p['activity_rights'].update(activity_scope_sha256=sha(enc(p['activity_scope'])),historical_rights_sha256=sha(raw['historical_rights']))
        raw={k:(v if type(v) is bytes else enc(v)) for k,v in p.items()}
        c['inputs']={k:{'path':c['session']+'/inputs/'+k+('.log' if k=='q_snapshot_log' else '.json'),
                        'bytes':len(v),'sha256':sha(v)} for k,v in raw.items()}
        candidate=enc(c);self.d.update(candidate_sha256=sha(candidate),scope_sha256=sha(raw['activity_scope']),rights_sha256=sha(raw['activity_rights']))
        decision=enc(self.d);self.r.update(candidate_sha256=sha(candidate),decision_sha256=sha(decision))
        review=enc(self.r);self.s.update(candidate_sha256=sha(candidate),decision_sha256=sha(decision),review_sha256=sha(review))
        seal=enc(self.s)
        return {'candidate':candidate,'decision':decision,'review':review,'seal':seal,'inputs':raw},sha(seal)

    def reference_pins(self, documents):
        roles=('historical_scope','historical_rights','role_authority','binding_schema',
            'q_old_result','q_old_seal','q_old_review','q_integration_result','q_integration_review',
            'q_snapshot_result','q_snapshot_log','source_cache','source_receipts','basis','source_manifest',
            'prerequisites','binding_plan','repair_overlay','q_repair_result','q_repair_review','factory_evidence','parent_evidence')
        pins={role:sha(documents['inputs'][role]) for role in roles}
        profile={k:v for k,v in self.p['dependency_config'].items() if k!='operation_id'}
        pins['dependency_profile']=sha(enc(profile))
        return pins
