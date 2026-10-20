"""Invented v2 transport; real captured gate/metadata, no runtime continuation."""
import base64
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from tools import dependency_operational_child as child
from tools import dependency_operational_launcher as parent
from tools import dependency_observation_launcher as observation
from tools import dependency_operational_metadata as metadata
import test_dependency_preparation_migration as preparation_tests
from test_dependency_observation_legacy import fixture as legacy_fixture


def wire(value):
    return {n:base64.b64encode(v).decode('ascii') if type(v) is bytes else v
            for n,v in value.items()}


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.case=preparation_tests.MigrationPreparation('test_real_gate_metadata_refresh_and_materializer_complete')
        self.case.setUp();self.addCleanup(self.case.doCleanups)
        self.prep=self.case.prep
        p=self.prep
        b64=lambda b:base64.b64encode(b).decode('ascii')
        self.packet=dict(schema='pending_operational_outer_packet_v2',
            documents={n:b64(p.documents[n]) for n in ('candidate','review','decision','seal')}|
                {'inputs':{n:b64(b) for n,b in p.documents['inputs'].items()}},
            reference_pins=p.reference_pins,seal_sha256=p.legacy_seal_sha256,
            request_bytes=b64(p.request_bytes),request_sha256=p.request_sha256,
            checked={n:b64(b) for n,b in p.checked_sources.items()},
            original_receipts=p.original_receipts,ordinary={n:b64(b) for n,b in p.ordinary.items()},
            ordinary_receipts=p.ordinary_receipts,repository_root=p.prepared_repository_root,
            historical_migration=wire(p.historical_migration))
        self.decoded=child.decode_packet(self.packet)

    def validated(self):
        return child.validate_gate(self.packet,self.decoded,self.prep.source_owner)

    def test_complete_wire_reaches_real_v6_gate_and_metadata(self):
        value=self.validated()
        args=child.preflight_arguments(self.packet,self.decoded,self.prep.source_owner,self.prep.adapter_owner,value)
        self.assertEqual(args['historical_migration'],self.prep.historical_migration)
        result=metadata.validate_pending(**args)
        self.assertEqual(result['schema'],'pending_operational_preflight_v2')
        self.assertFalse(result['execution_bootstrap_qualified'])
        for flag in metadata.FLAGS:self.assertIs(result[flag],False)
        raw=metadata.encoded(result)
        self.assertTrue(metadata.verify_saved(raw=raw,expected_sha256=metadata.sha(raw),**args))

    def test_rehashed_saved_false_migration_claim_refuses(self):
        args=child.preflight_arguments(self.packet,self.decoded,self.prep.source_owner,self.prep.adapter_owner,self.validated())
        result=metadata.validate_pending(**args)
        result['historical_migration']['context']['sha256']='0'*64
        raw=metadata.encoded(result)
        with self.assertRaisesRegex(ValueError,'operational_saved_preflight'):
            metadata.verify_saved(raw=raw,expected_sha256=metadata.sha(raw),**args)

    def test_wire_returns_detached_immutable_handoff(self):
        result=child.packet_migration(self.packet)
        self.packet['historical_migration']['expected_context_sha256']='0'*64
        self.assertEqual(result,self.prep.historical_migration)
        self.assertIs(type(result['context_bytes']),bytes)

    def test_missing_unknown_and_downgraded_packet_fields_refuse(self):
        for mode in ('missing','extra','downgrade'):
            packet=copy.deepcopy(self.packet)
            if mode=='missing':packet.pop('historical_migration')
            elif mode=='extra':packet['unknown']=False
            else:packet['schema']='pending_operational_outer_packet_v1'
            with self.subTest(mode=mode),self.assertRaisesRegex(ValueError,'operational_process_packet'):
                child.decode_packet(packet)

    def test_bad_wire_pins_types_and_bounds_refuse(self):
        for mode in ('extra','pin','empty','context_bound','proof_bound','base64','mutable'):
            packet=copy.deepcopy(self.packet);value=packet['historical_migration']
            if mode=='extra':value['extra']=False
            elif mode=='pin':value['expected_context_sha256']='0'*64
            elif mode=='empty':value['context_bytes']=''
            elif mode in ('context_bound','proof_bound'):
                name='context' if mode=='context_bound' else 'ancestry_proof'
                raw=b'x'*(16385 if name=='context' else 65537)
                value[name+'_bytes']=base64.b64encode(raw).decode('ascii')
                value['expected_'+name+'_sha256']=metadata.sha(raw)
            elif mode=='base64':value['context_bytes']='!'
            else:value['context_bytes']=bytearray(b'x')
            with self.subTest(mode=mode),self.assertRaises((ValueError,TypeError)):
                child.decode_packet(packet)

    def test_fully_dropped_migration_keeps_legacy_cross_operation_refusal(self):
        packet=copy.deepcopy(self.packet);packet.pop('historical_migration')
        packet['schema']='pending_operational_outer_packet_v1'
        decoded=child.decode_packet(packet)
        with self.assertRaisesRegex(ValueError,'operation_binding'):
            child.validate_gate(packet,decoded,self.prep.source_owner)

    def test_rehashed_wrong_historical_context_refuses_real_gate(self):
        packet=copy.deepcopy(self.packet);migration=child.packet_migration(packet)
        value=json.loads(migration['context_bytes']);value['operation_id']='6'*32
        raw=metadata.encoded(value)
        migration.update(context_bytes=raw,expected_context_sha256=metadata.sha(raw))
        packet['historical_migration']=wire(migration)
        with self.assertRaises(ValueError):child.validate_gate(packet,child.decode_packet(packet),self.prep.source_owner)

    def test_current_operation_must_still_match_candidate(self):
        packet=copy.deepcopy(self.packet);request=json.loads(self.prep.request_bytes)
        request['operation_id']='7'*32;raw=metadata.encoded(request)
        packet.update(request_bytes=base64.b64encode(raw).decode('ascii'),request_sha256=metadata.sha(raw))
        with self.assertRaisesRegex(ValueError,'operation_binding'):
            child.validate_gate(packet,child.decode_packet(packet),self.prep.source_owner)

    def owner_proxies(self):
        outer=SimpleNamespace(modules=self.prep.source_owner.modules,
            receipts=self.prep.source_owner.receipts,closed=False)
        original=self.prep.adapter_owner
        adapter=SimpleNamespace(modules=original.modules,buffers=original.buffers,
            intact=original.intact,closed=False)
        for owner in (outer,adapter):
            owner.close=Mock(side_effect=lambda o=owner:setattr(o,'closed',True))
        return outer,adapter

    def test_parent_validates_then_stops_before_outputs_or_bootstrap(self):
        outer,adapter=self.owner_proxies()
        folder=Path(json.loads(self.prep.request_bytes)['folder']).parent
        with patch.object(parent,'validate_capture'),patch.object(child,'owners',return_value=(outer,adapter)), \
             patch.object(child,'check_packet',return_value=self.decoded),patch.object(parent,'check_retained'), \
             patch.object(parent,'write',side_effect=AssertionError('no writes')) as write, \
             patch.object(parent,'BootstrapOwner',side_effect=AssertionError('no bootstrap')) as boot, \
             patch.object(parent.subprocess,'run',side_effect=AssertionError('no process')) as profile, \
             patch.object(child,'helper_owner',side_effect=AssertionError('no helpers')) as helper:
            with self.assertRaisesRegex(ValueError,'operational_process_v6_execution_pending'):
                parent._prepare_pending(folder=folder,packet=self.packet,buffers={},rows={},expected_hashes={})
        for spy in (write,boot,profile,helper):spy.assert_not_called()
        outer.close.assert_called_once();adapter.close.assert_called_once()

    def test_child_validates_then_stops_before_helpers_or_protected_prepare(self):
        outer,adapter=self.owner_proxies()
        prepared=self.decoded[2];request=dict(operation_id=prepared['operation_id'],folder=str(Path(prepared['folder']).parent))
        buffers=dict.fromkeys(child.ROSTER,b'pass\n');rows=dict.fromkeys(child.ROSTER,{})
        with patch.object(child,'sys',SimpleNamespace(modules={})), \
             patch.object(child,'owners',return_value=(outer,adapter)), \
             patch.object(child,'check_packet',return_value=self.decoded), \
             patch.object(child,'helper_owner',side_effect=AssertionError('no helpers')) as helper:
            with self.assertRaisesRegex(ValueError,'operational_process_v6_execution_pending'):
                child.child(request,self.packet,buffers,rows)
        helper.assert_not_called()
        self.assertFalse(self.prep.started);self.assertFalse(self.prep.bootstrap_modules)
        outer.close.assert_called_once();adapter.close.assert_called_once()


class ProjectionTests(unittest.TestCase):
    def test_projection_preserves_original_v1_and_adds_only_closed_v2_handoff(self):
        arguments=legacy_fixture();root=Path.cwd()
        old=observation.pending_projection(arguments,root,parent,root)
        migration=dict(context_bytes=b'invented context',ancestry_proof_bytes=b'invented proof')
        migration.update(expected_context_sha256=metadata.sha(migration['context_bytes']),
                         expected_ancestry_proof_sha256=metadata.sha(migration['ancestry_proof_bytes']))
        arguments['historical_migration']=migration
        new=observation.pending_projection(arguments,root,parent,root)
        self.assertEqual(child.packet_migration(new),migration)
        self.assertEqual(new['schema'],'pending_operational_outer_packet_v2')
        new.pop('historical_migration');new['schema']=old['schema'];self.assertEqual(new,old)

    def test_unknown_or_changed_projection_migration_refuses(self):
        arguments=legacy_fixture();root=Path.cwd();arguments['historical_migration']={}
        with self.assertRaisesRegex(ValueError,'migration_shape'):
            observation.pending_projection(arguments,root,parent,root)


if __name__=='__main__':unittest.main(verbosity=2)
