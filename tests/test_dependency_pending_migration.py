"""Pending-only migration qualification with invented records and source data.

Exactly six ordinary public files are read as opaque source bytes. All other
source strings, historical comparisons, dependency records, paths and command
metadata are invented. No captured source buffer is compiled or executed by the
proposal checker. Public pure definitions are imported by the fixture; no saved
private proposal, protected input or installed dependency is read by these tests.
Passing the pure proposal checker does not qualify the selected gate semantics.
"""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import dependency_observation_contract as c
from tools import dependency_producer as producer
from test_dependency_observation_contract import change, decided, fixture, raw, reseal


PUBLIC_SOURCES = {
    'host.launcher': 'tools/dependency_operational_launcher.py',
    'host_entry': 'tools/dependency_host_entry.py',
    'operational_metadata': 'tools/dependency_operational_metadata.py',
    'operational_preparation': 'tools/dependency_operational_preparation.py',
    'process_child': 'tools/dependency_operational_child.py',
    'retained_gate': 'tools/dependency_historical_gate.py',
}
DEPENDENCY_NULLS = ('expected_files', 'native_policy', 'record_sha256')


def pending_fixture():
    """Invent pending comparison state before taking the migration baseline."""
    args = fixture()
    change(args, 'activity_rights', lambda value: value.update(decisions={
        name: dict(disposition='pending', evidence=[]) for name in c.policy.RIGHTS}))
    original = raw(dict(schema='invented_original_comparison', role='binding_plan',
                        dependency=dict.fromkeys(DEPENDENCY_NULLS)))
    args['ordinary_buffers']['binding_plan'] = original
    args['retained_comparison_buffers']['binding_plan'] = original
    change(args, 'historical_evidence_index', lambda value: value.update(
        original_comparison={name: c.receipt(data)
                            for name, data in args['retained_comparison_buffers'].items()}))
    return reseal(args)


def replace_sources(args, replacements):
    """Rebind source expectations and existing acyclic edges, never authority."""
    args['source_buffers'].update(replacements)
    change(args, 'authored_source_manifest', lambda value: value['sources'].update({
        name: dict(path=PUBLIC_SOURCES[name], **c.receipt(data))
        for name, data in replacements.items()}))
    change(args, 'authored_source_receipts', lambda value: value.update(receipts={
        name: c.receipt(data) for name, data in args['source_buffers'].items()}))
    return reseal(args)


class PendingMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository = Path(__file__).resolve().parents[1]
        cls.public_sources = {role: (cls.repository / path).read_bytes()
                              for role, path in PUBLIC_SOURCES.items()}
        cls.before_pins = {role: dict(path=PUBLIC_SOURCES[role], **c.receipt(data))
                           for role, data in cls.public_sources.items()}

    @classmethod
    def tearDownClass(cls):
        cls.after_pins = {role: dict(path=path, **c.receipt((cls.repository / path).read_bytes()))
                          for role, path in PUBLIC_SOURCES.items()}
        if cls.after_pins != cls.before_pins:
            raise AssertionError('selected public source changed during qualification')

    def setUp(self):
        self.before = pending_fixture()
        self.args = replace_sources(copy.deepcopy(self.before), self.public_sources)

    def assert_pending(self, result):
        self.assertEqual(result['pending_decisions'], sorted(c.policy.RIGHTS))
        self.assertEqual(len(result['pending_decisions']), 5)
        self.assertEqual(result['denied_decisions'], [])
        for flag in c.FALSE_FLAGS:
            self.assertIs(result[flag], False, flag)
        self.assertIs(result['retained_semantics_revalidated'], False)
        self.assertIs(result['source_roster_completeness_attested'], False)
        self.assertEqual(result['camera_commands'], [])

    def test_six_current_sources_preserve_projection_dependencies_and_comparisons(self):
        before_call = copy.deepcopy(self.args)
        self.assert_pending(c.validate_proposal(**self.args))
        self.assertEqual(self.args, before_call)
        old = json.loads(self.before['ordinary_buffers']['authored_source_manifest'])
        new = json.loads(self.args['ordinary_buffers']['authored_source_manifest'])
        self.assertEqual(len(new['sources']), 51)
        self.assertEqual(len(new['prepared_sources']), 46)
        self.assertTrue(set(PUBLIC_SOURCES).isdisjoint(c.PREPARED_PROCESS_ROLES.values()))
        changed = {name for name in old['sources'] if old['sources'][name] != new['sources'][name]}
        self.assertEqual(changed, set(PUBLIC_SOURCES))
        self.assertEqual(new['prepared_sources'], old['prepared_sources'])
        self.assertEqual(new['dependency_source_roles'], old['dependency_source_roles'])
        for name in c.RETAINED | {'dependency_packet', 'dependency_fixed'}:
            self.assertEqual(self.args['ordinary_buffers'][name], self.before['ordinary_buffers'][name])
        self.assertEqual(self.args['retained_comparison_buffers'], self.before['retained_comparison_buffers'])
        self.assertEqual(json.loads(self.args['ordinary_buffers']['binding_plan'])['dependency'],
                         dict.fromkeys(DEPENDENCY_NULLS))
        for name in set(c.SOURCE_ROLES) - set(PUBLIC_SOURCES):
            self.assertEqual(self.args['source_buffers'][name], self.before['source_buffers'][name])
        for name in ('request_bytes', 'proposal_bytes', 'expected_source_manifest_sha256'):
            self.assertNotEqual(self.args[name], self.before[name])

    def test_stale_selected_source_hash_refuses(self):
        self.args['source_buffers']['host_entry'] += b'\n# invented drift\n'
        with self.assertRaisesRegex(ValueError, 'observation_original_bytes'):
            c.validate_proposal(**self.args)

    def test_missing_and_extra_source_roles_refuse(self):
        for where in ('buffers', 'manifest'):
            for extra in (False, True):
                args = copy.deepcopy(self.args)
                def mutate(rows):
                    if extra:
                        rows['invented.extra'] = b'# extra\n' if where == 'buffers' else dict(
                            path='tools/invented_extra.py', **c.receipt(b'# extra\n'))
                    else:
                        rows.pop('host.launcher')
                if where == 'buffers':
                    mutate(args['source_buffers'])
                else:
                    change(args, 'authored_source_manifest', lambda value: mutate(value['sources']))
                    reseal(args)
                with self.subTest(where=where, extra=extra), self.assertRaisesRegex(ValueError, 'roster'):
                    c.validate_proposal(**args)

    def test_wrong_prepared_process_projection_refuses(self):
        change(self.args, 'authored_source_manifest', lambda value: value['prepared_sources'].update(
            {'bound.role:core': dict(value['sources']['bound.role:capture'], entry=None)}))
        reseal(self.args)
        with self.assertRaisesRegex(ValueError, 'observation_prepared_process_role'):
            c.validate_proposal(**self.args)

    def test_old_manifest_anchor_refuses_resealed_migration(self):
        self.args['expected_source_manifest_sha256'] = self.before['expected_source_manifest_sha256']
        with self.assertRaisesRegex(ValueError, 'observation_source_anchor'):
            c.validate_proposal(**self.args)

    def test_forged_freshness_or_runtime_claim_refuses(self):
        for role, field in (('authored_source_receipts', 'freshness_verified'),
                            ('qualification_index', 'freshness_verified'),
                            ('qualification_index', 'actual_runtime_verified')):
            args = copy.deepcopy(self.args)
            change(args, role, lambda value: value.update({field: True}))
            reseal(args)
            with self.subTest(role=role, field=field), self.assertRaisesRegex(
                    ValueError, 'observation_source_expectations|observation_qualification_mode'):
                c.validate_proposal(**args)

    def test_command_request_hash_and_path_remain_bound(self):
        for index, value, error in ((9, 'f' * 64, 'observation_argv_binding'),
                                    (8, '/invented/elsewhere/request.json', 'observation_request_path')):
            args = copy.deepcopy(self.args)
            proposal = json.loads(args['proposal_bytes'])
            proposal['runtime']['argv'][index] = value
            args['proposal_bytes'] = raw(proposal)
            with self.subTest(index=index), self.assertRaisesRegex(ValueError, error):
                c.validate_proposal(**args)

    def test_decided_scope_refuses_all_five_pending_even_with_invented_allow_records(self):
        # These fake records are only the existing test helper's negative input.
        # No actual review, decision or external anchor is created or consulted.
        with self.assertRaisesRegex(ValueError, 'observation_undecided'):
            c.validate_decided_scope(**decided(self.args))

    def test_reanchored_nonprepared_gate_replacement_is_not_semantically_qualified(self):
        # Deliberately unacceptable gate code is accepted as consistent bytes.
        # Its body is not executed: this demonstrates the pure checker's limit.
        alternate = b'raise AssertionError("invented gate must never execute")\n'
        original_manifest = self.args['expected_source_manifest_sha256']
        replace_sources(self.args, {'retained_gate': alternate})
        self.assertNotEqual(self.args['expected_source_manifest_sha256'], original_manifest)
        self.assertEqual(self.args['source_buffers']['retained_gate'], alternate)
        with patch('builtins.compile', side_effect=AssertionError('source compile')), \
             patch('builtins.exec', side_effect=AssertionError('source execution')):
            self.assert_pending(c.validate_proposal(**self.args))

    def test_proposal_validation_opens_no_files_or_runtime(self):
        with patch('builtins.open', side_effect=AssertionError('file open')), \
             patch('pathlib.Path.open', side_effect=AssertionError('path open')), \
             patch('os.open', side_effect=AssertionError('os open')), \
             patch('subprocess.Popen', side_effect=AssertionError('process')), \
             patch.object(producer, 'RuntimeOps', side_effect=AssertionError('runtime')):
            self.assert_pending(c.validate_proposal(**self.args))


if __name__ == '__main__':
    unittest.main()
