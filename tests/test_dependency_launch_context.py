"""Request refusal before owned validators or callbacks can run."""
import unittest
from unittest.mock import Mock
from tools import dependency_launch_context as subject


class LaunchBoundaryTests(unittest.TestCase):
    def test_original_byte_change_refuses_before_any_owned_code(self):
        metadata=Mock();adapter=Mock()
        with self.assertRaisesRegex(ValueError,'launch_original_request'):
            subject.validate_invented_launch(request_bytes=b'{"a":1}\n',
                expected_request_bytes_sha256=subject.sha(b'{"a":1}'),
                checked_sources={},context_arguments={},metadata_owner=metadata,adapter_owner=adapter)
        self.assertEqual(metadata.mock_calls,[])
        self.assertEqual(adapter.mock_calls,[])

    def test_duplicate_keys_refuse_before_any_owned_code(self):
        metadata=Mock();adapter=Mock();raw=b'{"operation_id":1,"operation_id":2}'
        with self.assertRaisesRegex(ValueError,'launch_duplicate_key'):
            subject.validate_invented_launch(request_bytes=raw,expected_request_bytes_sha256=subject.sha(raw),
                checked_sources={},context_arguments={},metadata_owner=metadata,adapter_owner=adapter)
        self.assertEqual(metadata.mock_calls,[])
        self.assertEqual(adapter.mock_calls,[])

    def test_request_nonfinite_and_oversize_refuse(self):
        for raw in (b'{"x":NaN}',b' '* (2*1024**2+1)):
            metadata=Mock();adapter=Mock()
            with self.subTest(size=len(raw)),self.assertRaises(ValueError):
                subject.validate_invented_launch(request_bytes=raw,expected_request_bytes_sha256=subject.sha(raw),
                    checked_sources={},context_arguments={},metadata_owner=metadata,adapter_owner=adapter)
            self.assertEqual(metadata.mock_calls,[])
            self.assertEqual(adapter.mock_calls,[])

    def test_public_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):
            subject.run_runtime()
