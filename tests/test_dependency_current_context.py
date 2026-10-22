"""Current context construction from a real v6 gate over invented records.

No runtime continuation: captured validator policy is fixture-only, source files
are invented text, and supervisor dispatch is inert. No firmware/native access.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from tools import dependency_host_entry as host
from tools import dependency_operational_launcher as parent
from test_dependency_historical_outer import fixture


class CurrentContextTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.original=fixture(self.root)
        gate=ModuleType('_invented_current_context_gate')
        exec(compile(self.original['capture_buffers']['retained_gate'],
                     '<authored-gate-with-invented-policy>','exec'),vars(gate))
        with patch('builtins.open',side_effect=AssertionError('gate must not read')):
            self.validated=gate.validate_bundle_v6(
                self.original['legacy_documents'],
                expected_seal_sha256=self.original['legacy_expected_seal_sha256'],
                reference_pins=self.original['legacy_reference_pins'],
                expected_operation_id='1'*32,**self.original['historical_migration'])
        self.rows={}
        for name in sorted(parent.process.ROSTER):
            if name.startswith('bound.'):
                key=name[6:]
                path=Path(self.validated['inputs']['source_cache']['sources'][key]['path'])
                raw=self.validated['source_buffers'][key]
            else:
                path=self.root/'capture'/(name+'.py');raw=b'# invented non-executed source\n'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(raw)
            _,self.rows[name]=parent.entry.read_source(str(path))
        self.folder=self.root/'current-command';self.folder.mkdir()
        packet_path=self.folder/'packet.json';self.packet={'invented':True}
        packet_path.write_bytes(host.canonical(self.packet))
        _,packet_row=parent.entry.read_source(str(packet_path))
        self.request=dict(schema='disabled_operational_outer_request_v1',operation_id='1'*32,
            sources=copy.deepcopy(self.rows),packet=packet_row,folder=str(self.folder),
            argv_prefix=[sys.executable,'-I','-S','-B','-X','utf8','-c',parent.bootstrap()],
            expected_runtime={'executable':sys.executable},
            bootstrap_sha256=host.sha(parent.bootstrap().encode()),
            execution_authorized=False,camera_commands=[])
        self.request_path=self.folder/'request.json'

    def arguments(self):
        raw=host.canonical(self.request)
        return dict(request_bytes=raw,expected_request_sha256=host.sha(raw),
                    request_path=self.request_path,checked_source_rows=self.rows)

    def construct(self):
        return host.make_current_context(self.validated,**self.arguments())

    def test_current_context_keeps_twelve_fields_and_originals_without_io(self):
        before=copy.deepcopy((self.validated,self.request,self.rows,self.original))
        with (patch('builtins.open',side_effect=AssertionError('no reads')),
              patch.object(Path,'open',side_effect=AssertionError('no reads')),
              patch.object(parent.subprocess,'Popen',side_effect=AssertionError('no process'))):
            context=self.construct()
        self.assertEqual(before,(self.validated,self.request,self.rows,self.original))
        self.assertEqual(set(context),{'schema','session_dir','repository_root','operation_id',
            'execution_seal_sha256','basis','source_manifest','implementation_sha256',
            'ordinary_sha256','child_argv','deadline_seconds','limits'})
        self.assertEqual(context['schema'],'gdt_io_context_v1')
        self.assertEqual(context['basis'],self.validated['inputs']['basis'])
        self.assertEqual(context['source_manifest'],self.validated['inputs']['source_manifest'])
        self.assertEqual(context['execution_seal_sha256'],self.validated['seal_sha256'])
        self.assertEqual(context['child_argv'],self.request['argv_prefix']+
                         [str(self.request_path),self.arguments()['expected_request_sha256']])
        self.assertEqual((context['deadline_seconds'],context['limits']),(300,{'poll_seconds':0.05}))
        for role,name in [('candidate','activation-candidate.json'),('review','activation-review.json'),
                          ('decision','act-decision.json')]:
            self.assertEqual(context['ordinary_sha256'][self.validated['candidate']['session']+'/'+name],
                             self.validated['document_sha256'][role])

    def test_request_hash_and_duplicate_keys_refuse(self):
        args=self.arguments();args['expected_request_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'request_hash'):
            host.make_current_context(self.validated,**args)
        raw=b'{"operation_id":0,"operation_id":1}'
        args.update(request_bytes=raw,expected_request_sha256=host.sha(raw))
        with self.assertRaisesRegex(ValueError,'duplicate_key'):
            host.make_current_context(self.validated,**args)

    def test_changed_current_or_historical_operation_refuses_even_rehashed(self):
        for operation in ('2'*32,self.validated['historical_operation_id']):
            self.request['operation_id']=operation
            with self.subTest(operation=operation),self.assertRaisesRegex(ValueError,'operation'):
                self.construct()

    def test_source_receipt_drift_and_retained_rebinding_refuse(self):
        name=next(n for n in self.rows if n.startswith('bound.'))
        self.request['sources'][name]['size']+=1
        with self.assertRaisesRegex(ValueError,'sources'):self.construct()
        self.rows[name]['size']+=1
        with self.assertRaisesRegex(ValueError,'retained_source'):self.construct()

    def test_conflicting_path_hash_rejected_instead_of_overwriting(self):
        name=next(n for n in self.rows if n.startswith('bound.'))
        self.rows[name]['sha256']='0'*64
        self.request['sources']=copy.deepcopy(self.rows)
        with self.assertRaisesRegex(ValueError,'conflict'):self.construct()

    def test_changed_document_seal_refuses(self):
        self.validated['document_sha256']['seal']='0'*64
        with self.assertRaisesRegex(ValueError,'seal'):self.construct()

    def test_request_path_and_packet_path_must_belong_to_current_folder(self):
        args=self.arguments();args['request_path']=self.root/'other.json'
        with self.assertRaisesRegex(ValueError,'request_path'):
            host.make_current_context(self.validated,**args)
        self.request['packet']['path']=str(self.root/'elsewhere.json')
        with self.assertRaisesRegex(ValueError,'packet'):self.construct()

    def test_source_escape_and_parent_traversal_refuse(self):
        name=next(n for n in self.rows if not n.startswith('bound.'))
        for path in (self.root.parent/'outside.py',self.root/'capture'/'..'/'source.py'):
            self.rows[name]['path']=str(path);self.request['sources']=copy.deepcopy(self.rows)
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'path'):self.construct()

    def test_request_rehashed_bootstrap_drift_and_missing_isolation_refuse(self):
        original=copy.deepcopy(self.request)
        for index,value in ((7,'changed bootstrap'),(1,'-O')):
            self.request=copy.deepcopy(original);self.request['argv_prefix'][index]=value
            with self.subTest(index=index),self.assertRaisesRegex(ValueError,'argv'):self.construct()

    def test_complete_roster_and_exact_bootstrap_remain_explicit_caller_checks(self):
        name=next(n for n in self.rows if not n.startswith('bound.'))
        self.rows={name:self.rows[name]};self.request['sources']=copy.deepcopy(self.rows)
        self.construct()  # Binding agreement alone is not capture validation.
        with self.assertRaisesRegex(ValueError,'roster'):
            parent.validate_capture(buffers={},rows=self.rows,expected_hashes={})
        self.request['argv_prefix'][7]='# alternative body, never executed'
        self.request['bootstrap_sha256']=host.sha(self.request['argv_prefix'][7].encode())
        self.construct()  # Caller-selected bytes are not an approved bootstrap.
        with self.assertRaisesRegex(ValueError,'bootstrap'):parent.validate_request(self.request)

    def test_context_does_not_alias_mutable_input_metadata(self):
        context=self.construct();before=copy.deepcopy(context)
        self.validated['inputs']['basis']['new']='caller mutation'
        self.validated['inputs']['source_manifest']['sha256']='0'*64
        self.request['argv_prefix'][0]='changed'
        self.assertEqual(context,before)

    def test_existing_constructor_and_runtime_refusals_remain(self):
        with self.assertRaisesRegex(ValueError,'separate_execution_qualification'):
            host.make_context(self.validated)
        for call in (host.run_runtime,parent.run_runtime,parent.process.run_runtime):
            with self.assertRaisesRegex(ValueError,'real_activation_pending'):call()

    def test_parent_saved_checks_and_inert_supervisor_receive_current_context(self):
        raw=self.arguments()['request_bytes'];self.request_path.write_bytes(raw)
        context=self.construct()
        loader=SimpleNamespace(closed=False)
        def close_loader():
            if loader in sys.meta_path:sys.meta_path.remove(loader)
            loader.closed=True
        loader.close=close_loader
        records=SimpleNamespace(close=lambda:True)
        seen=[]
        def reserve_parent(**kw):seen.append(kw['context']);return records
        def run_parent_reserved(**kw):
            seen.append(kw['context'])
            return None,dict(status='inert-supervisor-handoff',host_exit_code=0)
        control=SimpleNamespace(reserve_parent=reserve_parent,run_parent_reserved=run_parent_reserved)
        plan=dict(request=self.request,request_bytes=raw,request_path=self.request_path,
            packet=self.packet,packet_bytes=host.canonical(self.packet),context=context,
            prepared={'operation_id':'1'*32},control=control,validation=loader)
        parent.check_saved(plan)
        with patch.object(parent.subprocess,'Popen',side_effect=AssertionError('must not launch')):
            result,ownership=parent._supervise(plan)
        self.assertEqual(result['status'],'inert-supervisor-handoff')
        self.assertEqual(seen,[context,context])
        self.assertTrue(ownership['parent_records_closed']);self.assertTrue(loader.closed)
        self.request_path.write_bytes(raw+b' ')
        with self.assertRaisesRegex(ValueError,'saved_request'):parent.check_saved(plan)


if __name__=='__main__':unittest.main(verbosity=2)
