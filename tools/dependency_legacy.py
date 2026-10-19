"""Pure legacy receipt adapter; preserves original text, grants no authority.

No historical event is renamed into a new event, and no production loader or
saved-file reader is provided. Inputs must already be detached ordinary data.
"""
import hashlib

from tools import dependency_evidence as core


ALIASES = ('Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Cipher.AES',
    'Cryptodome.Cipher._mode_ecb', 'Cryptodome.Cipher._mode_cbc', 'Cryptodome.Random',
    'Cryptodome.Util', 'Cryptodome.Util._raw_api', 'Cryptodome.Util._cpu_features',
    'Cryptodome.Util._file_system', 'Cryptodome.Util.py3compat')
TRUSTED = ('ctypes', '_ctypes', 'ctypes.util', 'ctypes._endian', 'platform')
NATIVE = {'cpuid':'Util/_cpuid_c.pyd', 'aes':'Cipher/_raw_aes.pyd',
    'aesni':'Cipher/_raw_aesni.pyd', 'ecb':'Cipher/_raw_ecb.pyd', 'cbc':'Cipher/_raw_cbc.pyd'}
PACKAGES = ('Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Random', 'Cryptodome.Util')
TRUSTED_PATHS = {'ctypes':'Lib/ctypes/__init__.py', '_ctypes':'DLLs/_ctypes.pyd',
    'ctypes.util':'Lib/ctypes/util.py', 'ctypes._endian':'Lib/ctypes/_endian.py', 'platform':'Lib/platform.py'}
LIMITATIONS = ['Trusted stdlib and _ctypes initialization are not package guarded-load proof.',
    'Pre/post path hashes do not attest the OS-mapped bytes or all transitive DLLs.',
    'This -I -S startup does not qualify a legacy -I GDT entry.']
BLOCKERS = (
    'legacy_raw_is_not_successor_guard_transcript',
    'legacy_events_are_not_successor_event_grammar',
    'individual_durability_steps_not_journaled',
    'guard_install_and_finish_not_explicit_events',
    'cleanup_claim_not_journaled',
    'read_only_open_mode_not_explicit_in_legacy_receipts',
    'pre_execution_expectation_approval_unestablished',
    'producer_source_authority_not_bound',
    'source_cache_content_not_revalidated',
    'fresh_runtime_observation_not_performed',
)
PUBLIC_VECTOR_PLAN_SHA256 = 'a914aca415d20a87a56440f36944f7ac6082ecbc36387b68694175a579bc43b5'
RAW_KEYS = ('schema', 'status', 'operation_id', 'evidence_class', 'test_injection_used',
    'config_sha256', 'cache_sha256', 'source_origins', 'trusted_origins', 'native_receipt',
    'cases', 'checks', 'events', 'gdt_execution_authorized', 'actual_gdt_entry_ready',
    'feature_supported', 'camera_commands', 'limitations')


def _same(left, right, code='legacy_binding'):
    core._need(core._canonical(left) == core._canonical(right), code)


def _producer_sizes(raw, journal):
    core._need(len(core._canonical(raw)) + 1 <= 2 * 1024**2, 'legacy_publication_bound')
    core._need(type(raw) is dict and type(raw.get('events')) is list, 'legacy_events')
    for row in raw['events'] + journal:
        core._need(len(core._canonical(row)) + 1 <= 32768, 'legacy_event_bound')


def _path(value):
    return core._loader_path(value)


def _origin_path(value):
    result = _path(value)
    core._need(core.ntpath.normpath(value) == value, 'legacy_path')
    return result


def _row(value, expected, *, raw_loader=False):
    core._shape(value, ('path', 'bytes', 'sha256'))
    core._integer(value['bytes'], 8 * 1024**2)
    core._need(value['bytes'] > 0, 'legacy_origin')
    core._digest(value['sha256'])
    path = _path(value['path']) if raw_loader else _origin_path(value['path'])
    core._need(path.casefold() == expected['path'].casefold()
               and value['bytes'] == expected['size']
               and value['sha256'] == expected['sha256'], 'legacy_origin')


