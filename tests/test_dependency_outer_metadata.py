"""Original gate bytes must bind before any downstream validator executes."""
import copy
import unittest
from unittest.mock import Mock, patch
from tools import dependency_outer_metadata as subject


def fixture():
    e=subject.e
    inputs={'q_snapshot_log':b'invented qualification log\n'}
    inputs.update({n:e.encoded({'invented':True}) for n in subject.current.BASIS})
    candidate={'operation_id':'1'*32,'repository_root':'D:/invented/fixture',
        'inputs':{n:dict(bytes=len(v),sha256=e.sha(v)) for n,v in inputs.items()}}
    docs=dict(candidate=e.encoded(candidate),review=b'{}',decision=b'{}',seal=b'{}',inputs=inputs)
    all_raw={n:docs[n] for n in ('candidate','review','decision','seal')}
    all_raw.update({'input:'+n:v for n,v in inputs.items()})
    receipts={n:dict(bytes=len(v),sha256=e.sha(v)) for n,v in all_raw.items()}
    request=e.encoded(dict(operation_id='1'*32))
    arguments=dict(request_bytes=request,expected_request_bytes_sha256=e.sha(request),
        ordinary_buffers=dict(inputs),context_arguments=dict(ordinary_buffers=dict(inputs)))
    return dict(outer_documents=docs,expected_outer_receipts=receipts,
        validated=dict(candidate=copy.deepcopy(candidate),inputs={n:e.strict(v) for n,v in inputs.items() if n!='q_snapshot_log'},
            document_sha256={n:e.sha(docs[n]) for n in ('candidate','review','decision','seal')},seal_sha256=e.sha(docs['seal'])),
        prepared_request_bytes=request,prepared_request_sha256=e.sha(request),prepared_repository_root='D:/invented',
        arguments=arguments,metadata_owner=Mock(),adapter_owner=Mock())


class OuterOriginalBoundaryTests(unittest.TestCase):
    def refuses(self,change,code):
        args=fixture();change(args)
        with patch.object(subject.current,'validate_invented_current',side_effect=AssertionError('late validator')) as downstream:
            with self.assertRaisesRegex(ValueError,code):subject.validate_invented_outer(**args)
            downstream.assert_not_called()
        self.assertEqual(args['adapter_owner'].mock_calls,[])
        self.assertEqual(args['metadata_owner'].mock_calls,[])

    def test_original_gate_document_whitespace_drift(self):
        self.refuses(lambda a:a['outer_documents'].__setitem__('review',b'{} '),'current_original_bytes')

    def test_validated_candidate_substitution(self):
        self.refuses(lambda a:a['validated']['candidate'].__setitem__('operation_id','2'*32),'outer_metadata_candidate')

    def test_reanchored_document_bytes_cannot_replace_validated_gate(self):
        for name in ('candidate','review','decision','seal'):
            def change(a):
                raw=a['outer_documents'][name]+b' '
                a['outer_documents'][name]=raw
                a['expected_outer_receipts'][name]=dict(bytes=len(raw),sha256=subject.e.sha(raw))
            with self.subTest(name=name):self.refuses(change,'outer_metadata_document_binding')

    def test_independent_validated_seal_hash_must_agree(self):
        self.refuses(lambda a:a['validated'].__setitem__('seal_sha256','0'*64),'outer_metadata_seal_binding')

    def test_input_roster_drift(self):
        self.refuses(lambda a:a['validated']['inputs'].__setitem__('other',{}),'outer_metadata_input_roster')

    def test_supplied_receipt_cannot_replace_gate_original(self):
        def change(a):
            name='basis';raw=a['outer_documents']['inputs'][name]+b' '
            a['outer_documents']['inputs'][name]=raw
            a['expected_outer_receipts']['input:'+name]=dict(bytes=len(raw),sha256=subject.e.sha(raw))
        self.refuses(change,'outer_metadata_gate_input_bytes')

    def test_log_original_is_checked_even_without_parsed_gate_entry(self):
        def change(a):
            raw=b'invented other log\n';a['outer_documents']['inputs']['q_snapshot_log']=raw
            a['expected_outer_receipts']['input:q_snapshot_log']=dict(bytes=len(raw),sha256=subject.e.sha(raw))
        self.refuses(change,'outer_metadata_gate_input_bytes')

    def test_request_original_whitespace_drift(self):
        self.refuses(lambda a:a.__setitem__('prepared_request_bytes',a['prepared_request_bytes']+b' '),'outer_metadata_prepared_request')

    def test_caller_cannot_supply_path_conversion(self):
        self.refuses(lambda a:a['arguments'].__setitem__('source_frames',{}),'outer_metadata_arguments')

    def test_different_operation_request(self):
        def change(a):
            raw=subject.e.encoded(dict(operation_id='2'*32));digest=subject.e.sha(raw)
            a.update(prepared_request_bytes=raw,prepared_request_sha256=digest)
            a['arguments'].update(request_bytes=raw,expected_request_bytes_sha256=digest)
        self.refuses(change,'outer_metadata_operation')

    def test_retained_basis_must_be_exact_original(self):
        self.refuses(lambda a:a['arguments']['ordinary_buffers'].__setitem__('basis',b'{}'),'outer_metadata_retained_input')

    def test_runtime_stays_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()
