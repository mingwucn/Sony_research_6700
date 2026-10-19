"""Invented dependency operations; no filesystem reader or native loader.

The cipher only looks up public vectors. Used by tests and bound child
composition, never as an installed-dependency observation.
"""
import copy
import json
import sys
import types

from tools import dependency_producer as subject
from tools import dependency_evidence as core

HELPER = '_invented_dependency_probe'


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
    def audit_probe(self, token): self.hook(subject.PROBE_EVENT, (token,))
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


def packet(data, ops, source_buffers, review_sha256):
    """Serialize invented test inputs before launch; never read installed files."""
    data = copy.deepcopy(data)
    data.pop('source_buffers')
    data['expectation']['source_sha256'] = {k: subject.sha(v) for k, v in source_buffers.items()}
    data['binding'] = dict(schema='prospective_dependency_binding_v1',
        expectation_sha256=core._hash(data['expectation']), package_sha256=core._hash(data['package']),
        review_sha256=review_sha256)
    return dict(schema='invented_dependency_packet_v1', inputs=data,
        contents={k: v.hex() for k, v in ops.contents.items()},
        observed=copy.deepcopy(ops.observed), roots=copy.deepcopy(ops.roots))


def expectations(value):
    """Caller freezes these independently of child results; not authentication."""
    return dict(expectation_sha256=core._hash(value['inputs']['expectation']),
        package_sha256=core._hash(value['inputs']['package']),
        root_sha256={k: core._hash(v) for k, v in value['roots'].items()})


def unpack(value, fixed, source_buffers, review_sha256):
    core._shape(value, ('schema', 'inputs', 'contents', 'observed', 'roots'))
    subject.need(value['schema'] == 'invented_dependency_packet_v1', 'invented_only')
    core._shape(fixed, ('expectation_sha256', 'package_sha256', 'root_sha256'))
    subject.need(core._canonical(expectations(value)) == core._canonical(fixed), 'fixed_expectations')
    data = value['inputs']
    core._shape(data, ('expectation', 'package', 'binding', 'config_json', 'cache_json'))
    subject.need(data['binding']['review_sha256'] == review_sha256, 'review_binding')
    policy, _, _, config, _ = subject.bind_inputs(**data, source_buffers=source_buffers)
    contents = {k: bytes.fromhex(v) for k, v in value['contents'].items()}
    paths = {subject.target(policy, row) for group in ('python_origins', 'native_libraries', 'trusted_origins')
             for row in policy[group].values()}
    core._shape(contents, paths); core._shape(value['observed'], paths)
    core._shape(value['roots'], policy['roots'])
    for group in ('python_origins', 'native_libraries', 'trusted_origins'):
        for row in policy[group].values():
            path = subject.target(policy, row)
            subject.need(subject.sha(contents[path]) == row['sha256'] and len(contents[path]) == row['size'], 'invented_bytes')
            core._receipt(value['observed'][path], path, row['sha256'], row['size'], row['identity'])
    for name, row in policy['roots'].items():
        subject.need(core._hash(value['roots'][name]) == row['identity_sha256'], 'root_identity')
    return dict(data, source_buffers=source_buffers), FakeOps(policy, contents, value['observed'], value['roots'], config['vectors'])


ARTIFACTS = ('expectation.json', 'binding.json', 'journal.jsonl', 'raw.json',
             'audit-acknowledgement.json', 'result.json')


