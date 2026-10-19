"""Invented metadata only; the linkage API does not execute supplied sources."""
import copy
import unittest

from tools import dependency_basis_links as links
from tests.test_dependency_authority_grammar import fixture as envelope_fixture, raw


def fixture():
    candidate, args = envelope_fixture()
    roles = {n:dict(path='private/invented-roles/'+n+'.py',
        sha256=links.contract.sha(args['source_buffers']['bound.role:'+n])) for n in links.ROLES}
    schema = dict(aliases={n:n for n in roles}, load_order=list(links.outer.ROLES[:-3]),
        protected_order=list(links.outer.ROLES[-3:]))
    plan = dict(roles=roles, load_order=schema['load_order'], protected_order=schema['protected_order'],
        blockers=['invented_blocker'], execution_authorized=False, actual_runtime_verified=False,
        actual_binding_ready=False, camera_commands=[])
    basis = {n:{} for n in links.contract.policy.BASIS_ROLES}
    basis['prior_stream'] = dict(input_package_bytes=100, input_package_sha256='d'*64)
    metadata = dict(basis=basis, source_manifest=dict(schema='gdt_io_source_manifest_v1',
        relative_path='private/invented-source.dat', bytes=100, sha256='d'*64,
        readonly_required=True, existing_private_acquisition=True, no_acquisition_or_download=True,
        camera_commands=[]), prerequisites=dict(qualified_roles=roles,
        binding_input=dict(schema='activation_binding_input_v1', roles=roles, dependency={}),
        constants_relative_path='private/invented-constants.py', constants_sha256='e'*64,
        constants_assignment_count=15, selected_literal_lengths=dict(common=16,candidate=32),
        crypto_python_relative_path='private/invented-venv/python.exe'),
        role_authority=dict(roles=roles), binding_schema=schema, binding_plan=plan)
    args['ordinary_buffers'].update({n:raw(v) for n,v in metadata.items()})
    candidate['protected']['firmware_package'].update(bytes=100,sha256='d'*64)
    candidate['protected']['operational_constants'].update(sha256='e'*64)
    return dict(candidate=candidate, ordinary_buffers=args['ordinary_buffers'],
        source_buffers=args['source_buffers'], recomputed_plan=copy.deepcopy(plan),
        frozen_basis=copy.deepcopy(basis), retained_schema=copy.deepcopy(schema))


def change(args, role, mutate):
    value=links.contract.decode(args['ordinary_buffers'][role]); mutate(value)
    args['ordinary_buffers'][role]=raw(value)


class BasisLinkTests(unittest.TestCase):
    def test_linkage_does_not_authenticate_fabricated_recomputations(self):
        args=fixture(); before=copy.deepcopy(args)
        result=links.validate_invented_basis_links(**args)
        self.assertEqual(args,before)
        self.assertEqual(result['checked_link_roles'],sorted(links.INPUTS))
        self.assertIs(result['recomputation_authenticated'],False)
        self.assertIs(result['execution_authorized'],False)

    def test_runtime_always_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'): links.run_runtime()

    def test_six_records_require_exact_shapes(self):
        for role in links.INPUTS:
            with self.subTest(role=role):
                args=fixture(); change(args,role,lambda value:value.update(extra=True))
                with self.assertRaises(ValueError): links.validate_invented_basis_links(**args)

    def test_changed_basis_and_source_identity(self):
        for mutate in (lambda a:a['frozen_basis']['prior_prefix'].update(changed=1),
            lambda a:change(a,'source_manifest',lambda v:v.update(bytes=101)),
            lambda a:a['candidate']['protected']['firmware_package'].update(sha256='b'*64),
            lambda a:a['candidate']['protected']['operational_constants'].update(sha256='b'*64)):
            args=fixture(); mutate(args)
            with self.assertRaises(ValueError): links.validate_invented_basis_links(**args)

    def test_full_plan_comparison_includes_hidden_fields(self):
        for mutate in (lambda v:v.update(blockers=[]),lambda v:v.update(hidden=True),
            lambda v:v.update(actual_binding_ready=True)):
            args=fixture(); change(args,'binding_plan',mutate)
            with self.assertRaisesRegex(ValueError,'retained_plan_difference'):
                links.validate_invented_basis_links(**args)

    def test_rebound_plan_cannot_authorize(self):
        args=fixture(); args['recomputed_plan']['execution_authorized']=True
        args['ordinary_buffers']['binding_plan']=raw(args['recomputed_plan'])
        with self.assertRaisesRegex(ValueError,'plan_authority'): links.validate_invented_basis_links(**args)

    def test_cross_role_source_mismatch(self):
        args=fixture(); args['source_buffers']['bound.role:acceptance']=b'changed'
        with self.assertRaisesRegex(ValueError,'role_source_bytes'): links.validate_invented_basis_links(**args)

    def test_qualified_and_binding_roles_must_agree(self):
        for name in ('qualified_roles','binding_input'):
            args=fixture()
            def mutate(v):
                target=v[name] if name=='qualified_roles' else v[name]['roles']
                target['acceptance']['sha256']='b'*64
            change(args,'prerequisites',mutate)
            with self.assertRaisesRegex(ValueError,'role_cross_binding'): links.validate_invented_basis_links(**args)

    def test_windows_alias_and_unsafe_paths(self):
        for path in ('private/../x','private/NUL.py','private/COM¹/x','private/x.','private/x ',
            'private/x:y','private//x','private/./x','private/\\x','private/x\x00'):
            with self.subTest(path=path),self.assertRaises(ValueError): links.private_path(path)

    def test_constants_and_interpreter_aliases(self):
        for field in ('constants_relative_path','crypto_python_relative_path'):
            args=fixture(); change(args,'prerequisites',lambda v:v.update({field:'private/invented-source.dat'}))
            with self.assertRaisesRegex(ValueError,'protected_path_alias'): links.validate_invented_basis_links(**args)

    def test_bool_cannot_replace_counts(self):
        args=fixture(); change(args,'source_manifest',lambda v:v.update(bytes=True))
        with self.assertRaises(ValueError): links.validate_invented_basis_links(**args)

    def test_hash_valid_different_basis_source_still_refuses(self):
        args=fixture(); args['frozen_basis']['prior_stream']['input_package_sha256']='a'*64
        args['ordinary_buffers']['basis']=raw(args['frozen_basis'])
        with self.assertRaisesRegex(ValueError,'basis_source_identity'): links.validate_invented_basis_links(**args)
