"""Captured invented-only wiring for genuine child controller qualification.

The unmodified public wiring source is preserved as a prefix.  Separate labelled
overrides use the genuine controller, collector, producer and saved verifier with
``invented=True`` and an exact captured FakeOps class.  The embedded inputs are
freshly generated inert package bytes, receipts, root identities and public
vectors; they contain no precomputed controller/dependency/terminal records.
Nothing in this helper reads an installed package, protected input or device.
This trusted test composition does not qualify or activate the runtime branch.
"""
import ast
import hashlib
import json
from pathlib import Path
import textwrap


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_PINS = {
    'tools/dependency_successor_wiring.py':
        '9bb5b33f37f5cf6e5231afdae87b230281423c058a852b8977de2fc754eeb31d',
    'tools/dependency_invented.py':
        '32e9e86456fd960bebdae31c883a67fe8fd411a04d521a3566a2dd637a0058d3',
    'tools/dependency_producer.py':
        '7211bd4ed46e821df79fb2f7660aefef9c04b0ee11f2500b3053c6f6c8dc05ce',
    'tools/dependency_evidence.py':
        '63eb311df4c818458edd28dd9853c3c20234460f3cf145eb16886ef0abbb12f3',
    'tools/dependency_package_preflight.py':
        'b323e8094ff8206a10d9cc804446990a811b9829c25c12d477b185a19c33d588',
    'tools/dependency_legacy.py':
        '13c6f6e7ca84d9cd24bdbd2060310e355fea697f5af743c3f3fe765efbef76af',
    'tests/test_dependency_package_preflight.py':
        'bb43675c36d0b821b5647f99223e7db18e328409ed06859271f127b7302e840f',
    'tests/test_dependency_producer.py':
        'de7fe608d26124ab9920506630cbdce7ed31f6a7a5ab0c9c2888c7a5998fd165',
    'tests/test_dependency_legacy.py':
        '7c466935ddf4e34e94d571edc7e007fcfbeb302869ccafeaa8a3a0e1b9c7812c',
}


def _source_buffers():
    result = {}
    for relative, expected in SOURCE_PINS.items():
        path = REPOSITORY / relative
        before = path.stat()
        raw = path.read_bytes()
        after = path.stat()
        stamp = lambda row: (row.st_dev, row.st_ino, row.st_size,
                             row.st_mtime_ns, row.st_ctime_ns)
        if (stamp(before) != stamp(after) or not 0 < len(raw) <= 2 * 1024**2 or
                hashlib.sha256(raw).hexdigest() != expected):
            raise AssertionError('invented child fixture authored source changed')
        result[relative] = raw
    return result


def selected_runtime_fixture_sources():
    """Verify and expose the finite ordinary authored source pin closure."""
    _source_buffers()
    return {str(REPOSITORY / name): digest for name, digest in SOURCE_PINS.items()}


