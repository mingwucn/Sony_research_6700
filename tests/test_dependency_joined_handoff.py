"""Joined synthetic preparation, genuine ordinary reservation and engine ownership.

Adapter projection, full metadata preflight, v6 gate, context checker, retained
control and helper ownership are real. Final dependency dispatch/collection and
callbacks are explicitly inert. Source refresh uses the existing fixture's
in-memory ordinary registry. No firmware, constants or native runtime is read.
The real gate algorithm uses regenerated ancestry/evidence policy for invented
records. Scoped alias removal is in-process setup, not observed child startup.
"""
import base64
from contextlib import contextmanager
import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
from tools import dependency_operational_child as process
import test_dependency_preparation_migration as migration_fixture
from test_dependency_retained_context import load_retained_checker, RETAINED_PATH, RETAINED_SHA256


FACTORY=migration_fixture.FACTORY.split(b'class ScopedCallbacks:')[0]+b'''class ScopedCallbacks:
 def __init__(self,**kw):self.calls=0;self.close_attempts=0;self.fail=False;self.close_fail=False
 def __call__(self,*a,**kw):
  self.calls+=1
  if self.fail:raise KeyboardInterrupt('invented callback interruption')
  return ('invented callback token',)
 def close(self):
  self.close_attempts+=1
  if self.close_fail:raise OSError('invented callback close interruption')
  return True
'''


@contextmanager
def without_tools_aliases():
    """Satisfy the unchanged child startup rule; restore exact prior objects."""
    prior={n:m for n,m in sys.modules.items() if n=='tools' or n.startswith('tools.')}
    for name in prior:del sys.modules[name]
    try:yield
    finally:
        unexpected={n:m for n,m in sys.modules.items() if n=='tools' or n.startswith('tools.')}
        for name in unexpected:del sys.modules[name]
        sys.modules.update(prior)
        if unexpected:raise AssertionError('synthetic child imported tools aliases')


