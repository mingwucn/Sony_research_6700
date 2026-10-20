"""Invented pending records; protected/materialization/runtime seams intercepted."""
import copy
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

from tools import dependency_operational_metadata as m
from tools import dependency_operational_sources as s
import test_dependency_operational_entry as entry_tests


def texts():
    prior = Path('private/sessions/20261019-RA-003-parent-evidence-v5/outer')
    return {n:Path('tools/dependency_parent.py').read_bytes() if n == 'parent_verifier' else
            (prior/('outer_gate.py' if n == 'retained_gate' else 'ordinary_io.py')).read_bytes()
            if n in ('retained_gate','ordinary_io') else Path('tools',n+'.py').read_bytes()
            for n in s.ROSTER}


def build_records(request, checked, originals, outer):
    operation = request['operation_id']
    def row(schema, **kw):
        return m.encoded(dict(schema=schema, operation_id=operation, camera_commands=[], **kw))
    ordinary = {n:originals['inputs'][n] for n in m.RETAINED}
    original_rows = m.receipts({n:originals[n] for n in ('candidate','review','decision','seal')} |
        {'input:'+n:b for n,b in originals['inputs'].items()})
    closure = m.encoded(request['sources'])
    ordinary['authored_source_manifest'] = row('pending_operational_sources_v1',
        prepared_sources=request['sources'], outer_sources=outer,
        derived=dict(closure_manifest=dict(kind='canonical_prepared_source_map_v1',
            bytes=len(closure),sha256=m.sha(closure))))
    ordinary['authored_source_receipts'] = row('pending_operational_source_byte_claims_v1',
        manifest_sha256=m.sha(ordinary['authored_source_manifest']),
        prepared=m.receipts(checked),outer=outer,source_reads_observed=False)
    ordinary['dependency_packet'] = m.encoded(request['dependency_packet'])
    ordinary['dependency_fixed'] = m.encoded(request['dependency_fixed'])
    from tools import dependency_operational_scope as policy
    ordinary['activity_scope'] = row('pending_operational_scope_v1',
        purpose='prepare_only_no_operational_act',request_bytes_sha256=m.sha(m.encoded(request)),
        limits=policy.SCOPE,originals=original_rows,
        sources_sha256=m.sha(ordinary['authored_source_manifest']),historical_blockers=list(policy.HISTORY))
    ordinary['activity_rights'] = row('pending_operational_rights_v1',
        scope_sha256=m.sha(ordinary['activity_scope']),owner_facts=policy.OWNER,
        decisions=dict.fromkeys(policy.RIGHTS,'pending'),legal_basis_established=False,execution_authorized=False)
    ordinary['historical_evidence_index'] = row('pending_operational_history_v1',
        purpose='comparison_only',original_inputs=m.receipts(originals['inputs']))
    ordinary['qualification_index'] = row('pending_operational_consistency_index_v1',
        ordinary=m.receipts(ordinary),checked_roles=sorted(policy.ORDINARY_INPUTS),
        execution_authenticated=False,freshness_verified=False)
    return ordinary, original_rows


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.case = entry_tests.EntryTests('test_child_metadata_before_dispatch_and_once_owned_lifetime')
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.texts = texts()
        self.owner = s.OuterSources(buffers=self.texts,hashes={n:m.sha(b) for n,b in self.texts.items()}).load()
        self.addCleanup(lambda: None if self.owner.closed else self.owner.close())
        f = self.case
        for name,role in (('dependency_successor_wiring','successor_wiring'),
                          ('dependency_successor_sources','namespace'),
                          ('ordinary_io','ordinary_io'),
                          ('parent_verifier','dependency.dependency_parent')):
            f.buffers[role]=self.texts[name]
            f.request['sources'][role].update(bytes=len(self.texts[name]),sha256=m.sha(self.texts[name]))
        # Rebind the derived dependency closure and packet after these source
        # additions; fixture() supplies a fresh consistent packet and buffers.
        from test_dependency_producer import refresh
        f.data['source_buffers']['closure_manifest']=m.encoded(f.request['sources'])
        f.data['expectation']['source_sha256']={n:m.sha(b) for n,b in f.data['source_buffers'].items()}
        refresh(f.data)
        f.request['dependency_packet']['inputs'] = {n:v for n,v in f.data.items() if n != 'source_buffers'}
        f.request['dependency_fixed']['expectation_sha256']=m.sha(m.encoded(f.data['expectation']))
        f.digest=m.sha(m.encoded(f.request))
        source_cache = {n.removeprefix('bound.'):dict(path=str(Path.cwd()/f.request['sources'][n]['path']),
             bytes=len(b),sha256=m.sha(b)) for n,b in f.buffers.items() if n.startswith('bound.')}
        inputs = {n:m.encoded(dict(invented_value=n)) for n in m.RETAINED}
        inputs['source_cache'] = m.encoded(dict(sources=source_cache))
        inputs['q_snapshot_log'] = b'invented raw log\r\n'
        candidate = dict(operation_id=f.request['operation_id'],repository_root=str(Path.cwd()),
            inputs={n:dict(bytes=len(b),sha256=m.sha(b)) for n,b in inputs.items()})
        self.docs = dict(candidate=m.encoded(candidate),review=b'{"invented":"review"}',
            decision=b'{"invented":"decision"}',seal=b'{"invented":"seal"}',inputs=inputs)
        self.validated = dict(candidate=candidate,inputs={n:m.strict(b) for n,b in inputs.items() if n != 'q_snapshot_log'},
            document_sha256={n:m.sha(self.docs[n]) for n in ('candidate','review','decision','seal')},
            seal_sha256=m.sha(self.docs['seal']),source_buffers={n.removeprefix('bound.'):b for n,b in f.buffers.items() if n.startswith('bound.')})
        self.ordinary,self.original_rows = build_records(f.request,f.buffers,self.docs,self.owner.receipts())
        self.prep = self.owner.modules['dependency_operational_preparation'].Preparation(
            source_owner=self.owner,adapter_owner=f.owner,request_bytes=m.encoded(f.request),
            request_sha256=f.digest,checked_sources=f.buffers,documents=self.docs,
            original_receipts=self.original_rows,ordinary=self.ordinary,
            ordinary_receipts=m.receipts(self.ordinary),legacy_seal_sha256=m.sha(self.docs['seal']),
            reference_pins={'invented':'a'*64},prepared_repository_root=str(Path.cwd()))
        self.addCleanup(lambda: None if self.prep.closed else self.prep.close())
        self.events = []
        def gate():self.events.append('gate');return self.validated
        def refresh(v):self.events.append('refresh');return dict(v['source_buffers']),{}
        def materialize(v,fresh):self.events.append('materialize');return {'control':f.control},None,f.callbacks
        # Only qualification replaces these instance seams. Production methods
        # are fixed authored-source calls, with no packet-supplied selectors.
        self.prep._validate_gate = Mock(side_effect=gate)
        self.prep._refresh = Mock(side_effect=refresh)
        self.prep._materialize = Mock(side_effect=materialize)

    def arguments(self):
        return self.prep.arguments(self.validated)

    def test_owned_graph_and_pending_preflight_recompute_from_originals(self):
        result = self.owner.modules['dependency_operational_metadata'].validate_pending(**self.arguments())
        self.assertEqual(result['checked_roles'],sorted(self.ordinary))
        self.assertEqual(result['original_receipts'],self.original_rows)
        for n in m.FLAGS:self.assertIs(result[n],False)
        raw=m.encoded(result)
        self.assertTrue(self.owner.modules['dependency_operational_preparation'].verify_saved_preflight(
            source_owner=self.owner,raw=raw,expected_sha256=m.sha(raw),arguments=self.arguments()))

    def test_child_engine_consumes_one_preparation_and_reserved_control(self):
        args=self.case.args();args['preparation']=self.prep
        result=self.owner.modules['dependency_operational_entry']._continue_child(**args)
        self.assertEqual(result['engine_result'],{'engine':'intercepted'})
        self.assertEqual(self.events,['gate','refresh','materialize'])
        self.assertEqual(self.case.events,['reserve','dispatch'])
        self.case.control.reserve_child.assert_called_once()
        self.case.records.close.assert_called_once()
        self.assertTrue(self.prep.closed)
        self.owner.intact()  # Separate outer owner outlives engine-owned scopes.
        with self.assertRaisesRegex(ValueError,'operational_preparation_reentry'):self.prep.prepare()

    def test_original_raw_log_change_refuses_before_refresh_materialization(self):
        self.prep.documents['inputs']['q_snapshot_log'] += b'changed'
        with self.assertRaisesRegex(ValueError,'operational_original_bytes'):self.prep.prepare()
        self.prep._refresh.assert_not_called();self.prep._materialize.assert_not_called()

    def test_retained_basis_change_refuses_even_with_rebound_ordinary_receipt(self):
        self.prep.ordinary['basis']=b'{"changed":true}'
        self.prep.ordinary_receipts=m.receipts(self.prep.ordinary)
        with self.assertRaisesRegex(ValueError,'operational_retained_original'):self.prep.prepare()
        self.prep._materialize.assert_not_called()

    def test_pending_records_cannot_claim_rights_source_reads_or_new_role(self):
        cases=(('activity_rights','execution_authorized',True,'operational_rights_pending'),
               ('authored_source_receipts','source_reads_observed',True,'operational_source_claim_mode'),
               ('activity_scope','purpose','execute_now','operational_scope'))
        for name,key,value,code in cases:
            with self.subTest(name=name):
                args=self.arguments();args['ordinary']=dict(args['ordinary'])
                record=m.strict(args['ordinary'][name]);record[key]=value
                args['ordinary'][name]=m.encoded(record)
                args['ordinary_receipts']=m.receipts(args['ordinary'])
                with self.assertRaisesRegex(ValueError,code):m.validate_pending(**args)

    def test_source_origin_mismatch_refuses_before_fresh_open(self):
        self.validated['inputs']['source_cache']['sources']['role:core']['path'] += '.elsewhere'
        # Keep original input parsing bound; original candidate hashes cannot be
        # rewritten in-place under the separately supplied original receipts.
        with self.assertRaisesRegex(ValueError,'operational_original_parsed'):self.prep.prepare()
        self.prep._refresh.assert_not_called()

    def test_preparation_failure_cleanup_is_owned_by_engine_and_not_retried(self):
        self.prep._refresh.side_effect=KeyboardInterrupt('ordinary refresh interrupted')
        args=self.case.args();args['preparation']=self.prep
        with self.assertRaisesRegex(KeyboardInterrupt,'ordinary refresh interrupted'):
            self.owner.modules['dependency_operational_entry']._continue_child(**args)
        self.assertTrue(self.prep.closed)
        self.case.control.reserve_child.assert_not_called()
        self.prep._materialize.assert_not_called()
        self.case.helper.close.assert_called_once()

    def test_post_materialization_mutation_refuses_and_closes_callbacks_once(self):
        module=self.owner.modules['dependency_operational_metadata']
        original=module.FLAGS
        def materialize(*args):
            module.FLAGS=()
            return {'control':self.case.control},None,self.case.callbacks
        self.prep._materialize.side_effect=materialize
        args=self.case.args();args['preparation']=self.prep
        try:
            with self.assertRaisesRegex(ValueError,'operational_outer_live_code'):
                self.owner.modules['dependency_operational_entry']._continue_child(**args)
        finally:
            module.FLAGS=original
        self.case.callbacks.close.assert_called_once_with()
        self.case.control.reserve_child.assert_not_called()
        self.assertTrue(self.prep.closed)

    def test_callback_cleanup_failure_still_removes_bootstrap_aliases_without_retry(self):
        from types import ModuleType
        alias='_preparation_cleanup_test'
        module=ModuleType(alias);sys.modules[alias]=module
        self.addCleanup(lambda:sys.modules.pop(alias,None))
        self.prep.bootstrap_modules['test']=module
        self.prep.prepare()
        self.case.callbacks.close.side_effect=OSError('callback release interrupted')
        with self.assertRaisesRegex(OSError,'callback release interrupted'):self.prep.close()
        self.assertNotIn(alias,sys.modules)
        self.case.callbacks.close.assert_called_once_with()
        with self.assertRaisesRegex(ValueError,'operational_preparation_reclose'):self.prep.close()
        self.case.callbacks.close.assert_called_once_with()

    def test_saved_extra_claim_or_rebound_originals_cannot_pass(self):
        expected=m.validate_pending(**self.arguments())
        for change in ('extra','originals','authority'):
            result=copy.deepcopy(expected)
            if change=='extra':result['extra']='claimed'
            elif change=='originals':result['original_receipts']['candidate']['sha256']='0'*64
            else:result['execution_authorized']=True
            raw=m.encoded(result)
            with self.subTest(change=change),self.assertRaisesRegex(ValueError,'operational_saved_preflight'):
                m.verify_saved(raw=raw,expected_sha256=m.sha(raw),**self.arguments())

    def test_live_owned_preparation_class_mutation_refuses(self):
        cls=self.owner.modules['dependency_operational_preparation'].Preparation
        original=cls.prepare
        try:
            cls.prepare=lambda self:None
            with self.assertRaisesRegex(ValueError,'operational_outer_live_code'):self.owner.intact()
        finally:cls.prepare=original

    def parent_arguments(self):
        args=self.case.parent_args()
        args.pop('runtime_wiring')
        preflight=m.validate_pending(**self.arguments())
        raw=m.encoded(preflight)
        return dict(source_owner=self.owner,raw=raw,expected_sha256=m.sha(raw),
                    preflight_arguments=self.arguments(),**args)

    def test_parent_preflight_refusal_closes_without_engine_dispatch(self):
        args=self.parent_arguments()
        saved=m.strict(args['raw']);saved['execution_authorized']=True
        args['raw']=m.encoded(saved);args['expected_sha256']=m.sha(args['raw'])
        module=self.owner.modules['dependency_operational_preparation']
        with self.assertRaisesRegex(ValueError,'operational_saved_preflight'):
            module.reconcile_saved_parent(**args)
        self.case.helper.close.assert_called_once()
        self.assertTrue(self.case.owner.closed)
        self.owner.intact()

    def test_parent_separate_source_owner_survives_engine_teardown(self):
        args=self.parent_arguments()
        # Intercept the underlying helper verifier rather than replacing the
        # owned wiring function or its frozen module globals.
        self.case.helper.verify=Mock(return_value={'saved':'intercepted'})
        result=self.owner.modules['dependency_operational_preparation'].reconcile_saved_parent(**args)
        self.assertEqual(result['engine_result'],{'saved':'intercepted'})
        self.case.helper.verify.assert_called_once()
        self.case.helper.close.assert_called_once()
        self.assertTrue(self.case.owner.closed)
        self.owner.intact()

    def test_parent_closed_owner_refuses_and_cleans_transferred_inputs(self):
        args=self.parent_arguments()
        function=self.owner.modules['dependency_operational_preparation'].reconcile_saved_parent
        self.owner.close()
        with self.assertRaisesRegex(ValueError,'operational_outer_inactive'):function(**args)
        self.case.helper.close.assert_called_once_with()
        self.assertTrue(self.case.owner.closed)

    def test_parent_changed_engine_never_executes_before_ownership_check(self):
        args=self.parent_arguments()
        module=self.owner.modules['dependency_operational_entry']
        original=module.OnceClose
        replacement=Mock(side_effect=AssertionError('untrusted engine executed'))
        module.OnceClose=replacement
        try:
            with self.assertRaisesRegex(ValueError,'operational_outer_live_code'):
                self.owner.modules['dependency_operational_preparation'].reconcile_saved_parent(**args)
        finally:module.OnceClose=original
        replacement.assert_not_called()
        self.case.helper.close.assert_called_once_with()
        self.assertTrue(self.case.owner.closed)


