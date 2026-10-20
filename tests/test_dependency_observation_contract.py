"""Invented source strings and metadata; no installation or protected reads."""
import copy
import json
import unittest
from unittest.mock import patch

from tools import dependency_observation_contract as c
from tools import dependency_operational_child as current_child
from tools import dependency_producer as producer
from test_dependency_producer import fixture as dependency_fixture, refresh as refresh_dependency


def raw(value):
    return c.encoded(value)


def change(a,role,mutate):
    v=json.loads(a['ordinary_buffers'][role]);mutate(v)
    a['ordinary_buffers'][role]=raw(v)


def reseal(a):
    """Rehash edges, preserving semantic mutations. Never supplies authority."""
    ordinary=a['ordinary_buffers']
    request=json.loads(a['request_bytes'])
    request['source_manifest_sha256']=c.sha(ordinary['authored_source_manifest'])
    request['dependency_fixed_sha256']=c.sha(ordinary['dependency_fixed'])
    a['request_bytes']=raw(request)
    change(a,'activity_scope',lambda v:v.update(request_sha256=c.sha(a['request_bytes'])))
    change(a,'activity_rights',lambda v:v.update(scope_sha256=c.sha(ordinary['activity_scope'])))
    change(a,'authored_source_receipts',lambda v:v.update(manifest_sha256=request['source_manifest_sha256']))
    change(a,'qualification_index',lambda v:v.update(
        ordinary={n:c.receipt(b) for n,b in ordinary.items() if n!='qualification_index'},
        source_manifest_sha256=request['source_manifest_sha256']))
    proposal=json.loads(a['proposal_bytes'])
    proposal['request_sha256']=c.sha(a['request_bytes'])
    proposal['ordinary']={n:c.receipt(b) for n,b in ordinary.items()}
    proposal['runtime']['argv'][-1]=c.sha(a['request_bytes'])
    a['proposal_bytes']=raw(proposal)
    a['expected_source_manifest_sha256']=request['source_manifest_sha256']
    return a


def decided(a):
    operation=json.loads(a['request_bytes'])['operation_id']
    def record(schema,**kw):return raw(dict(schema=schema,operation_id=operation,camera_commands=[],**kw))
    review=record('gdt_observation_review_v1',proposal_sha256=c.sha(a['proposal_bytes']),
                  outcome='accepted_scope',evidence=[c.receipt(b'invented source review')])
    decision=record('gdt_observation_decision_v1',proposal_sha256=c.sha(a['proposal_bytes']),
        review_sha256=c.sha(review),activity_rights_sha256=c.sha(a['ordinary_buffers']['activity_rights']),outcome='allow_scope')
    anchor=record('gdt_observation_external_decision_v1',proposal_sha256=c.sha(a['proposal_bytes']),
        request_sha256=c.sha(a['request_bytes']),review_sha256=c.sha(review),decision_sha256=c.sha(decision),
        outcome='allow_scope',evidence=[c.receipt(b'invented external record; no real consent')])
    return dict(a,review_bytes=review,decision_bytes=decision,external_anchor_bytes=anchor,
                expected_external_anchor_sha256=c.sha(anchor))


