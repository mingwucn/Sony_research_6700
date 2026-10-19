"""Invented dependency metadata only; no installed package or native execution."""
import copy
import unittest

from tools import dependency_legacy_bridge as subject
from tests.test_dependency_source_receipts import fixture as source_fixture

e=subject.e


def context(policy,fixed,dep):
    return dict(operation_id=policy['operation_id'],source_roles=dep['source_roles'],
        source_sha256=policy['source_sha256'],config_text_sha256=policy['config_sha256'],
        cache_text_sha256=policy['cache_sha256'],root_sha256=fixed['root_sha256'],
        loader_kwargs=policy['loader_kwargs'],bootstrap_boundary=policy['bootstrap_boundary'],
        manifest_sha256=policy['manifest_sha256'],installed_proof_sha256=policy['installed_proof_sha256'])


def trusted(policy):
    result={}
    for alias,row in policy['trusted_origins'].items():
        stamp=dict(row['identity'],nlink=1,ctime_ns=5678,file_attributes=0)
        result[alias]=dict(path=policy['roots']['runtime']['path']+'/'+row['relative_path'],
            size=row['size'],sha256=row['sha256'],opened_read_only=True,
            **{k:dict(stamp) for k in ('lstat_before','fstat_before','fstat_after','lstat_after')})
    return result


def fixture(complete=False,original_wheel=False):
    c,args,dep,source=source_fixture();o=args['ordinary_buffers']
    packet=e.decode(o['dependency_packet']);fixed=e.decode(o['dependency_fixed'])
    # Public basis-link fixture intentionally has only a skeletal plan. Build
    # an explicit invented legacy plan here; the private integration fixture
    # separately exercises the retained full binding-plan result.
    legacy=dict(schema='activation_dependency_plan_v1',version='3.24.1',wheel_sha256='a'*64,
        record_sha256=None,expected_files=None,native_policy=None)
    manifest=packet['inputs']['package']['manifest']
    if not original_wheel:legacy['wheel_sha256']=manifest['wheel_sha256']
    receipts=trusted(packet['inputs']['expectation'])
    if complete:
        legacy.update(record_sha256=manifest['record_sha256'],expected_files=manifest['files'],
            native_policy=subject.project_native_policy(packet['inputs']['expectation'],manifest,receipts))
    return dict(legacy=legacy,prerequisites_dependency=copy.deepcopy(legacy),packet=packet,fixed=fixed,
        source_buffers=args['source_buffers'],dependency_anchor=dep,trusted_receipts=receipts,
        successor_context=context(packet['inputs']['expectation'],fixed,dep))


