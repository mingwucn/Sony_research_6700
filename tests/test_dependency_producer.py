"""Invented modules/receipts and temporary outputs; no installed crypto or DLLs.

The fake cipher is a public-vector lookup table, not a crypto implementation.
The loader emits simulated audit events without calling a native loader.
"""
import copy
import importlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import dependency_producer as subject
from tools import dependency_evidence as core
from test_dependency_legacy import fixture as legacy_fixture


HELPER = '_invented_dependency_probe'


def refresh(data):
    policy = data['expectation']; package = data['package']
    manifest = package['manifest']; proof = package['installed_proof']
    for path, receipt in package['installed_receipts'].items():
        manifest['files'][path] = {k: receipt[k] for k in ('sha256', 'size')}
    manifest['roster_sha256'] = core._hash(manifest['files'])
    proof['roster_sha256'] = manifest['roster_sha256']
    proof['files'] = {path: dict(manifest['files'][path], open_identity_sha256=core._hash(row))
                      for path, row in package['installed_receipts'].items()}
    policy['manifest_sha256'] = core._hash(manifest)
    policy['installed_proof_sha256'] = core._hash(proof)
    data['binding'] = dict(schema='prospective_dependency_binding_v1',
        expectation_sha256=core._hash(policy), package_sha256=core._hash(package), review_sha256='b'*64)


