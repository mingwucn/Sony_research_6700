"""Successor dispatch and ownership tests; invented arguments only."""
import types
import unittest
from unittest.mock import Mock

from tools import dependency_wiring as subject


class WiringTests(unittest.TestCase):
    def setUp(self):
        self.call = Mock(return_value=object())
        self.kw = dict(controller=types.SimpleNamespace(run_invented=self.call),
            inputs={'expectation': {'operation_id': 'invented'}}, ops=object(), folder=object(),
            control=object(), context={'operation_id': 'invented'}, records=object(),
            make_callbacks_after_receipt=object(), release_callbacks_after_controller=object(),
            monotonic=object(), identity={'operation_id': 'invented'})

    def test_exact_controller_arguments_and_ownership_preserved(self):
        result = subject.run_invented(**self.kw)
        expected = {k: v for k, v in self.kw.items() if k != 'controller'}
        self.call.assert_called_once_with(**expected)
        self.assertIs(result, self.call.return_value)

    def test_context_operation_refused_before_controller(self):
        self.kw['context']['operation_id'] = 'other'
        with self.assertRaisesRegex(ValueError, '^wiring_operation$'):
            subject.run_invented(**self.kw)
        self.call.assert_not_called()

    def test_identity_operation_refused_before_controller(self):
        self.kw['identity']['operation_id'] = 'other'
        with self.assertRaisesRegex(ValueError, '^wiring_operation$'):
            subject.run_invented(**self.kw)
        self.call.assert_not_called()

    def test_primary_controller_failure_retained(self):
        error = KeyboardInterrupt('invented')
        self.call.side_effect = error
        with self.assertRaises(KeyboardInterrupt) as raised:
            subject.run_invented(**self.kw)
        self.assertIs(raised.exception, error)
        self.call.assert_called_once()

    def test_runtime_refuses_without_touching_arguments(self):
        with self.assertRaisesRegex(ValueError, '^real_activation_pending$'):
            subject.run_runtime(controller=object())
        self.assertEqual(subject.main(), 2)


if __name__ == '__main__':
    unittest.main()
