"""Genuine RuntimeOps startup/callback and Python guard-probe delivery.

Generated child-only instance shims delegate to unchanged original class methods
over the existing invented-files composition. Bootstrap/native loading/vector
cipher/protected processing stay inert. Python audit hooks cannot be removed;
the diagnostic observer, optional suppressor and original guard are retained
inert until the disposable process exits. Nothing here emits ctypes audit events.
"""
from dependency_filesystem_runtime_fixture import filesystem_runtime_source


MODES = ('complete', 'suppressed_install', 'missing_probe', 'wrong_probe',
         'duplicate_probe', 'swallowed_probe', 'install_error', 'probe_error')


def audit_runtime_source(mode='complete'):
    """Return separately labelled child source without replacing runtime engines."""
    if type(mode) is not str or mode not in MODES:
        raise ValueError('synthetic_audit_runtime_mode')
    raw = filesystem_runtime_source('complete')
    old = b'            _install_filesystem_observer(self)'
    if raw.count(old) != 1:
        raise AssertionError('synthetic audit filesystem constructor drift')
    raw = raw.replace(old, old + b'\n            _install_audit_runtime(self)')
    suffix = rb'''

def _audit_guard_state(owner):
    guard = getattr(owner, 'audit_guard', None)
    if guard is None:
        return None
    return dict(active=guard.active, finished=guard.finished, failed=guard.failed,
                bootstrap=guard.bootstrap, probe_count=guard.probe_count)


def _install_audit_runtime(owner):
    ops = owner.ops
    owner.audit_original_methods = {name: getattr(owner.original_class, name)
        for name in ('startup', 'audit_install', 'audit_probe', 'callback')}
    owner.audit_initialized = True
    owner.audit_guard = None
    owner.audit_startup_calls = owner.audit_startup_delegations = 0
    owner.audit_startup_returns = 0
    owner.audit_startup_value = None
    owner.audit_install_calls = owner.audit_install_delegations = 0
    owner.audit_install_returns = 0
    owner.audit_probe_calls = owner.audit_probe_delegations = 0
    owner.audit_probe_returns = owner.audit_probe_delegate_returns = 0
    owner.audit_callback_calls = owner.audit_callback_delegations = 0
    owner.audit_callback_returns = 0
    owner.audit_install_events = []
    owner.audit_probe_events = []
    owner.audit_startup_events = []
    owner.audit_callback_events = []
    owner.audit_probe_monitor = []
    owner.audit_observer_install_attempts = owner.audit_observer_install_returns = 0
    owner.audit_observer_enabled = True
    owner.audit_suppressor_installed = False
    owner.audit_suppression_enabled = False
    owner.audit_suppression_count = 0
    owner.audit_phase = 'production'
    owner.audit_guard_final = None
    owner.audit_after_cleanup_probe = dict(attempts=0, delegations=0, returned=False,
        count_before=None, count_after=None, count_unchanged=False,
        error_type=None, error_code=None)

    def observer(event, args):
        # Passive independent observer: filter this one probe event, record no
        # token value, never mutate the guard and never deliberately raise.
        if not owner.audit_observer_enabled or event != owner.producer.PROBE_EVENT:
            return
        guard = owner.audit_guard
        owner.audit_probe_monitor.append(dict(phase=owner.audit_phase,
            count_before=None if guard is None else guard.probe_count,
            active=None if guard is None else guard.active,
            finished=None if guard is None else guard.finished,
            failed=None if guard is None else guard.failed,
            bootstrap=None if guard is None else guard.bootstrap,
            token_matches=guard is not None and args == (guard.probe_token,)))
    owner.audit_observer = observer
    owner.audit_observer_install_attempts += 1
    sys.addaudithook(observer)
    owner.audit_observer_install_returns += 1

    if _AUDIT_MODE == 'suppressed_install':
        def suppressor(event, args):
            if owner.audit_suppression_enabled and event == 'sys.addaudithook':
                owner.audit_suppression_count += 1
                # CPython suppresses RuntimeError from an existing audit hook
                # during registration. The original method still returns, but
                # the producer must reject the missing guard acknowledgement.
                raise RuntimeError('synthetic_audit_registration_suppressed')
        owner.audit_suppressor = suppressor
        sys.addaudithook(suppressor)
        owner.audit_suppressor_installed = True
        owner.audit_suppression_enabled = True

    def startup():
        owner.audit_startup_calls += 1
        event = dict(returned=False)
        owner.audit_startup_events.append(event)
        try:
            owner.audit_startup_delegations += 1
            value = owner.audit_original_methods['startup'](ops)
        except BaseException as error:
            event.update(error_type=type(error).__name__, error_code=str(error))
            raise
        owner.audit_startup_value = copy.deepcopy(value)
        owner.audit_startup_returns += 1
        event['returned'] = True
        return value

    def audit_install(hook):
        owner.audit_install_calls += 1
        event = dict(returned=False, delegated=False)
        owner.audit_install_events.append(event)
        # Preserve the exact bound original guard hook for the existing fake
        # loader's direct simulated native events. No real native event is sent.
        ops.hook = hook
        owner.audit_guard = hook.__self__
        try:
            if _AUDIT_MODE == 'install_error':
                raise OSError('synthetic_audit_install_error')
            owner.audit_install_delegations += 1
            event['delegated'] = True
            owner.audit_original_methods['audit_install'](ops, hook)
        except BaseException as error:
            event.update(error_type=type(error).__name__, error_code=str(error))
            raise
        owner.audit_install_returns += 1
        event['returned'] = True

    def original_probe(token, kind, swallowed=False):
        # Production delegations and cleanup proof are counted separately.
        owner.audit_probe_delegations += 1
        event = dict(kind=kind, returned=False, swallowed=False)
        owner.audit_probe_events.append(event)
        try:
            owner.audit_original_methods['audit_probe'](ops, token)
        except BaseException as error:
            event.update(error_type=type(error).__name__, error_code=str(error),
                         swallowed=swallowed)
            raise
        owner.audit_probe_delegate_returns += 1
        event['returned'] = True

    def audit_probe(token):
        owner.audit_probe_calls += 1
        if _AUDIT_MODE == 'probe_error':
            owner.audit_probe_events.append(dict(kind='before_delegation',
                returned=False, swallowed=False, error_type='OSError',
                error_code='synthetic_audit_probe_error'))
            raise OSError('synthetic_audit_probe_error')
        if _AUDIT_MODE == 'missing_probe':
            owner.audit_probe_events.append(dict(kind='skipped', returned=True,
                                                 swallowed=False))
        elif _AUDIT_MODE == 'wrong_probe':
            original_probe('invented-wrong-probe', 'wrong')
        elif _AUDIT_MODE == 'duplicate_probe':
            original_probe(token, 'valid_first')
            original_probe(token, 'duplicate')
        elif _AUDIT_MODE == 'swallowed_probe':
            try:
                original_probe('invented-wrong-probe', 'wrong_swallowed', swallowed=True)
            except owner.producer.core.EvidenceError:
                pass
            original_probe(token, 'valid_after_swallowed')
        else:
            original_probe(token, 'valid')
        owner.audit_probe_returns += 1

    def callback(AES, vectors):
        owner.audit_callback_calls += 1
        ops.callback_calls += 1
        event = dict(returned=False)
        owner.audit_callback_events.append(event)
        try:
            owner.audit_callback_delegations += 1
            owner.audit_original_methods['callback'](ops, AES, vectors)
        except BaseException as error:
            event.update(error_type=type(error).__name__, error_code=str(error))
            raise
        owner.audit_callback_returns += 1
        event['returned'] = True

    ops.startup = startup
    ops.audit_install = audit_install
    ops.audit_probe = audit_probe
    ops.callback = callback


def _audit_after_cleanup(owner):
    if not getattr(owner, 'audit_initialized', False):
        return
    owner.audit_suppression_enabled = False
    owner.audit_phase = 'after_cleanup'
    result = owner.audit_after_cleanup_probe
    try:
        owner.audit_guard_final = _audit_guard_state(owner)
        guard = owner.audit_guard
        if guard is None:
            raise ValueError('synthetic_audit_cleanup_guard_missing')
        result['count_before'] = guard.probe_count
        if guard.active is not False or guard.finished is not True:
            raise ValueError('synthetic_audit_cleanup_guard_live')
        result['attempts'] += 1
        result['delegations'] += 1
        # Call the genuine original method directly, never the injection shim.
        owner.audit_original_methods['audit_probe'](owner.ops, 'invented-after-cleanup')
        result['returned'] = True
        result['count_after'] = guard.probe_count
        result['count_unchanged'] = result['count_before'] == result['count_after']
        if not result['count_unchanged']:
            raise ValueError('synthetic_audit_cleanup_probe_changed')
    except BaseException as error:
        result.update(error_type=type(error).__name__, error_code=str(error))
        owner.cleanup_errors.append('audit_after_cleanup:' + type(error).__name__ + ':' + str(error))
    finally:
        # Hooks remain registered until process exit. Disabled observation and
        # suppression plus the inactive guard are never described as removal.
        owner.audit_observer_enabled = False


_AUDIT_BASE_OWNER_CLOSE = _SyntheticRuntimeOwner.close


def _audit_owner_close(owner):
    primary = None
    answer = None
    try:
        answer = _AUDIT_BASE_OWNER_CLOSE(owner)
    except BaseException as error:
        primary = error
    finally:
        _audit_after_cleanup(owner)
    if primary is not None:
        raise primary
    if owner.cleanup_errors:
        raise ValueError('synthetic_audit_cleanup_ownership')
    return answer


def _audit_observation(owner):
    methods = getattr(owner, 'audit_original_methods', {})
    intact = bool(methods) and all(getattr(owner.original_class, name, None) is value
                                  for name, value in methods.items())
    return dict(schema='synthetic_audit_runtime_observation_v1', mode=_AUDIT_MODE,
        original_startup_delegated=owner.audit_startup_delegations > 0,
        original_audit_install_delegated=owner.audit_install_delegations > 0,
        original_audit_probe_delegated=owner.audit_probe_delegations > 0,
        original_callback_delegated=owner.audit_callback_delegations > 0,
        original_methods_intact=intact,
        startup_calls=owner.audit_startup_calls,
        startup_delegations=owner.audit_startup_delegations,
        startup_returns=owner.audit_startup_returns,
        startup_value=copy.deepcopy(owner.audit_startup_value),
        startup_events=copy.deepcopy(owner.audit_startup_events),
        install_calls=owner.audit_install_calls,
        install_delegations=owner.audit_install_delegations,
        install_returns=owner.audit_install_returns,
        install_events=copy.deepcopy(owner.audit_install_events),
        probe_calls=owner.audit_probe_calls,
        probe_delegations=owner.audit_probe_delegations,
        probe_returns=owner.audit_probe_returns,
        probe_delegate_returns=owner.audit_probe_delegate_returns,
        probe_events=copy.deepcopy(owner.audit_probe_events),
        callback_calls=owner.audit_callback_calls,
        callback_delegations=owner.audit_callback_delegations,
        callback_returns=owner.audit_callback_returns,
        callback_events=copy.deepcopy(owner.audit_callback_events),
        observer_install_attempts=owner.audit_observer_install_attempts,
        observer_install_returns=owner.audit_observer_install_returns,
        observer_enabled=owner.audit_observer_enabled,
        observer_retained_inert=(owner.audit_observer_install_returns == 1 and
                                 not owner.audit_observer_enabled),
        suppression_count=owner.audit_suppression_count,
        suppression_enabled=owner.audit_suppression_enabled,
        suppressor_installed=owner.audit_suppressor_installed,
        suppressor_retained_inert=(owner.audit_suppressor_installed and
                                  not owner.audit_suppression_enabled),
        probe_monitor=copy.deepcopy(owner.audit_probe_monitor),
        guard_final=copy.deepcopy(owner.audit_guard_final),
        after_cleanup_probe=copy.deepcopy(owner.audit_after_cleanup_probe),
        hooks_removed=False, native_audit_delivery_is_direct_simulation=True,
        bootstrap_is_inert=True, vector_cipher_is_lookup=True,
        cleanup_errors=list(owner.cleanup_errors),
        installed_dependency_observed=False, native_execution_performed=False,
        real_cryptography_performed=False, actual_runtime_verified=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


_SyntheticRuntimeOwner.close = _audit_owner_close
_SyntheticRuntimeOwner.audit_observation = _audit_observation
'''
    return raw + b'\n_AUDIT_MODE=' + repr(mode).encode('ascii') + b'\n' + suffix
