"""Captured authored validators, invented metadata and intercepted legacy gate.

No protected input, installed dependency, runtime observation or actual records.
"""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from tools import dependency_observation_outer as outer
from tools import dependency_observation_contract as c
from test_dependency_observation_contract import fixture as contract_fixture, reseal, decided, change
from test_dependency_producer import refresh


def fixture():
    a = contract_fixture()
    sources = a['source_buffers']
    for name, role, _ in outer.GRAPH:
        if role not in outer.ADDED and name != 'retained_gate':
            sources[role] = Path('tools', name+'.py').read_bytes()
    gate = b'''import json
def validate_bundle(documents, *, expected_seal_sha256, reference_pins):
    # Invented intercepted legacy result. No old authority is promoted.
    return json.loads(documents['candidate'])
'''
    sources['retained_gate'] = gate
    manifest = json.loads(a['ordinary_buffers']['authored_source_manifest'])
    for role, raw in sources.items():
        manifest['sources'][role].update(c.receipt(raw))
    for role, row in manifest['prepared_sources'].items():
        row.update(c.receipt(sources[c.PREPARED_PROCESS_ROLES[role]]))
    a['ordinary_buffers']['authored_source_manifest'] = c.encoded(manifest)
    change(a, 'authored_source_receipts', lambda v:v.update(receipts={n:c.receipt(b) for n,b in sources.items()}))
    dep = json.loads(a['ordinary_buffers']['dependency_packet'])['inputs']
    dep['expectation']['source_sha256'] = {n:c.sha(c.encoded(manifest['prepared_sources'])
        if r == 'closure_manifest' else sources[r]) for n,r in c.DEPENDENCY_SOURCE_ROLES.items()}
    refresh(dep)
    a['ordinary_buffers']['dependency_packet'] = c.encoded(dict(schema='runtime_dependency_packet_v1', inputs=dep))
    fixed = json.loads(a['ordinary_buffers']['dependency_fixed'])
    fixed['expectation_sha256'] = c.sha(c.encoded(dep['expectation']))
    a['ordinary_buffers']['dependency_fixed'] = c.encoded(fixed)
    reseal(a)
    d = decided(a)
    proposal = json.loads(a['proposal_bytes'])
    legacy = dict(candidate=c.encoded(dict(candidate=dict(operation_id='1'*32),
        source_buffers={n.removeprefix('bound.'):b.decode() for n,b in sources.items() if n.startswith('bound.')},
        inputs=dict(source_manifest=proposal['protected_identities']['firmware_package'],
                    prerequisites=dict(constants_sha256='c'*64)))),
        review=b'invented old review', decision=b'invented old decision', seal=b'invented old seal',
        inputs=dict(a['retained_comparison_buffers']))
    # The intercepted result requires bytes for retained sources; the stub's
    # JSON decoding is amended below to restore only those invented fields.
    sources['retained_gate'] += b'''\n_original = validate_bundle
def validate_bundle(documents, **kw):
    result = _original(documents, **kw)
    result['source_buffers'] = {n:b.encode() for n,b in result['source_buffers'].items()}
    return result
'''
    manifest['sources']['retained_gate'].update(c.receipt(sources['retained_gate']))
    # The gate is outside the prepared dependency projection.
    a['ordinary_buffers']['authored_source_manifest'] = c.encoded(manifest)
    change(a, 'authored_source_receipts', lambda v:v.update(receipts={n:c.receipt(b) for n,b in sources.items()}))
    reseal(a)
    d = decided(a)
    captures = dict(sources)
    for name, role in (('dependency_observation_contract','observation.contract'),
                       ('dependency_observation_outer','observation.outer')):
        captures[role] = Path('tools', name+'.py').read_bytes()
    return dict(capture_buffers=captures, expected_capture_hashes={n:c.sha(b) for n,b in captures.items()},
        proposal_arguments=a, **{n:d[n] for n in ('review_bytes','decision_bytes','external_anchor_bytes',
                                                'expected_external_anchor_sha256')},
        runtime_expectation=json.loads(a['proposal_bytes'])['runtime'], legacy_documents=legacy,
        legacy_expected_seal_sha256=c.sha(legacy['seal']), legacy_reference_pins=dict(invented='f'*64))


