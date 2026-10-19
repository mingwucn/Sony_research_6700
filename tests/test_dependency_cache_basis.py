"""Invented records only; no cache, installed dependency or actual receipts."""
import copy
import hashlib
import json
import unittest

from tools import dependency_cache_basis as subject
from tools import dependency_digest_diagnostic as diagnostic
from tools.dependency_evidence import EvidenceError
from test_dependency_digest_diagnostic import inputs
from test_dependency_legacy import encoded


def fixture():
    data = inputs()
    # Simulate two serializations of identical cache JSON, without reading files.
    cache = {'invented': 'inert text'}
    canonical = hashlib.sha256(encoded(cache) + b'\n').hexdigest()
    file_hash = hashlib.sha256(json.dumps(cache, indent=2).encode()).hexdigest()
    raw = json.loads(data['raw_json']); raw['cache_sha256'] = canonical
    data['raw_json'] = (encoded(raw) + b'\n').decode()
    data['declared_cache_file_sha256'] = file_hash
    result = diagnostic.compare_saved_dependency_digests(**data)
    pins = dict(core='a'*64, diagnostic='b'*64, failure='c'*64,
        config=hashlib.sha256(data['config_json'].encode()).hexdigest(),
        raw=hashlib.sha256(data['raw_json'].encode()).hexdigest())
    saved = dict(schema='saved_digest_diagnostic_v1', status='digest_localization_recorded',
        failed_attempt_sha256=pins['failure'], input_sha256=pins, localization=result,
        legacy_adapter_executed=False, cache_body_read=False, firmware_read=False,
        installed_dependency_executed=False, camera_commands=[])
    return dict(config_json=data['config_json'], raw_json=data['raw_json'],
        localization_json=(encoded(saved)+b'\n').decode(), core_sha256=pins['core'],
        diagnostic_sha256=pins['diagnostic'], original_failure_sha256=pins['failure'],
        cache_file_sha256=file_hash)


class CacheBasisTests(unittest.TestCase):
    def setUp(self): self.data = fixture()
    def run_basis(self): return subject.declare_cache_digest_domains(**self.data)
    def change_saved(self, change):
        saved = json.loads(self.data['localization_json']); change(saved)
        self.data['localization_json'] = (encoded(saved)+b'\n').decode()
    def refused(self):
        with self.assertRaises(EvidenceError): self.run_basis()

    def test_domains_are_preserved_and_self_report_is_never_independent(self):
        before = copy.deepcopy(self.data); out = self.run_basis(); self.assertEqual(before,self.data)
        self.assertEqual(out['file_bytes']['sha256'], self.data['cache_file_sha256'])
        self.assertEqual(out['legacy_cache_expectation_sha256'],
            json.loads(self.data['raw_json'])['cache_sha256'])
        self.assertNotEqual(out['file_bytes']['sha256'], out['legacy_cache_expectation_sha256'])
        self.assertEqual(out['blockers'], list(subject.BLOCKERS))
        for key, value in out.items():
            if type(value) is bool: self.assertIs(value,False,key)
        self.assertEqual(out['camera_commands'], [])

    def test_each_source_failure_and_input_cross_binding_is_required(self):
        for key in ['core_sha256','diagnostic_sha256','original_failure_sha256','cache_file_sha256']:
            with self.subTest(key=key):
                self.data=fixture(); self.data[key]='f'*64; self.refused()
        for key in ['config_json','raw_json']:
            with self.subTest(key=key):
                self.data=fixture(); self.data[key]+=' '; self.refused()

    def test_localization_equality_predicates_and_negative_claims_cannot_be_changed(self):
        for key in ['status','first_failing_digest_predicate','cache_content_revalidated',
                    'cache_content_change_proven','execution_authorized','whole_record_semantics_validated']:
            with self.subTest(key=key):
                self.data=fixture()
                self.change_saved(lambda s:s['localization'].update({key:True}))
                self.refused()
        self.data=fixture();self.change_saved(lambda s:s['localization']['comparisons'].reverse());self.refused()

    def test_outer_authority_unknown_fields_and_pin_roster_refused(self):
        for change in [lambda s:s.update(extra=True),lambda s:s.update(cache_body_read=True),
                lambda s:s.update(camera_commands=['invented']),
                lambda s:s['input_sha256'].update(extra='e'*64),
                lambda s:s.update(failed_attempt_sha256='f'*64)]:
            with self.subTest(change=change):
                self.data=fixture();self.change_saved(change);self.refused()

    def test_same_domain_equal_hashes_are_outside_this_correction_scope(self):
        self.data['cache_file_sha256']=json.loads(self.data['raw_json'])['cache_sha256']
        self.refused()

    def test_serialization_change_requires_new_bound_localization(self):
        self.data['config_json']=json.dumps(json.loads(self.data['config_json']),indent=2)
        self.refused()

    def test_duplicate_floating_nonfinite_and_overbound_metadata_refused(self):
        for value in ['{"a":1,"a":2}','{"a":1.1}','{"a":NaN}',' '*(4*1024**2+1)]:
            with self.subTest(value=value[:24]):
                self.data=fixture();self.data['localization_json']=value;self.refused()

    def test_rebound_changed_semantic_claim_still_cannot_prove_cache_content(self):
        # Even a consistently rebound declaration only labels the new claim.
        raw=json.loads(self.data['raw_json']);raw['cache_sha256']='f'*64
        self.data['raw_json']=(encoded(raw)+b'\n').decode()
        saved=json.loads(self.data['localization_json'])
        saved['input_sha256']['raw']=hashlib.sha256(self.data['raw_json'].encode()).hexdigest()
        saved['localization']=diagnostic.compare_saved_dependency_digests(
            config_json=self.data['config_json'],raw_json=self.data['raw_json'],
            declared_cache_file_sha256=self.data['cache_file_sha256'])
        self.data['localization_json']=(encoded(saved)+b'\n').decode()
        out=self.run_basis();self.assertFalse(out['independent_cache_expectation'])
        self.assertFalse(out['cache_content_revalidated']);self.assertEqual(out['legacy_cache_expectation_sha256'],'f'*64)


if __name__=='__main__': unittest.main()
