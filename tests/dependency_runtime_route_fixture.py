"""Generate one labelled synthetic constructor owner for the runtime route.

The generated helper leaves dispatch, collection, controller, producer, saved
verification and the original RuntimeOps class unchanged.  Only the child
producer module's RuntimeOps constructor binding is temporarily replaced.  Its
replacement returns the exact authored FakeOps implementation over fresh inert
package bytes and public-vector lookups; it never imports an installed package
or invokes a real native loader.  Runtime-shaped saved fields are grammar under
this test composition, not evidence of actual dependency activation.
"""
import ast
import json
import textwrap

from dependency_child_runtime_fixture import _source_buffers


MODES = ('complete', 'constructor_error', 'reader_error', 'native_intent', 'preloaded')


def route_fixture_source(mode='complete'):
    """Return child helper source; generation builds only invented fixture data.

    ``native_intent`` asks the genuine guard's wrapper to load an unlisted
    invented path once that wrapper exists.  The unchanged guard must refuse
    before it can delegate to FakeOps.load.  ``preloaded`` deliberately owns one
    inert platform alias at installation, so the genuine pre-constructor check
    must refuse without constructing an observer.
    """
    if type(mode) is not str or mode not in MODES:
        raise ValueError('synthetic_runtime_route_mode')
    sources = _source_buffers()
    from test_dependency_package_preflight import complete_fixture
    _, ops = complete_fixture()
    package = dict(contents={name: raw.hex() for name, raw in ops.contents.items()},
                   observed=ops.observed, roots=ops.roots, vectors=ops.vectors)
    encoded = json.dumps(package, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=True, allow_nan=False)
    invented = sources['tools/dependency_invented.py'].decode('utf-8')
    matches = [node for node in ast.parse(invented).body
               if isinstance(node, ast.ClassDef) and node.name == 'FakeOps']
    if len(matches) != 1:
        raise AssertionError('synthetic_runtime_route_fake_ops')
    fake_ops = ast.get_source_segment(invented, matches[0])
    if not fake_ops:
        raise AssertionError('synthetic_runtime_route_fake_ops_source')
    prefix = (
        '# Separate synthetic RuntimeOps constructor qualification owner.\n'
        'import copy\nimport json\nimport sys\nimport types\n'
        '_SYNTHETIC_ROUTE_MODE = ' + repr(mode) + '\n'
        '_SYNTHETIC_ROUTE_PACKAGE = ' + repr(encoded) + '\n\n'
        'def _synthetic_route_ops(package, inputs):\n'
        '    subject = package.dependency_producer\n'
        '    core = package.dependency_evidence\n' +
        textwrap.indent(fake_ops, '    ') + '\n'
        '    value = json.loads(_SYNTHETIC_ROUTE_PACKAGE)\n'
        '    vectors = json.loads(inputs["config_json"])["vectors"]\n'
        '    if vectors != value["vectors"]:\n'
        '        raise ValueError("synthetic_runtime_route_vectors")\n'
        '    return FakeOps(inputs["expectation"],\n'
        '        {name: bytes.fromhex(raw) for name, raw in value["contents"].items()},\n'
        '        value["observed"], value["roots"], vectors)\n'
    )
    owner = r'''

class _SyntheticRuntimeOwner:
    """Child-only trusted test owner; no runtime or source authority granted."""
    FORBIDDEN = ('ctypes', '_ctypes', 'platform', 'cffi', '_cffi_backend',
                 'pycparser', 'Cryptodome')

    def __init__(self, helpers, inputs):
        if helpers.mode != 'child':
            raise ValueError('synthetic_runtime_route_child_only')
        helpers.intact()
        self.helpers = helpers
        self.package = helpers.package
        self.producer = self.package.dependency_producer
        self.inputs = inputs
        self.mode = _SYNTHETIC_ROUTE_MODE
        self.original_class = self.producer.RuntimeOps
        self.original_class_members = dict(vars(self.original_class))
        self.original_functions = {name: getattr(self.producer, name)
            for name in ('_produce', 'bind_inputs', 'Guard', 'Sources', 'run_vectors')}
        self.ops = None
        self.owned_aliases = []
        self.constructor_calls = 0
        self.native_intent_requests = 0
        self.install_attempts = self.close_attempts = 0
        self.installed = self.closed = False
        self.constructor_roots = None
        self.failure_stage = None
        self.cleanup_errors = []

        def constructor():
            self.constructor_calls += 1
            self.failure_stage = 'constructor_entry'
            roots = sorted({name.split('.')[0] for name in sys.modules
                            if name.split('.')[0] in self.FORBIDDEN})
            self.constructor_roots = roots
            if roots or self.constructor_calls != 1 or not self._original_intact():
                raise ValueError('synthetic_runtime_route_constructor_boundary')
            if self.mode == 'constructor_error':
                self.failure_stage = 'constructor_error'
                raise OSError('synthetic_runtime_constructor_error')
            self.ops = _synthetic_route_ops(self.package, self.inputs)
            if self.mode == 'reader_error':
                def fail_read(ops, path):
                    self.failure_stage = 'reader_error'
                    raise OSError('synthetic_runtime_reader_error')
                self.ops.read_action = fail_read
            elif self.mode == 'native_intent':
                def native_intent(ops, path):
                    backend = ops.modules['ctypes']
                    if backend.CDLL is not ops.original:
                        self.native_intent_requests += 1
                        self.failure_stage = 'native_intent'
                        # This invokes only the genuine guard wrapper around
                        # fake ctypes. It must reject this unlisted path before
                        # delegating to the inert FakeOps.load implementation.
                        backend.CDLL('Z:/invented-unlisted-native.bin',
                                     **ops.policy['loader_kwargs'])
                        raise AssertionError('synthetic_runtime_native_intent_accepted')
                self.ops.read_action = native_intent
            helper = types.ModuleType('_invented_dependency_probe')
            helper.new = self.ops.new
            self._own_alias('_invented_dependency_probe', helper)
            self._own_alias('ctypes', self.ops.modules['ctypes'])
            self.failure_stage = None
            return self.ops
        self.constructor = constructor

    def _original_intact(self):
        return (set(vars(self.original_class)) == set(self.original_class_members) and
                all(vars(self.original_class).get(name) is value
                    for name, value in self.original_class_members.items()) and
                all(getattr(self.producer, name, None) is value
                    for name, value in self.original_functions.items()))

    def _own_alias(self, name, module):
        if name in sys.modules:
            raise ValueError('synthetic_runtime_route_alias_preloaded')
        sys.modules[name] = module
        self.owned_aliases.append((name, module))

    def install(self):
        self.install_attempts += 1
        if (self.install_attempts != 1 or self.closed or self.installed or
                self.producer.RuntimeOps is not self.original_class or
                not self._original_intact()):
            raise ValueError('synthetic_runtime_route_install')
        self.helpers.intact()
        self.producer.RuntimeOps = self.constructor
        self.installed = True
        if self.mode == 'preloaded':
            self._own_alias('platform', types.ModuleType('platform'))

    def close(self):
        self.close_attempts += 1
        if self.close_attempts != 1:
            raise ValueError('synthetic_runtime_route_close_reentry')
        self.closed = True
        # Each owned binding is reconciled independently. Foreign replacements
        # are preserved and reported; a failure never skips another release.
        if self.installed:
            if self.producer.RuntimeOps is self.constructor:
                self.producer.RuntimeOps = self.original_class
            else:
                self.cleanup_errors.append('constructor_ownership')
        for name, module in reversed(self.owned_aliases):
            if sys.modules.get(name) is module:
                del sys.modules[name]
            else:
                self.cleanup_errors.append('alias_ownership:' + name)
        if not self._original_intact():
            self.cleanup_errors.append('original_source_binding_ownership')
        if self.cleanup_errors:
            raise ValueError('synthetic_runtime_route_cleanup_ownership')

    def observation(self):
        ops = self.ops
        policy = self.inputs['expectation']
        source_paths = {self.producer.target(policy, row)
                        for row in policy['python_origins'].values()}
        trusted_paths = {self.producer.target(policy, row)
                         for row in policy['trusted_origins'].values()}
        native_paths = {self.producer.target(policy, row)
                        for row in policy['native_libraries'].values()}
        reads = [] if ops is None else list(ops.reads)
        return dict(schema='synthetic_runtime_route_observation_v1',
            mode=self.mode, constructor_replacement_is_synthetic=True,
            install_attempts=self.install_attempts, close_attempts=self.close_attempts,
            constructor_calls=self.constructor_calls, constructor_preloaded_roots=self.constructor_roots,
            original_class_restored=self.producer.RuntimeOps is self.original_class,
            original_class_and_producer_functions_intact=self._original_intact(),
            installed=self.installed, closed=self.closed,
            fake_reads=len(reads), fake_source_reads=sum(path in source_paths for path in reads),
            fake_trusted_reads=sum(path in trusted_paths for path in reads),
            fake_native_reads=sum(path in native_paths for path in reads),
            fake_root_calls=0 if ops is None else ops.root_calls,
            fake_loader_calls=0 if ops is None else ops.loader_calls,
            fake_cipher_calls=0 if ops is None else ops.cipher_calls,
            fake_callback_calls=0 if ops is None else ops.callback_calls,
            native_intent_requests=self.native_intent_requests,
            fake_loader_restored=ops is None or ops.modules['ctypes'].CDLL is ops.original,
            live_owned_aliases=[name for name, module in self.owned_aliases
                                if sys.modules.get(name) is module],
            foreign_alias_replacements=[name for name, module in self.owned_aliases
                if name in sys.modules and sys.modules[name] is not module],
            cleanup_errors=list(self.cleanup_errors), failure_stage=self.failure_stage,
            no_real_native_or_package=True, actual_dependency_observation_performed=False,
            runtime_shaped_saved_fields_are_synthetic=True,
            execution_authorized=False, feature_supported=False, recovery_proven=False,
            device_write_gate_passed=False, camera_commands=[])
'''
    return (prefix + owner).encode('utf-8')
