"""Complete invented legacy records through the unchanged captured gate.

Reads authored validator/fixture/gate sources and three pinned repair sources.
No old saved results, protected inputs, dependency activation or observer runs.
Synthetic legacy authority/receipts are consistency inputs, never real consent.
"""
import base64
import copy
import json
from pathlib import Path
import stat
import types
import unittest
from unittest.mock import patch

from tools import dependency_observation_outer as outer
from tools import dependency_observation_contract as c
from test_dependency_observation_outer import fixture as intercepted_fixture
from test_dependency_observation_contract import reseal, decided, change
from test_dependency_producer import refresh


HERE = Path('private/sessions/20261019-RA-003-parent-evidence-v5')
GATE_SHA = 'faa196abe6dbea4ef141deab810558f8f0e03fdda9bc0b9d9c4b6acda2f25172'
FIXTURE_SHA = 'fd1c6e34c706a58dcc4bbabdd6afe9e6f47f0580be4d202ad2a182572e7e303c'


def load_source(path, expected):
    raw = path.read_bytes()
    if c.sha(raw) != expected:
        raise ValueError('invented_fixture_source_changed')
    module = types.ModuleType('_invented_legacy_' + path.stem)
    exec(compile(raw, '<authored-' + path.name + '>', 'exec'), vars(module))
    return module, raw


def legacy_fixture():
    """Construct metadata in memory. Path labels are never opened.

    Gate policy is never changed. Frozen historical qualification declarations
    are invented evidence in this new chain; they are not fresh test results.
    Three source-cache entries use real authored code to meet frozen repairs;
    all remaining role/dependency/cache bytes are inert invented Python text.
    """
    gate, raw = load_source(HERE/'outer/outer_gate.py', GATE_SHA)
    fixtures, _ = load_source(HERE/'outer/outer_fixtures.py', FIXTURE_SHA)
    names = ('REQUIRED_OUTER_TEST_IDS','REQUIRED_OUTER_SOURCE_NAMES',
        'REQUIRED_OUTER_SOURCE_PINS','REQUIRED_REPAIR_TEST_IDS',
        'REQUIRED_REPAIR_SOURCE_PINS','REQUIRED_FACTORY_TEST_IDS',
        'REQUIRED_CHILD_TEST_IDS','PARENT_EVIDENCE_POLICY')
    for name in names:
        setattr(fixtures, name, copy.deepcopy(getattr(gate, name)))
    f = fixtures.Fixture(Path.cwd()/'private/invented-observation-root')
    p = f.p
    sources = p['source_cache']['sources']
    receipts = p['source_receipts']['receipts']
    for key in tuple(sources):
        if key.startswith('role:'):
            del sources[key]
            del receipts[key]
    legacy = f.c['legacy_session']
    roles = {}

    def put(key, path, data):
        sources[key] = dict(path=str(path), **c.receipt(data),
                            base64=base64.b64encode(data).decode('ascii'))
        stamp = dict(st_dev=1, st_ino=len(sources), st_mode=stat.S_IFREG|0o666,
            st_nlink=1, st_size=len(data), st_mtime_ns=1, st_ctime_ns=1, st_file_attributes=0)
        receipts[key] = dict(path=str(path), **c.receipt(data), close_attempts=1,
            eof_probes=1, closed=True,
            **{n:copy.deepcopy(stamp) for n in ('lstat_before','lstat_after','fstat_before','fstat_after')})

    for name in c.comparison.ROLES:
        key = 'role:' + name
        data = ('# invented inert role ' + name + '\n').encode('ascii')
        if key in gate.REPAIR_KEYS:
            path = HERE/gate.REPAIR_SOURCE_NAMES[key]
            data = path.read_bytes()
            if c.sha(data) != gate.REQUIRED_REPAIR_SOURCE_PINS[gate.REPAIR_SOURCE_NAMES[key]]:
                raise ValueError('invented_fixture_repair_source_changed')
        relative = legacy + '/' + name + '.py'
        put(key, f.root/relative, data)
        roles[name] = dict(path=relative, sha256=c.sha(data))
    key = 'bootstrap:io_entry'
    data = (HERE/gate.REPAIR_SOURCE_NAMES[key]).read_bytes()
    if c.sha(data) != gate.REQUIRED_REPAIR_SOURCE_PINS[gate.REPAIR_SOURCE_NAMES[key]]:
        raise ValueError('invented_fixture_repair_source_changed')
    put(key, f.root/legacy/'io_entry.py', data)
    p['role_authority']['roles'] = roles
    p['binding_schema'] = dict(aliases={n:n for n in roles},
        load_order=list(roles)[:23], protected_order=list(roles)[23:])
    p['prerequisites']['qualified_roles'] = copy.deepcopy(roles)
    p['prerequisites']['binding_input']['roles'] = copy.deepcopy(roles)
    old = {Path(row['path']).name:row['sha256'] for key,row in sources.items()
           if key.startswith(('role:','bootstrap:'))}
    for key in gate.REPAIR_KEYS:
        name = Path(sources[key]['path']).name
        old[name] = '9'*64
        p['repair_overlay']['repairs'][key] = dict(path=legacy+'/'+name,
            old_sha256='9'*64, new_sha256=sources[key]['sha256'])
    old.update({'invented_extra_'+str(i)+'.py':'f'*64 for i in range(66)})
    for name in ('q_old_result','q_old_seal','q_old_review'):
        p[name]['sources_sha256'] = copy.deepcopy(old)
    composition = p['factory_evidence']['composition']['source_sha256']
    for key in tuple(composition):
        if key.startswith('roles/'):
            del composition[key]
    composition.update({'roles/'+n+'.py':row['sha256'] for n,row in roles.items()})
    composition['io_entry.py'] = sources['bootstrap:io_entry']['sha256']
    p['source_manifest'].update(bytes=1024017848, sha256='a'*64)
    p['basis']['prior_stream'].update(input_package_bytes=1024017848, input_package_sha256='a'*64)
    p['prerequisites']['constants_sha256'] = 'c'*64
    return f, gate, raw


