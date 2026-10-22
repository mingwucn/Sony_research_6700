"""New ordinary files containing only the complete invented dependency fixture.

This parent-side helper independently records filesystem observations without
calling the producer's reader, root observer, loader, or RuntimeOps.  Its output
is a synthetic expectation bound to these newly authored files.  Five inert
native-suffix files are package members, and five inert trusted-origin files
are separate; none is an installed dependency or executable native payload.
Failures retain the caller-owned directory for inspection and are never retried.
"""
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

from dependency_child_runtime_fixture import _source_buffers


_STAMP = ('device', 'inode', 'mode', 'nlink', 'size', 'mtime_ns', 'ctime_ns',
          'file_attributes')
_CROSS = ('device', 'inode', 'mode', 'size', 'mtime_ns')
_LIMIT = 8 * 1024**2


def _need(condition, code):
    if not condition:
        raise ValueError(code)


def _encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def _hash(value):
    return hashlib.sha256(_encoded(value)).hexdigest()


def _stamp(value):
    return dict(zip(_STAMP, (value.st_dev, value.st_ino, value.st_mode,
        value.st_nlink, value.st_size, value.st_mtime_ns, value.st_ctime_ns,
        getattr(value, 'st_file_attributes', 0))))


def _safe_directory(value):
    return (stat.S_ISDIR(value.st_mode) and not stat.S_ISLNK(value.st_mode)
            and not getattr(value, 'st_file_attributes', 0) & 0x400)


def _directory_observation(path):
    """Independent lstat observations; native ancestor spelling matches schema."""
    rows = []
    for item in reversed((Path(path), *Path(path).parents)):
        value = os.lstat(item)
        _need(_safe_directory(value), 'synthetic_filesystem_directory_kind')
        rows.append(dict(path=str(item), device=value.st_dev, inode=value.st_ino,
                         mode=value.st_mode,
                         file_attributes=getattr(value, 'st_file_attributes', 0)))
    return dict(schema='dependency_directory_identity_v1', path=path, ancestors=rows)


def _relative(value):
    _need(type(value) is str and 0 < len(value) <= 512 and
          '\\' not in value and ':' not in value and
          PurePosixPath(value).as_posix() == value and
          all(part not in ('', '.', '..') and not part.endswith(('.', ' '))
              for part in value.split('/')),
          'synthetic_filesystem_relative_path')
    _need(not any(ord(char) < 32 or ord(char) == 127 or char in '<>"|?*'
                  for char in value), 'synthetic_filesystem_relative_path')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$', 'CLOCK$'}
    reserved |= {prefix + suffix for prefix in ('COM', 'LPT')
                 for suffix in tuple('123456789') + ('¹', '²', '³')}
    _need(all(part.split('.')[0].upper() not in reserved for part in value.split('/')),
          'synthetic_filesystem_relative_path')
    return value


def _regular(value):
    return (stat.S_ISREG(value.st_mode) and value.st_nlink == 1
            and not getattr(value, 'st_file_attributes', 0) & 0x400
            and 0 <= value.st_size <= _LIMIT)


def _write_new(path, raw, counters):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags, 0o600)
    counters['write_opens'] += 1
    try:
        _need(_regular(os.fstat(descriptor)), 'synthetic_filesystem_write_kind')
        counters['write_calls'] += 1
        written = os.write(descriptor, raw)
        _need(written == len(raw), 'synthetic_filesystem_short_write_no_retry')
        counters['written_bytes'] += written
    finally:
        counters['write_close_attempts'] += 1
        os.close(descriptor)
        counters['write_close_returns'] += 1