def _read(row, expected):
    """Check legacy descriptor stamps without inventing an open-mode field."""
    core._shape(row, ('path', 'sha256', 'bytes', 'lstat_before', 'fstat_before',
        'fstat_after', 'lstat_after', 'read_calls', 'eof_probes', 'closed'))
    _row({k: row[k] for k in ('path', 'bytes', 'sha256')}, expected)
    core._integer(row['read_calls'], 8 * 1024**2 + 1)
    core._integer(row['eof_probes'], 1)
    core._need((row['bytes'] + 1024**2 - 1) // 1024**2 + 1 <= row['read_calls'] <= row['bytes'] + 1
               and row['eof_probes'] == 1
               and row['closed'] is True, 'legacy_read')
    for key in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'):
        stamp = row[key]; core._shape(stamp, core.STAMP)
        for value in stamp.values(): core._integer(value)
        core._need(core.stat.S_ISREG(stamp['mode']) and stamp['nlink'] == 1
            and stamp['size'] == row['bytes'] and not stamp['file_attributes'] & 0x400, 'legacy_file_kind')
    _same(row['lstat_before'], row['lstat_after'], 'legacy_read')
    _same(row['fstat_before'], row['fstat_after'], 'legacy_read')
    for key in ('lstat_before', 'fstat_before'):
        _same({k:row[key][k] for k in core.CROSS}, expected['identity'], 'legacy_identity')


def _expectations(policy):
    groups = {}
    for name in ('python_origins', 'native_libraries', 'trusted_origins'):
        groups[name] = {}
        for alias, row in policy[name].items():
            path = policy['roots'][row['root']]['path'].rstrip('/') + '/' + row['relative_path']
            groups[name][alias] = dict(row, path=path)
    core._shape(groups['python_origins'], ALIASES)
    core._shape(groups['trusted_origins'], TRUSTED)
    # This expectation schema has exact sets, not optional members. The audited
    # five-load profile is supported; a four-load AESNI-absent profile refuses.
    core._shape(groups['native_libraries'], NATIVE)
    for alias, row in groups['python_origins'].items():
        tail = '/'.join(alias.split('.'))
        wanted = tail + '/__init__.py' if alias in PACKAGES else tail + '.py'
        core._need(row['relative_path'] == wanted, 'legacy_profile')
    for alias, row in groups['native_libraries'].items():
        core._need(row['relative_path'] == 'Cryptodome/' + NATIVE[alias], 'legacy_profile')
    for alias, row in groups['trusted_origins'].items():
        core._need(row['relative_path'] == TRUSTED_PATHS[alias], 'legacy_profile')
    return groups


def _source_budget(rows):
    total = 0
    for row in rows.values():
        core._integer(row['bytes'], 1024**2)
        total += row['bytes']
    core._need(total <= 4 * 1024**2, 'legacy_source_budget')


def _startup(entry, probe, policy, config):
    core._shape(entry, ('implementation', 'version', 'platform', 'os_name', 'maxsize',
        'isolated', 'no_site', 'dont_write_bytecode', 'optimize', 'executable',
        'base_executable', 'prefix', 'base_prefix', 'path'))
    for key, expected in (('isolated', 1), ('no_site', 1), ('optimize', 0), ('maxsize', 2**63 - 1)):
        core._integer(entry[key]); core._need(entry[key] == expected, 'legacy_startup')
    _same(entry['version'], [3, 13, 12], 'legacy_startup')
    core._need(entry['implementation'] == 'cpython' and entry['platform'] == 'win32'
        and entry['os_name'] == 'nt' and entry['dont_write_bytecode'] is True, 'legacy_startup')
    base = policy['roots']['runtime']['path'].rstrip('/')
    venv = _path(config['package_root'])
    for _ in range(3): venv = core.ntpath.dirname(venv).replace('\\', '/')
    for key, wanted in (('executable', venv + '/Scripts/python.exe'),
            ('base_executable', base + '/python.exe'), ('prefix', base), ('base_prefix', base)):
        core._need(_origin_path(entry[key]).casefold() == wanted.casefold(), 'legacy_startup')
        _same(probe[key], entry[key], 'legacy_startup')
    paths = [base + '/python313.zip', base + '/DLLs', base + '/Lib', base]
    core._need(type(entry['path']) is list and len(entry['path']) == 4, 'legacy_startup')
    _same([_origin_path(p).casefold() for p in entry['path']], [p.casefold() for p in paths], 'legacy_startup')
    _same(probe['path'], entry['path'], 'legacy_startup')
    core._need(type(probe['version']) is str and probe['version'].startswith('3.13.12 '), 'legacy_startup')
    _same(probe['normalized_path'], [core.ntpath.normcase(core.ntpath.normpath(p)) for p in entry['path']], 'legacy_startup')