class JoinedHandoffTests(unittest.TestCase):
    def setUp(self):
        self.checker=load_retained_checker()
        control=RETAINED_PATH.read_bytes()
        self.assertEqual(parent.sha(control),RETAINED_SHA256)
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        fixture=migration_fixture.MigrationPreparation()
        fixture.fixture_root=self.root;fixture.fixture_control=control
        fixture.fixture_factory=getattr(self,'fixture_factory',FACTORY)
        if hasattr(self,'fixture_ordinary_io'):fixture.fixture_ordinary_io=self.fixture_ordinary_io
        for name in ('fixture_basis','fixture_source_manifest','fixture_role_aliases','fixture_role_sources','fixture_wiring','fixture_prerequisites','fixture_binding_source','fixture_binding_plan','fixture_binding_schema','fixture_dependency_data'):
            if hasattr(self,name):setattr(fixture,name,getattr(self,name))
        fixture.setUp();self.addCleanup(fixture.doCleanups)
        self.fixture=fixture;self.original=fixture.prep
        self.validated=self.original._validate_gate()
        request=json.loads(self.original.request_bytes)
        self.folder=Path(request['folder']).parent;self.folder.mkdir(parents=True)
        self.buffers={role:self.original.source_owner.buffers[name] for name,role in process.OUTER.items()}
        self.buffers.update({role:self.original.adapter_owner.buffers[name]
            for name,role in self.original.source_owner.modules['dependency_adapter_sources'].BUFFER_KEYS.items()})
        self.buffers.update({role:raw for role,raw in self.original.checked_sources.items()
                             if role.startswith(('bound.','dependency.'))})
        self.buffers['outer_loader']=Path('tools/dependency_operational_sources.py').read_bytes()
        self.buffers['process_child']=Path('tools/dependency_operational_child.py').read_bytes()+getattr(self,'fixture_child_suffix',b'')
        self.assertEqual(set(self.buffers),process.ROSTER)
        paths={}
        binding=self.original.adapter_owner.modules['dependency_adapter_binding']
        for role,row in request['sources'].items():
            key=('adapter' if role in binding.ENTRIES else 'adapter_scope' if role=='adapter.scope_policy'
                 else 'adapter_comparison' if role=='adapter.comparison_contract' else role)
            paths[key]=self.root/row['path']
        self.rows={}
        for role,raw in self.buffers.items():
            path=paths.get(role,self.root/'capture'/(role+'.py'))
            self.write_new(path,raw)
            _,self.rows[role]=parent.entry.read_source(str(path))
        self.expected={n:parent.sha(raw) for n,raw in self.buffers.items()}
        docs=self.original.documents
        for name,row in self.validated['candidate']['inputs'].items():self.write_new(self.root/row['path'],docs['inputs'][name])
        for name,row in self.validated['inputs']['source_cache']['sources'].items():
            self.write_new(Path(row['path']),self.validated['source_buffers'][name])
        here=self.root/self.validated['candidate']['session']
        for name,filename in (('candidate','activation-candidate.json'),('review','activation-review.json'),
                              ('decision','act-decision.json'),('seal','execution-seal.json')):
            self.write_new(here/filename,docs[name])
        for name,row in self.validated['candidate']['bootstrap'].items():self.write_new(self.root/row['path'],name.encode())
        b64=lambda raw:base64.b64encode(raw).decode('ascii')
        self.packet=dict(schema='pending_operational_outer_packet_v2',
            documents={n:b64(docs[n]) for n in ('candidate','review','decision','seal')}|
                {'inputs':{n:b64(raw) for n,raw in docs['inputs'].items()}},
            reference_pins=self.original.reference_pins,seal_sha256=self.original.legacy_seal_sha256,
            request_bytes=b64(self.original.request_bytes),request_sha256=self.original.request_sha256,
            checked={n:b64(raw) for n,raw in self.original.checked_sources.items()},
            original_receipts=copy.deepcopy(self.original.original_receipts),
            ordinary={n:b64(raw) for n,raw in self.original.ordinary.items()},
            ordinary_receipts=copy.deepcopy(self.original.ordinary_receipts),repository_root=str(self.root),
            historical_migration={n:b64(v) if type(v) is bytes else v for n,v in self.original.historical_migration.items()})
        self.plan=self.prep=self.helpers=self.parent_records=self.child_records=None
        self.events=[];self.mode='complete'

    def write_new(self,path,raw):
        self.assertTrue(path.is_relative_to(self.root))
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():self.assertEqual(path.read_bytes(),raw)
        else:
            with path.open('xb') as stream:stream.write(raw)

    def prepare(self):
        self.plan=parent.prepare_synthetic_owned(folder=self.folder,packet=self.packet,
            buffers=self.buffers,rows=self.rows,expected_hashes=self.expected,runtime_profile={'executable':sys.executable})
        return self.plan

    def dispatch(self,**kw):
        self.events.append('inert_dispatch');self.helpers.intact()
        self.child_records=kw['records'].value
        self.assertFalse(self.child_records.closed)
        self.assertTrue(all(not handle.closed for handle in self.child_records.handles.values()))
        self.assertFalse(self.parent_records.closed)
        if self.mode=='dispatch_interrupt':raise KeyboardInterrupt('invented dispatch interruption')
        callback=self.prep.callback_lease.value
        callback.fail=self.mode=='callback_interrupt'
        callback.close_fail=self.mode=='callback_close_interrupt'
        self.assertEqual(kw['make_callbacks_after_receipt'](None,None,None),('invented callback token',))
        if self.mode=='partial_return':return {'inert':'incomplete'}
        kw['release_callbacks_after_controller']();kw['records'].close()
        return {'inert':'completed handoff'}

    def collect(self,**kw):
        self.events.append('inert_collection');self.helpers.intact()
        self.assertTrue(self.child_records.closed)
        if self.mode=='collection_interrupt':raise KeyboardInterrupt('invented collection interruption')
        return {'invented_completion_only':True}

    def engine(self, *, preexisting_child=False):
        plan=self.plan;outer=plan['outer'];adapter=plan['adapter'];args=plan['preflight_arguments']
        self.assertIs(self.checker.verify_context(plan['context']),True)
        self.parent_records=self.checker.reserve_parent(context=plan['context'])
        try:
            if preexisting_child:self.write_new(plan['context']['session_dir']/self.checker.CHILD_FILES[1],b'preserved child evidence')
            self.helpers=process.helper_owner(outer,self.buffers,self.rows,'child')
            cls=outer.modules['dependency_operational_preparation'].Preparation
            self.prep=cls(source_owner=outer,adapter_owner=adapter,
                **{n:args[n] for n in ('request_bytes','request_sha256','checked_sources','documents',
                    'original_receipts','ordinary','ordinary_receipts','prepared_repository_root','historical_migration')},
                legacy_seal_sha256=self.packet['seal_sha256'],reference_pins=self.packet['reference_pins'])
            dependency={n:self.buffers['dependency.'+n] for n in self.helpers.order}
            dependency['closure_manifest']=parent.encoded(plan['prepared']['sources'])
            return outer.modules['dependency_operational_entry']._continue_child(
                request=plan['prepared'],request_sha256=args['request_sha256'],checked_sources=plan['checked'],
                adapter_owner=adapter,helpers=self.helpers,dependency_source_buffers=dependency,
                runtime_wiring=SimpleNamespace(_dispatch_runtime=self.dispatch,_collect_completion=self.collect),
                preparation=self.prep,context=plan['context'],identity={'operation_id':plan['prepared']['operation_id']})
        finally:
            self.assertIs(self.parent_records.close(),True)

    @contextmanager
    def joined_scope(self):
        with without_tools_aliases():
            try:yield
            finally:
                if self.plan is not None:
                    for owner in (self.helpers,self.prep,self.plan['adapter'],self.plan['outer']):
                        if owner is not None and not owner.closed:owner.close()

    def assert_engine_closed(self):
        self.assertTrue(self.helpers.closed);self.assertTrue(self.prep.closed)
        self.assertTrue(self.plan['adapter'].closed)
        self.assertEqual(self.prep.callback_lease.value.close_attempts,1)
        self.assertTrue(self.parent_records.closed)
        self.assertTrue(all(handle.closed for handle in self.parent_records.handles.values()))
        if self.child_records is not None:
            self.assertTrue(self.child_records.closed)
            self.assertTrue(all(handle.closed for handle in self.child_records.handles.values()))
        self.plan['outer'].intact()
        self.assertFalse(any(n.startswith('_a6700_successor') or n in
            ('_successor_binding','_successor_control','_successor_factory','gdt_preflight') for n in sys.modules))

    def test_joined_real_preflight_context_control_and_helper_handoff(self):
        with self.joined_scope():
            plan=self.prepare();result=self.engine()
            self.assertEqual(plan['preflight']['schema'],'pending_operational_preflight_v2')
            self.assertFalse(plan['preflight']['execution_bootstrap_qualified'])
            self.assertEqual(result['engine_result'],{'inert':'completed handoff'})
            self.assertEqual(result['completion_evidence'],{'invented_completion_only':True})
            for name in ('execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','production_runtime_qualified'):
                self.assertIs(result[name],False)
            self.assertEqual(self.events,['inert_dispatch','inert_collection'])
            self.assertEqual(self.prep.callback_lease.value.calls,1);self.assert_engine_closed()

    def test_projection_refusal_closes_both_source_owners_before_outputs(self):
        self.packet['checked'][next(iter(self.packet['checked']))]=base64.b64encode(b'# changed\n').decode()
        owners=[];original=process.owners
        def capture(buffers):
            pair=original(buffers);owners.extend(pair);return pair
        with self.joined_scope(),patch.object(process,'owners',side_effect=capture):
            with self.assertRaisesRegex(ValueError,'operational_process_projection'):self.prepare()
            self.assertTrue(all(owner.closed for owner in owners));self.assertEqual(list(self.folder.iterdir()),[])

    def test_full_metadata_preflight_refuses_rehashed_ordinary_drift(self):
        raw=b'{"invented":"changed activity scope"}'
        self.packet['ordinary']['activity_scope']=base64.b64encode(raw).decode()
        self.packet['ordinary_receipts']['activity_scope']={'bytes':len(raw),'sha256':parent.sha(raw)}
        with self.joined_scope():
            with self.assertRaises(ValueError):self.prepare()
            self.assertEqual(list(self.folder.iterdir()),[])

    def test_returned_preflight_receipts_are_detached_from_original_packet(self):
        with self.joined_scope():
            plan=self.prepare();before=copy.deepcopy(plan['preflight_arguments']['original_receipts'])
            self.packet['original_receipts']['candidate']['sha256']='0'*64
            self.packet['ordinary_receipts'].clear()
            self.assertEqual(plan['preflight_arguments']['original_receipts'],before)
            result=plan['outer'].modules['dependency_operational_metadata'].validate_pending(**plan['preflight_arguments'])
            self.assertEqual(result,plan['preflight'])

    def test_disk_drift_retains_partial_outputs_and_closes_source_owners(self):
        Path(self.rows['process_child']['path']).write_bytes(b'# changed on disk\n')
        owners=[];original=process.owners
        def capture(buffers):
            pair=original(buffers);owners.extend(pair);return pair
        with self.joined_scope(),patch.object(process,'owners',side_effect=capture):
            with self.assertRaisesRegex(ValueError,'saved_source'):self.prepare()
            self.assertTrue(all(owner.closed for owner in owners))
            self.assertEqual({p.name for p in self.folder.iterdir()},{'packet.json','request.json'})

    def test_genuine_partial_child_reservation_preserves_files_and_cleans_owners(self):
        opened=[];original=Path.open
        def tracked(path,*args,**kwargs):
            handle=original(path,*args,**kwargs)
            if args and args[0]=='xb' and path.name in self.checker.CHILD_FILES:opened.append(handle)
            return handle
        with self.joined_scope():
            plan=self.prepare()
            with patch.object(Path,'open',tracked),self.assertRaises(ValueError) as caught:self.engine(preexisting_child=True)
            self.assertEqual((caught.exception.stage,caught.exception.reason),
                             ('record_reservation','exclusive_reservation_failed'))
            self.assertEqual(self.events,[]);self.assert_engine_closed()
            self.assertTrue(opened and all(handle.closed for handle in opened))
            here=plan['context']['session_dir']
            self.assertEqual((here/self.checker.CHILD_FILES[1]).read_bytes(),b'preserved child evidence')
            self.assertTrue((here/self.checker.CHILD_FILES[0]).exists())

    def test_dispatch_interruption_closes_real_records_and_all_transferred_owners(self):
        self.mode='dispatch_interrupt'
        with self.joined_scope():
            self.prepare()
            with self.assertRaisesRegex(KeyboardInterrupt,'invented dispatch interruption'):self.engine()
            self.assert_engine_closed();self.assertEqual(self.prep.callback_lease.value.calls,0)

    def test_callback_interruption_preserves_primary_and_cleans_once(self):
        self.mode='callback_interrupt'
        with self.joined_scope():
            self.prepare()
            with self.assertRaisesRegex(KeyboardInterrupt,'invented callback interruption'):self.engine()
            self.assert_engine_closed();self.assertEqual(self.prep.callback_lease.value.calls,1)

    def test_callback_close_failure_does_not_retry_or_suppress_other_cleanup(self):
        self.mode='callback_close_interrupt'
        with self.joined_scope():
            self.prepare()
            with self.assertRaisesRegex(OSError,'invented callback close interruption'):self.engine()
            self.assert_engine_closed();self.assertFalse(self.prep.callback_lease.closed)

    def test_partial_engine_return_cannot_claim_completion(self):
        self.mode='partial_return'
        with self.joined_scope():
            self.prepare()
            with self.assertRaisesRegex(ValueError,'operational_child_incomplete'):self.engine()
            self.assert_engine_closed();self.assertEqual(self.events,['inert_dispatch'])

    def test_collection_interruption_closes_after_real_record_release(self):
        self.mode='collection_interrupt'
        with self.joined_scope():
            self.prepare()
            with self.assertRaisesRegex(KeyboardInterrupt,'invented collection interruption'):self.engine()
            self.assert_engine_closed();self.assertEqual(self.events,['inert_dispatch','inert_collection'])


if __name__=='__main__':unittest.main(verbosity=2)