def _capture_file(path, raw, counters):
    """lstat/open/fstat/read/EOF/fstat/close/lstat, with parent-chain checks."""
    parents = _directory_observation(Path(path).parent.as_posix())
    before = os.lstat(path)
    _need(_regular(before), 'synthetic_filesystem_capture_kind')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    counters['read_opens'] += 1
    chunks = []
    total = 0
    try:
        opened = os.fstat(descriptor)
        _need(_regular(opened) and all(_stamp(before)[key] == _stamp(opened)[key]
                                      for key in _CROSS),
              'synthetic_filesystem_capture_identity')
        while True:
            counters['read_calls'] += 1
            block = os.read(descriptor, min(65536, _LIMIT + 1 - total))
            if not block:
                counters['eof_returns'] += 1
                break
            total += len(block)
            _need(total <= _LIMIT, 'synthetic_filesystem_capture_bound')
            counters['read_bytes'] += len(block)
            chunks.append(block)
        final = os.fstat(descriptor)
    finally:
        counters['read_close_attempts'] += 1
        os.close(descriptor)
        counters['read_close_returns'] += 1
    after = os.lstat(path)
    observed = b''.join(chunks)
    _need(_regular(final) and _regular(after) and
          _stamp(before) == _stamp(after) and _stamp(opened) == _stamp(final) and
          all(_stamp(after)[key] == _stamp(final)[key] for key in _CROSS) and
          observed == raw and len(observed) == before.st_size and
          parents == _directory_observation(Path(path).parent.as_posix()),
          'synthetic_filesystem_capture_changed')
    return dict(path=path, size=len(observed),
                sha256=hashlib.sha256(observed).hexdigest(), opened_read_only=True,
                lstat_before=_stamp(before), fstat_before=_stamp(opened),
                fstat_after=_stamp(final), lstat_after=_stamp(after))


