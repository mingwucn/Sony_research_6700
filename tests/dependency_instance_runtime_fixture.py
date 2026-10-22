"""Exact original RuntimeOps instances with an explicit inert adapter.

Generated code retains genuine host-method delegation over the existing invented
files, audit probes and preparation/parent path. The original bootstrap method
uses a scoped inert import adapter; native events and vector ciphers stay doubles.
The child has no FakeOps observer, source function, inherited observer or byte/
receipt fallback. No installed dependency or executable native input is used.
"""
import ast

from dependency_audit_runtime_fixture import audit_runtime_source


MODES = ('complete', 'bootstrap_error', 'missing_module', 'wrong_origin',
         'wrong_cipher', 'callback_error', 'missing_native_audit', 'callback_cipher',
         'foreign_importlib')


def _drop_captured_fake(source):
    """Remove the old captured observer and its unused package literal by span."""
    tree = ast.parse(source)
    roots = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == '_synthetic_route_ops') or
             (isinstance(node, ast.Assign) and len(node.targets) == 1 and
              isinstance(node.targets[0], ast.Name) and
              node.targets[0].id == '_SYNTHETIC_ROUTE_PACKAGE')]
    if len(roots) != 2:
        raise AssertionError('synthetic instance captured observer source drift')
    owners = [node for node in tree.body if isinstance(node, ast.ClassDef) and
              node.name == '_SyntheticRuntimeOwner']
    if len(owners) != 1:
        raise AssertionError('synthetic instance owner source drift')
    init = next(node for node in owners[0].body
                if isinstance(node, ast.FunctionDef) and node.name == '__init__')
    constructor = next(node for node in init.body
                       if isinstance(node, ast.FunctionDef) and node.name == 'constructor')
    # These historical constructor-fault branches belong to the old FakeOps
    # composition. New instance faults live solely in the explicit adapter.
    faults = [node for node in constructor.body if isinstance(node, ast.If) and
              isinstance(node.test, ast.Compare) and
              isinstance(node.test.left, ast.Attribute) and
              isinstance(node.test.left.value, ast.Name) and
              node.test.left.value.id == 'self' and node.test.left.attr == 'mode' and
              len(node.test.comparators) == 1 and
              isinstance(node.test.comparators[0], ast.Constant) and
              node.test.comparators[0].value in ('constructor_error', 'reader_error')]
    if len(faults) != 2:
        raise AssertionError('synthetic instance historical fault source drift')
    lines = source.splitlines(keepends=True)
    for node in sorted(roots + faults, key=lambda item: item.lineno, reverse=True):
        lines[node.lineno - 1:node.end_lineno] = []
    return ''.join(lines)


