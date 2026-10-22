"""Shared command preparation with invented metadata and an inert child only.

No adapter projection, operational preflight, runtime callbacks or firmware is
executed. The actual v6 parent/child routes remain separately refused.
"""
import base64
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
import test_dependency_current_context as current_fixture
from test_dependency_retained_context import load_retained_checker, materialize_invented_context


class PreparationContextTests(unittest.TestCase):
    def setUp(self):
        self.fixture=current_fixture.CurrentContextTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.folder=self.fixture.root/'prepared-command';self.folder.mkdir()
        self.rows=copy.deepcopy(self.fixture.rows)
        self.buffers={n:Path(row['path']).read_bytes() for n,row in self.rows.items()}
        self.expected={n:parent.sha(raw) for n,raw in self.buffers.items()}
        self.runtime={'executable':sys.executable}
        self.prepared={'operation_id':'1'*32,'folder':str(self.folder/'composition')}
        original=self.fixture.original
        documents=original['legacy_documents']
        b64=lambda raw:base64.b64encode(raw).decode('ascii')
        migration={n:b64(v) if type(v) is bytes else v
                   for n,v in original['historical_migration'].items()}
        # Inner runtime packet fields stay invented and are not qualified here.
        self.packet=dict(schema='pending_operational_outer_packet_v2',
            documents={n:b64(documents[n]) for n in ('candidate','review','decision','seal')}|
                {'inputs':{n:b64(raw) for n,raw in documents['inputs'].items()}},
            reference_pins=original['legacy_reference_pins'],seal_sha256=self.fixture.validated['seal_sha256'],
            checked={},original_receipts={},ordinary={},ordinary_receipts={},
            repository_root=str(self.fixture.root),historical_migration=migration)
        self.refresh_prepared()

    def refresh_prepared(self):
        raw=parent.encoded(self.prepared)
        self.packet.update(request_bytes=base64.b64encode(raw).decode('ascii'),request_sha256=parent.sha(raw))

    def prepare(self):
        return parent.prepare_synthetic_context(folder=self.folder,packet=self.packet,
            validated=self.fixture.validated,buffers=self.buffers,rows=self.rows,
            expected_hashes=self.expected,runtime_profile=self.runtime)

    def test_shared_saved_command_has_no_executable_owner_and_passes_real_checker(self):
        checker=load_retained_checker()
        materialize_invented_context(self.fixture)
        before=copy.deepcopy((self.fixture.validated,self.packet,self.rows,self.runtime))
        with (patch.object(parent.process,'owners',side_effect=AssertionError('no source execution')),
              patch.object(parent,'BootstrapOwner',side_effect=AssertionError('no bootstrap')),
              patch.object(parent.process,'helper_owner',side_effect=AssertionError('no helpers')),
              patch.object(parent.subprocess,'Popen',side_effect=AssertionError('no child'))):
            plan=self.prepare()
            self.assertIs(checker.verify_context(plan['context']),True)
        self.assertEqual(before,(self.fixture.validated,self.packet,self.rows,self.runtime))
        self.assertEqual(set(plan),{'folder','packet','packet_bytes','request','request_bytes',
            'request_path','prepared','context'})
        self.assertEqual(len(plan['context']),12)
        self.assertFalse(plan['request']['execution_authorized'])
        self.assertEqual(plan['request']['camera_commands'],[])
        parent.check_saved(plan)

    def test_omitted_capture_role_refuses_before_new_files(self):
        self.buffers.pop(next(iter(self.buffers)))
        with self.assertRaisesRegex(ValueError,'operational_launch_roster'):self.prepare()
        self.assertEqual(list(self.folder.iterdir()),[])

    def test_capture_rehash_cannot_replace_retained_source(self):
        role=next(n for n in self.rows if n.startswith('bound.'))
        raw=self.buffers[role]+b'# drift\n';self.buffers[role]=raw
        self.rows[role].update(size=len(raw),sha256=parent.sha(raw));self.expected[role]=parent.sha(raw)
        with self.assertRaisesRegex(ValueError,'operational_launch_retained'):self.prepare()
        self.assertEqual(list(self.folder.iterdir()),[])

    def test_wrong_operation_or_folder_refuses_before_new_files(self):
        for key,value in (('operation_id','9'*32),('folder',str(self.folder/'different'))):
            before=dict(self.prepared);self.prepared[key]=value;self.refresh_prepared()
            with self.subTest(key=key),self.assertRaises(ValueError):self.prepare()
            self.assertEqual(list(self.folder.iterdir()),[])
            self.prepared=before;self.refresh_prepared()

    def test_rehashed_packet_documents_cannot_drift_from_gate_result(self):
        for role in ('candidate','inputs'):
            packet=copy.deepcopy(self.packet)
            if role=='inputs':self.packet['documents']['inputs'].pop(next(iter(self.packet['documents']['inputs'])))
            else:self.packet['documents'][role]=base64.b64encode(b'{}').decode('ascii')
            with self.subTest(role=role),self.assertRaisesRegex(ValueError,'gate_documents'):self.prepare()
            self.assertEqual(list(self.folder.iterdir()),[]);self.packet=packet

    def test_existing_packet_is_preserved_and_no_request_is_created(self):
        path=self.folder/'packet.json';path.write_bytes(b'preserved invented file')
        with self.assertRaises(FileExistsError):self.prepare()
        self.assertEqual(path.read_bytes(),b'preserved invented file')
        self.assertFalse((self.folder/'request.json').exists())

    def test_existing_request_preserved_with_partial_packet_and_no_retry(self):
        path=self.folder/'request.json';path.write_bytes(b'preserved invented request')
        with patch.object(parent,'write',wraps=parent.write) as writes:
            with self.assertRaises(FileExistsError):self.prepare()
        self.assertEqual([call.args[0].name for call in writes.call_args_list],['packet.json','request.json'])
        self.assertEqual(path.read_bytes(),b'preserved invented request')
        self.assertEqual((self.folder/'packet.json').read_bytes(),parent.encoded(self.packet))

    def test_source_drift_before_prepare_refuses_at_fresh_saved_check(self):
        path=Path(next(iter(self.rows.values()))['path']);path.write_bytes(b'# changed before preparation\n')
        with patch.object(parent,'write',wraps=parent.write) as writes:
            with self.assertRaisesRegex(ValueError,'saved_source'):self.prepare()
        self.assertEqual([call.args[0].name for call in writes.call_args_list],['packet.json','request.json'])
        self.assertEqual({p.name for p in self.folder.iterdir()},{'packet.json','request.json'})
        self.assertEqual(path.read_bytes(),b'# changed before preparation\n')

    def test_saved_source_drift_refuses(self):
        plan=self.prepare();Path(next(iter(self.rows.values()))['path']).write_bytes(b'# changed\n')
        with self.assertRaisesRegex(ValueError,'saved_source'):parent.check_saved(plan)

    def test_saved_packet_drift_refuses(self):
        plan=self.prepare();(self.folder/'packet.json').write_bytes(plan['packet_bytes']+b' ')
        with self.assertRaisesRegex(ValueError,'saved_packet'):parent.check_saved(plan)

    def test_saved_request_drift_refuses(self):
        plan=self.prepare();plan['request_path'].write_bytes(plan['request_bytes']+b' ')
        with self.assertRaisesRegex(ValueError,'saved_request'):parent.check_saved(plan)

    def test_self_rehashed_replacement_bootstrap_still_refuses(self):
        plan=self.prepare();request=plan['request'];request['argv_prefix'][7]='# alternative never executed'
        request['bootstrap_sha256']=parent.sha(request['argv_prefix'][7].encode())
        plan['request_bytes']=parent.encoded(request);plan['request_path'].write_bytes(plan['request_bytes'])
        plan['context']['child_argv']=request['argv_prefix']+[str(plan['request_path']),parent.sha(plan['request_bytes'])]
        with self.assertRaisesRegex(ValueError,'operational_launch_bootstrap'):parent.check_saved(plan)

    def test_plan_metadata_is_detached_from_callers(self):
        plan=self.prepare();before=copy.deepcopy(plan)
        self.rows.clear();self.runtime['executable']='changed';self.packet['checked']['changed']=True
        self.prepared['operation_id']='4'*32
        self.assertEqual(plan,before);parent.check_saved(plan)

    def test_existing_bootstrap_transports_saved_request_to_inert_child(self):
        raw=b'''import json,sys
def child(request,packet,buffers,rows):
 print(json.dumps(dict(status='invented-child-received',operation_id=request['operation_id'],
  source_count=len(buffers),packet_schema=packet['schema'],camera_commands=[])))
 return 0
'''
        path=Path(self.rows['process_child']['path']);path.write_bytes(raw)
        self.buffers['process_child'],self.rows['process_child']=parent.entry.read_source(str(path))
        self.expected['process_child']=parent.sha(raw)
        profile=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',parent.PROFILE],
            capture_output=True,check=True,timeout=15)
        self.runtime=json.loads(profile.stdout)
        plan=self.prepare();parent.check_saved(plan)
        result=subprocess.run(plan['context']['child_argv'],capture_output=True,timeout=15)
        self.assertEqual((result.returncode,result.stderr),(0,b''))
        observed=json.loads(result.stdout)
        self.assertEqual(observed,dict(status='invented-child-received',operation_id='1'*32,
            source_count=49,packet_schema='pending_operational_outer_packet_v2',camera_commands=[]))


if __name__=='__main__':unittest.main(verbosity=2)