class ObservationOuterTests(unittest.TestCase):
    def setUp(self):
        self.a = fixture()

    def test_owned_preflight_and_saved_parent_comparison(self):
        before = copy.deepcopy(self.a)
        result = outer.preflight(**self.a)
        self.assertEqual(self.a, before)
        self.assertEqual(result['status'], 'decided_scope_preflight_consistency_only')
        self.assertTrue(result['retained_comparison_semantics_revalidated'])
        self.assertFalse(result['legacy_authority_promoted'])
        self.assertEqual(len(result['capture_receipts']), 53)
        self.assertEqual(outer.CAPTURE_ROLES, c.SOURCE_ROLES | outer.ADDED)
        self.assertFalse(result['source_roster_delta']['operational_execution_roster_derived'])
        for field in outer.FALSE:
            self.assertIs(result[field], False)
        raw = outer.encoded(result)
        self.assertTrue(outer.verify_saved(raw=raw, expected_sha256=c.sha(raw), **self.a))

    def test_complete_source_graph_checked_before_any_execution(self):
        for kind in ('hash','roster','same_count_roster','edges','syntax'):
            a = copy.deepcopy(self.a)
            if kind == 'hash':a['capture_buffers']['adapter'] += b'\n'
            elif kind == 'roster':a['capture_buffers'].pop('host.launcher')
            elif kind == 'same_count_roster':
                for key in ('capture_buffers','expected_capture_hashes'):
                    a[key]['unexpected.role'] = a[key].pop('bound.role:core')
            else:
                value = b'import ctypes\n' if kind == 'edges' else b'if invalid\n'
                a['capture_buffers']['observation.contract'] = value
                a['expected_capture_hashes']['observation.contract'] = c.sha(value)
            with self.subTest(kind=kind), patch('builtins.exec', side_effect=AssertionError('exec')):
                with self.assertRaises((ValueError,SyntaxError)):
                    outer.preflight(**a)

    def test_new_authority_records_are_bound_outside_immutable_request(self):
        for key in ('expected_external_anchor_sha256','review_bytes','decision_bytes','external_anchor_bytes'):
            a = copy.deepcopy(self.a)
            a[key] = 'f'*64 if key.startswith('expected') else a[key]+b' '
            with self.subTest(key=key), self.assertRaises(ValueError):outer.preflight(**a)

    def test_pending_disposition_refuses_even_with_rehashed_local_chain(self):
        a = self.a['proposal_arguments']
        change(a, 'activity_rights', lambda v:v['decisions']['constants_provenance'].update(
            disposition='pending', evidence=[]))
        reseal(a)
        self.a.update({n:v for n,v in decided(a).items() if n not in a})
        with self.assertRaisesRegex(ValueError,'undecided'):outer.preflight(**self.a)

    def test_outside_runtime_expectation_blocks_rehashed_argv_change(self):
        a = self.a['proposal_arguments']
        p = json.loads(a['proposal_bytes'])
        p['runtime']['bootstrap'] = '# changed inert command'
        p['runtime']['argv'][7] = p['runtime']['bootstrap']
        a['proposal_bytes'] = c.encoded(p)
        self.a.update({n:v for n,v in decided(a).items() if n not in a})
        with self.assertRaisesRegex(ValueError,'runtime_expectation'):outer.preflight(**self.a)

    def test_capture_and_manifest_cannot_name_different_source_buffers(self):
        self.a['capture_buffers']['host.launcher'] += b'\n'
        self.a['expected_capture_hashes']['host.launcher'] = c.sha(self.a['capture_buffers']['host.launcher'])
        with self.assertRaisesRegex(ValueError,'original_sources'):outer.preflight(**self.a)

    def test_retained_original_bytes_and_protected_metadata_are_bound(self):
        for kind in ('basis','retained_source','firmware','constants','operation'):
            a = copy.deepcopy(self.a)
            if kind == 'basis':a['legacy_documents']['inputs']['basis'] += b' '
            else:
                v = json.loads(a['legacy_documents']['candidate'])
                if kind == 'retained_source':v['source_buffers']['role:core'] += '\n'
                elif kind == 'firmware':v['inputs']['source_manifest']['sha256'] = 'f'*64
                elif kind == 'constants':v['inputs']['prerequisites']['constants_sha256'] = 'f'*64
                else:v['candidate']['operation_id'] = '2'*32
                a['legacy_documents']['candidate'] = c.encoded(v)
            with self.subTest(kind=kind),self.assertRaises(ValueError):outer.preflight(**a)

    def test_actual_retained_gate_refuses_incomplete_invented_bundle(self):
        a = self.a
        raw = Path('private/sessions/20261019-RA-003-parent-evidence-v5/outer/outer_gate.py').read_bytes()
        a['capture_buffers']['retained_gate'] = raw
        a['expected_capture_hashes']['retained_gate'] = c.sha(raw)
        a['proposal_arguments']['source_buffers']['retained_gate'] = raw
        change(a['proposal_arguments'],'authored_source_manifest',lambda v:v['sources']['retained_gate'].update(c.receipt(raw)))
        change(a['proposal_arguments'],'authored_source_receipts',lambda v:v['receipts'].update(retained_gate=c.receipt(raw)))
        reseal(a['proposal_arguments'])
        a.update({n:v for n,v in decided(a['proposal_arguments']).items() if n not in a['proposal_arguments']})
        with self.assertRaises(ValueError):outer.preflight(**a)

    def test_live_validator_substitution_refuses_and_cleanup_clears_owner(self):
        owner = outer.Validators(buffers=self.a['capture_buffers'], expected_hashes=self.a['expected_capture_hashes']).load()
        owner.modules['dependency_observation_contract'].validate_decided_scope = lambda **k: {}
        with self.assertRaisesRegex(ValueError,'live_changed'):owner.intact()
        with self.assertRaisesRegex(ValueError,'live_changed'):owner.close()
        self.assertTrue(owner.closed)
        self.assertFalse(owner.modules)
        self.assertFalse(owner.buffers)
        with self.assertRaisesRegex(ValueError,'reclose'):owner.close()

    def test_refusal_closes_once_and_preserves_primary_if_cleanup_fails(self):
        calls = []
        close = outer.Validators.close
        def broken(owner):
            calls.append(owner)
            close(owner)
            raise OSError('invented cleanup failure')
        a = self.a
        a['expected_external_anchor_sha256'] = 'f'*64
        with patch.object(outer.Validators,'close',broken):
            with self.assertRaisesRegex(ValueError,'external_anchor') as got:outer.preflight(**a)
        self.assertEqual(len(calls),1)
        self.assertIsInstance(got.exception.__cause__,OSError)
        self.assertTrue(calls[0].closed)

    def test_cleanup_failure_never_returns_success(self):
        close = outer.Validators.close
        def broken(owner):
            close(owner)
            raise OSError('invented cleanup failure')
        with patch.object(outer.Validators,'close',broken):
            with self.assertRaises(OSError):outer.preflight(**self.a)

    def test_saved_freshness_or_changed_original_cannot_be_resealed(self):
        result = outer.preflight(**self.a)
        result['fresh_observation_verified'] = True
        raw = outer.encoded(result)
        with self.assertRaisesRegex(ValueError,'saved_original'):
            outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a)
        raw = outer.encoded(outer.preflight(**self.a))
        self.a['legacy_documents']['review'] += b' changed'
        with self.assertRaisesRegex(ValueError,'saved_original'):
            outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a)

    def test_no_io_runtime_observer_process_or_alias_changes(self):
        before = {n:m for n,m in sys.modules.items() if n=='tools' or n.startswith(('tools.','_observation_preflight'))}
        with patch('builtins.open',side_effect=AssertionError('open')), \
             patch('pathlib.Path.open',side_effect=AssertionError('path open')), \
             patch('os.open',side_effect=AssertionError('os open')), \
             patch('subprocess.Popen',side_effect=AssertionError('process')), \
             patch('ctypes.CDLL',side_effect=AssertionError('native')):
            self.assertFalse(outer.preflight(**self.a)['actual_inputs_accessed'])
        after = {n:m for n,m in sys.modules.items() if n=='tools' or n.startswith(('tools.','_observation_preflight'))}
        self.assertEqual(before,after)

    def test_public_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):outer.run_runtime()


if __name__ == '__main__':
    unittest.main()
