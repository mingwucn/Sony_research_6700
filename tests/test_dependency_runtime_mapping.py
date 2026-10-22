"""Domain and full-receipt preservation on invented Windows metadata only."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from tools import dependency_legacy_bridge as subject
from tests.test_dependency_evidence import fixture
from tests.test_dependency_legacy_bridge import fixture as bridge_fixture


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',', ':'),
        ensure_ascii=True,allow_nan=False).encode('ascii')).hexdigest()


def mapped_bridge_fixture():
    """Give the older bridge's invented files distinct declared identities.

    Its original producer fixture reused IDs across Python/native/trusted groups.
    This new fixture keeps the stricter mapping predicate and reseals all metadata
    dependent on the invented identities. Existing fixture/source is unchanged.
    """
    args=bridge_fixture();inputs=args['packet']['inputs'];policy=inputs['expectation'];package=inputs['package']
    for index,row in enumerate(package['installed_receipts'].values()):
        for stamp in ('lstat_before','lstat_after','fstat_before','fstat_after'):row[stamp]['inode']=10000+index
    for group in ('python_origins','native_libraries'):
        for row in policy[group].values():
            receipt=package['installed_receipts'][row['relative_path']]
            row['identity']={k:receipt['lstat_before'][k] for k in subject.core.CROSS}
    for index,(alias,row) in enumerate(args['trusted_receipts'].items()):
        for stamp in ('lstat_before','lstat_after','fstat_before','fstat_after'):row[stamp]['inode']=20000+index
        policy['trusted_origins'][alias]['identity']={k:row['lstat_before'][k] for k in subject.core.CROSS}
    package['installed_proof']['files']={p:dict(package['manifest']['files'][p],open_identity_sha256=digest(row))
        for p,row in package['installed_receipts'].items()}
    policy['installed_proof_sha256']=digest(package['installed_proof'])
    inputs['binding'].update(expectation_sha256=digest(policy),package_sha256=digest(package))
    args['fixed'].update(expectation_sha256=digest(policy),package_sha256=digest(package))
    args['dependency_anchor']['fixed_file_sha256']=subject.e.sha(subject.e.policy.encoded(args['fixed']))
    args['successor_context']['installed_proof_sha256']=policy['installed_proof_sha256']
    args['legacy'].update(record_sha256=package['manifest']['record_sha256'],expected_files=package['manifest']['files'],
        native_policy=subject.project_native_policy(policy,package['manifest'],args['trusted_receipts']))
    args['prerequisites_dependency']=copy.deepcopy(args['legacy'])
    return args


class RuntimeMappingTests(unittest.TestCase):
    def setUp(self):
        data=fixture()
        self.policy=data['expectation']; self.package=data['package']
        self.trusted=data['observation']['trusted_origins']

    def prepare(self, **overrides):
        args=dict(expectation=self.policy,package=self.package,trusted_receipts=self.trusted)
        args.update(overrides)
        return subject.prepare_runtime_mapping(**args)

    def validate(self, mapping):
        return subject.validate_runtime_mapping(mapping=mapping,expectation=self.policy,
            package=self.package,trusted_receipts=self.trusted)

    def test_complete_mapping_preserves_roots_origins_and_every_receipt(self):
        mapping=self.prepare()
        self.assertEqual(self.validate(mapping),'consistent_metadata_not_launchable')
        self.assertEqual(mapping['successor_expectation'],self.policy)
        self.assertEqual((len(mapping['package_receipts']),len(mapping['trusted_receipts'])),(351,5))
        for relative,row in self.package['installed_receipts'].items():
            pair=mapping['package_receipts'][relative]
            self.assertEqual(pair['relative_receipt'],row)
            self.assertEqual(pair['absolute_receipt'],dict(row,path=self.policy['roots']['package']['path']+'/'+relative))
            self.assertEqual(dict(pair['absolute_receipt'],path=relative),row)
            self.assertEqual(pair['relative_receipt_sha256'],digest(row))
            self.assertEqual(pair['absolute_receipt_sha256'],digest(pair['absolute_receipt']))
        for alias,row in self.trusted.items():
            pair=mapping['trusted_receipts'][alias]
            relative=self.policy['trusted_origins'][alias]['relative_path']
            self.assertEqual(pair['absolute_receipt'],row)
            self.assertEqual(pair['relative_receipt'],dict(row,path=relative))
            self.assertEqual(dict(pair['relative_receipt'],path=row['path']),row)
        for group,rows in self.policy.items():
            if group not in mapping['origins']:continue
            for alias,row in rows.items():
                bound=mapping['origins'][group][alias]
                self.assertEqual(bound['identity'],row['identity'])
                self.assertEqual(bound['root'],row['root'])
                self.assertEqual(bound['root_identity_sha256'],self.policy['roots'][row['root']]['identity_sha256'])
                self.assertEqual(bound['absolute_path'],self.policy['roots'][row['root']]['path']+'/'+row['relative_path'])

    def test_complete_receipts_reuse_original_projection_helper(self):
        with patch.object(subject,'project_native_policy',wraps=subject.project_native_policy) as original:
            mapping=self.prepare()
        original.assert_called_once()
        self.assertEqual(mapping['relative_native_policy'],
            subject.project_native_policy(self.policy,self.package['manifest'],self.trusted))
        for alias,row in self.trusted.items():
            projected=dict(row,path=self.policy['trusted_origins'][alias]['relative_path'])
            token=mapping['relative_native_policy']['backend_origins'][alias]['open_identity_sha256']
            self.assertEqual(token,digest(projected))
            self.assertNotEqual(token,digest(row))
            self.assertNotEqual(token,digest(self.policy['trusted_origins'][alias]['identity']))

    def test_missing_runtime_receipts_do_not_create_tokens_or_native_policy(self):
        with patch.object(subject,'project_native_policy',side_effect=AssertionError('must not project')):
            mapping=self.prepare(trusted_receipts=None)
        self.assertFalse(mapping['receipt_mapping_complete'])
        self.assertEqual(mapping['missing_full_trusted_receipts'],sorted(self.policy['trusted_origins']))
        self.assertEqual(mapping['trusted_receipts'],{})
        self.assertIsNone(mapping['relative_native_policy'])
        for row in mapping['origins']['trusted_origins'].values():
            self.assertEqual(row['receipt_status'],'missing_full_receipt')
            self.assertIsNone(row['relative_receipt_sha256']); self.assertIsNone(row['absolute_receipt_sha256'])
        self.assertEqual(subject.validate_runtime_mapping(mapping=mapping,expectation=self.policy,
            package=self.package),'consistent_metadata_not_launchable')

    def test_partial_trusted_roster_remains_explicitly_incomplete(self):
        alias=next(iter(self.trusted))
        mapping=self.prepare(trusted_receipts={alias:self.trusted[alias]})
        self.assertEqual(len(mapping['trusted_receipts']),1)
        self.assertEqual(len(mapping['missing_full_trusted_receipts']),4)
        self.assertIsNone(mapping['relative_native_policy'])

    def test_preparation_and_validation_are_detached_from_caller_mutation(self):
        original=copy.deepcopy((self.policy,self.package,self.trusted))
        mapping=self.prepare(); self.validate(mapping)
        self.assertEqual((self.policy,self.package,self.trusted),original)
        saved=copy.deepcopy(mapping)
        self.policy['roots']['runtime']['identity_sha256']='0'*64
        next(iter(self.package['installed_receipts'].values()))['lstat_before']['ctime_ns']+=1
        next(iter(self.trusted.values()))['lstat_before']['ctime_ns']+=1
        self.assertEqual(mapping,saved)

    def test_same_cross_identity_cannot_stand_in_for_complete_receipt_ctime(self):
        first=self.prepare(); alias=next(iter(self.trusted)); identity=copy.deepcopy(self.policy['trusted_origins'][alias]['identity'])
        for key in ('lstat_before','lstat_after','fstat_before','fstat_after'):
            self.trusted[alias][key]['ctime_ns']+=1
        second=self.prepare()
        self.assertEqual(self.policy['trusted_origins'][alias]['identity'],identity)
        self.assertNotEqual(first['trusted_receipts'][alias]['absolute_receipt_sha256'],second['trusted_receipts'][alias]['absolute_receipt_sha256'])
        self.assertNotEqual(first['relative_native_policy'],second['relative_native_policy'])
        with self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):self.validate(first)

    def test_same_cross_identity_with_changed_nonreparse_attributes_changes_token(self):
        first=self.prepare(); alias=next(iter(self.trusted))
        for key in ('lstat_before','lstat_after','fstat_before','fstat_after'):
            self.trusted[alias][key]['file_attributes']=0x20
        second=self.prepare()
        self.assertNotEqual(first['trusted_receipts'][alias]['relative_receipt_sha256'],second['trusted_receipts'][alias]['relative_receipt_sha256'])

    def test_wrong_runtime_receipt_path_is_refused(self):
        next(iter(self.trusted.values()))['path']='Z:/other/runtime.py'
        with self.assertRaises(ValueError):self.prepare()

    def test_incomplete_trusted_receipt_is_refused(self):
        next(iter(self.trusted.values())).pop('fstat_after')
        with self.assertRaises(ValueError):self.prepare()

    def test_unknown_alias_is_not_an_extra_trusted_origin(self):
        self.trusted['extra']=copy.deepcopy(next(iter(self.trusted.values())))
        with self.assertRaisesRegex(ValueError,'mapping_trusted_roster'):self.prepare()

    def test_receipt_identity_summary_is_not_a_complete_receipt(self):
        self.trusted={a:row['identity'] for a,row in self.policy['trusted_origins'].items()}
        with self.assertRaises(ValueError):self.prepare()

    def test_wrong_root_domain_is_refused(self):
        next(iter(self.policy['trusted_origins'].values()))['root']='package'
        with self.assertRaisesRegex(ValueError,'origin_domain'):self.prepare()

    def test_overlapping_roots_are_refused(self):
        self.policy['roots']['runtime']['path']=self.policy['roots']['package']['path']+'/runtime'
        with self.assertRaisesRegex(ValueError,'root_overlap'):self.prepare()

    def test_cross_root_relative_path_collision_is_not_flattened(self):
        alias=next(iter(self.policy['trusted_origins']))
        relative=next(iter(self.policy['python_origins'].values()))['relative_path']
        self.policy['trusted_origins'][alias]['relative_path']=relative
        self.trusted[alias]['path']=self.policy['roots']['runtime']['path']+'/'+relative
        with self.assertRaisesRegex(ValueError,'duplicate_path'):self.prepare()

    def test_casefold_cross_root_path_collision_is_refused(self):
        alias=next(iter(self.policy['trusted_origins']))
        relative=next(iter(self.policy['python_origins'].values()))['relative_path'].upper()
        self.policy['trusted_origins'][alias]['relative_path']=relative
        self.trusted[alias]['path']=self.policy['roots']['runtime']['path']+'/'+relative
        with self.assertRaisesRegex(ValueError,'duplicate_path'):self.prepare()

    def test_declared_physical_identity_alias_across_domains_is_refused(self):
        alias=next(iter(self.trusted)); other=next(iter(self.package['installed_receipts'].values()))['lstat_before']
        for key in ('device','inode'):
            self.policy['trusted_origins'][alias]['identity'][key]=other[key]
            for stamp in ('lstat_before','lstat_after','fstat_before','fstat_after'):self.trusted[alias][stamp][key]=other[key]
        with self.assertRaisesRegex(ValueError,'mapping_identity_alias'):self.prepare()

    def test_wrong_package_proof_cannot_be_repaired_by_mapping(self):
        next(iter(self.package['installed_proof']['files'].values()))['open_identity_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'installed_proof'):self.prepare()

    def test_boolean_stamp_value_is_not_an_integer(self):
        next(iter(self.trusted.values()))['fstat_after']['inode']=True
        with self.assertRaises(ValueError):self.prepare()

    def test_path_traversal_and_drive_relative_roots_are_refused(self):
        for value in ('Y:runtime','Y:/fixtures/../runtime','Y:/fixtures/runtime/'):
            with self.subTest(value=value):
                policy=copy.deepcopy(self.policy);policy['roots']['runtime']['path']=value
                with self.assertRaises(ValueError):self.prepare(expectation=policy)

    def test_reparse_and_multiple_link_receipts_are_refused(self):
        for key,value in (('file_attributes',0x400),('nlink',2)):
            trusted=copy.deepcopy(self.trusted)
            for stamp in ('lstat_before','lstat_after','fstat_before','fstat_after'):
                next(iter(trusted.values()))[stamp][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.prepare(trusted_receipts=trusted)

    def test_output_domain_hash_and_receipt_tampering_is_recomputed(self):
        original=self.prepare()
        for field in ('root','absolute_path','relative_receipt_sha256'):
            mapping=copy.deepcopy(original)
            next(iter(mapping['origins']['trusted_origins'].values()))[field]='wrong'
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):
                self.validate(mapping)

    def test_receipt_pair_cannot_drop_a_stamp_or_relabel_source_domain(self):
        original=self.prepare()
        for partial in (True,False):
            mapping=copy.deepcopy(original);pair=next(iter(mapping['trusted_receipts'].values()))
            if partial:pair['absolute_receipt'].pop('lstat_after')
            else:pair['source_receipt_domain']='package_relative'
            with self.subTest(partial=partial),self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):self.validate(mapping)

    def test_rehashing_saved_mapping_does_not_authenticate_it(self):
        mapping=self.prepare();mapping['package_sha256']='0'*64
        saved=json.loads(json.dumps(mapping));self.assertEqual(len(digest(saved)),64)
        with self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):self.validate(saved)

    def test_false_effects_and_sidecar_requirement_cannot_be_promoted(self):
        original=self.prepare()
        for key,value in (('execution_authorized',True),('actual_runtime_verified',True),
            ('current_filesystem_observed',True),('feature_supported',True),('recovery_proven',True),
            ('device_write_gate_passed',True),('legacy_projection_requires_domain_sidecar',False),('camera_commands',['invented'])):
            mapping=copy.deepcopy(original);mapping[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):self.validate(mapping)

    def test_bound_and_nonrecord_inputs_are_refused(self):
        with self.assertRaises(ValueError):self.prepare(trusted_receipts=[])
        with self.assertRaises(ValueError):self.prepare(expectation={'huge':'x'*(2049)})
        mapping=self.prepare();mapping['extra']={'huge':'x'*(2049)}
        with self.assertRaises(ValueError):self.validate(mapping)

    def test_preparation_does_not_dispatch_projection_or_activation_api(self):
        with (patch.object(subject,'run_runtime',side_effect=AssertionError('activation')),
              patch.object(subject.activity.composed.dependency.execution,'bind_runtime_packet',side_effect=AssertionError('packet'))):
            mapping=self.prepare();self.validate(mapping)
        for key in ('execution_authorized','current_filesystem_observed','actual_runtime_verified',
            'feature_supported','recovery_proven','device_write_gate_passed','original_legacy_token_provenance_verified'):
            self.assertIs(mapping[key],False)
        self.assertTrue(mapping['root_identities_are_caller_declarations'])
        self.assertTrue(mapping['legacy_projection_requires_domain_sidecar'])
        self.assertEqual(mapping['camera_commands'],[])

    def test_existing_retained_comparison_consumes_original_input_bound_mapping(self):
        args=mapped_bridge_fixture()
        inputs=args['packet']['inputs']
        mapping=subject.prepare_runtime_mapping(expectation=inputs['expectation'],
            package=inputs['package'],trusted_receipts=args['trusted_receipts'])
        with patch.object(subject,'validate_runtime_mapping',wraps=subject.validate_runtime_mapping) as checked:
            result=subject.compare_invented_metadata(runtime_mapping=mapping,**args)
        checked.assert_called_once()
        self.assertTrue(result['shared_plan_metadata_complete'])
        self.assertFalse(result['dependency_bridge_verified'])
        self.assertFalse(result['actual_startup_verified'])
        self.assertFalse(result['execution_authorized'])

    def test_existing_comparison_refuses_missing_or_tampered_mapping_receipts(self):
        args=mapped_bridge_fixture();inputs=args['packet']['inputs']
        mapping=subject.prepare_runtime_mapping(expectation=inputs['expectation'],package=inputs['package'])
        with self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):
            subject.compare_invented_metadata(runtime_mapping=mapping,**args)
        mapping=subject.prepare_runtime_mapping(expectation=inputs['expectation'],package=inputs['package'],
            trusted_receipts=args['trusted_receipts'])
        next(iter(mapping['trusted_receipts'].values()))['absolute_receipt']['fstat_after']['ctime_ns']+=1
        with self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):
            subject.compare_invented_metadata(runtime_mapping=mapping,**args)

    def test_valid_mapping_for_another_operation_cannot_replace_retained_inputs(self):
        args=mapped_bridge_fixture();inputs=args['packet']['inputs']
        other=copy.deepcopy(inputs['expectation']);other['operation_id']='another-invented-operation'
        mapping=subject.prepare_runtime_mapping(expectation=other,package=inputs['package'],
            trusted_receipts=args['trusted_receipts'])
        with self.assertRaisesRegex(ValueError,'runtime_mapping_changed'):
            subject.compare_invented_metadata(runtime_mapping=mapping,**args)


if __name__=='__main__':unittest.main()