def _vectors(config, raw):
    vectors = config['vectors']
    core._need(type(vectors) is list and len(vectors) == 6, 'legacy_vectors')
    core._need(core._hash(vectors) == PUBLIC_VECTOR_PLAN_SHA256, 'legacy_vector_plan')
    cases = []
    for index, row in enumerate(vectors):
        core._shape(row, ('id', 'mode', 'key_bits', 'key_hex', 'plaintext_hex', 'iv_hex', 'ciphertext_hex'))
        mode = 'ECB' if index < 3 else 'CBC'
        bits = (128, 192, 256)[index % 3]
        core._integer(row['key_bits'])
        core._need(row['mode'] == mode and row['key_bits'] == bits
                   and row['id'] == mode + '-' + str(bits), 'legacy_vectors')
        for key, size in (('key_hex', bits // 4), ('plaintext_hex', 128), ('ciphertext_hex', 128)):
            text = row[key]
            core._need(type(text) is str and len(text) == size
                       and all(c in '0123456789abcdef' for c in text), 'legacy_vectors')
        core._need(row['iv_hex'] is None if mode == 'ECB' else
                   type(row['iv_hex']) is str and len(row['iv_hex']) == 32
                   and all(c in '0123456789abcdef' for c in row['iv_hex']), 'legacy_vectors')
        for branch in ('default', 'generic'):
            cases.append(dict(id=row['id'], branch_request=branch, encrypt=True, decrypt=True))
    _same(raw['cases'], cases, 'legacy_vectors')
    core._integer(raw['checks'])
    core._need(raw['checks'] == 24, 'legacy_vectors')


def _native(raw, groups):
    native = raw['native_receipt']
    core._shape(native, ('schema', 'backend', 'intents', 'completions', 'aesni_loaded',
        'failures', 'audit_required', 'transitive_os_dependencies_attested'))
    core._need(native['schema'] == 'dependency_probe_native_receipt_v1'
        and native['backend'] == 'ctypes' and native['failures'] == []
        and native['audit_required'] is True
        and native['transitive_os_dependencies_attested'] is False, 'legacy_native')
    intents, completions = native['intents'], native['completions']
    count = len(groups['native_libraries'])
    core._need(type(intents) is list and type(completions) is list
               and len(intents) == len(completions) == count, 'legacy_native')
    seen = set()
    for index, (intent, completion) in enumerate(zip(intents, completions), 1):
        core._shape(intent, ('logical', 'path', 'sha256', 'bytes', 'api', 'arguments',
            'keyword_arguments', 'before', 'audit_seen', 'audit_argument'))
        name = intent['logical']
        core._need(type(name) is str and name in groups['native_libraries']
                   and name not in seen, 'legacy_native')
        expected = groups['native_libraries'][name]
        _row({k: intent[k] for k in ('path', 'bytes', 'sha256')}, expected, raw_loader=True)
        core._need(intent['api'] == 'ctypes.CDLL' and intent['audit_seen'] is True
                   and intent['arguments'] == [intent['path']]
                   and intent['keyword_arguments'] == {}, 'legacy_loader')
        core._need(_path(intent['audit_argument']).casefold() == expected['path'].casefold(), 'legacy_loader')
        _read(intent['before'], expected)
        core._shape(completion, ('logical', 'intent_sequence', 'after', 'audit_seen'))
        core._integer(completion['intent_sequence'])
        core._need(completion['logical'] == name and completion['intent_sequence'] == index
                   and completion['audit_seen'] is True, 'legacy_native')
        _read(completion['after'], expected)
        _same(intent['before'], completion['after'], 'legacy_read')
        seen.add(name)
    core._need(seen == set(groups['native_libraries'])
               and native['aesni_loaded'] is ('aesni' in seen), 'legacy_native')


def _events(raw, journal, config, completion):
    rows = raw['events']
    core._need(type(rows) is list and 4 <= len(rows) <= 256, 'legacy_events')
    for number, row in enumerate(rows, 1):
        core._shape(row, ('sequence', 'event', 'data'))
        core._integer(row['sequence'])
        core._need(row['sequence'] == number and type(row['data']) is dict, 'legacy_events')
    first = rows[0]
    core._need(first['event'] == 'probe_started', 'legacy_events')
    core._shape(first['data'], ('operation_id', 'test_injection_used', 'startup'))
    core._need(first['data']['operation_id'] == config['operation_id']
               and first['data']['test_injection_used'] is False, 'legacy_startup')
    startup = first['data']['startup']
    core._shape(startup, ('executable', 'base_executable', 'prefix', 'base_prefix', 'version',
        'path', 'normalized_path', 'pre_guard_modules', 'isolated', 'no_site',
        'dont_write_bytecode', 'pre_guard_ctypes_loaded'))
    core._need(type(startup['isolated']) is int and startup['isolated'] == 1
               and type(startup['no_site']) is int and startup['no_site'] == 1
               and startup['dont_write_bytecode'] is True
               and startup['pre_guard_ctypes_loaded'] is False, 'legacy_startup')
    modules = startup['pre_guard_modules']
    core._need(type(modules) is list and all(type(m) is str for m in modules)
               and modules == sorted(set(modules))
               and '_ctypes' not in modules
               and not any(m == 'Cryptodome' or m.startswith('Cryptodome.')
                           or m.split('.')[0] in ('cffi', '_cffi_backend', 'pycparser') for m in modules), 'legacy_startup')
    cursor = 1
    bootstrap = set()
    while cursor < len(rows) and rows[cursor]['event'] == 'trusted_bootstrap_native':
        data = rows[cursor]['data']
        core._shape(data, ('argument', 'guarded_file_origin'))
        value = data['argument']
        core._need(value in (None, 'kernel32') and value not in bootstrap
                   and data['guarded_file_origin'] is False, 'legacy_bootstrap')
        bootstrap.add(value); cursor += 1
    core._need(cursor < len(rows) and rows[cursor]['event'] == 'trusted_backend_initialized', 'legacy_events')
    _same(rows[cursor]['data'], dict(origins=raw['trusted_origins'], guarded_initialization=False))
    cursor += 1
    stack, started, finished = [], set(), set()
    pending, native_index, case_index = None, 0, 0
    completed_native = set()
    native = raw['native_receipt']
    for row in rows[cursor:-1]:
        kind, data = row['event'], row['data']
        if kind in ('source_execute_intent', 'source_execute_complete'):
            core._shape(data, ('alias', 'path', 'sha256'))
            alias = data['alias']
            core._need(type(alias) is str and alias in raw['source_origins'], 'legacy_import')
            source = raw['source_origins'][alias]
            _same(data, dict(alias=alias, path=source['path'], sha256=source['sha256']))
            if kind == 'source_execute_intent':
                core._need(alias not in started, 'legacy_import'); started.add(alias); stack.append(alias)
            else:
                core._need(stack and stack[-1] == alias, 'legacy_import'); stack.pop(); finished.add(alias)
        elif kind == 'native_intent':
            core._need(pending is None and native_index < len(native['intents']), 'legacy_events')
            intent = native['intents'][native_index]
            _same(data, dict(intent, audit_seen=False, audit_argument=None))
            pending = 'audit'
        elif kind == 'native_audit':
            core._need(pending == 'audit', 'legacy_events')
            intent = native['intents'][native_index]
            _same(data, dict(logical=intent['logical'], raw_request=intent['path'],
                            audit_argument=intent['audit_argument'], effective_winmode_observed=False))
            pending = 'completion'
        elif kind == 'native_completion':
            core._need(pending == 'completion', 'legacy_events')
            _same(data, native['completions'][native_index])
            completed_native.add(data['logical']); native_index += 1; pending = None
        elif kind == 'vector_case':
            core._need(pending is None and case_index < len(raw['cases']), 'legacy_events')
            mode = raw['cases'][case_index]['id'].split('-')[0].lower()
            core._need(not stack and 'Cryptodome.Cipher.AES' in finished
                       and 'Cryptodome.Cipher._mode_' + mode in finished, 'legacy_import')
            core._need({'aes', mode} <= completed_native, 'legacy_native_order')
            _same(data, raw['cases'][case_index]); case_index += 1
        else:
            raise core.EvidenceError('legacy_events')
    core._need(not stack and finished == set(ALIASES) and pending is None
               and native_index == len(native['intents']) and case_index == 12, 'legacy_events')
    core._need(rows[-1]['event'] == 'computation_complete', 'legacy_events')
    _same(rows[-1]['data'], dict(cases=12, checks=24, native_completions=native_index))
    core._need(len(journal) == len(rows) + 4, 'legacy_journal')
    for number, row in enumerate(journal, 1):
        core._shape(row, ('sequence', 'event', 'data')); core._integer(row['sequence'])
        core._need(row['sequence'] == number, 'legacy_journal')
    core._need(journal[0]['event'] == 'integrated_entry_started', 'legacy_journal')
    data = journal[0]['data']
    core._shape(data, ('startup', 'test_injection_used', 'actual_gdt_entry_ready', 'gdt_execution_authorized'))
    core._need(data['test_injection_used'] is False and data['actual_gdt_entry_ready'] is False
               and data['gdt_execution_authorized'] is False, 'legacy_journal')
    # The outer journal numbers the same events one position later; retain both
    # original sequences in the envelope rather than modifying either transcript.
    _same(journal[1:len(rows) + 1], [dict(row, sequence=row['sequence'] + 1) for row in rows], 'legacy_journal')
    anchor = completion['provenance']
    for row, name, payload in zip(journal[-3:],
            ('native_provenance_persisted', 'protected_callback_claimed', 'protected_callback_returned'),
            (anchor, dict(provenance=anchor, attempt=1), dict(attempt=1))):
        core._need(row['event'] == name, 'legacy_journal'); _same(row['data'], payload, 'legacy_journal')
    return {'probe_startup':startup, 'entry_startup':data['startup']}


def adapt_legacy_dependency_records(*, expectation, package, config, completion,
                                   raw_receipt_json, journal_jsonl):
    """Return a lossless, blocked legacy envelope, never a successor receipt."""
    try:
        raw_bytes = core._text_bytes(raw_receipt_json)
        journal_bytes = core._text_bytes(journal_jsonl)
        lines = journal_jsonl.splitlines()
        core._need(1 <= len(lines) <= 1024 and all(lines), 'journal_lines')
        raw = core._json_text(raw_receipt_json)
        journal = [core._json_text(line) for line in lines]
        expectation, package, config, completion, raw, journal = core._bounded_copy(
            [expectation, package, config, completion, raw, journal])
        _producer_sizes(raw, journal)
        manifest, receipts = core._package(package)
        core._policy(expectation, package, manifest, receipts)
        core._need(expectation['loader_kwargs'] == {}, 'legacy_loader')
        groups = _expectations(expectation)
        core._shape(config, ('schema', 'operation_id', 'package_root', 'source_rows', 'native_rows', 'trusted_origins', 'vectors'))
        core._need(config['schema'] == 'dependency_probe_config_v1'
                   and config['operation_id'] == expectation['operation_id'], 'legacy_config')
        operation = config['operation_id']
        core._need(len(operation) == 32 and all(c in '0123456789abcdef' for c in operation), 'legacy_config')
        core._need(_origin_path(config['package_root']).casefold() ==
                   (expectation['roots']['package']['path'].rstrip('/') + '/Cryptodome').casefold(), 'legacy_config')
        for key, group in (('source_rows', 'python_origins'), ('native_rows', 'native_libraries'), ('trusted_origins', 'trusted_origins')):
            core._shape(config[key], groups[group])
            for name, row in config[key].items(): _row(row, groups[group][name])
        _source_budget(config['source_rows'])
        core._shape(raw, RAW_KEYS)
        core._need(raw['schema'] == 'dependency_probe_raw_result_v1'
                   and raw['status'] == 'complete_dependency_vectors'
                   and raw['operation_id'] == config['operation_id']
                   and raw['evidence_class'] == 'runtime-observed'
                   and raw['test_injection_used'] is False, 'legacy_raw')
        for key in ('gdt_execution_authorized', 'actual_gdt_entry_ready', 'feature_supported'):
            core._need(raw[key] is False, 'authority')
        core._need(raw['camera_commands'] == [], 'authority')
        _same(raw['limitations'], LIMITATIONS, 'legacy_limitations')
        _same(raw['config_sha256'], hashlib.sha256(core._canonical(config) + b'\n').hexdigest())
        _same(raw['config_sha256'], expectation['config_sha256'])
        _same(raw['cache_sha256'], expectation['cache_sha256'])
        _same(core._hash(config['vectors']), expectation['vector_plan_sha256'])
        core._shape(raw['source_origins'], groups['python_origins'])
        core._shape(raw['trusted_origins'], groups['trusted_origins'])
        _same(raw['source_origins'], config['source_rows'], 'legacy_origin')
        for alias, row in raw['source_origins'].items(): _row(row, groups['python_origins'][alias])
        for alias, row in raw['trusted_origins'].items():
            _read(row, groups['trusted_origins'][alias])
            _same(row['path'], config['trusted_origins'][alias]['path'], 'legacy_origin')
        _vectors(config, raw); _native(raw, groups)
        core._shape(completion, ('schema', 'status', 'callback_result', 'provenance', 'test_injection_used',
            'evidence_class', 'actual_gdt_entry_ready', 'gdt_execution_authorized', 'feature_supported',
            'camera_commands', 'fresh_source_receipts', 'source_finder_and_alias_cleanup_verified', 'runtime_source_sha256'))
        core._need(completion['schema'] == 'gdt_dependency_continuation_result_v1'
            and completion['status'] == 'protected_callback_returned'
            and completion['test_injection_used'] is False and completion['evidence_class'] == 'runtime-observed'
            and completion['actual_gdt_entry_ready'] is False and completion['gdt_execution_authorized'] is False
            and completion['feature_supported'] is False and completion['camera_commands'] == []
            and completion['source_finder_and_alias_cleanup_verified'] is True, 'legacy_completion')
        core._need('runtime' in expectation['source_sha256'], 'legacy_source')
        _same(completion['runtime_source_sha256'], expectation['source_sha256']['runtime'], 'legacy_source')
        _same(completion['callback_result'], dict(status='public_vectors_during_live_continuation', checks=24,
            durable_receipt_verified_before_callback=True, camera_commands=[], gdt_execution_authorized=False, feature_supported=False), 'legacy_callback')
        core._shape(completion['fresh_source_receipts'], groups['python_origins'])
        for alias, row in completion['fresh_source_receipts'].items():
            _read(row, groups['python_origins'][alias])
            _same(row['path'], config['source_rows'][alias]['path'], 'legacy_origin')
        for intent in raw['native_receipt']['intents']:
            _same(intent['before']['path'], config['native_rows'][intent['logical']]['path'], 'legacy_origin')
        anchor = completion['provenance']; core._shape(anchor, ('path', 'sha256', 'bytes'))
        _origin_path(anchor['path']); core._integer(anchor['bytes'], 4 * 1024**2)
        core._need(anchor['bytes'] == len(raw_bytes) and anchor['sha256'] == hashlib.sha256(raw_bytes).hexdigest(), 'legacy_raw_hash')
        startup = _events(raw, journal, config, completion)
        _startup(startup['entry_startup'], startup['probe_startup'], expectation, config)
        return dict(schema='legacy_dependency_envelope_v1', status='legacy_records_consistent_with_blockers',
            expectation=expectation, package=package, config=config, completion=completion,
            original_raw_receipt_json=raw_receipt_json, original_journal_jsonl=journal_jsonl,
            raw_receipt_sha256=hashlib.sha256(raw_bytes).hexdigest(), journal_sha256=hashlib.sha256(journal_bytes).hexdigest(),
            startup_projection=startup, native_loads=len(raw['native_receipt']['intents']),
            python_origins=len(raw['source_origins']), trusted_origins=len(raw['trusted_origins']),
            blockers=list(BLOCKERS), successor_contract_applied=False, actual_records_observed=False,
            historical_events_authenticated=False, execution_authorized=False, operational_acceptance=False,
            feature_supported=False, recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    except core.EvidenceError:
        raise
    except Exception:
        raise core.EvidenceError('legacy_shape') from None