def fixture(source_changes=None):
    old = legacy_fixture(); policy = old['expectation']; package = old['package']
    source = {alias: '# invented inert module\n' for alias in subject.ALIASES}
    source['Cryptodome.Util._raw_api'] = "from ctypes import CDLL\nbackend = 'ctypes'\n"
    paths = [subject.target(policy, row) for row in policy['native_libraries'].values()]
    source['Cryptodome.Cipher.AES'] = (
        'import importlib\nfrom '+HELPER+' import new\n'
        'from ctypes import CDLL\nMODE_ECB = 1\nMODE_CBC = 2\n'
        + ''.join('importlib.import_module('+repr(alias)+')\n'
                  for alias in subject.ALIASES if alias != 'Cryptodome.Cipher.AES')
        + ''.join('CDLL('+repr(path)+')\n' for path in paths))
    source.update(source_changes or {})
    contents = {}; observed = {}
    for group in ('python_origins', 'native_libraries', 'trusted_origins'):
        for index, (alias, row) in enumerate(policy[group].items()):
            raw = (source[alias].encode('utf-8') if group == 'python_origins'
                   else ('invented inert bytes '+group+' '+alias).encode('ascii'))
            path = subject.target(policy, row)
            metadata = dict(device=7, inode=1000+index, mode=stat.S_IFREG | 0o600,
                nlink=1, size=len(raw), mtime_ns=1234, ctime_ns=5678, file_attributes=0)
            receipt = dict(path=path, size=len(raw), sha256=subject.sha(raw), opened_read_only=True,
                **{key: dict(metadata) for key in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after')})
            row.update(size=len(raw), sha256=subject.sha(raw), identity={k: metadata[k] for k in core.CROSS})
            contents[path] = raw; observed[path] = receipt
            if group != 'trusted_origins':
                package['installed_receipts'][row['relative_path']] = dict(receipt, path=row['relative_path'])
    config = dict(schema='prospective_dependency_config_v1', operation_id=policy['operation_id'], vectors=old['config']['vectors'])
    cache = dict(schema='prospective_dependency_source_cache_v1', sources=source)
    config_json = subject.encoded(config).decode('ascii'); cache_json = subject.encoded(cache).decode('ascii')
    policy['config_sha256'] = subject.sha(config_json.encode()); policy['cache_sha256'] = subject.sha(cache_json.encode())
    source_buffers = {'runtime': b'# invented producer identity\n', 'continuation': b'# invented continuation identity\n'}
    policy['source_sha256'] = {k: subject.sha(v) for k, v in source_buffers.items()}
    roots = {name: dict(schema='dependency_directory_identity_v1', path=row['path'],
             ancestors=[dict(path=row['path'], device=7, inode=i+1, mode=stat.S_IFDIR | 0o700, file_attributes=0)])
             for i, (name, row) in enumerate(policy['roots'].items())}
    for name, value in roots.items(): policy['roots'][name]['identity_sha256'] = core._hash(value)
    data = dict(expectation=policy, package=package, config_json=config_json, cache_json=cache_json, source_buffers=source_buffers)
    refresh(data)
    return data, FakeOps(policy, contents, observed, roots, config['vectors'])


class FakeOps:
    def __init__(self, policy, contents, observed, roots, vectors):
        self.policy = policy; self.contents = contents; self.observed = observed; self.roots = roots; self.vectors = vectors
        self.hook = None; self.callback_calls = 0; self.loader_calls = 0; self.cipher_calls = 0
        self.reads = []; self.root_calls = 0; self.load_action = None; self.callback_action = None
        self.root_action = None; self.read_action = None
        self.modules = {}
        for name, row in policy['trusted_origins'].items():
            module = types.ModuleType(name); module.__file__ = subject.target(policy, row); self.modules[name] = module
        self.original = self.load; self.modules['ctypes'].CDLL = self.original
    def reader(self, path, row):
        self.reads.append(path)
        if self.read_action: self.read_action(self, path)
        raw, receipt = self.contents[path], copy.deepcopy(self.observed[path])
        core._receipt(receipt, path, row['sha256'], row['size'], row['identity'])
        return raw, receipt
    def root(self, path):
        self.root_calls += 1
        result = copy.deepcopy(next(v for v in self.roots.values() if v['path'] == path))
        return self.root_action(self, result) if self.root_action else result
    def startup(self):
        return dict(isolated=True, no_site=True, no_user_site=True, no_bytecode=True,
            preloaded_package_aliases=[], bootstrap_boundary=self.policy['bootstrap_boundary'])
    def audit_install(self, hook): self.hook = hook
    def bootstrap(self): return self.modules
    def load(self, path, **kwargs):
        self.loader_calls += 1
        if self.load_action: return self.load_action(self, path)
        self.hook('ctypes.dlopen', (path,)); return object()
    def new(self, key, mode, **kwargs):
        self.cipher_calls += 1
        vector = next(v for v in self.vectors if bytes.fromhex(v['key_hex']) == key and
                      (1 if v['mode'] == 'ECB' else 2) == mode)
        if mode == 2: assert kwargs['iv'] == bytes.fromhex(vector['iv_hex'])
        assert set(kwargs) <= {'iv', 'use_aesni'}
        plain, cipher = bytes.fromhex(vector['plaintext_hex']), bytes.fromhex(vector['ciphertext_hex'])
        class Cipher:
            def encrypt(self, value):
                assert value == plain
                return cipher
            def decrypt(self, value):
                assert value == cipher
                return plain
        return Cipher()
    def callback(self, AES, vectors):
        self.callback_calls += 1
        if self.callback_action: self.callback_action(self, AES)
        subject.run_vectors(AES, vectors)


class ProducerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)/'attempt'
        self.old_meta_object = sys.meta_path; self.old_path_object = sys.path
        self.old_meta = list(sys.meta_path); self.old_path = list(sys.path)
        self.old_modules = dict(sys.modules)
        self.addCleanup(self.restore)
    def restore(self):
        # Test isolation only. The producer itself must preserve foreign changes.
        sys.meta_path = self.old_meta_object; sys.path = self.old_path_object
        sys.meta_path[:] = self.old_meta; sys.path[:] = self.old_path
        for name in tuple(sys.modules):
            if name == HELPER or name == 'Cryptodome' or name.startswith('Cryptodome.') or name == 'ctypes':
                if name in self.old_modules: sys.modules[name] = self.old_modules[name]
                else: sys.modules.pop(name, None)
    def execute(self, data, ops):
        helper = types.ModuleType(HELPER); helper.new = ops.new
        sys.modules[HELPER] = helper; sys.modules['ctypes'] = ops.modules['ctypes']
        return subject.produce_invented(**data, folder=str(self.folder), ops=ops)
    def events(self):
        path = self.folder/'journal.jsonl'
        return [json.loads(row)['event'] for row in path.read_text().splitlines()] if path.exists() else []
    def refused(self, data, ops, code=None):
        with self.assertRaises(core.EvidenceError) as caught: self.execute(data, ops)
        if code: self.assertEqual(str(caught.exception), code)
        self.assertFalse((self.folder/'result.json').exists())
        self.assertNotIn('cleanup_complete', self.events())
        self.assertIs(ops.modules['ctypes'].CDLL, ops.original)
        self.assertEqual(sys.meta_path, self.old_meta)
    def test_complete_real_import_hook_and_outputs_with_invented_dependencies(self):
        data, ops = fixture(); before = copy.deepcopy(data)
        result = self.execute(data, ops)
        self.assertEqual(data, before)
        self.assertEqual((ops.loader_calls, ops.callback_calls, ops.cipher_calls), (5, 1, 48))
        self.assertEqual(result['observation']['evidence_mode'], 'invented')
        self.assertEqual(result['consistency']['status'], 'dependency_record_contract_consistent')
        self.assertEqual(len(result['source_execution_trace']), 22)
        self.assertEqual(self.events()[-8:], ['raw_written', 'raw_flushed', 'raw_fsynced', 'raw_closed',
            'raw_reverified', 'callback_claimed', 'callback_returned', 'cleanup_complete'])
        transcript = json.loads((self.folder/'raw.json').read_text())
        self.assertEqual(transcript['events'][-1]['event'], 'guard_finished')
        self.assertIs(ops.modules['ctypes'].CDLL, ops.original)
        self.assertEqual(sys.meta_path, self.old_meta)
        self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
        for name in ('executing_producer_authenticated', 'execution_authorized', 'operational_acceptance',
                     'feature_supported', 'recovery_proven', 'device_write_gate_passed'):
            self.assertIs(result[name], False)
        self.assertEqual(result['camera_commands'], [])
        # Retained simulated hook is inert after cleanup, even for a forbidden event.
        ops.hook('ctypes.dlopen', ('unrelated',))
    def test_before_execution_source_hash_change_refuses_without_output(self):
        data, ops = fixture(); data['source_buffers']['runtime'] += b'changed'
        self.refused(data, ops, 'source_hash'); self.assertFalse(self.folder.exists()); self.assertEqual(ops.reads, [])
    def test_cache_hash_change_refuses_before_any_import(self):
        data, ops = fixture(); data['cache_json'] += ' '
        self.refused(data, ops, 'input_hash'); self.assertFalse(self.folder.exists())
    def test_rebound_cache_missing_alias_refuses_before_output(self):
        data, ops = fixture(); cache = json.loads(data['cache_json']); cache['sources'].pop('Cryptodome.Random')
        data['cache_json'] = subject.encoded(cache).decode(); data['expectation']['cache_sha256'] = subject.sha(data['cache_json'].encode()); refresh(data)
        self.refused(data, ops, 'shape'); self.assertFalse(self.folder.exists())
    def test_review_binding_substitution_refuses_before_output(self):
        data, ops = fixture(); data['binding']['expectation_sha256'] = '0'*64
        self.refused(data, ops, 'prior_binding'); self.assertFalse(self.folder.exists())
    def test_root_substitution_before_output(self):
        data, ops = fixture(); ops.root_action = lambda _, row: dict(row, path='Z:/substituted')
        self.refused(data, ops, 'root_identity'); self.assertFalse(self.folder.exists())
    def test_root_change_during_callback_refuses(self):
        data, ops = fixture()
        ops.root_action = lambda op, row: dict(row, path='Z:/changed') if op.root_calls > 2 else row
        self.refused(data, ops, 'root_changed'); self.assertEqual(ops.callback_calls, 1)
    def test_source_buffer_differs_from_fresh_read(self):
        data, ops = fixture(); path = subject.target(data['expectation'], data['expectation']['python_origins']['Cryptodome'])
        ops.contents[path] = b'changed without expected receipt'
        self.refused(data, ops, 'executing_buffer'); self.assertEqual(ops.callback_calls, 0)
    def test_partial_source_execution_is_not_reported_complete(self):
        data, ops = fixture({'Cryptodome.Random': "raise ValueError('invented partial execution')\n"})
        with self.assertRaises(ValueError): self.execute(data, ops)
        self.assertNotIn('vectors_complete', self.events()); self.assertEqual(ops.callback_calls, 0)
        self.assertNotIn('Cryptodome.Random', sys.modules)
    def test_swallowed_source_failure_is_sticky(self):
        data, ops = fixture({'Cryptodome.Random': "raise ValueError('invented')\n"})
        finder = subject.Sources(data['expectation'],
            {name: text.encode() for name, text in json.loads(data['cache_json'])['sources'].items()},
            ops.reader, lambda *a: None)
        # Simulate code catching a partial import, without a second uncaught import
        # masking whether the loader itself retained its failure.
        module = types.ModuleType('Cryptodome.Random'); module.__loader__ = finder
        sys.modules[module.__name__] = module
        try: finder.exec_module(module)
        except ValueError: pass
        self.assertTrue(finder.failed); self.assertNotIn(module.__name__, finder.completed)
        self.assertEqual([row['stage'] for row in finder.trace], ['source_execute_intent'])
    def test_missing_native_audit_refuses(self):
        data, ops = fixture(); ops.load_action = lambda *a: object()
        self.refused(data, ops, 'missing_audit'); self.assertEqual(ops.callback_calls, 0)
    def test_duplicate_native_audit_refuses_even_if_swallowed(self):
        data, ops = fixture()
        def load(op, path):
            op.hook('ctypes.dlopen', (path,))
            try: op.hook('ctypes.dlopen', (path,))
            except core.EvidenceError: pass
            return object()
        ops.load_action = load; self.refused(data, ops, 'missing_audit'); self.assertEqual(ops.callback_calls, 0)
    def test_wrong_audit_target_refuses(self):
        data, ops = fixture(); ops.load_action = lambda op, path: op.hook('ctypes.dlopen', ('Z:/wrong.pyd',))
        self.refused(data, ops, 'unexpected_audit')
    def test_swallowed_process_attempt_is_sticky(self):
        data, ops = fixture()
        def load(op, path):
            op.hook('ctypes.dlopen', (path,))
            try: op.hook('subprocess.Popen', ('invented',))
            except core.EvidenceError: pass
            return object()
        ops.load_action = load; self.refused(data, ops, 'missing_audit'); self.assertEqual(ops.callback_calls, 0)
    def test_reentrant_native_attempt_is_sticky(self):
        data, ops = fixture()
        def load(op, path):
            try: op.modules['ctypes'].CDLL(path)
            except core.EvidenceError: pass
            op.hook('ctypes.dlopen', (path,))
        ops.load_action = load; self.refused(data, ops, 'unexpected_audit')
    def test_callback_lazy_native_load_is_refused_even_if_swallowed(self):
        data, ops = fixture()
        def callback(op, AES):
            try: op.modules['ctypes'].CDLL(next(iter(op.contents)))
            except core.EvidenceError: pass
        ops.callback_action = callback; self.refused(data, ops, 'sticky_guard_failure')
        self.assertNotIn('callback_returned', self.events())
    def test_callback_keyboard_interrupt_cleans_up_and_does_not_return_success(self):
        data, ops = fixture()
        def callback(*args): raise KeyboardInterrupt()
        ops.callback_action = callback
        with self.assertRaises(KeyboardInterrupt): self.execute(data, ops)
        self.assertIs(ops.modules['ctypes'].CDLL, ops.original)
        self.assertEqual(sys.meta_path, self.old_meta); self.assertNotIn('callback_returned', self.events())
        self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
    def test_callback_system_exit_cleans_up(self):
        data, ops = fixture()
        def callback(*args): raise SystemExit(9)
        ops.callback_action = callback
        with self.assertRaises(SystemExit): self.execute(data, ops)
        self.assertIs(ops.modules['ctypes'].CDLL, ops.original); self.assertNotIn('cleanup_complete', self.events())
    def test_foreign_alias_replacement_survives_refusal(self):
        data, ops = fixture(); foreign = types.ModuleType('Cryptodome.Random')
        ops.callback_action = lambda *a: sys.modules.__setitem__('Cryptodome.Random', foreign)
        self.refused(data, ops, 'source_ownership'); self.assertIs(sys.modules['Cryptodome.Random'], foreign)
    def test_foreign_finder_survives_refusal(self):
        data, ops = fixture(); foreign = object()
        ops.callback_action = lambda *a: sys.meta_path.append(foreign)
        with self.assertRaisesRegex(core.EvidenceError, '^runtime_changed$'): self.execute(data, ops)
        self.assertIn(foreign, sys.meta_path); self.assertNotIn('cleanup_complete', self.events())
    def test_foreign_native_wrapper_survives_refusal(self):
        data, ops = fixture(); foreign = object()
        ops.callback_action = lambda *a: setattr(ops.modules['ctypes'], 'CDLL', foreign)
        with self.assertRaisesRegex(core.EvidenceError, '^runtime_changed$'): self.execute(data, ops)
        self.assertIs(ops.modules['ctypes'].CDLL, foreign); self.assertNotIn('cleanup_complete', self.events())
    def test_existing_attempt_is_not_overwritten(self):
        data, ops = fixture(); self.folder.mkdir(); sentinel = self.folder/'sentinel'; sentinel.write_bytes(b'preserve')
        with self.assertRaises(FileExistsError): self.execute(data, ops)
        self.assertEqual(sentinel.read_bytes(), b'preserve'); self.assertEqual(ops.callback_calls, 0)
    def test_real_runtime_and_subclass_are_refused(self):
        class Derived(subject.RuntimeOps): pass
        for ops in (subject.RuntimeOps(), Derived()):
            with self.subTest(type=type(ops).__name__), self.assertRaisesRegex(core.EvidenceError, '^real_activation_pending$'):
                subject.produce_invented(ops=ops)
    def test_cli_refuses_without_opening_inputs(self):
        with patch('builtins.print') as output: self.assertEqual(subject.main(), 2)
        self.assertEqual(json.loads(output.call_args.args[0])['camera_commands'], [])
    def test_preloaded_package_alias_refuses_before_output(self):
        data, ops = fixture(); sys.modules['Cryptodome'] = types.ModuleType('Cryptodome')
        with self.assertRaisesRegex(core.EvidenceError, '^preloaded_alias$'): self.execute(data, ops)
        self.assertFalse(self.folder.exists()); self.assertEqual(ops.reads, [])
    def test_native_bytes_change_after_simulated_load(self):
        data, ops = fixture()
        def load(op, path):
            op.hook('ctypes.dlopen', (path,)); op.contents[path] += b'changed'; return object()
        ops.load_action = load; self.refused(data, ops, 'native_changed'); self.assertEqual(ops.callback_calls, 0)
    def test_trusted_identity_change_during_bootstrap(self):
        data, ops = fixture(); original = ops.bootstrap
        def bootstrap():
            path = subject.target(ops.policy, ops.policy['trusted_origins']['ctypes'])
            ops.observed[path]['lstat_after']['inode'] += 1
            return original()
        ops.bootstrap = bootstrap; self.refused(data, ops, 'file_changed'); self.assertEqual(ops.loader_calls, 0)
    def test_second_raw_verification_failure_prevents_callback(self):
        data, ops = fixture(); original = subject.Outputs.verify_raw; calls = []
        def verify(out, raw):
            calls.append(1)
            if len(calls) == 2: raise core.EvidenceError('invented_second_readback')
            return original(out, raw)
        with patch.object(subject.Outputs, 'verify_raw', verify):
            self.refused(data, ops, 'invented_second_readback')
        self.assertEqual(ops.callback_calls, 0); self.assertNotIn('callback_claimed', self.events())
    def test_each_publication_journal_failure_prevents_callback(self):
        original = subject.Outputs.emit
        for event in ('raw_written', 'raw_flushed', 'raw_fsynced', 'raw_closed', 'raw_reverified', 'callback_claimed'):
            with self.subTest(event=event):
                self.folder = Path(self.temp.name)/event
                data, ops = fixture()
                def emit(out, name, payload):
                    if name == event:
                        out.failed = True
                        raise core.EvidenceError('invented_journal_failure')
                    return original(out, name, payload)
                with patch.object(subject.Outputs, 'emit', emit): self.refused(data, ops, 'invented_journal_failure')
                self.assertEqual(ops.callback_calls, 0); self.assertNotIn(event, self.events())
    def test_deleted_loader_attribute_does_not_skip_alias_or_output_cleanup(self):
        data, ops = fixture(); closed = []; original = subject.Outputs.close
        def close(out):
            original(out); closed.append((out.raw, out.journal))
        ops.callback_action = lambda *a: delattr(ops.modules['ctypes'], 'CDLL')
        with patch.object(subject.Outputs, 'close', close), self.assertRaises(AttributeError): self.execute(data, ops)
        self.assertEqual(closed, [(None, None)])
        self.assertEqual(sys.meta_path, self.old_meta)
        self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
        self.assertNotIn('cleanup_complete', self.events())
    def test_interrupt_during_wrapper_restoration_still_closes_outputs(self):
        data, ops = fixture(); closed = []; original = subject.Outputs.close
        class BrokenRestore(types.ModuleType):
            def __setattr__(module, name, value):
                if name == 'CDLL' and value is ops.original: raise KeyboardInterrupt('invented cleanup interrupt')
                return super().__setattr__(name, value)
        def callback(*a): ops.modules['ctypes'].__class__ = BrokenRestore
        def close(out): original(out); closed.append(1)
        ops.callback_action = callback
        with patch.object(subject.Outputs, 'close', close), self.assertRaises(KeyboardInterrupt): self.execute(data, ops)
        self.assertEqual(closed, [1]); self.assertEqual(sys.meta_path, self.old_meta)
        self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
        self.assertNotIn('cleanup_complete', self.events())
    def test_primary_callback_exception_preserved_when_cleanup_also_fails(self):
        data, ops = fixture(); closed = []; original = subject.Outputs.close
        def callback(*a):
            del ops.modules['ctypes'].CDLL
            raise SystemExit(17)
        def close(out): original(out); closed.append(1)
        ops.callback_action = callback
        with patch.object(subject.Outputs, 'close', close), self.assertRaises(SystemExit) as error: self.execute(data, ops)
        self.assertEqual(error.exception.code, 17); self.assertEqual(closed, [1])
        self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
    def test_finder_removal_failure_still_releases_aliases_and_closes(self):
        data, ops = fixture(); closed = []; original = subject.Outputs.close
        class BrokenList(list):
            def __delitem__(self, index): raise RuntimeError('invented finder removal failure')
        def callback(*a): sys.meta_path = BrokenList(sys.meta_path)
        def close(out): original(out); closed.append(1)
        ops.callback_action = callback
        with patch.object(subject.Outputs, 'close', close), self.assertRaisesRegex(RuntimeError, 'finder removal'): self.execute(data, ops)
        self.assertEqual(closed, [1]); self.assertFalse(any(n.startswith('Cryptodome') for n in sys.modules))
        self.assertNotIn('cleanup_complete', self.events())
    def test_unavailable_fallback_probe_does_not_reach_later_finder(self):
        data, ops = fixture(); finder = subject.Sources(data['expectation'], {}, ops.reader, lambda *a: None)
        calls = []
        class LaterFinder:
            def find_spec(self, fullname, path=None, target=None): calls.append(fullname); raise AssertionError('fallback executed')
        sys.meta_path[:] = [finder, LaterFinder()]
        with patch.object(importlib.machinery.PathFinder, 'find_spec', return_value=None):
            for name in ('cffi', '_cffi_backend', 'pycparser'):
                with self.subTest(name=name), self.assertRaises(ModuleNotFoundError): importlib.import_module(name)
        self.assertEqual(calls, []); self.assertFalse(finder.failed)
    def test_reachable_fallback_probe_is_sticky_without_loading(self):
        data, ops = fixture(); finder = subject.Sources(data['expectation'], {}, ops.reader, lambda *a: None)
        with patch.object(importlib.machinery.PathFinder, 'find_spec', return_value=object()):
            with self.assertRaisesRegex(core.EvidenceError, '^fallback_reachable$'): finder.find_spec('cffi')
        self.assertTrue(finder.failed)


class DisposableAuditTests(unittest.TestCase):
    def child(self, scenario):
        code = '''
import json,pathlib,sys,tempfile,types
sys.path.insert(0,str(pathlib.Path.cwd()))
sys.path.insert(0,str(pathlib.Path.cwd()/'tests'))
from test_dependency_producer import fixture,HELPER
from tools import dependency_producer as subject
from tools import dependency_evidence as core
data,ops=fixture()
helper=types.ModuleType(HELPER);helper.new=ops.new
sys.modules[HELPER]=helper;sys.modules['ctypes']=ops.modules['ctypes']
def install(hook):
 sys.addaudithook(hook)
 ops.hook=lambda event,args:sys.audit(event,*args)
ops.audit_install=install
scenario=SCENARIO
if scenario=='swallowed_process':
 def callback(op,AES):
  try:sys.audit('os.system',b'invented event only; no command executed')
  except core.EvidenceError:pass
 ops.callback_action=callback
with tempfile.TemporaryDirectory() as folder:
 try:
  result=subject.produce_invented(**data,folder=str(pathlib.Path(folder)/'attempt'),ops=ops)
  assert scenario=='success' and result['test_injection_used'] is True
 except core.EvidenceError as error:
  assert scenario=='swallowed_process' and str(error)=='sticky_guard_failure'
 assert not any(n=='Cryptodome' or n.startswith('Cryptodome.') for n in sys.modules)
 assert ops.modules['ctypes'].CDLL is ops.original
 # Audit hooks cannot be removed; this event returns only because it is inert.
 sys.audit('ctypes.dlopen','invented after cleanup; no native operation')
print(json.dumps(dict(scenario=scenario,inert_after_cleanup=True,native_loader_executed=False)))
'''.replace('SCENARIO', repr(scenario))
        result = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=25)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertTrue(receipt['inert_after_cleanup']); self.assertFalse(receipt['native_loader_executed'])
    def test_real_inert_audit_hook_in_disposable_child(self): self.child('success')
    def test_real_audit_swallowed_process_event_is_sticky(self): self.child('swallowed_process')


