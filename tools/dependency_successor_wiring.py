"""Closed successor composition seams; ordinary runtime entry is disabled.

Only invented qualification is authorized. These private functions are authored
engine seams, not permission checks or a standalone operational launcher.
"""
import sys


def _startup():
    if not (sys.implementation.name == 'cpython' and sys.platform == 'win32' and
            sys.flags.isolated == sys.flags.no_site == sys.flags.no_user_site == 1 and
            sys.dont_write_bytecode is True and sys.flags.optimize == 0):
        raise ValueError('successor_startup')
    if any(n == 'Crypto' or n.startswith('Crypto.') or n == 'Cryptodome' or
           n.startswith('Cryptodome.') for n in sys.modules):
        raise ValueError('successor_preloaded')


def _dispatch_runtime(*, helpers, packet, fixed, source_buffers, review_sha256,
                      folder, control, context, records, make_callbacks_after_receipt,
                      release_callbacks_after_controller, monotonic, identity):
    """Future reviewed engine call, no injectable observer or mode selector.

    All packet validation precedes controller reservation and record ownership.
    Exact interpreter/argv/source/request authority remains the outer entry's job.
    """
    _startup()
    if helpers.mode != 'child':
        raise ValueError('successor_helper_mode')
    helpers.intact()
    package = helpers.package
    inputs = package.dependency_execution.bind_runtime_packet(packet, fixed, source_buffers, review_sha256)
    operation = inputs['expectation']['operation_id']
    if (type(context) is not dict or type(identity) is not dict or
            operation != context.get('operation_id') or operation != identity.get('operation_id')):
        raise ValueError('successor_operation')
    # No legacy second owner; the controller transfers ownership on reservation.
    return package.dependency_controller._run(inputs=inputs, folder=folder,
        control=control, context=context, records=records,
        make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller,
        monotonic=monotonic, identity=identity, invented=False)


def _verify_saved_runtime(*, helpers, folder, inputs, operation_id, stdout,
                          stdout_sha256, dependency_sha256, bridge_sha256):
    """Saved runtime-shaped records only; no claim that the producer ran."""
    if helpers.mode != 'parent':
        raise ValueError('successor_helper_mode')
    return helpers.verify(folder=folder, inputs=inputs, operation_id=operation_id,
        stdout=stdout, stdout_sha256=stdout_sha256, dependency_sha256=dependency_sha256,
        bridge_sha256=bridge_sha256, invented=False)


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