class SourceTests(unittest.TestCase):
    def test_complete_graph_checked_before_any_execution(self):
        buffers=texts();buffers[s.ORDER[-1]]+=b'\nfrom tools import unexpected\n'
        with patch('builtins.exec',side_effect=AssertionError('must not execute')):
            with self.assertRaisesRegex(ValueError,'operational_outer_edges'):
                s.OuterSources(buffers=buffers,hashes={n:m.sha(b) for n,b in buffers.items()})

    def test_compiled_or_buffer_replacement_refuses_before_execution(self):
        for kind in ('compiled','buffer'):
            buffers=texts();owner=s.OuterSources(buffers=buffers,hashes={n:m.sha(b) for n,b in buffers.items()})
            if kind=='compiled':owner.compiled[s.ORDER[0]]=compile('raise AssertionError()', '<wrong>', 'exec')
            else:owner.buffers[s.ORDER[0]]+=b'\n'
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'operational_outer_policy'):owner.load()
            self.assertTrue(owner.closed)

    def test_no_aliases_or_installed_dependencies_loaded(self):
        before=dict(sys.modules);buffers=texts()
        owner=s.OuterSources(buffers=buffers,hashes={n:m.sha(b) for n,b in buffers.items()}).load()
        self.assertFalse(any(n.startswith('_disabled_outer') for n in sys.modules))
        self.assertFalse(any(n not in before and n.split('.')[0] in ('Crypto','Cryptodome','ctypes','_ctypes') for n in sys.modules))
        self.assertTrue(owner.close())
        self.assertIsNone(owner.policy)
        self.assertEqual(owner.compiled,{})

    def test_all_public_runtimes_and_clis_refuse(self):
        for name in ('dependency_operational_metadata','dependency_operational_preparation','dependency_operational_sources'):
            result=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8',str(Path('tools',name+'.py').resolve()),'--activate'],capture_output=True,timeout=10)
            self.assertEqual((result.returncode,result.stdout,result.stderr),(2,b'',b''))


if __name__=='__main__':
    unittest.main()