class HandleProxy:
    def __init__(self, handle, fail): self.handle = handle; self.fail = fail; self.close_calls = 0
    def write(self, raw):
        if self.fail == 'write': return self.handle.write(raw[:-1])
        return self.handle.write(raw)
    def flush(self):
        if self.fail == 'flush': raise OSError('invented flush failure')
        return self.handle.flush()
    def fileno(self): return self.handle.fileno()
    def close(self):
        self.close_calls += 1
        result = self.handle.close()
        if self.fail == 'close': raise OSError('invented uncertain close')
        return result


class OutputFaultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.out = subject.Outputs(Path(self.temp.name)/'attempt'); self.out.reserve({}, {})
        self.addCleanup(self.release)
    def release(self):
        try: self.out.close()
        except core.EvidenceError: pass
    def test_short_raw_write_is_sticky_without_success_marker(self):
        self.out.raw = HandleProxy(self.out.raw, 'write')
        with self.assertRaisesRegex(core.EvidenceError, '^raw_write$'): self.out.publish({}, 'invented')
        self.assertEqual(self.out.events, [])
        with self.assertRaisesRegex(core.EvidenceError, '^sticky_failure$'): self.out.emit('later', {})
    def test_raw_flush_failure_records_only_completed_write(self):
        self.out.raw = HandleProxy(self.out.raw, 'flush')
        with self.assertRaises(OSError): self.out.publish({}, 'invented')
        self.assertEqual([r['event'] for r in self.out.events], ['raw_written']); self.assertTrue(self.out.failed)
    def test_raw_fsync_failure_records_no_fsync_marker(self):
        raw_fd = self.out.raw.fileno(); original = os.fsync
        def fsync(fd):
            if fd == raw_fd: raise OSError('invented fsync')
            original(fd)
        with patch.object(subject.os, 'fsync', fsync), self.assertRaises(OSError): self.out.publish({}, 'invented')
        self.assertEqual([r['event'] for r in self.out.events], ['raw_written', 'raw_flushed'])
    def test_uncertain_raw_close_is_never_retried(self):
        proxy = HandleProxy(self.out.raw, 'close'); self.out.raw = proxy
        with self.assertRaises(OSError): self.out.publish({}, 'invented')
        self.out.close(); self.assertEqual(proxy.close_calls, 1)
        self.assertNotIn('raw_closed', [r['event'] for r in self.out.events])
    def test_readback_failure_is_sticky(self):
        with patch.object(subject, 'read_verified', side_effect=core.EvidenceError('invented_readback')):
            with self.assertRaisesRegex(core.EvidenceError, '^invented_readback$'): self.out.publish({}, 'invented')
        self.assertTrue(self.out.failed)
        self.assertEqual(self.out.events[-1]['event'], 'raw_closed')
    def test_journal_short_write_is_sticky(self):
        self.out.journal = HandleProxy(self.out.journal, 'write')
        with self.assertRaisesRegex(core.EvidenceError, '^journal_write$'): self.out.emit('invented', {})
        self.assertTrue(self.out.failed); self.assertEqual(self.out.events, [])
    def test_journal_flush_failure_does_not_claim_success(self):
        self.out.journal = HandleProxy(self.out.journal, 'flush')
        with self.assertRaises(OSError): self.out.emit('invented', {})
        self.assertTrue(self.out.failed); self.assertEqual(self.out.events, [])
    def test_journal_fsync_failure_does_not_claim_success(self):
        with patch.object(subject.os, 'fsync', side_effect=OSError('invented fsync')):
            with self.assertRaises(OSError): self.out.emit('invented', {})
        self.assertTrue(self.out.failed); self.assertEqual(self.out.events, [])
    def test_uncertain_journal_close_is_never_retried(self):
        proxy = HandleProxy(self.out.journal, 'close'); self.out.journal = proxy
        with self.assertRaisesRegex(core.EvidenceError, '^output_close$'): self.out.close()
        self.out.close(); self.assertEqual(proxy.close_calls, 1)


class OrdinaryReaderTests(unittest.TestCase):
    def test_new_temporary_file_read_has_complete_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'invented.txt'; path.write_bytes(b'invented only')
            raw, receipt = subject.read_verified(str(path))
            self.assertEqual(raw, b'invented only')
            self.assertIs(receipt['opened_read_only'], True)
    def test_read_limit_and_hard_link_refuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'invented.txt'; path.write_bytes(b'invented only')
            with self.assertRaisesRegex(core.EvidenceError, '^file_kind$'): subject.read_verified(str(path), limit=1)
            for limit in (0, True, -1, 8*1024**2+1):
                with self.subTest(limit=limit), self.assertRaisesRegex(core.EvidenceError, '^read_bound$'):
                    subject.read_verified(str(path), limit=limit)
            os.link(path, Path(tmp)/'link.txt')
            with self.assertRaisesRegex(core.EvidenceError, '^file_kind$'): subject.read_verified(str(path))


if __name__ == '__main__': unittest.main()
