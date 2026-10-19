"""Invented-only successor wiring; actual runtime activation remains disabled.

The collected controller owns records and callback release. Do not wrap it in
the frozen entry's second record owner or legacy provenance callback.
"""


def run_invented(*, controller, inputs, ops, folder, control, context, records,
                 make_callbacks_after_receipt, release_callbacks_after_controller,
                 monotonic, identity):
    operation = inputs['expectation']['operation_id']
    if (type(operation) is not str or context.get('operation_id') != operation or
            identity.get('operation_id') != operation):
        raise ValueError('wiring_operation')
    return controller.run_invented(inputs=inputs, ops=ops, folder=folder,
        control=control, context=context, records=records,
        make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller,
        monotonic=monotonic, identity=identity)


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