def instance_runtime_source(mode='complete'):
    """Generate child-only composition without executing any generated code."""
    if type(mode) is not str or mode not in MODES:
        raise ValueError('synthetic_instance_runtime_mode')
    source = _drop_captured_fake(audit_runtime_source('complete').decode('utf-8'))
    replacements = (
        ('            self.ops = _synthetic_route_ops(self.package, self.inputs)',
         '            self.ops = self.original_class()\n'
         '            self.adapter = _InertRuntimeAdapter(self)\n'
         '            self.ops.bootstrap = self.adapter.bootstrap'),
        ('helper.new = self.ops.new', 'helper.new = self.adapter.new'),
        ("self._own_alias('ctypes', self.ops.modules['ctypes'])",
         "self._own_alias('ctypes', self.adapter.modules['ctypes'])"),
        ('    def observation(self):\n        ops = self.ops',
         '    def observation(self):\n        ops = None if self.ops is None else self.adapter'),
        (' # Remove all fallback bytes/receipts. Every observer read must delegate to the\n'
         ' # exact original class method on a newly authored file, never FakeOps.reader.\n'
         ' ops.contents=ops.observed=ops.roots=None',
         ' # Original instance has no byte/receipt fallback attributes.'),
        ('ops.reads.append(path)', 'owner.adapter.reads.append(path)'),
        ('ops.root_calls+=1', 'owner.adapter.root_calls+=1'),
        ('        ops.hook = hook', '        owner.adapter.hook = hook'),
        ('        ops.callback_calls += 1', '        owner.adapter.callback_calls += 1'),
        ('owner.ops is not None and owner.ops.contents is owner.ops.observed is owner.ops.roots is None',
         "owner.ops is not None and not any(hasattr(owner.ops, name) for name in ('contents','observed','roots'))"),
        ('owner.filesystem_original_reader(ops,path,row)',
         "_instance_original_call(owner,'reader',path,row)"),
        ('owner.filesystem_original_root(ops,path)',
         "_instance_original_call(owner,'root',path)"),
        ("owner.audit_original_methods['startup'](ops)",
         "_instance_original_call(owner, 'startup')"),
        ("owner.audit_original_methods['audit_install'](ops, hook)",
         "_instance_original_call(owner, 'audit_install', hook)"),
        ("owner.audit_original_methods['audit_probe'](ops, token)",
         "_instance_original_call(owner, 'audit_probe', token)"),
        ("owner.audit_original_methods['callback'](ops, AES, vectors)",
         "_instance_original_call(owner, 'callback', AES, vectors)"),
        ("owner.audit_original_methods['audit_probe'](owner.ops, 'invented-after-cleanup')",
         "_instance_original_call(owner, 'audit_probe', 'invented-after-cleanup')"),
        ('            owner.audit_callback_delegations += 1',
         "            if _INSTANCE_MODE == 'callback_error':\n"
         "                raise OSError('synthetic_instance_callback_error')\n"
         '            owner.audit_callback_delegations += 1'),
    )
    for before, after in replacements:
        if source.count(before) != 1:
            raise AssertionError('synthetic instance instrumentation source drift')
        source = source.replace(before, after)
    suffix = r'''

_INSTANCE_TRUSTED = ('ctypes', '_ctypes', 'ctypes.util', 'ctypes._endian', 'platform')


class _InertRuntimeAdapter:
    """Inert import/native/cipher adapter; never an observer subclass."""
    def __init__(self, owner):
        self.owner = owner
        self.policy = owner.inputs['expectation']
        self.vectors = json.loads(owner.inputs['config_json'])['vectors']
        self.reads = []
        self.root_calls = self.callback_calls = 0
        self.loader_calls = self.cipher_calls = 0
        self.bootstrap_calls = self.bootstrap_returns = 0
        self.bootstrap_imports = []
        self.bootstrap_import_origins = {}
        self.bootstrap_import_active = False
        self.importlib_original = owner.producer.importlib
        self.importlib_installs = 0
        self.importlib_restored = False
        self.importlib_foreign = None
        self.importlib_foreign_preserved = False
        self.package_continuation_importlib_checks = 0
        self.direct_native_audit_calls = self.skipped_native_audit_calls = 0
        self.corrupted_cipher_lookups = 0
        self.cipher_fault_stage = None
        self.callback_entered = self.callback_active = False
        self.callback_state = 'not_entered'
        self.hook = None
        self.modules = {}
        self.original_methods = {name: getattr(owner.original_class, name)
            for name in ('reader', 'root', 'startup', 'audit_install', 'audit_probe',
                         'callback', 'bootstrap')}
        self.original_delegations = []
        for name, row in self.policy['trusted_origins'].items():
            module = types.ModuleType(name)
            module.__file__ = owner.producer.target(self.policy, row)
            self.modules[name] = module
        self.original = self.load
        self.modules['ctypes'].CDLL = self.original

    def bootstrap(self):
        self.bootstrap_calls += 1
        if (self.bootstrap_calls != 1 or tuple(self.owner.producer.TRUSTED) != _INSTANCE_TRUSTED or
                self.owner.producer.importlib is not self.importlib_original):
            raise ValueError('synthetic_instance_bootstrap_boundary')
        self.owner.producer.importlib = self
        self.importlib_installs += 1
        self.bootstrap_import_active = True
        try:
            # Invoke the exact unchanged class method on the observer already
            # used by the preparation/controller path. Only its module's
            # importlib binding is scoped; no real import or native event runs.
            value = _instance_original_call(self.owner, 'bootstrap')
            if tuple(self.bootstrap_imports) != _INSTANCE_TRUSTED:
                raise ValueError('synthetic_instance_bootstrap_import_roster')
            if _INSTANCE_MODE == 'missing_module':
                del value['platform']
            self.bootstrap_returns += 1
            return value
        finally:
            self.bootstrap_import_active = False
            if self.owner.producer.importlib is self:
                self.owner.producer.importlib = self.importlib_original
                self.importlib_restored = True
            else:
                # A foreign replacement is preserved. Do not clobber it in an
                # attempt to report successful cleanup or enter the packages.
                self.importlib_foreign_preserved = (
                    self.owner.producer.importlib is self.importlib_foreign)
                raise ValueError('synthetic_instance_importlib_ownership')

    def import_module(self, name):
        trusted = _INSTANCE_TRUSTED
        index = len(self.bootstrap_imports)
        if (not self.bootstrap_import_active or self.owner.producer.importlib is not self or
                index >= len(trusted) or type(name) is not str or name != trusted[index]):
            raise ValueError('synthetic_instance_bootstrap_import')
        self.bootstrap_imports.append(name)
        if _INSTANCE_MODE == 'bootstrap_error':
            raise OSError('synthetic_instance_bootstrap_error')
        module = self.modules[name]
        if _INSTANCE_MODE == 'wrong_origin' and name == 'platform':
            module.__file__ = 'Z:/invented-wrong-origin/platform.py'
        self.bootstrap_import_origins[name] = module.__file__
        if _INSTANCE_MODE == 'foreign_importlib' and name == trusted[-1]:
            self.importlib_foreign = types.SimpleNamespace(invented_foreign_importlib=True)
            self.owner.producer.importlib = self.importlib_foreign
        return module

    def load(self, path, **kwargs):
        if not self.importlib_restored or self.owner.producer.importlib is not self.importlib_original:
            raise ValueError('synthetic_instance_package_importlib_boundary')
        self.package_continuation_importlib_checks += 1
        self.loader_calls += 1
        if _INSTANCE_MODE == 'missing_native_audit':
            self.skipped_native_audit_calls += 1
        else:
            self.direct_native_audit_calls += 1
            # Exact guard hook only: no sys.audit/native loader/import call.
            self.hook('ctypes.dlopen', (path,))
        return object()

    def new(self, key, mode, **kwargs):
        self.cipher_calls += 1
        vector = next(value for value in self.vectors
                      if bytes.fromhex(value['key_hex']) == key and
                      (1 if value['mode'] == 'ECB' else 2) == mode)
        if mode == 2:
            assert kwargs['iv'] == bytes.fromhex(vector['iv_hex'])
        assert set(kwargs) <= {'iv', 'use_aesni'}
        plain = bytes.fromhex(vector['plaintext_hex'])
        cipher = bytes.fromhex(vector['ciphertext_hex'])
        corrupt = (self.corrupted_cipher_lookups == 0 and
            (_INSTANCE_MODE == 'wrong_cipher' or
             (_INSTANCE_MODE == 'callback_cipher' and self.callback_active)))
        if corrupt:
            self.corrupted_cipher_lookups += 1
            self.cipher_fault_stage = ('original_callback' if self.callback_active
                                       else 'producer_vectors')
            cipher = bytes([cipher[0] ^ 1]) + cipher[1:]
        class Cipher:
            def encrypt(self, value):
                assert value == plain
                return cipher
            def decrypt(self, value):
                assert value == cipher
                return plain
        return Cipher()


def _instance_original_call(owner, name, *args):
    adapter = owner.adapter
    method = adapter.original_methods[name]
    exact = (type(owner.ops) is owner.original_class and
             getattr(owner.original_class, name, None) is method)
    row = dict(method=name, phase=getattr(owner, 'audit_phase', 'construction'),
               bound_original_instance=exact, returned=False)
    adapter.original_delegations.append(row)
    if not exact:
        raise ValueError('synthetic_instance_original_method_boundary')
    if name == 'callback':
        adapter.callback_entered = adapter.callback_active = True
        adapter.callback_state = 'running'
    try:
        answer = method(owner.ops, *args)
    except BaseException as error:
        row.update(error_type=type(error).__name__, error_code=str(error))
        if name == 'callback':
            adapter.callback_state = 'failed'
        raise
    else:
        row['returned'] = True
        if name == 'callback':
            adapter.callback_state = 'complete'
        return answer
    finally:
        if name == 'callback':
            adapter.callback_active = False


def _instance_observation(owner):
    adapter = getattr(owner, 'adapter', None)
    ops = owner.ops
    expected = sorted(('reader', 'root', 'startup', 'audit_install', 'audit_probe',
                       'callback', 'bootstrap'))
    attributes = [] if ops is None else sorted(vars(ops))
    exact = ops is not None and type(ops) is owner.original_class
    delegates = [] if adapter is None else copy.deepcopy(adapter.original_delegations)
    return dict(schema='synthetic_instance_runtime_observation_v1', mode=_INSTANCE_MODE,
        exact_original_type=exact, no_class_inheritance=exact,
        no_custom_observer_subclass=exact, no_fake_ops_observer=exact,
        no_fallback_attributes=ops is not None and not any(hasattr(ops, name)
            for name in ('contents', 'observed', 'roots', 'reads', 'root_calls',
                         'callback_calls', 'hook', 'modules', 'new', 'load')),
        original_class_methods_intact=adapter is not None and all(
            getattr(owner.original_class, name, None) is method
            for name, method in adapter.original_methods.items()),
        ops_instance_attributes=attributes, expected_instance_attributes=expected,
        original_delegates_use_exact_instance=bool(delegates) and
            all(row['bound_original_instance'] for row in delegates),
        original_delegations=delegates,
        bootstrap_calls=0 if adapter is None else adapter.bootstrap_calls,
        bootstrap_returns=0 if adapter is None else adapter.bootstrap_returns,
        bootstrap_imports=[] if adapter is None else list(adapter.bootstrap_imports),
        bootstrap_import_origins={} if adapter is None else dict(adapter.bootstrap_import_origins),
        bootstrap_imports_are_simulated=True,
        bootstrap_import_adapter_installs=0 if adapter is None else adapter.importlib_installs,
        bootstrap_import_adapter_restored=adapter is not None and adapter.importlib_restored,
        bootstrap_import_adapter_active=adapter is not None and adapter.bootstrap_import_active,
        bootstrap_import_foreign_preserved=adapter is not None and adapter.importlib_foreign_preserved,
        package_continuation_importlib_checks=0 if adapter is None else adapter.package_continuation_importlib_checks,
        loader_calls=0 if adapter is None else adapter.loader_calls,
        direct_native_audit_calls=0 if adapter is None else adapter.direct_native_audit_calls,
        skipped_native_audit_calls=0 if adapter is None else adapter.skipped_native_audit_calls,
        cipher_calls=0 if adapter is None else adapter.cipher_calls,
        corrupted_cipher_lookups=0 if adapter is None else adapter.corrupted_cipher_lookups,
        cipher_fault_stage=None if adapter is None else adapter.cipher_fault_stage,
        callback_calls=0 if adapter is None else adapter.callback_calls,
        callback_entered=adapter is not None and adapter.callback_entered,
        callback_active=adapter is not None and adapter.callback_active,
        callback_state=None if adapter is None else adapter.callback_state,
        reads=0 if adapter is None else len(adapter.reads),
        root_calls=0 if adapter is None else adapter.root_calls,
        bootstrap_original_method_called=any(row['method']=='bootstrap' for row in delegates),
        bootstrap_original_method_returned=any(row['method']=='bootstrap' and row['returned'] for row in delegates),
        explicit_inert_adapter=True,
        native_events_are_direct_simulation=True, vector_cipher_is_lookup=True,
        constructor_binding_remains_synthetic=True, class_source_unchanged=True,
        installed_dependency_observed=False, native_execution_performed=False,
        real_cryptography_performed=False, actual_runtime_verified=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


_SyntheticRuntimeOwner.instance_observation = _instance_observation
'''
    source += '\n_INSTANCE_MODE=' + repr(mode) + '\n' + suffix
    tree = ast.parse(source)
    if any(isinstance(node, ast.ClassDef) and node.name == 'FakeOps' or
           isinstance(node, (ast.FunctionDef, ast.Name)) and
           getattr(node, 'name', getattr(node, 'id', None)) == '_synthetic_route_ops'
           for node in ast.walk(tree)):
        raise AssertionError('synthetic instance retained captured observer')
    return source.encode('utf-8')