class LegacyBridgeTests(unittest.TestCase):
    def test_original_fourteen_role_fixture_wheel_is_inconsistent(self):
        with self.assertRaisesRegex(ValueError,'bridge_wheel'):subject.compare_invented_metadata(**fixture(original_wheel=True))

    def test_missing_fields_reported_without_inference_or_authority(self):
        f=fixture();before=copy.deepcopy(f);r=subject.compare_invented_metadata(**f)
        self.assertEqual(f,before)
        self.assertEqual(r['missing_legacy_fields'],['record_sha256','expected_files','native_policy'])
        self.assertFalse(r['shared_plan_metadata_complete'])
        self.assertEqual(r['legacy_absent_context'],list(subject.ABSENT_CONTEXT))

    def test_complete_shared_fields_do_not_create_missing_legacy_context(self):
        r=subject.compare_invented_metadata(**fixture(complete=True))
        self.assertEqual(r['missing_legacy_fields'],[]);self.assertTrue(r['shared_plan_metadata_complete'])
        for key in ('legacy_context_binding_present','original_legacy_token_provenance_verified',
            'source_mapping_observed','cache_freshness_verified','dependency_bridge_verified','actual_startup_verified',
            'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(r[key],False)

    def test_version_wheel_record_and_files_are_exact(self):
        for key,value in (('version','3.24.2'),('wheel_sha256','0'*64),('record_sha256','0'*64),('expected_files',{})):
            f=fixture(complete=True);f['legacy'][key]=value;f['prerequisites_dependency']=copy.deepcopy(f['legacy'])
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'bridge_'+key.split('_sha256')[0]):
                subject.compare_invented_metadata(**f)

    def test_plan_and_prerequisite_cannot_diverge(self):
        f=fixture();f['prerequisites_dependency']['wheel_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'bridge_legacy_prerequisites'):subject.compare_invented_metadata(**f)

    def test_native_backend_suffix_no_fallback_and_rosters_must_match(self):
        for key,value in (('backend','cffi'),('extension_suffix','.dll'),('no_fallback',False),
            ('python_origins',{}),('backend_origins',{}),('native_libraries',{})):
            f=fixture(complete=True);f['legacy']['native_policy'][key]=value
            f['prerequisites_dependency']=copy.deepcopy(f['legacy'])
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'bridge_native_policy'):
                subject.compare_invented_metadata(**f)

    def test_projection_changes_only_receipt_path_and_preserves_absolute_input(self):
        f=fixture();before=copy.deepcopy(f['trusted_receipts']);p=f['packet']['inputs']['expectation']
        native=subject.project_native_policy(p,f['packet']['inputs']['package']['manifest'],f['trusted_receipts'])
        self.assertEqual(before,f['trusted_receipts'])
        for alias,row in before.items():
            projected=copy.deepcopy(row);projected['path']=p['trusted_origins'][alias]['relative_path']
            expected=e.sha(e.policy.encoded(projected))
            self.assertEqual(native['backend_origins'][alias]['open_identity_sha256'],expected)
            self.assertNotEqual(expected,e.sha(e.policy.encoded(row)))

    def test_trusted_receipts_validate_path_identity_and_readonly_claims(self):
        for key,value in (('path','Z:/wrong.py'),('opened_read_only',False),('sha256','0'*64)):
            f=fixture();next(iter(f['trusted_receipts'].values()))[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):subject.compare_invented_metadata(**f)

    def test_trusted_roster_cannot_be_partial(self):
        f=fixture();f['trusted_receipts'].pop('ctypes')
        with self.assertRaisesRegex(ValueError,'bridge_trusted_roster'):subject.compare_invented_metadata(**f)

    def test_relative_projection_cannot_alias_distinct_roots(self):
        f=fixture();p=f['packet']['inputs']['expectation'];row=p['trusted_origins']['ctypes']
        row['relative_path']=next(iter(p['python_origins'].values()))['relative_path']
        f['trusted_receipts']=trusted(p)
        with self.assertRaises(ValueError):subject.project_native_policy(p,f['packet']['inputs']['package']['manifest'],f['trusted_receipts'])

    def test_successor_context_rosters_hashes_operations_and_policy_are_exact(self):
        for key,value in (('operation_id','other'),('source_roles',{}),('source_sha256',{}),
            ('cache_text_sha256','0'*64),('config_text_sha256','0'*64),('root_sha256',{}),
            ('loader_kwargs',{'winmode':0}),('bootstrap_boundary',[]),('extra',True)):
            f=fixture();f['successor_context'][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'bridge_successor_context'):
                subject.compare_invented_metadata(**f)

    def test_declared_operation_cannot_override_successor_policy(self):
        f=fixture();f['dependency_anchor']['operation_id']='other'
        with self.assertRaisesRegex(ValueError,'bridge_operation'):subject.compare_invented_metadata(**f)

    def test_source_alias_mapping_is_exact_injective_and_bounded(self):
        for mapping in ({'extra':'host_parent_adapter'},{'runtime':'host_parent_adapter','continuation':[]},
            dict(runtime='host_parent_adapter',continuation='host_parent_adapter')):
            f=fixture();f['dependency_anchor']['source_roles']=mapping
            with self.subTest(mapping=mapping),self.assertRaises(ValueError):subject.compare_invented_metadata(**f)

    def test_legacy_extra_fields_cannot_pretend_to_bind_context(self):
        f=fixture();f['legacy']['operation_id']=f['successor_context']['operation_id']
        with self.assertRaisesRegex(ValueError,'bridge_legacy_shape'):subject.compare_invented_metadata(**f)

    def test_successor_fixed_expectation_and_cache_keep_retained_validation(self):
        f=fixture();f['fixed']['package_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'fixed_expectations'):subject.compare_invented_metadata(**f)
        f=fixture();f['packet']['inputs']['cache_json']+=' '
        with self.assertRaisesRegex(ValueError,'input_hash'):subject.compare_invented_metadata(**f)

    def test_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()

    def test_each_optional_legacy_field_is_missing_not_inferred(self):
        for key in ('record_sha256','expected_files','native_policy'):
            f=fixture(complete=True);f['legacy'][key]=None;f['prerequisites_dependency']=copy.deepcopy(f['legacy'])
            result=subject.compare_invented_metadata(**f)
            self.assertEqual(result['missing_legacy_fields'],[key]);self.assertFalse(result['dependency_bridge_verified'])

    def test_trusted_identity_readonly_and_type_predicates_are_not_weakened(self):
        for stamp,key,value in (('fstat_after','mtime_ns',999),('lstat_before','nlink',2),
            ('fstat_before','file_attributes',0x400),('lstat_after','size',True),('fstat_after','inode',False)):
            f=fixture();next(iter(f['trusted_receipts'].values()))[stamp][key]=value
            with self.subTest(stamp=stamp,key=key),self.assertRaises(ValueError):subject.compare_invented_metadata(**f)

    def test_lower_helper_does_not_authenticate_original_fixed_file_digest(self):
        f=fixture();f['dependency_anchor']['fixed_file_sha256']='0'*64
        result=subject.compare_invented_metadata(**f)
        self.assertFalse(result['dependency_bridge_verified'])