def wiring_source():
    """Return a separately captured invented wiring source, never execute it.

    Parent-side generation calls only the existing ordinary synthetic builder.
    The launched child must create all collection/producer/controller outputs
    afresh.  The real public source and its runtime refusal are left unchanged.
    """
    sources = _source_buffers()
    # These builders create logical fixture data in memory.  Pin the complete
    # authored builder closure before importing its definition into this test.
    from test_dependency_package_preflight import complete_fixture
    _, ops = complete_fixture()
    package = dict(contents={name: raw.hex() for name, raw in ops.contents.items()},
                   observed=ops.observed, roots=ops.roots, vectors=ops.vectors)
    text = json.dumps(package, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)
    # Keep the exact authored class source; its subject/core bindings become
    # lexical references to this child helper owner's genuine producer/evidence.
    invented = sources['tools/dependency_invented.py'].decode('utf-8')
    matches = [node for node in ast.parse(invented).body
               if isinstance(node, ast.ClassDef) and node.name == 'FakeOps']
    if len(matches) != 1:
        raise AssertionError('invented child fixture FakeOps class missing')
    fake_ops = ast.get_source_segment(invented, matches[0])
    if not fake_ops:
        raise AssertionError('invented child fixture FakeOps source unavailable')
    constructor = (
        '\n# BEGIN SEPARATE INVENTED CHILD QUALIFICATION WIRING\n'
        '# All generated records use invented=True; actual runtime stays disabled.\n'
        'import copy\nimport json\nimport types\n'
        '_INVENTED_PACKAGE_TEXT = ' + repr(text) + '\n\n'
        'def _invented_ops(package, inputs):\n'
        '    subject = package.dependency_producer\n'
        '    core = package.dependency_evidence\n' +
        textwrap.indent(fake_ops, '    ') + '\n'
        '    value = json.loads(_INVENTED_PACKAGE_TEXT)\n'
        '    vectors = json.loads(inputs["config_json"])["vectors"]\n'
        '    if vectors != value["vectors"]:\n'
        '        raise ValueError("synthetic_child_public_vectors")\n'
        '    return FakeOps(inputs["expectation"],\n'
        '        {name: bytes.fromhex(raw) for name, raw in value["contents"].items()},\n'
        '        value["observed"], value["roots"], vectors)\n'
    )
    suffix = r'''

def _dispatch_runtime(*, helpers, packet, fixed, source_buffers, review_sha256,
                      folder, control, context, records, make_callbacks_after_receipt,
                      release_callbacks_after_controller, monotonic, identity):
    """Separate invented dispatch; never calls RuntimeOps or runtime producer."""
    _startup()
    if helpers.mode != 'child':
        raise ValueError('successor_helper_mode')
    helpers.intact()
    package = helpers.package
    inputs = package.dependency_execution.bind_runtime_packet(
        packet, fixed, source_buffers, review_sha256)
    operation = inputs['expectation']['operation_id']
    if (type(context) is not dict or type(identity) is not dict or
            operation != context.get('operation_id') or operation != identity.get('operation_id')):
        raise ValueError('successor_operation')
    ops = _invented_ops(package, inputs)
    if isinstance(ops, package.dependency_producer.RuntimeOps):
        raise ValueError('synthetic_child_concrete_observer')
    alias = '_invented_dependency_probe'
    if alias in sys.modules or 'ctypes' in sys.modules:
        raise ValueError('synthetic_child_preloaded_alias')
    helper = types.ModuleType(alias)
    helper.new = ops.new
    owned = ((alias, helper), ('ctypes', ops.modules['ctypes']))
    primary = cleanup = None
    answer = None
    try:
        for name, module in owned:
            sys.modules[name] = module
        answer = package.dependency_controller.run_invented(
            inputs=inputs, ops=ops, folder=folder, control=control, context=context,
            records=records, make_callbacks_after_receipt=make_callbacks_after_receipt,
            release_callbacks_after_controller=release_callbacks_after_controller,
            monotonic=monotonic, identity=identity)
        if ops.modules['ctypes'].CDLL is not ops.original:
            raise ValueError('synthetic_child_loader_cleanup')
        helpers.intact()
    except BaseException as error:
        primary = error
    finally:
        for name, module in reversed(owned):
            try:
                # Preserve a foreign replacement and report uncertain ownership.
                if sys.modules.get(name) is not module:
                    raise ValueError('synthetic_child_alias_ownership')
                del sys.modules[name]
            except BaseException as error:
                if cleanup is None:
                    cleanup = error
    if primary is not None:
        if cleanup is not None:
            raise primary from cleanup
        raise primary
    if cleanup is not None:
        raise cleanup
    return answer


def _collect_completion(*, helpers, folder, inputs, answer, control):
    """Genuine saved-artifact collection using only the invented grammar."""
    if helpers.mode != 'child':
        raise ValueError('successor_helper_mode')
    helpers.intact()
    package = helpers.package
    dependency = package.dependency_execution.validate_saved_composition(
        Path(folder) / 'collected', inputs, invented=True)
    bridge = {}
    for name in ('completion.json', 'controller-result.json'):
        raw, _ = package.dependency_producer.read_verified(
            str(Path(folder) / name), limit=2*1024**2)
        bridge[name] = hashlib.sha256(raw).hexdigest()
    code, summary = answer['callback_result']
    if type(code) is not int or code != 0:
        raise ValueError('successor_completion_code')
    stdout = control.encoded(summary, 16384)
    if type(stdout) is not bytes or not 0 < len(stdout) <= 16384:
        raise ValueError('successor_completion_stdout')
    helpers.intact()
    return dict(dependency_sha256=dependency, bridge_sha256=bridge,
                stdout=stdout, stdout_sha256=hashlib.sha256(stdout).hexdigest())


def _verify_saved_runtime(*, helpers, folder, inputs, operation_id, stdout,
                          stdout_sha256, dependency_sha256, bridge_sha256):
    """Separate invented saved verifier, without any observer activation."""
    if helpers.mode != 'parent':
        raise ValueError('successor_helper_mode')
    return helpers.verify(folder=folder, inputs=inputs, operation_id=operation_id,
        stdout=stdout, stdout_sha256=stdout_sha256, dependency_sha256=dependency_sha256,
        bridge_sha256=bridge_sha256, invented=True)

# END SEPARATE INVENTED CHILD QUALIFICATION WIRING
'''
    return sources['tools/dependency_successor_wiring.py'] + constructor.encode('utf-8') + suffix.encode('utf-8')