def fixture():
    """Replace all intercepted legacy inputs; no intercepted gate survives."""
    a = intercepted_fixture()
    f, gate, raw = legacy_fixture()
    docs, seal = f.pack()
    args = a['proposal_arguments']
    source = args['source_buffers']
    source['retained_gate'] = raw
    for name in source:
        if name.startswith('bound.'):
            source[name] = base64.b64decode(f.p['source_cache']['sources'][name.removeprefix('bound.')]['base64'])
    original = {n:docs['inputs'][n] for n in c.RETAINED}
    args['retained_comparison_buffers'] = original
    args['ordinary_buffers'].update(original)
    change(args, 'historical_evidence_index', lambda v:v.update(
        original_comparison={n:c.receipt(b) for n,b in original.items()}))
    manifest = json.loads(args['ordinary_buffers']['authored_source_manifest'])
    for name, data in source.items():
        manifest['sources'][name].update(c.receipt(data))
    for name, row in manifest['prepared_sources'].items():
        row.update(c.receipt(source[c.PREPARED_PROCESS_ROLES[name]]))
    args['ordinary_buffers']['authored_source_manifest'] = c.encoded(manifest)
    change(args, 'authored_source_receipts', lambda v:v.update(receipts={n:c.receipt(b) for n,b in source.items()}))
    dep = json.loads(args['ordinary_buffers']['dependency_packet'])['inputs']
    dep['expectation']['source_sha256'] = {n:c.sha(c.encoded(manifest['prepared_sources'])
        if role=='closure_manifest' else source[role]) for n,role in c.DEPENDENCY_SOURCE_ROLES.items()}
    refresh(dep)
    args['ordinary_buffers']['dependency_packet'] = c.encoded(dict(schema='runtime_dependency_packet_v1', inputs=dep))
    fixed = json.loads(args['ordinary_buffers']['dependency_fixed'])
    fixed['expectation_sha256'] = c.sha(c.encoded(dep['expectation']))
    args['ordinary_buffers']['dependency_fixed'] = c.encoded(fixed)
    reseal(args)
    a.update({n:v for n,v in decided(args).items() if n not in args})
    a['runtime_expectation'] = json.loads(args['proposal_bytes'])['runtime']
    a['capture_buffers'].update(source)
    a['expected_capture_hashes'] = {n:c.sha(b) for n,b in a['capture_buffers'].items()}
    a.update(legacy_documents=docs, legacy_expected_seal_sha256=seal,
        legacy_reference_pins=f.reference_pins(docs))
    return a