def validate_saved(folder, value, fixed, source_buffers, review_sha256):
    """Recompute the pure contract from newly saved ordinary invented records."""
    from pathlib import Path
    data, _ = unpack(value, fixed, source_buffers, review_sha256)
    raw = {name: subject.read_verified(str(Path(folder)/name), limit=4*1024**2)[0] for name in ARTIFACTS}
    rows = {name: core._json_text(buf.decode('utf-8')) for name, buf in raw.items() if name != 'journal.jsonl'}
    result = rows['result.json']
    core._shape(result, ('schema', 'status', 'observation', 'consistency', 'source_execution_trace',
        'test_injection_used', 'audit_hook_retained_inert', 'audit_hook_acknowledged',
        'audit_acknowledgement_is_invented', 'source_buffers_are_caller_supplied',
        'executing_producer_authenticated', 'prior_binding_is_caller_declaration',
        'operational_acceptance', 'execution_authorized', 'feature_supported', 'recovery_proven',
        'device_write_gate_passed', 'camera_commands'))
    expected = dict(result)
    expected.update(schema='prospective_dependency_producer_result_v1', status='produced_consistent_dependency_records',
        test_injection_used=True, audit_hook_retained_inert=True, audit_hook_acknowledged=True,
        audit_acknowledgement_is_invented=True, source_buffers_are_caller_supplied=True,
        executing_producer_authenticated=False, prior_binding_is_caller_declaration=True,
        operational_acceptance=False, execution_authorized=False, feature_supported=False,
        recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    subject.need(core._canonical(result) == core._canonical(expected), 'invented_result_flags')
    subject.need(core._canonical(rows['expectation.json']) == core._canonical(data['expectation']) and
                 core._canonical(rows['binding.json']) == core._canonical(data['binding']), 'saved_binding')
    subject.need(result['observation']['evidence_mode'] == 'invented', 'invented_only')
    consistency = core.validate_dependency_records(expectation=data['expectation'], package=data['package'],
        observation=result['observation'], raw_receipt_json=raw['raw.json'].decode('utf-8'),
        journal_jsonl=raw['journal.jsonl'].decode('utf-8'))
    subject.need(core._canonical(consistency) == core._canonical(result['consistency']), 'saved_consistency')
    trace = result['source_execution_trace']; starts = {}; ends = {}; stack = []
    subject.need(type(trace) is list and len(trace) == 22, 'source_trace')
    for row in trace:
        core._shape(row, ('alias', 'stage', 'sha256'))
        alias = row['alias']; subject.need(alias in data['expectation']['python_origins'], 'source_trace')
        subject.need(row['sha256'] == data['expectation']['python_origins'][alias]['sha256'], 'source_trace')
        if row['stage'] == 'source_execute_intent':
            subject.need(alias not in starts, 'source_trace'); starts[alias] = row; stack.append(alias)
        else:
            subject.need(row['stage'] == 'source_execute_complete' and alias in starts and alias not in ends, 'source_trace')
            subject.need(stack and stack[-1] == alias, 'source_trace'); stack.pop(); ends[alias] = row
    subject.need(not stack and set(starts) == set(ends) == set(subject.ALIASES), 'source_trace')
    imports = [row['data']['alias'] for row in result['observation']['events'] if row['event'] == 'python_import']
    subject.need(list(ends) == imports, 'source_trace_order')
    ack = rows['audit-acknowledgement.json']
    core._shape(ack, ('schema', 'operation_id', 'probe_event', 'probe_token', 'acknowledged', 'test_injection_used'))
    subject.need(type(ack['probe_token']) is str and len(ack['probe_token']) == 32 and
                 all(c in '0123456789abcdef' for c in ack['probe_token']), 'audit_token')
    expected_ack = dict(schema='dependency_audit_acknowledgement_v1', operation_id=data['expectation']['operation_id'],
        probe_event=subject.PROBE_EVENT, probe_token=ack['probe_token'], acknowledged=True, test_injection_used=True)
    subject.need(core._canonical(ack) == core._canonical(expected_ack), 'audit_acknowledgement')
    return {name: subject.sha(buf) for name, buf in raw.items()}


def execute(value, fixed, source_buffers, review_sha256, folder):
    """Real Python audit delivery, invented reader/loader/cipher, one callback."""
    data, ops = unpack(value, fixed, source_buffers, review_sha256)
    subject.need(HELPER not in sys.modules and 'ctypes' not in sys.modules, 'preloaded_invented_helper')
    helper = types.ModuleType(HELPER); helper.new = ops.new
    sys.modules[HELPER] = helper; sys.modules['ctypes'] = ops.modules['ctypes']
    # Keep the installed audit hook in a disposable child. Native events are
    # manual sys.audit calls; FakeOps.load never invokes an OS loader.
    def install(hook):
        sys.addaudithook(hook)
        ops.hook = lambda event, args: sys.audit(event, *args)
    ops.audit_install = install
    primary = None
    try:
        subject.produce_invented(**data, ops=ops, folder=folder)
    except BaseException as error:
        primary = error
    finally:
        for alias, module in ((HELPER, helper), ('ctypes', ops.modules['ctypes'])):
            try:
                subject.need(sys.modules.get(alias) is module, 'invented_cleanup_ownership')
                del sys.modules[alias]
            except BaseException as error:
                if primary is None: primary = error
    if primary is not None: raise primary
    subject.need((ops.loader_calls, ops.callback_calls, ops.cipher_calls) == (5, 1, 48), 'invented_counts')
    subject.need(not any(n == 'Cryptodome' or n.startswith('Cryptodome.') for n in sys.modules), 'invented_cleanup')
    sys.audit(subject.PROBE_EVENT, 'inert_after_cleanup')
    sys.audit('ctypes.dlopen', 'inert_after_cleanup')
    return validate_saved(folder, value, fixed, source_buffers, review_sha256)