def materialize_filesystem_fixture(root, data, ops):
    """Return ``(rebound_data, summary)`` for a NEW caller-owned Windows root.

    Data and operations must come from complete_fixture. They are not mutated.
    Only cache source literals containing the five invented native paths are
    rebound; source_buffers, config_json and public vector plan stay identical.
    Actual independent receipts are captured after every file has been written.
    Callers retain cleanup ownership, including after a partial failure.
    """
    _source_buffers()  # Verify the finite ordinary fixture/refresh source closure.
    from test_dependency_producer import refresh
    _need(os.name == 'nt', 'synthetic_filesystem_windows_only')
    root = Path(root)
    _need(root.is_absolute() and len(root.drive) == 2 and root.drive[1] == ':' and
          root.drive[0].isascii() and root.drive[0].isalpha(),
          'synthetic_filesystem_absolute_root')
    root_text = root.as_posix()
    root_text = root_text[0].upper() + root_text[1:]
    _relative(root_text[3:])
    root = Path(root_text)
    try:
        os.lstat(root)
    except FileNotFoundError:
        pass
    else:
        raise ValueError('synthetic_filesystem_root_exists')
    _directory_observation(root.parent.as_posix())
    rebound = copy.deepcopy(data)
    policy = rebound['expectation']
    old_roots = {name: row['path'] for name, row in policy['roots'].items()}
    _need(set(old_roots) == {'package', 'runtime'}, 'synthetic_filesystem_root_roster')
    new_roots = {name: (root / name).as_posix() for name in old_roots}
    package = rebound['package']
    receipts = package['installed_receipts']
    _need(len(receipts) == 351 and len(policy['trusted_origins']) == 5 and
          len(policy['native_libraries']) == 5 and len(policy['python_origins']) == 11,
          'synthetic_filesystem_origin_roster')
    cache = json.loads(rebound['cache_json'])
    _need(set(cache) == {'schema', 'sources'} and
          cache['schema'] == 'prospective_dependency_source_cache_v1' and
          set(cache['sources']) == set(policy['python_origins']),
          'synthetic_filesystem_source_cache')
    planned = {}
    old_paths = set()
    for relative, receipt in receipts.items():
        _relative(relative)
        old_path = old_roots['package'].rstrip('/') + '/' + relative
        new_path = new_roots['package'] + '/' + relative
        raw = ops.contents[old_path]
        _need(type(raw) is bytes and 0 < len(raw) <= _LIMIT and
              len(raw) == receipt['size'] and
              hashlib.sha256(raw).hexdigest() == receipt['sha256'],
              'synthetic_filesystem_package_bytes')
        planned[new_path] = raw
        old_paths.add(old_path)
    for alias, row in policy['trusted_origins'].items():
        relative = _relative(row['relative_path'])
        old_path = old_roots['runtime'].rstrip('/') + '/' + relative
        raw = ops.contents[old_path]
        _need(raw == ('invented inert bytes trusted_origins ' + alias).encode('ascii'),
              'synthetic_filesystem_trusted_bytes')
        planned[new_roots['runtime'] + '/' + relative] = raw
        old_paths.add(old_path)
    _need(set(ops.contents) == old_paths and len(planned) == 356 and
          len({path.casefold() for path in planned}) == len(planned),
          'synthetic_filesystem_file_roster')
    source_changes = []
    aes_alias = 'Cryptodome.Cipher.AES'
    aes_source = cache['sources'][aes_alias]
    for alias, row in policy['native_libraries'].items():
        relative = _relative(row['relative_path'])
        old_path = old_roots['package'].rstrip('/') + '/' + relative
        new_path = new_roots['package'] + '/' + relative
        _need(planned[new_path] == ('invented inert bytes native_libraries ' + alias).encode('ascii'),
              'synthetic_filesystem_native_bytes')
        before, after = repr(old_path), repr(new_path)
        _need(aes_source.count(before) == 1, 'synthetic_filesystem_native_literal')
        aes_source = aes_source.replace(before, after)
        source_changes.append(alias)
    for alias, row in policy['python_origins'].items():
        path = new_roots['package'] + '/' + row['relative_path']
        _need(planned[path] == cache['sources'][alias].encode('utf-8'),
              'synthetic_filesystem_cached_source_bytes')
    cache['sources'][aes_alias] = aes_source
    planned[new_roots['package'] + '/' + policy['python_origins'][aes_alias]['relative_path']] = aes_source.encode('utf-8')
    _need(sum(map(len, planned.values())) <= 64 * 1024**2,
          'synthetic_filesystem_total_bound')
    counters = dict(write_opens=0, write_calls=0, write_close_attempts=0,
                    write_close_returns=0, written_bytes=0, read_opens=0,
                    read_calls=0, read_bytes=0, eof_returns=0,
                    read_close_attempts=0, read_close_returns=0)
    root.mkdir(exist_ok=False)
    directories = {root / name for name in new_roots}
    for path in planned:
        parent = Path(path).parent
        while parent != root:
            _need(root in parent.parents, 'synthetic_filesystem_target_escape')
            directories.add(parent)
            parent = parent.parent
    for directory in sorted(directories, key=lambda item: (len(item.parts), item.as_posix())):
        directory.mkdir(exist_ok=False)
        _need(_safe_directory(os.lstat(directory)), 'synthetic_filesystem_new_directory_kind')
    for path, raw in sorted(planned.items()):
        _write_new(path, raw, counters)
    absolute_receipts = {}
    file_capture_counters = {}
    for path, raw in sorted(planned.items()):
        before_capture = dict(counters)
        absolute_receipts[path] = _capture_file(path, raw, counters)
        file_capture_counters[path] = {key: counters[key] - before_capture[key]
            for key in ('read_opens', 'read_calls', 'read_bytes', 'eof_returns',
                        'read_close_attempts', 'read_close_returns')}
    for relative in receipts:
        absolute = new_roots['package'] + '/' + relative
        receipts[relative] = dict(copy.deepcopy(absolute_receipts[absolute]), path=relative)
    for group in ('python_origins', 'native_libraries', 'trusted_origins'):
        for row in policy[group].values():
            absolute = new_roots[row['root']] + '/' + row['relative_path']
            observed = absolute_receipts[absolute]
            row.update(size=observed['size'], sha256=observed['sha256'],
                       identity={key: observed['lstat_before'][key] for key in _CROSS})
    root_receipts = {name: _directory_observation(path) for name, path in new_roots.items()}
    for name, path in new_roots.items():
        policy['roots'][name] = dict(path=path, identity_sha256=_hash(root_receipts[name]))
    rebound['cache_json'] = (_encoded(cache) + b'\n').decode('ascii')
    policy['cache_sha256'] = hashlib.sha256(rebound['cache_json'].encode('utf-8')).hexdigest()
    previous_review = rebound['binding']['review_sha256']
    refresh(rebound)
    rebound['binding']['review_sha256'] = previous_review
    _need(rebound['config_json'] == data['config_json'] and
          rebound['source_buffers'] == data['source_buffers'] and
          policy['vector_plan_sha256'] == data['expectation']['vector_plan_sha256'],
          'synthetic_filesystem_unrelated_input_changed')
    summary = dict(schema='synthetic_dependency_filesystem_fixture_v1',
        root=root_text, roots=new_roots, root_receipts=root_receipts,
        absolute_receipts=absolute_receipts, capture_counters=counters,
        file_capture_counters=file_capture_counters,
        package_files=351, trusted_files=5, native_files_within_package=5,
        authored_files=len(planned), total_authored_bytes=sum(map(len, planned.values())),
        native_source_path_literals_rebound=source_changes,
        input_data_and_ops_unchanged=True, production_reader_used_for_expectations=False,
        receipts_independently_captured=True, installed_inputs_read=False,
        native_loader_used=False, protected_inputs_read=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])
    return rebound, summary