def fixture():
    operation='1'*32
    data,_=dependency_fixture()
    data['expectation']['operation_id']=operation
    config=json.loads(data['config_json']);config['operation_id']=operation
    data['config_json']=raw(config).decode()
    data['expectation']['config_sha256']=c.sha(data['config_json'].encode())
    refresh_dependency(data)
    sources={n:('# invented '+n+'\n').encode() for n in c.SOURCE_ROLES}
    sources['dependency.dependency_producer']=data['source_buffers']['runtime']
    sources['bound.integration:prospective_child']=data['source_buffers']['continuation']
    paths={n:'private/invented/source_'+str(i)+'.py' for i,n in enumerate(sorted(sources))}
    paths.update(adapter='tools/dependency_adapter_binding.py',adapter_scope='tools/dependency_operational_scope.py',
                 adapter_comparison='tools/dependency_outer_contract.py')
    rows={n:dict(path=paths[n],**c.receipt(b)) for n,b in sources.items()}
    mapping={n:n for n in c.adapter.SOURCE_ROLES}
    mapping.update({n:'adapter' for n in c.adapter.ENTRIES})
    mapping.update({'adapter.scope_policy':'adapter_scope','adapter.comparison_contract':'adapter_comparison'})
    prepared={n:dict(rows[r],entry=c.adapter.ENTRIES.get(n)) for n,r in mapping.items()}
    data['source_buffers']={alias:raw(prepared) if role=='closure_manifest' else sources[mapping[role]]
                            for alias,role in c.DEPENDENCY_SOURCE_ROLES.items()}
    data['expectation']['source_sha256']={n:c.sha(b) for n,b in data['source_buffers'].items()}
    refresh_dependency(data)
    def record(schema,**kw):return raw(dict(schema=schema,operation_id=operation,camera_commands=[],**kw))
    originals={n:raw(dict(schema='invented_original_comparison',role=n)) for n in c.RETAINED}
    ordinary=dict(originals)
    ordinary['authored_source_manifest']=record('gdt_observation_sources_v1',sources=rows,prepared_sources=prepared,
        dependency_source_roles=c.DEPENDENCY_SOURCE_ROLES,
        prior_dependency_review_sha256=data['binding']['review_sha256'])
    ordinary['dependency_packet']=raw(dict(schema='runtime_dependency_packet_v1',inputs={k:v for k,v in data.items() if k!='source_buffers'}))
    ordinary['dependency_fixed']=raw(dict(expectation_sha256=c.sha(raw(data['expectation'])),package_sha256=c.sha(raw(data['package'])),
        root_sha256={k:r['identity_sha256'] for k,r in data['expectation']['roots'].items()}))
    request=raw(dict(schema='gdt_observation_request_core_v1',operation_id=operation,
        source_manifest_sha256=c.sha(ordinary['authored_source_manifest']),dependency_fixed_sha256=c.sha(ordinary['dependency_fixed']),
        scope_policy_sha256=c.sha(raw(dict(limits=c.policy.SCOPE,effects=c.EFFECTS,stop=c.STOP))),result_folder='/invented/operation'))
    ordinary['authored_source_receipts']=record('gdt_observation_source_expectations_v1',
        manifest_sha256=c.sha(ordinary['authored_source_manifest']),receipts={n:c.receipt(b) for n,b in sources.items()},
        stage='review_expectations_only',freshness_verified=False)
    ordinary['activity_scope']=record('gdt_observation_scope_v1',request_sha256=c.sha(request),limits=c.policy.SCOPE,
        effects=c.EFFECTS,stop=c.STOP,historical_blockers=list(c.policy.HISTORY))
    ordinary['activity_rights']=record('gdt_observation_activity_dispositions_v1',scope_sha256=c.sha(ordinary['activity_scope']),
        owner_facts=c.policy.OWNER,decisions={n:dict(disposition='allow_scope',evidence=[c.receipt(('invented '+n).encode())]) for n in c.policy.RIGHTS})
    ordinary['historical_evidence_index']=record('gdt_observation_history_v1',purpose='comparison_only',
        original_comparison={n:c.receipt(b) for n,b in originals.items()},basis_roles=list(c.policy.BASIS_ROLES),historical_blockers=list(c.policy.HISTORY))
    ordinary['qualification_index']=record('gdt_observation_qualification_v1',ordinary={},source_manifest_sha256='0'*64,
        evidence=[c.receipt(b'invented synthetic qualification')],stage='source_and_synthetic_only',freshness_verified=False,actual_runtime_verified=False)
    proposal=record('gdt_observation_proposal_v1',request_sha256=c.sha(request),ordinary={},
        protected_identities=dict(firmware_package=dict(bytes=1024017848,sha256='a'*64),operational_constants=dict(bytes=123,sha256='c'*64)),
        runtime=dict(interpreter='/invented/python',profile_sha256='d'*64,bootstrap='# inert invented bootstrap',
                     argv=['/invented/python','-I','-S','-B','-X','utf8','-c','# inert invented bootstrap','/invented/operation/request.json',c.sha(request)]))
    return reseal(dict(proposal_bytes=proposal,request_bytes=request,ordinary_buffers=ordinary,
        source_buffers=sources,retained_comparison_buffers=originals,expected_source_manifest_sha256='0'*64))


