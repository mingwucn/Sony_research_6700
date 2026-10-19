"""Original-byte receipt and pending-only runtime boundaries."""
import unittest
from tools import dependency_current_metadata as subject


class CurrentBoundaryTests(unittest.TestCase):
    def test_original_bytes_not_equivalent_json(self):
        raw=b'{"x":1}'
        rows={'record':dict(bytes=len(raw),sha256=subject.launch.sha(raw))}
        with self.assertRaisesRegex(ValueError,'current_original_bytes'):
            subject.receipts(rows,{'record':raw+b'\n'})

    def test_missing_extra_and_boolean_size_refuse(self):
        raw=b'x'
        for rows in ({},{'record':dict(bytes=True,sha256=subject.launch.sha(raw))},
                     {'record':dict(bytes=1,sha256=subject.launch.sha(raw)),'extra':{}}):
            with self.subTest(rows=rows),self.assertRaises(ValueError):subject.receipts(rows,{'record':raw})

    def test_operational_or_camera_record_refuses(self):
        for field,value in (('invented',False),('camera_commands',['contact']),('operation_id','different')):
            record=dict(schema='invented',invented=True,operation_id='operation',camera_commands=[])
            record[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                subject.record(subject.launch.encoded(record),'invented',(),'operation')

    def test_public_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()
