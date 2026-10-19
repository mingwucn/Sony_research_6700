"""Migration packets cannot become activation requests or widen the frozen act."""
import copy
import unittest

from tools import dependency_operational_scope as scope


def fixture():
    rows={}
    for index,role in enumerate(sorted(scope.SOURCE_ROLES)):
        rows[role]=dict(path='private/invented/'+str(index)+'.py',bytes=1,sha256='a'*64,
            disposition='requires_successor' if role in scope.REPLACEMENTS else 'retain_contract_rebind_sources')
    legacy={n:'historical_index_only' for n in scope.LEGACY_INPUTS}
    legacy.update(dict.fromkeys(('basis','source_manifest','prerequisites','binding_plan','role_authority','binding_schema'),'fresh_current_metadata'))
    legacy.update(dict.fromkeys(('activity_scope','activity_rights'),'new_activity_specific_record'))
    legacy.update(dict.fromkeys(('dependency_config','source_cache','source_receipts'),'replace_semantics'))
    return dict(schema='source_only_operational_scope_v1',purpose='non_executable_adapter_migration_review',
        source_inventory=rows,host_source=dict(path='private/invented/parent.py',bytes=1,sha256='b'*64,disposition='requires_successor'),
        ordinary_input_roles=sorted(scope.ORDINARY_INPUTS),historical_input_disposition=legacy,
        protected_input_roles=['firmware_package','operational_constants'],metadata_basis_roles=list(scope.BASIS_ROLES),
        scope=dict(scope.SCOPE),owner_facts=dict(scope.OWNER),rights_uncertainties=sorted(scope.RIGHTS),
        historical_blockers=list(scope.HISTORY),historical_evidence_unchanged=True,
        unimplemented_bindings=['new_authority_input_grammar','operational_host_child_source_binding',
            'internal_runtime_observer_continuation','saved_runtime_parent_reconciliation',
            'independent_activity_specific_decision_and_external_anchor'],
        camera_commands=[],**dict.fromkeys(scope.FLAGS,False))


class ScopeTests(unittest.TestCase):
    def refuses(self,mutate):
        value=fixture();mutate(value)
        with self.assertRaises(ValueError):scope.validate_review_packet(value)

    def test_packet_is_review_identity_only(self):
        value=fixture();before=copy.deepcopy(value)
        result=scope.validate_review_packet(value)
        self.assertEqual(value,before)
        self.assertEqual(result['status'],'non_executable_review_only')
        self.assertFalse(result['execution_authorized'])
        self.assertEqual(result['child_comparison_sources'],43)
        self.assertEqual(len(scope.HISTORY),17)

    def test_source_identity_changes_review_digest(self):
        first=fixture();second=copy.deepcopy(first)
        second['source_inventory']['outer_gate']['sha256']='c'*64
        self.assertNotEqual(scope.validate_review_packet(first)['sha256'],scope.validate_review_packet(second)['sha256'])

    def test_all_authority_promotions_refuse(self):
        for flag in scope.FLAGS:
            with self.subTest(flag=flag):self.refuses(lambda v:v.update({flag:True}))

    def test_executable_fields_refuse(self):
        for field,value in (('operation_id','1'*32),('session','invented'),('argv',['python']),('seal','a'*64),('input_paths',{})):
            with self.subTest(field=field):self.refuses(lambda v:v.update({field:value}))

    def test_invented_helper_cannot_enter_source_roster(self):
        self.refuses(lambda v:v['source_inventory'].update(invented_fixture=v['host_source']))

    def test_source_omission_and_duplicate_paths_refuse(self):
        self.refuses(lambda v:v['source_inventory'].pop('namespace'))
        self.refuses(lambda v:v['host_source'].update(path=v['source_inventory']['namespace']['path']))

    def test_source_disposition_cannot_be_marked_ready(self):
        self.refuses(lambda v:v['source_inventory']['outer_gate'].update(disposition='retain_contract_rebind_sources'))
        self.refuses(lambda v:v['host_source'].update(disposition='retain_contract_rebind_sources'))

    def test_paths_cannot_point_to_payloads_or_escape(self):
        for path in ('private/body.dat','private/../outside.py','D:/private/constants.py','/private/constants.py','private\\constants.py'):
            with self.subTest(path=path):self.refuses(lambda v:v['host_source'].update(path=path))

    def test_protected_data_cannot_become_ordinary_input(self):
        for name in ('firmware_package','operational_constants'):
            with self.subTest(name=name):self.refuses(lambda v:v['ordinary_input_roles'].append(name))

    def test_scope_cannot_expand_reads_or_retention(self):
        for field in ('source_opens','full_source_passes','descriptor_bytes_total','content_reads','network_operations','camera_operations'):
            with self.subTest(field=field):self.refuses(lambda v:v['scope'].update({field:v['scope'][field]+1}))

    def test_scope_bool_does_not_equal_numeric_value(self):
        self.refuses(lambda v:v['scope'].update(preparation_attempts=True))

    def test_old_cache_cannot_be_declared_fresh_proof(self):
        for name in ('source_cache','source_receipts','dependency_config','q_old_seal'):
            with self.subTest(name=name):self.refuses(lambda v:v['historical_input_disposition'].update({name:'fresh_current_metadata'}))

    def test_historical_blockers_and_rights_cannot_disappear(self):
        self.refuses(lambda v:v['historical_blockers'].pop())
        self.refuses(lambda v:v['rights_uncertainties'].pop())
        self.refuses(lambda v:v['owner_facts'].update(existing_inspection_rights='approved'))
        self.refuses(lambda v:v.update(historical_evidence_unchanged=False))

    def test_runtime_and_cli_remain_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):scope.run_runtime()
        self.assertEqual(scope.main(),2)


if __name__=='__main__':unittest.main()