class ObservationContractTests(unittest.TestCase):
    def setUp(self):self.a=fixture()

    def check(self,a=None):return c.validate_decided_scope(**decided(self.a if a is None else a))

    def test_distinct_decided_schema_expresses_allow_without_authorizing(self):
        before=copy.deepcopy(self.a);result=self.check()
        self.assertEqual(self.a,before)
        self.assertEqual(result['status'],'decided_scope_consistency_only')
        for flag in c.FALSE_FLAGS:self.assertIs(result[flag],False)
        self.assertFalse(result['retained_semantics_revalidated'])
        self.assertFalse(result['source_roster_completeness_attested'])
        self.assertEqual(set(c.CHILD_ROLES),set(current_child.ROSTER))
        self.assertEqual(len(c.SOURCE_ROLES),51)

    def test_pending_or_denied_can_be_reviewed_but_not_decided(self):
        for status in ('pending','deny_scope'):
            a=copy.deepcopy(self.a)
            change(a,'activity_rights',lambda v:v['decisions']['constants_provenance'].update(
                disposition=status,evidence=[] if status=='pending' else [c.receipt(b'invented refusal')]))
            reseal(a)
            self.assertFalse(c.validate_proposal(**a)['execution_authorized'])
            with self.assertRaisesRegex(ValueError,'undecided'):self.check(a)

    def test_rehashed_scope_mutations_are_semantic_refusals(self):
        for field,value in (('source_opens',3),('full_source_passes',2),('source_bytes_on_success',65536),
                            ('camera_operations',1),('content_reads',True),('child_deadline_seconds',301)):
            a=copy.deepcopy(self.a);change(a,'activity_scope',lambda v:v['limits'].update({field:value}));reseal(a)
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'observation_scope'):self.check(a)

    def test_effects_stop_and_history_cannot_be_resealed_away(self):
        for role,mutate in (
            ('activity_scope',lambda v:v['effects'].update(root_proposals_suppressed=False)),
            ('activity_scope',lambda v:v['stop'].pop()),
            ('historical_evidence_index',lambda v:v.update(purpose='fresh_observation')),
            ('historical_evidence_index',lambda v:v['basis_roles'].pop())):
            a=copy.deepcopy(self.a);change(a,role,mutate);reseal(a)
            with self.subTest(role=role),self.assertRaises(ValueError):self.check(a)

    def test_original_comparison_bytes_cannot_be_replaced(self):
        self.a['ordinary_buffers']['basis']=b'{"changed":true}';reseal(self.a)
        with self.assertRaisesRegex(ValueError,'retained_original'):self.check()

    def test_missing_extra_and_protected_ordinary_roles_refuse(self):
        for added in ('extra','firmware_package','operational_constants'):
            a=copy.deepcopy(self.a);a['ordinary_buffers'][added]=b'not payload'
            with self.subTest(added=added),self.assertRaisesRegex(ValueError,'buffer_roster'):self.check(a)
        del self.a['ordinary_buffers']['basis']
        with self.assertRaises(ValueError):self.check()

    def test_freshness_and_runtime_promotions_refuse_after_reseal(self):
        for role,field in (('authored_source_receipts','freshness_verified'),('qualification_index','freshness_verified'),
                           ('qualification_index','actual_runtime_verified')):
            a=copy.deepcopy(self.a);change(a,role,lambda v:v.update({field:True}));reseal(a)
            with self.subTest(role=role,field=field),self.assertRaises(ValueError):self.check(a)

    def test_stage_and_owner_facts_cannot_be_silently_promoted(self):
        for role,mutate in (
            ('authored_source_receipts',lambda v:v.update(stage='actual_read')),
            ('qualification_index',lambda v:v.update(stage='actual_runtime')),
            ('activity_rights',lambda v:v['owner_facts'].update(existing_inspection_rights='approved'))):
            a=copy.deepcopy(self.a);change(a,role,mutate);reseal(a)
            with self.subTest(role=role),self.assertRaises(ValueError):self.check(a)

    def test_prior_dependency_review_and_original_text_hash_domains(self):
        for mutate in (
            lambda v:v.update(prior_dependency_review_sha256='e'*64),
            lambda v:v['dependency_source_roles'].update(runtime='bound.role:core')):
            a=copy.deepcopy(self.a);change(a,'authored_source_manifest',mutate);reseal(a)
            with self.assertRaises(ValueError):self.check(a)
        for name in ('config_json','cache_json'):
            a=copy.deepcopy(self.a)
            change(a,'dependency_packet',lambda v:v['inputs'].update({name:json.dumps(json.loads(v['inputs'][name]),indent=2)}))
            reseal(a)
            with self.subTest(name=name),self.assertRaises(ValueError):self.check(a)

    def test_external_anchor_survives_local_resealing(self):
        old=decided(self.a)
        proposal=json.loads(self.a['proposal_bytes']);proposal['runtime']['bootstrap']='# changed inert bootstrap'
        proposal['runtime']['argv'][7]=proposal['runtime']['bootstrap'];self.a['proposal_bytes']=raw(proposal)
        new=decided(self.a)
        new['expected_external_anchor_sha256']=old['expected_external_anchor_sha256']
        with self.assertRaisesRegex(ValueError,'external_anchor'):c.validate_decided_scope(**new)
        new['external_anchor_bytes']=old['external_anchor_bytes']
        with self.assertRaisesRegex(ValueError,'external_binding'):c.validate_decided_scope(**new)

    def test_source_manifest_requires_external_selected_digest(self):
        self.a['expected_source_manifest_sha256']='e'*64
        with self.assertRaisesRegex(ValueError,'source_anchor'):self.check()

    def test_dependency_roster_omission_substitution_and_permutation(self):
        for mutate in (
            lambda v:v['dependency_source_roles'].pop('closure_manifest'),
            lambda v:v['dependency_source_roles'].update(dependency_producer='bound.role:core'),
            lambda v:v['dependency_source_roles'].update(dependency_producer='dependency.dependency_execution',
                                                       dependency_execution='dependency.dependency_producer')):
            a=copy.deepcopy(self.a);change(a,'authored_source_manifest',mutate);reseal(a)
            with self.assertRaisesRegex(ValueError,'dependency_aliases'):self.check(a)

    def test_prepared_projection_requires_exact_process_role(self):
        # Both rows and bytes exist and are well formed. Membership alone must
        # not allow a different inventoried source to implement a prepared role.
        change(self.a,'authored_source_manifest',lambda v:v['prepared_sources'].update(
            **{'bound.role:core':dict(v['sources']['bound.role:capture'],entry=None)}))
        reseal(self.a)
        with self.assertRaisesRegex(ValueError,'prepared_process_role'):self.check()

    def test_external_anchor_buffer_bounds(self):
        for value in (None,bytearray(b'{}'),b' '*(c.MAX_BYTES+1)):
            a=decided(self.a);a['external_anchor_bytes']=value
            with self.assertRaisesRegex(ValueError,'buffer_bound'):c.validate_decided_scope(**a)

    def test_command_profile_request_and_bootstrap_bindings(self):
        for mutate in (
            lambda v:v['runtime']['argv'].__setitem__(1,'-O'),
            lambda v:v['runtime'].update(bootstrap='# different'),
            lambda v:v['runtime']['argv'].__setitem__(8,'/invented/other/request.json'),
            lambda v:v['runtime']['argv'].__setitem__(9,'f'*64),
            lambda v:v['runtime'].update(profile_sha256=True)):
            a=copy.deepcopy(self.a);v=json.loads(a['proposal_bytes']);mutate(v);a['proposal_bytes']=raw(v)
            with self.assertRaises(ValueError):self.check(a)

    def test_request_is_acyclic_closed_core(self):
        for field in ('proposal_sha256','decision_sha256','anchor_sha256','execution_authorized'):
            a=copy.deepcopy(self.a);v=json.loads(a['request_bytes']);v[field]='a'*64;a['request_bytes']=raw(v)
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'request_shape'):self.check(a)

    def test_windows_paths_are_metadata_only(self):
        a=copy.deepcopy(self.a);r=json.loads(a['request_bytes']);r['result_folder']='Z:/invented/operation';a['request_bytes']=raw(r)
        p=json.loads(a['proposal_bytes']);p['runtime']['interpreter']='Z:/invented/python.exe'
        p['runtime']['argv'][0]=p['runtime']['interpreter'];p['runtime']['argv'][8]='Z:/invented/operation/request.json';a['proposal_bytes']=raw(p)
        self.assertFalse(self.check(reseal(a))['execution_authorized'])

    def test_source_alias_escaping_and_extra_role_refuse(self):
        for mutate in (
            lambda v:v['sources']['adapter'].update(path='private/../outside.py'),
            lambda v:v['sources']['adapter'].update(path='tools/constants.dat'),
            lambda v:v['sources']['adapter'].update(bytes=True),
            lambda v:v['sources'].pop('host.launcher'),
            lambda v:v['sources'].update(extra=dict(path='private/e.py',bytes=2,sha256='a'*64))):
            a=copy.deepcopy(self.a);change(a,'authored_source_manifest',mutate);reseal(a)
            with self.assertRaises(ValueError):self.check(a)

    def test_protected_metadata_bounds_and_extra_payload(self):
        for mutate in (
            lambda v:v['protected_identities']['firmware_package'].update(bytes=True),
            lambda v:v['protected_identities']['operational_constants'].update(bytes=65537),
            lambda v:v['protected_identities']['firmware_package'].update(payload='forbidden')):
            a=copy.deepcopy(self.a);p=json.loads(a['proposal_bytes']);mutate(p);a['proposal_bytes']=raw(p)
            with self.assertRaises(ValueError):self.check(a)

    def test_decision_review_and_evidence_edges(self):
        for name,mutate in (
            ('review_bytes',lambda v:v.update(outcome='refused')),
            ('review_bytes',lambda v:v.update(evidence=[])),
            ('decision_bytes',lambda v:v.update(activity_rights_sha256='f'*64)),
            ('decision_bytes',lambda v:v.update(outcome='pending')),
            ('external_anchor_bytes',lambda v:v.update(outcome='deny_scope'))):
            a=decided(self.a);v=json.loads(a[name]);mutate(v);a[name]=raw(v)
            if name=='external_anchor_bytes':a['expected_external_anchor_sha256']=c.sha(a[name])
            with self.subTest(name=name),self.assertRaises(ValueError):c.validate_decided_scope(**a)

    def test_bounds_duplicate_nonfinite_depth_and_wrong_buffer_types(self):
        for b in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1e999}',b'['*40+b'0'+b']'*40,
                  b' '* (c.MAX_BYTES+1),b'\xff','not bytes'):
            with self.subTest(kind=type(b).__name__),self.assertRaises(ValueError):c.decode(b)
        a=copy.deepcopy(self.a);a['source_buffers']['adapter']=bytearray(b'pass')
        with self.assertRaisesRegex(ValueError,'buffer_bound'):self.check(a)

    def test_no_file_process_or_native_observer_access(self):
        with patch('builtins.open',side_effect=AssertionError('file open')), \
             patch('pathlib.Path.open',side_effect=AssertionError('path open')), \
             patch('os.open',side_effect=AssertionError('os open')), \
             patch('subprocess.Popen',side_effect=AssertionError('process')), \
             patch.object(producer,'RuntimeOps',side_effect=AssertionError('runtime')):
            self.assertFalse(self.check()['execution_authorized'])

    def test_public_runtime_stays_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):c.run_runtime()


if __name__=='__main__':unittest.main()
