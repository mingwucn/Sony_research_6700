"""Pure, closed metadata contract for a dependency-only observation.

No file access, import hook, native loader, child process or activation API.
Consistency of caller-supplied records never grants execution authority or
authenticates historical events. Raw-receipt adapters are outside this module.
"""
import hashlib
import json
import ntpath
import stat
import unicodedata


class EvidenceError(ValueError):
    """Fixed error code; never include input paths, credentials or raw records."""


def _need(condition, code):
    if not condition:
        raise EvidenceError(code)


def _shape(value, keys):
    _need(type(value) is dict and set(value) == set(keys), 'shape')


def _integer(value, maximum=2**128 - 1):
    _need(type(value) is int and 0 <= value <= maximum, 'integer')


def _digest(value):
    _need(type(value) is str and len(value) == 64
          and all(c in '0123456789abcdef' for c in value), 'digest')


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def _hash(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _bounded_copy(values):
    nodes, encoded_bytes = 0, 0

    def account(size):
        nonlocal encoded_bytes
        encoded_bytes += size
        _need(encoded_bytes <= 8 * 1024**2, 'bound')

    def visit(value, depth):
        nonlocal nodes
        nodes += 1
        _need(nodes <= 100000 and depth <= 14, 'bound')
        if type(value) is dict:
            _need(len(value) <= 2048, 'bound')
            account(2 + max(0, len(value) - 1))
            for key, item in value.items():
                _need(type(key) is str and len(key) <= 1024, 'shape')
                account(len(_canonical(key)) + 1)
                visit(item, depth + 1)
        elif type(value) is list:
            _need(len(value) <= 2048, 'bound')
            account(2 + max(0, len(value) - 1))
            for item in value:
                visit(item, depth + 1)
        elif type(value) is str:
            _need(len(value) <= 2048, 'bound')
            account(len(_canonical(value)))
        elif type(value) is int:
            _integer(value)
            account(len(_canonical(value)))
        else:
            _need(value is None or type(value) is bool, 'shape')
            account(len(_canonical(value)))

    visit(values, 0)
    data = _canonical(values)
    _need(len(data) == encoded_bytes, 'bound')
    return json.loads(data)


def _text_bytes(text):
    _need(type(text) is str and len(text) <= 4 * 1024**2, 'transcript_bound')
    count = 0
    for offset in range(0, len(text), 4096):
        count += len(text[offset:offset + 4096].encode('utf-8'))
        _need(count <= 4 * 1024**2, 'transcript_bound')
    return text.encode('utf-8')


def _json_text(text):
    def pairs(rows):
        result = {}
        for key, value in rows:
            _need(key not in result, 'duplicate_key')
            result[key] = value
        return result

    def invalid_number(value):
        raise EvidenceError('json_number')

    return json.loads(text, object_pairs_hook=pairs,
                      parse_float=invalid_number, parse_constant=invalid_number)


def _relative(value):
    _need(type(value) is str and 0 < len(value) <= 512
          and unicodedata.normalize('NFC', value) == value, 'path')
    _need(not any(ord(c) < 32 or ord(c) == 127 or c in '\\:<>"|?*'
                  for c in value), 'path')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$', 'CLOCK$'}
    reserved |= {s + n for s in ('COM', 'LPT') for n in tuple('123456789') + ('¹', '²', '³')}
    for part in value.split('/'):
        _need(part not in ('', '.', '..') and not part.endswith(('.', ' '))
              and part.split('.')[0].upper() not in reserved, 'path')


def _absolute(value):
    _need(type(value) is str and len(value) >= 3 and len(value) <= 1024
          and value[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and value[1:3] == ':/', 'path')
    if len(value) > 3:
        _relative(value[3:])
    return value


def _loader_path(value):
    _need(type(value) is str and 0 < len(value) <= 2048
          and not any(ord(c) < 32 or ord(c) == 127 for c in value), 'loader_path')
    drive, tail = ntpath.splitdrive(value)
    _need(len(drive) == 2 and drive[0].isascii() and drive[0].isalpha()
          and drive[1] == ':' and tail.startswith(('\\', '/')), 'loader_path')
    normalized = ntpath.normpath(value).replace('\\', '/')
    return _absolute(normalized[0].upper() + normalized[1:])


def _alias(value):
    _need(type(value) is str and 0 < len(value) <= 256
          and all(part.isidentifier() for part in value.split('.')), 'alias')


def _unique(paths):
    seen = set()
    for path in paths:
        folded = path.casefold()
        _need(folded not in seen, 'duplicate_path')
        seen.add(folded)


STAMP = ('device', 'inode', 'mode', 'nlink', 'size', 'mtime_ns', 'ctime_ns', 'file_attributes')
CROSS = ('device', 'inode', 'mode', 'size', 'mtime_ns')
FLAGS = ('execution_authorized', 'actual_runtime_verified', 'actual_binding_ready')


def _receipt(row, path, digest, size, identity=None):
    _shape(row, ('path', 'sha256', 'size', 'opened_read_only',
                 'lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'))
    _need(row['path'] == path and row['sha256'] == digest and row['size'] == size
          and row['opened_read_only'] is True, 'receipt_binding')
    _integer(row['size'], 64 * 1024**2)
    for name in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'):
        stamp = row[name]
        _shape(stamp, STAMP)
        for value in stamp.values():
            _integer(value)
        _need(stat.S_ISREG(stamp['mode']) and stamp['nlink'] == 1
              and stamp['size'] == size and not stamp['file_attributes'] & 0x400, 'file_kind')
    _need(row['lstat_before'] == row['lstat_after']
          and row['fstat_before'] == row['fstat_after'], 'file_changed')
    for left, right in (('lstat_before', 'fstat_before'), ('lstat_after', 'fstat_after')):
        _need(all(row[left][k] == row[right][k] for k in CROSS), 'file_identity')
    if identity is not None:
        _shape(identity, CROSS)
        for value in identity.values():
            _integer(value)
        _need(identity == {k: row['lstat_before'][k] for k in CROSS}, 'expected_identity')


def _package(package):
    _shape(package, ('manifest', 'installed_receipts', 'installed_proof'))
    manifest, receipts, proof = (package[k] for k in ('manifest', 'installed_receipts', 'installed_proof'))
    _shape(manifest, ('schema', 'status', 'version', 'wheel_sha256', 'record_sha256',
        'files', 'roster_sha256', 'record_rows', 'archive_entries', *FLAGS, 'camera_commands'))
    _need(manifest['schema'] == 'activation_wheel_manifest_v1'
          and manifest['status'] == 'wheel_buffer_manifest_validated'
          and manifest['version'] == '3.24.1', 'package_schema')
    for flag in FLAGS:
        _need(manifest[flag] is False, 'authority')
    _need(manifest['camera_commands'] == [], 'authority')
    for key in ('wheel_sha256', 'record_sha256', 'roster_sha256'):
        _digest(manifest[key])
    _integer(manifest['record_rows']); _integer(manifest['archive_entries'])
    _need(manifest['record_rows'] == 351 and manifest['archive_entries'] == 352, 'roster')
    files = manifest['files']
    _need(type(files) is dict and len(files) == 351, 'roster')
    _unique(files)
    total = 0
    for path, row in files.items():
        _relative(path); _shape(row, ('sha256', 'size')); _digest(row['sha256'])
        _integer(row['size'], 64 * 1024**2)
        total += row['size']
    _need(total <= 64 * 1024**2 and manifest['roster_sha256'] == _hash(files), 'roster')
    _shape(receipts, files)
    derived = {}
    for path, row in receipts.items():
        _receipt(row, path, files[path]['sha256'], files[path]['size'])
        derived[path] = dict(files[path], open_identity_sha256=_hash(row))
    expected = dict(schema='activation_installed_proof_v1', status='installed_receipt_set_validated',
        roster_sha256=manifest['roster_sha256'], record_sha256=manifest['record_sha256'],
        files=derived, **{k: False for k in FLAGS}, camera_commands=[])
    # Canonical equality is type-sensitive: False is not integer zero.
    _need(_canonical(proof) == _canonical(expected), 'installed_proof')
    return manifest, receipts


def _policy(policy, package, manifest, receipts):
    _shape(policy, ('schema', 'operation_id', 'platform', 'backend', 'extension_suffix',
        'roots', 'python_origins', 'native_libraries', 'trusted_origins', 'source_sha256',
        'config_sha256', 'cache_sha256', 'manifest_sha256', 'installed_proof_sha256',
        'vector_plan_sha256', 'loader_kwargs', 'no_fallback', 'bootstrap_boundary'))
    _need(policy['schema'] == 'dependency_expectation_v1' and policy['platform'] == 'windows'
          and policy['backend'] == 'ctypes' and policy['no_fallback'] is True, 'policy_schema')
    operation = policy['operation_id']
    _need(type(operation) is str and 1 <= len(operation) <= 96
          and all(c.isascii() and (c.isalnum() or c in '_-') for c in operation), 'operation')
    suffix = policy['extension_suffix']
    _need(type(suffix) is str and 1 < len(suffix) <= 128 and suffix.startswith('.')
          and all(c.isascii() and (c.isalnum() or c in '._-') for c in suffix), 'suffix')
    for key in ('config_sha256', 'cache_sha256', 'manifest_sha256', 'installed_proof_sha256', 'vector_plan_sha256'):
        _digest(policy[key])
    _need(policy['manifest_sha256'] == _hash(manifest)
          and policy['installed_proof_sha256'] == _hash(package['installed_proof']), 'package_binding')
    sources = policy['source_sha256']
    _need(type(sources) is dict and 1 <= len(sources) <= 32, 'sources')
    for alias, digest in sources.items():
        _alias(alias); _digest(digest)
    _shape(policy['roots'], ('package', 'runtime'))
    for root in policy['roots'].values():
        _shape(root, ('path', 'identity_sha256')); _absolute(root['path']); _digest(root['identity_sha256'])
    roots = [v['path'].casefold().rstrip('/') + '/' for v in policy['roots'].values()]
    _need(not roots[0].startswith(roots[1]) and not roots[1].startswith(roots[0]), 'root_overlap')
    _need(policy['bootstrap_boundary'] == ['interpreter', 'stdlib', '_ctypes', 'os_loader'], 'bootstrap')
    kwargs = policy['loader_kwargs']
    _need(type(kwargs) is dict and set(kwargs) in (set(), {'winmode'}), 'loader_arguments')
    if kwargs:
        _integer(kwargs['winmode'], 2**32 - 1)
    paths, aliases = [], set()
    for group in ('python_origins', 'native_libraries', 'trusted_origins'):
        rows = policy[group]
        _need(type(rows) is dict and 1 <= len(rows) <= 128, 'origin_roster')
        for alias, row in rows.items():
            _alias(alias); _need(alias not in aliases, 'duplicate_alias'); aliases.add(alias)
            _shape(row, ('root', 'relative_path', 'sha256', 'size', 'identity'))
            root_name = 'runtime' if group == 'trusted_origins' else 'package'
            _need(row['root'] == root_name, 'origin_domain')
            path = row['relative_path']; _relative(path); _digest(row['sha256']); _integer(row['size'], 64 * 1024**2)
            _shape(row['identity'], CROSS)
            for value in row['identity'].values():
                _integer(value)
            _need(row['identity']['size'] == row['size'], 'expected_identity')
            if group != 'trusted_origins':
                _need(path in manifest['files'] and manifest['files'][path] == {'sha256':row['sha256'], 'size':row['size']}, 'package_origin')
                _need(row['identity'] == {k:receipts[path]['lstat_before'][k] for k in CROSS}, 'expected_identity')
            if group == 'python_origins':
                _need(path.endswith('.py'), 'origin_suffix')
            if group == 'native_libraries':
                _need(path.endswith(suffix), 'origin_suffix')
            paths.append(policy['roots'][root_name]['path'].rstrip('/') + '/' + path)
    _unique(paths)


def _origins(policy, observation):
    for group in ('python_origins', 'trusted_origins'):
        _shape(observation[group], policy[group])
        for alias, expected in policy[group].items():
            path = policy['roots'][expected['root']]['path'].rstrip('/') + '/' + expected['relative_path']
            _receipt(observation[group][alias], path, expected['sha256'], expected['size'], expected['identity'])
    _shape(observation['native_loads'], policy['native_libraries'])
    for alias, expected in policy['native_libraries'].items():
        load = observation['native_loads'][alias]
        _shape(load, ('intent', 'audit', 'after'))
        intent, audit = load['intent'], load['audit']
        _shape(intent, ('api', 'arguments', 'keyword_arguments', 'before'))
        _shape(audit, ('api', 'argument'))
        _need(intent['api'] == 'ctypes.CDLL' and audit['api'] == 'ctypes.dlopen', 'loader_api')
        _need(type(intent['arguments']) is list and len(intent['arguments']) == 1
              and _canonical(intent['keyword_arguments']) == _canonical(policy['loader_kwargs']), 'loader_arguments')
        # Do not equate raw spellings. Normalize only for target comparison.
        path = policy['roots']['package']['path'].rstrip('/') + '/' + expected['relative_path']
        _need(_loader_path(intent['arguments'][0]).casefold() == path.casefold()
              and _loader_path(audit['argument']).casefold() == path.casefold(), 'loader_target')
        for row in (intent['before'], load['after']):
            _receipt(row, path, expected['sha256'], expected['size'], expected['identity'])


def _events(policy, observation):
    events = observation['events']
    _need(type(events) is list and 1 <= len(events) <= 1024, 'events')
    cursor = 0

    def take(name, data):
        nonlocal cursor
        _need(cursor < len(events), 'event_order')
        row = events[cursor]
        _shape(row, ('sequence', 'event', 'data')); _integer(row['sequence'])
        _need(row['sequence'] == cursor + 1 and row['event'] == name
              and _canonical(row['data']) == _canonical(data), 'event_order')
        cursor += 1

    take('expectation_bound', {'sha256':_hash(policy)})
    take('bootstrap_complete', {'sha256':_hash(observation['startup'])})
    take('guard_installed', {'backend':'ctypes'})
    seen_python, seen_native, pending = set(), set(), None
    while cursor < len(events) and events[cursor].get('event') in ('python_import', 'native_intent', 'native_audit', 'native_complete'):
        row = events[cursor]
        _need(type(row['data']) is dict, 'shape')
        if row['event'] == 'python_import':
            alias = row['data'].get('alias')
            _need(type(alias) is str and alias in policy['python_origins'] and alias not in seen_python, 'python_event')
            take('python_import', {'alias':alias, 'receipt_sha256':_hash(observation['python_origins'][alias])})
            seen_python.add(alias)
        else:
            name = row['data'].get('name')
            _need(type(name) is str and name in policy['native_libraries'], 'native_event')
            load = observation['native_loads'][name]
            if row['event'] == 'native_intent':
                _need(pending is None and name not in seen_native, 'native_event')
                take('native_intent', {'name':name,'sha256':_hash(load['intent'])}); pending = (name, 'audit')
            elif row['event'] == 'native_audit':
                _need(pending == (name, 'audit'), 'native_event')
                take('native_audit', {'name':name,'sha256':_hash(load['audit'])}); pending = (name, 'complete')
            else:
                _need(pending == (name, 'complete'), 'native_event')
                take('native_complete', {'name':name,'sha256':_hash(load['after'])})
                pending = None; seen_native.add(name)
    _need(pending is None and seen_python == set(policy['python_origins'])
          and seen_native == set(policy['native_libraries']), 'incomplete_loads')
    take('vectors_complete', observation['vectors'])
    take('guard_finished', {'native_names':sorted(seen_native)})
    anchor = {'raw_receipt_sha256':observation['raw_receipt_sha256'], 'operation_id':policy['operation_id']}
    for event in ('raw_written', 'raw_flushed', 'raw_fsynced', 'raw_closed', 'raw_reverified', 'callback_claimed'):
        take(event, anchor)
    take('callback_returned', {'success':True})
    take('cleanup_complete', {'aliases_released':True, 'finder_removed':True, 'native_wrapper_removed':True})
    _need(cursor == len(events), 'extra_event')


def _transcripts(policy, observation, raw, journal):
    _shape(raw, ('schema', 'operation_id', 'expectation_sha256', 'startup',
        'python_origins', 'trusted_origins', 'native_loads', 'vectors', 'events'))
    _need(raw['schema'] == 'dependency_guard_transcript_v1'
          and raw['operation_id'] == policy['operation_id']
          and raw['expectation_sha256'] == _hash(policy), 'raw_binding')
    for key in ('startup', 'python_origins', 'trusted_origins', 'native_loads', 'vectors'):
        _need(_canonical(raw[key]) == _canonical(observation[key]), 'raw_projection')
    finish = next(i for i, event in enumerate(observation['events']) if event['event'] == 'guard_finished')
    _need(_canonical(raw['events']) == _canonical(observation['events'][:finish + 1]), 'raw_projection')
    _need(_canonical(journal) == _canonical(observation['events']), 'journal_projection')


def validate_dependency_records(*, expectation, observation, package, raw_receipt_json, journal_jsonl):
    """Validate detached records; output is a consistency result with no authority.

    Root/identity/event assertions come from the caller. Exact supplied UTF-8
    transcript bytes and their projections are checked, not their truth, durable
    storage, actual file content, CPU result or operating-system behavior.
    """
    try:
        raw_bytes, journal_bytes = _text_bytes(raw_receipt_json), _text_bytes(journal_jsonl)
        lines = journal_jsonl.splitlines()
        _need(1 <= len(lines) <= 1024 and all(lines), 'journal_lines')
        raw, journal = _json_text(raw_receipt_json), [_json_text(line) for line in lines]
        expectation, observation, package, raw, journal = _bounded_copy([expectation, observation, package, raw, journal])
        manifest, receipts = _package(package)
        _policy(expectation, package, manifest, receipts)
        _shape(observation, ('schema', 'evidence_mode', 'operation_id', 'expectation_sha256',
            'source_sha256', 'config_sha256', 'cache_sha256', 'root_identities', 'startup',
            'python_origins', 'trusted_origins', 'native_loads', 'vectors', 'raw_receipt_sha256',
            'journal_sha256', 'events', 'transitive_os_dependencies_attested'))
        _need(observation['schema'] == 'dependency_observation_v1'
              and observation['evidence_mode'] in ('invented', 'saved_records'), 'observation_schema')
        _need(observation['operation_id'] == expectation['operation_id']
              and observation['expectation_sha256'] == _hash(expectation), 'expectation_binding')
        for key in ('source_sha256', 'config_sha256', 'cache_sha256'):
            _need(observation[key] == expectation[key], 'source_binding')
        _need(observation['root_identities'] == {k:v['identity_sha256'] for k,v in expectation['roots'].items()}, 'root_identity')
        _shape(observation['startup'], ('isolated', 'no_site', 'no_user_site', 'no_bytecode', 'preloaded_package_aliases', 'bootstrap_boundary'))
        for flag in ('isolated', 'no_site', 'no_user_site', 'no_bytecode'):
            _need(observation['startup'][flag] is True, 'startup')
        _need(observation['startup']['preloaded_package_aliases'] == []
              and observation['startup']['bootstrap_boundary'] == expectation['bootstrap_boundary'], 'startup')
        _need(observation['transitive_os_dependencies_attested'] is False, 'unsupported_attestation')
        for key in ('raw_receipt_sha256', 'journal_sha256'):
            _digest(observation[key])
        _shape(observation['vectors'], ('plan_sha256', 'cases', 'comparisons', 'passed'))
        vectors = observation['vectors']
        _integer(vectors['cases']); _integer(vectors['comparisons'])
        _need(vectors['plan_sha256'] == expectation['vector_plan_sha256'] and vectors['cases'] == 12
              and vectors['comparisons'] == 24 and vectors['passed'] is True, 'vectors')
        _origins(expectation, observation)
        _events(expectation, observation)
        _need(hashlib.sha256(raw_bytes).hexdigest() == observation['raw_receipt_sha256']
              and hashlib.sha256(journal_bytes).hexdigest() == observation['journal_sha256'], 'transcript_hash')
        _transcripts(expectation, observation, raw, journal)
        return {'schema':'dependency_record_consistency_v1', 'status':'dependency_record_contract_consistent',
            'evidence_mode':observation['evidence_mode'], 'expectation_sha256':_hash(expectation),
            'observation_sha256':_hash(observation), 'package_sha256':_hash(package),
            'payload_files':351, 'python_origins':len(expectation['python_origins']),
            'native_loads':len(expectation['native_libraries']), 'trusted_origins':len(expectation['trusted_origins']),
            'supplied_transcript_hashes_checked':True, 'event_projections_match_supplied_transcripts':True,
            'complete_before_any_cipher_use':False, 'historical_events_authenticated':False,
            'fresh_observation_performed':False, 'execution_authorized':False,
            'operational_acceptance':False, 'feature_supported':False,
            'recovery_proven':False, 'device_write_gate_passed':False, 'camera_commands':[]}
    except EvidenceError:
        raise
    except Exception:
        raise EvidenceError('shape') from None
