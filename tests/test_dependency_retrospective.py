"""Invented metadata only; no private records, sources or native dependencies."""
import copy
import json
import unittest

from tools import dependency_evidence as core
from tools import dependency_legacy as legacy
from tools import dependency_retrospective as subject
from test_dependency_legacy import fixture, rebind, encoded


def inputs():
    data = fixture()
    policy = data.pop('expectation')
    data['producer_sha256'] = dict(subject.PRODUCERS)
    data['completion']['runtime_source_sha256'] = subject.PRODUCERS['runtime']
    data['cache_sha256'] = policy['cache_sha256']
    return data


class RetrospectiveTests(unittest.TestCase):
    def setUp(self):
        self.data = inputs()

    def refused(self):
        with self.assertRaises(core.EvidenceError):
            subject.reconcile_legacy_metadata(**self.data)

    def test_composed_comparison_preserves_all_legacy_blockers_and_transcripts(self):
        before = copy.deepcopy(self.data)
        result = subject.reconcile_legacy_metadata(**self.data)
        self.assertEqual(self.data, before)
        self.assertEqual(result['status'], 'retrospective_consistency_with_blockers')
        self.assertEqual(result['envelope']['original_raw_receipt_json'], self.data['raw_receipt_json'])
        self.assertEqual(result['envelope']['original_journal_jsonl'], self.data['journal_jsonl'])
        self.assertEqual(result['blockers'], list(legacy.BLOCKERS) + list(subject.EXTRA_BLOCKERS))
        for key, value in result.items():
            if type(value) is bool:
                self.assertIs(value, False, key)
        self.assertEqual(result['camera_commands'], [])

    def test_root_tokens_explicitly_label_paths_without_claiming_directory_observation(self):
        result = subject.reconcile_legacy_metadata(**self.data)
        roots = result['envelope']['expectation']['roots']
        for domain, path in [('package','X:/fixtures/venv/Lib/site-packages'), ('runtime','Y:/fixtures/runtime')]:
            self.assertEqual(roots[domain]['identity_sha256'], core._hash(dict(
                schema='retrospective_path_label_v1', domain=domain, path=path)))
        self.assertIn('not_directory_identity', result['expectation_basis']['root_tokens'])

    def test_derived_output_is_detached(self):
        out = subject.reconcile_legacy_metadata(**self.data)
        out['envelope']['config']['source_rows'].clear()
        self.assertEqual(len(self.data['config']['source_rows']), 11)

    def test_config_digest_is_canonical_plus_newline(self):
        out = subject.reconcile_legacy_metadata(**self.data)
        import hashlib
        wanted = hashlib.sha256(encoded(self.data['config']) + b'\n').hexdigest()
        self.assertEqual(out['envelope']['expectation']['config_sha256'], wanted)
        self.assertNotEqual(wanted, hashlib.sha256(json.dumps(self.data['config'],indent=2).encode()).hexdigest())

    def test_declared_producer_substitutions_and_unknown_sources_refused(self):
        for alias in subject.PRODUCERS:
            with self.subTest(alias=alias):
                self.data = inputs(); self.data['producer_sha256'][alias] = 'f'*64; self.refused()
        self.data = inputs();self.data['producer_sha256']['extra'] = 'f'*64;self.refused()
        self.data = inputs();self.data['producer_sha256'].pop('continuation');self.refused()

    def test_completion_runtime_cannot_disagree_with_declared_profile(self):
        self.data['completion']['runtime_source_sha256'] = 'f'*64;self.refused()

    def test_cache_digest_declaration_binds_raw_but_never_validates_cache_content(self):
        self.data['cache_sha256'] = 'f'*64;self.refused()

    def test_package_origin_hash_changes_not_derived_from_later_claims(self):
        self.data['config']['source_rows']['Cryptodome.Cipher.AES']['sha256'] = 'f'*64
        raw = json.loads(self.data['raw_receipt_json'])
        raw['source_origins'] = copy.deepcopy(self.data['config']['source_rows'])
        import hashlib
        raw['config_sha256'] = hashlib.sha256(encoded(self.data['config'])+b'\n').hexdigest()
        rebind(self.data,raw);self.refused()

    def test_trusted_receipt_path_cannot_escape_fixed_runtime_relative_path(self):
        raw = json.loads(self.data['raw_receipt_json'])
        raw['trusted_origins']['platform']['path'] = 'Z:\\other\\platform.py'
        rebind(self.data, raw); self.refused()

    def test_root_change_without_corresponding_origins_refused(self):
        for domain in ['package','runtime']:
            with self.subTest(domain=domain):
                self.data = inputs()
                if domain == 'package': self.data['config']['package_root'] = 'Z:\\other\\Cryptodome'
                else:
                    rows=[json.loads(x) for x in self.data['journal_jsonl'].splitlines()]
                    rows[0]['data']['startup']['base_prefix'] = 'Z:\\other'
                    self.data['journal_jsonl']=''.join(encoded(x).decode()+'\n' for x in rows)
                self.refused()

    def test_wrong_leaf_missing_members_and_shape_injections_refused(self):
        for change in ['leaf','package','completion','raw','journal','config']:
            with self.subTest(change=change):
                self.data = inputs()
                if change=='leaf':self.data['config']['package_root']='X:\\other\\Wrong'
                elif change=='package':self.data['package']['installed_receipts'].pop('Cryptodome/Cipher/AES.py')
                elif change=='completion':self.data['completion']['feature_supported']=True
                elif change=='raw':self.data['raw_receipt_json']='{}'
                elif change=='journal':self.data['journal_jsonl']='{}\n'
                else:self.data['config']['unknown']=True
                self.refused()

    def test_duplicate_json_float_nonfinite_and_blank_journal_refused(self):
        for text in ['{"a":1,"a":2}', '{"a":1.2}', '{"a":NaN}']:
            with self.subTest(text=text):
                self.data=inputs();self.data['raw_receipt_json']=text;self.refused()
        self.data=inputs();self.data['journal_jsonl']+='\n';self.refused()

    def test_manifest_and_proof_must_recompute(self):
        self.data['package']['installed_proof']['files']['Cryptodome/Cipher/AES.py']['size']+=1
        self.refused()

    def test_raw_anchor_and_journal_cannot_be_silently_rebuilt(self):
        self.data['raw_receipt_json']+=' ';self.refused()

    def test_trusted_identity_changes_without_matching_receipt_stamps_refused(self):
        raw=json.loads(self.data['raw_receipt_json'])
        raw['trusted_origins']['platform']['lstat_before']['inode']+=1
        rebind(self.data,raw);self.refused()

    def test_vector_and_source_native_rosters_still_enforced(self):
        for key in ['vectors','source_rows','native_rows','trusted_origins']:
            with self.subTest(key=key):
                self.data=inputs()
                if key=='vectors':self.data['config'][key][0]['key_hex']='00'*16
                else:self.data['config'][key].pop(next(iter(self.data['config'][key])))
                self.refused()

    def test_representation_limits_still_apply(self):
        self.data['raw_receipt_json']=' '*(4*1024**2+1);self.refused()

    def test_custom_objects_cannot_supply_mutable_metadata(self):
        class Custom(dict): pass
        self.data['producer_sha256']=Custom(subject.PRODUCERS);self.refused()


if __name__ == '__main__':
    unittest.main()