class UnchangedLegacyObservationTests(unittest.TestCase):
    def setUp(self):
        self.a = fixture()

    def test_complete_unchanged_gate_and_saved_parent(self):
        self.assertEqual(c.sha(self.a['capture_buffers']['retained_gate']), GATE_SHA)
        before = copy.deepcopy(self.a)
        result = outer.preflight(**self.a)
        self.assertEqual(before, self.a)
        self.assertTrue(result['retained_comparison_semantics_revalidated'])
        self.assertTrue(result['source_owner_closed'])
        self.assertFalse(result['legacy_authority_promoted'])
        for field in outer.FALSE:
            self.assertIs(result[field], False)
        self.assertEqual(len(result['legacy_original_receipts']), 31)
        self.assertEqual(len(result['capture_receipts']), 53)
        raw = outer.encoded(result)
        self.assertTrue(outer.verify_saved(raw=raw, expected_sha256=c.sha(raw), **self.a))

    def test_gate_policy_unchanged_and_repairs_exact(self):
        f, gate, raw = legacy_fixture()
        policy = {n:copy.deepcopy(getattr(gate,n)) for n in (
            'REQUIRED_REPAIR_SOURCE_PINS','REQUIRED_OUTER_SOURCE_PINS','PARENT_EVIDENCE_POLICY')}
        docs, seal = f.pack()
        value = gate.validate_bundle(docs, expected_seal_sha256=seal, reference_pins=f.reference_pins(docs))
        self.assertEqual(c.sha(raw), GATE_SHA)
        for name, before in policy.items():
            self.assertEqual(getattr(gate,name), before)
        for key, path in gate.REPAIR_SOURCE_NAMES.items():
            self.assertEqual(c.sha(value['source_buffers'][key]), gate.REQUIRED_REPAIR_SOURCE_PINS[path])
        self.assertTrue(value['execution_authorized'])  # Historical invented field only.
        self.assertFalse(outer.preflight(**self.a)['legacy_authority_promoted'])

    def test_original_six_legacy_records_refuse_substitution(self):
        for name in c.RETAINED:
            a = copy.deepcopy(self.a)
            a['legacy_documents']['inputs'][name] += b' '
            with self.subTest(name=name), self.assertRaisesRegex(ValueError,'original_comparison'):
                outer.preflight(**a)

    def test_resealed_legacy_repair_pin_cannot_be_replaced(self):
        f, gate, _ = legacy_fixture()
        key = 'role:gdt_gate'
        row = f.p['source_cache']['sources'][key]
        row['sha256'] = 'f'*64
        f.p['repair_overlay']['repairs'][key]['new_sha256'] = 'f'*64
        docs, seal = f.pack()
        a = self.a
        # Preserve original six comparison inputs so the unchanged gate is reached.
        a.update(legacy_documents=docs, legacy_expected_seal_sha256=seal,
                 legacy_reference_pins=f.reference_pins(docs))
        with self.assertRaisesRegex(ValueError,'repair_identity'):
            outer.preflight(**a)

    def test_external_legacy_reference_and_seal_are_not_local_reseals(self):
        for kind in ('seal','reference'):
            a = copy.deepcopy(self.a)
            if kind=='seal':
                a['legacy_expected_seal_sha256'] = 'f'*64
            else:
                a['legacy_reference_pins']['factory_evidence'] = 'f'*64
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError,'external_anchor|reference_authority'):
                outer.preflight(**a)

    def test_noncomparison_original_is_still_bound_by_legacy_gate(self):
        self.a['legacy_documents']['inputs']['factory_evidence'] += b' '
        with self.assertRaisesRegex(ValueError,'input_binding'):
            outer.preflight(**self.a)

    def test_captured_retained_source_resealed_locally_still_refuses(self):
        a = self.a
        args = a['proposal_arguments']
        name = 'bound.role:core'
        args['source_buffers'][name] += b'# replaced\n'
        manifest = json.loads(args['ordinary_buffers']['authored_source_manifest'])
        manifest['sources'][name].update(c.receipt(args['source_buffers'][name]))
        for role,row in manifest['prepared_sources'].items():
            if c.PREPARED_PROCESS_ROLES[role]==name:
                row.update(c.receipt(args['source_buffers'][name]))
        args['ordinary_buffers']['authored_source_manifest'] = c.encoded(manifest)
        change(args,'authored_source_receipts',lambda v:v['receipts'].update({name:c.receipt(args['source_buffers'][name])}))
        dep = json.loads(args['ordinary_buffers']['dependency_packet'])['inputs']
        dep['expectation']['source_sha256']['closure_manifest'] = c.sha(c.encoded(manifest['prepared_sources']))
        refresh(dep)
        args['ordinary_buffers']['dependency_packet'] = c.encoded(dict(schema='runtime_dependency_packet_v1',inputs=dep))
        fixed = json.loads(args['ordinary_buffers']['dependency_fixed'])
        fixed['expectation_sha256'] = c.sha(c.encoded(dep['expectation']))
        args['ordinary_buffers']['dependency_fixed'] = c.encoded(fixed)
        reseal(args)
        a.update({n:v for n,v in decided(args).items() if n not in args})
        # Deliberately select a new invented outside command expectation so the
        # deeper unchanged legacy source-byte comparison is exercised.
        a['runtime_expectation'] = json.loads(args['proposal_bytes'])['runtime']
        a['capture_buffers'][name] = args['source_buffers'][name]
        a['expected_capture_hashes'][name] = c.sha(args['source_buffers'][name])
        with self.assertRaisesRegex(ValueError,'retained_sources'):
            outer.preflight(**a)

    def test_complete_chain_remains_no_io_after_source_capture(self):
        import ctypes
        import os
        import socket
        import subprocess
        with patch('builtins.open',side_effect=AssertionError('open')), \
             patch.object(Path,'open',side_effect=AssertionError('path_open')), \
             patch.object(os,'open',side_effect=AssertionError('os_open')), \
             patch.object(os,'read',side_effect=AssertionError('os_read')), \
             patch.object(socket,'socket',side_effect=AssertionError('socket')), \
             patch.object(subprocess,'Popen',side_effect=AssertionError('process')), \
             patch.object(ctypes,'CDLL',side_effect=AssertionError('native')):
            value = outer.preflight(**self.a)
            raw = outer.encoded(value)
            self.assertTrue(outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a))

    def test_outside_current_anchor_and_runtime_still_refuse(self):
        for kind in ('anchor','runtime'):
            a = copy.deepcopy(self.a)
            if kind=='anchor':a['expected_external_anchor_sha256'] = 'f'*64
            else:a['runtime_expectation']['bootstrap'] += '# changed'
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                outer.preflight(**a)

    def test_pending_actual_style_disposition_refuses(self):
        args = self.a['proposal_arguments']
        change(args,'activity_rights',lambda v:v['decisions']['constants_provenance'].update(disposition='pending',evidence=[]))
        reseal(args)
        self.a.update({n:v for n,v in decided(args).items() if n not in args})
        with self.assertRaisesRegex(ValueError,'undecided'):
            outer.preflight(**self.a)

    def test_saved_result_cannot_promote_historical_authority(self):
        result = outer.preflight(**self.a)
        for field in ('legacy_authority_promoted','execution_authorized','feature_supported'):
            changed = copy.deepcopy(result)
            changed[field] = True
            raw = outer.encoded(changed)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError,'saved_original'):
                outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a)

    def test_success_and_gate_refusal_close_validator_owner_once(self):
        close = outer.Validators.close
        calls = []
        def counted(owner):
            calls.append(owner)
            return close(owner)
        with patch.object(outer.Validators,'close',counted):
            outer.preflight(**self.a)
            self.a['legacy_reference_pins']['parent_evidence'] = 'f'*64
            with self.assertRaisesRegex(ValueError,'reference_authority'):
                outer.preflight(**self.a)
        self.assertEqual(len(calls),2)
        self.assertIsNot(calls[0],calls[1])
        for owner in calls:
            self.assertTrue(owner.closed)
            self.assertFalse(owner.buffers or owner.modules or owner.compiled)

    def test_reselected_proposal_protected_identity_still_matches_legacy(self):
        for name in ('firmware_package','operational_constants'):
            a = copy.deepcopy(self.a)
            args = a['proposal_arguments']
            value = json.loads(args['proposal_bytes'])
            value['protected_identities'][name]['sha256'] = 'f'*64
            args['proposal_bytes'] = c.encoded(value)
            a.update({n:v for n,v in decided(args).items() if n not in args})
            with self.subTest(name=name), self.assertRaisesRegex(ValueError,'protected_identity'):
                outer.preflight(**a)

    def test_valid_other_legacy_operation_is_refused(self):
        f, gate, _ = legacy_fixture()
        for value in (f.c, f.d, f.r, f.s, f.p['activity_scope'], f.p['dependency_config']):
            value['operation_id'] = '2'*32
        docs, seal = f.pack()
        refs = f.reference_pins(docs)
        # Establish this is a valid other legacy operation, not a malformed
        # authority chain rejected earlier by the captured retained gate.
        self.assertEqual(gate.validate_bundle(docs,expected_seal_sha256=seal,
            reference_pins=refs)['candidate']['operation_id'],'2'*32)
        self.a.update(legacy_documents=docs,legacy_expected_seal_sha256=seal,
                      legacy_reference_pins=refs)
        with self.assertRaisesRegex(ValueError,'observation_outer_operation'):
            outer.preflight(**self.a)

    def test_cleanup_failure_cannot_return_success_or_hide_gate_failure(self):
        close = outer.Validators.close
        calls = []
        def fail(owner):
            calls.append(owner)
            close(owner)
            raise RuntimeError('invented_cleanup_uncertainty')
        with patch.object(outer.Validators,'close',fail):
            with self.assertRaisesRegex(RuntimeError,'cleanup_uncertainty'):
                outer.preflight(**self.a)
            self.a['legacy_reference_pins']['parent_evidence'] = 'f'*64
            with self.assertRaisesRegex(ValueError,'reference_authority') as error:
                outer.preflight(**self.a)
        self.assertIsInstance(error.exception.__cause__,RuntimeError)
        self.assertEqual(len(calls),2)
        self.assertTrue(all(owner.closed and not owner.modules for owner in calls))


if __name__=='__main__':
    unittest.main()
