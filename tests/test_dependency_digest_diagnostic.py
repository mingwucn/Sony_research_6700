"""Invented records only; no cache body or actual saved input is read."""
import copy
import hashlib
import json
import unittest

from tools import dependency_digest_diagnostic as subject
from tools.dependency_evidence import EvidenceError
from test_dependency_legacy import fixture,encoded


def inputs():
    data=fixture()
    return dict(config_json=(encoded(data['config'])+b'\n').decode(),
        raw_json=data['raw_receipt_json'],declared_cache_file_sha256=data['expectation']['cache_sha256'])


class DigestDiagnosticTests(unittest.TestCase):
    def setUp(self):self.data=inputs()
    def change_raw(self,change):
        raw=json.loads(self.data['raw_json']);change(raw)
        self.data['raw_json']=(encoded(raw)+b'\n').decode()
    def run_comparison(self):return subject.compare_saved_dependency_digests(**self.data)

    def test_equal_digest_prefix_does_not_accept_events_or_legacy_comparison(self):
        before=copy.deepcopy(self.data);out=self.run_comparison();self.assertEqual(before,self.data)
        self.assertIsNone(out['first_failing_digest_predicate'])
        self.assertEqual(out['status'],'digest_prefix_equal_event_failure_unlocalized')
        for key in ['cache_content_change_proven','cache_content_revalidated','whole_record_semantics_validated',
            'legacy_comparison_retried','historical_events_authenticated','execution_authorized','feature_supported',
            'recovery_proven','device_write_gate_passed']:self.assertIs(out[key],False)
        self.assertEqual(out['camera_commands'],[])

    def test_config_file_formatting_is_not_a_canonical_digest_mismatch(self):
        self.data['config_json']=json.dumps(json.loads(self.data['config_json']),indent=2)+'\n'
        out=self.run_comparison();self.assertFalse(out['config_file_equals_canonical_digest'])
        self.assertTrue(out['comparisons'][0]['equal']);self.assertIsNone(out['first_failing_digest_predicate'])

    def test_cache_file_and_semantic_hash_can_differ_for_identical_json_data(self):
        cache=dict(schema='dependency_probe_source_cache_v1',sources=dict(invented='inert source text'))
        canonical=encoded(cache)+b'\n';pretty=(json.dumps(cache,indent=2)+'\n').encode()
        self.assertEqual(json.loads(canonical),json.loads(pretty))
        self.data['declared_cache_file_sha256']=hashlib.sha256(pretty).hexdigest()
        self.change_raw(lambda r:r.update(cache_sha256=hashlib.sha256(canonical).hexdigest()))
        out=self.run_comparison()
        self.assertEqual(out['first_failing_digest_predicate'],'raw_cache_equals_declared_cache_file_digest')
        self.assertFalse(out['cache_content_change_proven']);self.assertFalse(out['cache_content_revalidated'])

    def test_config_failure_precedes_cache_failure(self):
        self.change_raw(lambda r:r.update(config_sha256='f'*64,cache_sha256='e'*64))
        out=self.run_comparison();self.assertEqual(out['first_failing_digest_predicate'],'raw_config_equals_canonical_config')
        self.assertFalse(out['comparisons'][1]['equal']);self.assertFalse(out['comparisons'][2]['equal'])

    def test_vector_failure_after_consistently_rebound_config_digest(self):
        config=json.loads(self.data['config_json']);config['vectors'][0]['key_hex']='00'*16
        self.data['config_json']=(encoded(config)+b'\n').decode()
        self.change_raw(lambda r:r.update(config_sha256=hashlib.sha256(self.data['config_json'].encode()).hexdigest()))
        out=self.run_comparison();self.assertEqual(out['first_failing_digest_predicate'],'vector_plan_equals_reviewed_public_plan')

    def test_event_failure_is_not_silently_accepted_when_digest_prefix_matches(self):
        self.change_raw(lambda r:r.update(events=[]));out=self.run_comparison()
        self.assertIsNone(out['first_failing_digest_predicate']);self.assertFalse(out['whole_record_semantics_validated'])

    def test_unknown_duplicate_float_nonfinite_and_oversize_records_refused(self):
        for raw in ['{"schema":1,"schema":2}','{"x":1.2}','{"x":NaN}',' '*(4*1024**2+1)]:
            with self.subTest(raw=raw[:24]):
                self.data=inputs();self.data['raw_json']=raw
                with self.assertRaises(EvidenceError):self.run_comparison()
        self.data=inputs();self.change_raw(lambda r:r.update(extra=True))
        with self.assertRaises(EvidenceError):self.run_comparison()

    def test_operation_authority_and_digest_types_refused(self):
        for change in [lambda r:r.update(operation_id='b'*32),lambda r:r.update(feature_supported=True),
                lambda r:r.update(config_sha256=False),lambda r:r.update(cache_sha256='bad')]:
            with self.subTest(change=change):
                self.data=inputs();self.change_raw(change)
                with self.assertRaises(EvidenceError):self.run_comparison()


if __name__=='__main__':unittest.main()
