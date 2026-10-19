"""Invented 351-file package/receipts; no installed or native input reads."""
import copy
import stat
import unittest
from unittest.mock import patch

from tools import dependency_package_preflight as subject
from tools import dependency_producer as producer
from tools import dependency_evidence as core
from test_dependency_producer import fixture, refresh


def complete_fixture():
    data, ops = fixture(); policy = data['expectation']
    for index, (relative, receipt) in enumerate(data['package']['installed_receipts'].items()):
        path = policy['roots']['package']['path']+'/'+relative
        if path in ops.contents: continue
        raw = ('invented package data '+relative).encode('ascii')
        metadata = dict(device=7, inode=10000+index, mode=stat.S_IFREG | 0o600,
            nlink=1, size=len(raw), mtime_ns=1234, ctime_ns=5678, file_attributes=0)
        receipt = dict(path=relative, size=len(raw), sha256=producer.sha(raw), opened_read_only=True,
            **{k: dict(metadata) for k in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after')})
        data['package']['installed_receipts'][relative] = receipt
        ops.contents[path] = raw; ops.observed[path] = dict(copy.deepcopy(receipt), path=path)
    refresh(data)
    return data, ops


class PackageCollectionTests(unittest.TestCase):
    def execute(self, data, ops): return subject.collect_invented(ops=ops, **data)

    def test_reads_all_351_and_five_trusted_without_any_bootstrap(self):
        data, ops = complete_fixture(); before = copy.deepcopy(data)
        with patch.object(ops, 'bootstrap', side_effect=AssertionError('bootstrap prohibited')), \
             patch.object(ops, 'audit_install', side_effect=AssertionError('hook not needed')):
            result = self.execute(data, ops)
        self.assertEqual(data, before)
        self.assertEqual((result['package_reads'], result['trusted_reads'], len(ops.reads)), (351, 5, 356))
        self.assertEqual((ops.loader_calls, ops.callback_calls, ops.cipher_calls), (0, 0, 0))
        self.assertEqual(len(result['source_aliases']), 11)
        self.assertEqual(result['prior_package_sha256'], core._hash(data['package']))
        self.assertEqual(result['observed_package_sha256'], core._hash(result['package']))
        for key in ('dependency_bootstrap_performed', 'actual_installation_observed', 'atomic_snapshot_proven',
                    'execution_authorized', 'operational_acceptance', 'feature_supported', 'recovery_proven', 'device_write_gate_passed'):
            self.assertIs(result[key], False)
        self.assertIs(result['test_injection_used'], True); self.assertEqual(result['camera_commands'], [])

    def test_absolute_opened_paths_and_relative_projections_both_preserved(self):
        data, ops = complete_fixture(); result = self.execute(data, ops)
        for relative, receipt in result['absolute_receipts'].items():
            self.assertEqual(receipt['path'], data['expectation']['roots']['package']['path']+'/'+relative)
            projected = result['package']['installed_receipts'][relative]
            self.assertEqual(projected['path'], relative)
            self.assertEqual(dict(projected, path=receipt['path']), receipt)
            self.assertEqual(result['relative_projection'][relative],
                dict(absolute_receipt_sha256=core._hash(receipt), relative_receipt_sha256=core._hash(projected)))

    def test_unused_package_member_change_is_detected(self):
        data, ops = complete_fixture(); path = next(p for p in ops.contents if '/data/item' in p)
        ops.contents[path] += b'changed'
        with self.assertRaisesRegex(core.EvidenceError, '^fresh_bytes$'): self.execute(data, ops)

    def test_unused_member_receipt_identity_change_is_detected(self):
        data, ops = complete_fixture(); path = next(p for p in ops.contents if '/data/item' in p)
        for name in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'):
            ops.observed[path][name]['inode'] += 1
        with self.assertRaisesRegex(core.EvidenceError, '^expected_identity$'): self.execute(data, ops)

    def test_missing_unused_member_does_not_fall_back_to_filesystem(self):
        data, ops = complete_fixture(); path = next(p for p in ops.contents if '/data/item' in p)
        del ops.contents[path]
        with self.assertRaises(KeyError): self.execute(data, ops)

    def test_preload_source_hash_mismatch_stops_before_any_observation(self):
        data, ops = complete_fixture(); data['source_buffers']['runtime'] += b'changed'
        with self.assertRaisesRegex(core.EvidenceError, '^source_hash$'): self.execute(data, ops)
        self.assertEqual(ops.reads, []); self.assertEqual(ops.root_calls, 0)

    def test_root_substitution_stops_before_any_file_read(self):
        data, ops = complete_fixture(); ops.root_action = lambda op, row: dict(row, path='Z:/changed')
        with self.assertRaisesRegex(core.EvidenceError, '^root_identity$'): self.execute(data, ops)
        self.assertEqual(ops.reads, [])

    def test_root_change_at_end_refuses_complete_collection(self):
        data, ops = complete_fixture()
        ops.root_action = lambda op, row: dict(row, path='Z:/changed') if op.root_calls > 2 else row
        with self.assertRaisesRegex(core.EvidenceError, '^root_changed$'): self.execute(data, ops)
        self.assertEqual(len(ops.reads), 356)

    def test_trusted_byte_change_is_detected(self):
        data, ops = complete_fixture(); row = data['expectation']['trusted_origins']['ctypes']
        ops.contents[producer.target(data['expectation'], row)] += b'changed'
        with self.assertRaisesRegex(core.EvidenceError, '^fresh_bytes$'): self.execute(data, ops)

    def test_concrete_read_bound_is_not_silently_increased(self):
        data, ops = complete_fixture(); relative = next(p for p in data['package']['installed_receipts'] if '/data/item' in p)
        row = data['package']['installed_receipts'][relative]; row['size'] = 8*1024**2+1
        for name in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'): row[name]['size'] = row['size']
        refresh(data)
        with self.assertRaisesRegex(core.EvidenceError, '^package_read_bound$'): self.execute(data, ops)
        self.assertEqual((ops.root_calls, ops.reads), (0, []))

    def test_oversized_trusted_origin_refuses_before_any_observation(self):
        data, ops = complete_fixture(); row = data['expectation']['trusted_origins']['ctypes']
        row['size'] = 8*1024**2+1; row['identity']['size'] = row['size']; refresh(data)
        with self.assertRaisesRegex(core.EvidenceError, '^package_read_bound$'): self.execute(data, ops)
        self.assertEqual((ops.root_calls, ops.reads), (0, []))

    def mutation_case(self, trusted):
        data, ops = complete_fixture(); original = ops.reader
        target = producer.target(data['expectation'], data['expectation']['trusted_origins']['ctypes']) if trusted else next(iter(ops.contents))
        calls = []
        def read(path, expected):
            calls.append(path)
            if path != target: return original(path, expected)
            raw = ops.contents[path]+b'rebound'; receipt = copy.deepcopy(ops.observed[path])
            expected.update(size=len(raw), sha256=producer.sha(raw)); expected['identity']['size'] = len(raw)
            receipt.update(size=len(raw), sha256=producer.sha(raw))
            for key in ('lstat_before', 'fstat_before', 'fstat_after', 'lstat_after'): receipt[key]['size'] = len(raw)
            return raw, receipt
        ops.reader = read
        with self.assertRaisesRegex(core.EvidenceError, '^fresh_bytes$'): self.execute(data, ops)
        self.assertEqual(calls[-1], target)

    def test_trusted_observer_cannot_rebind_expected_bytes(self): self.mutation_case(True)

    def test_package_observer_cannot_rebind_expected_bytes(self): self.mutation_case(False)

    def test_observer_receipts_are_detached_before_next_read(self):
        data, ops = complete_fixture(); shared = {}; original = ops.reader
        def read(path, expected):
            raw, receipt = original(path, expected); shared.clear(); shared.update(receipt)
            return raw, shared
        ops.reader = read; result = self.execute(data, ops)
        self.assertEqual(len({r['path'] for r in result['absolute_receipts'].values()}), 351)
        shared.clear(); self.assertEqual(len(result['trusted_origins']['ctypes']), 8)

    def test_new_receipt_proof_is_distinct_from_frozen_prior_package(self):
        data, ops = complete_fixture(); path = next(p for p in ops.observed if '/data/item' in p)
        # Different per-API ctime observations do not alter cross-API identity.
        ops.observed[path]['fstat_before']['ctime_ns'] += 1
        ops.observed[path]['fstat_after']['ctime_ns'] += 1
        result = self.execute(data, ops)
        self.assertNotEqual(result['prior_package_sha256'], result['observed_package_sha256'])
        self.assertEqual(result['package']['manifest'], data['package']['manifest'])

    def test_wrong_receipt_path_cannot_be_silently_relabelled(self):
        data, ops = complete_fixture(); original = ops.reader
        def read(path, expected):
            raw, receipt = original(path, expected); receipt['path'] = 'Z:/unrelated'
            return raw, receipt
        ops.reader = read
        with self.assertRaisesRegex(core.EvidenceError, '^receipt_binding$'): self.execute(data, ops)

    def test_reader_exception_is_not_retried(self):
        data, ops = complete_fixture(); calls = []
        def read(path, expected): calls.append(path); raise OSError('invented read failure')
        ops.reader = read
        with self.assertRaisesRegex(OSError, 'invented read failure'): self.execute(data, ops)
        self.assertEqual(len(calls), 1)

    def test_real_runtime_and_subclass_refuse_before_read(self):
        data, _ = complete_fixture()
        class Derived(producer.RuntimeOps): pass
        for ops in (producer.RuntimeOps(), Derived()):
            with self.subTest(kind=type(ops).__name__), self.assertRaisesRegex(core.EvidenceError, '^real_activation_pending$'):
                self.execute(data, ops)

    def test_ordinary_cli_refuses(self):
        with patch('builtins.print') as out: self.assertEqual(subject.main(), 2)
        self.assertIn('real_activation_pending', out.call_args.args[0])


if __name__ == '__main__': unittest.main()
