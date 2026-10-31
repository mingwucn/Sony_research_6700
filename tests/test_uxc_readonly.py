import struct
import unittest
from tools.uxc_readonly import parse_uxc, UxcError

def resource(texts=("Language","English","简体中文"),group=39):
    count=len(texts); base=(16+2*count+3)&~3
    raw=bytearray(base);raw[:8]=b"uxc\x07\0\0\0\0"
    struct.pack_into("<HHI",raw,8,8,group,count|(((count+1)&~1)<<12))
    for index,text in enumerate(texts):
        if text is None:struct.pack_into("<H",raw,16+2*index,65535);continue
        struct.pack_into("<H",raw,16+2*index,(len(raw)-base)//4)
        rid=0x02000000|((group<<13)+index)
        raw+=struct.pack("<I",0x1e000000|(rid&0xffffff))+text.encode("utf-8")+b"\0"
        raw+=b"\0"*((-len(raw))%4)
    return bytes(raw)

class UxcReadOnlyTests(unittest.TestCase):
    def test_unicode_and_ids(self):
        r=parse_uxc(resource());self.assertEqual(r.slot_count,3)
        self.assertEqual(list(r.texts.values()),["Language","English","简体中文"])
        self.assertEqual(min(r.texts),0x02000000|(39<<13))
    def test_missing_slot(self):
        r=parse_uxc(resource(("one",None,"three")));self.assertEqual(len(r.texts),2)
    def test_wrong_magic(self):
        with self.assertRaises(UxcError):parse_uxc(b"wrong"+resource()[5:])
    def test_wrong_descriptor(self):
        r=bytearray(resource());struct.pack_into("<I",r,12,0)
        with self.assertRaises(UxcError):parse_uxc(bytes(r))
    def test_pointer_outside(self):
        r=bytearray(resource());struct.pack_into("<H",r,16,65534)
        with self.assertRaises(UxcError):parse_uxc(bytes(r))
    def test_bad_tag(self):
        r=bytearray(resource());r[24]^=1
        with self.assertRaises(UxcError):parse_uxc(bytes(r))
    def test_bad_utf8(self):
        r=bytearray(resource(("abc",)));base=(18+3)&~3;r[base+4]=255
        with self.assertRaises(UxcError):parse_uxc(bytes(r))
    def test_unterminated(self):
        r=bytearray(resource(("abc",)));r[-1]=1
        with self.assertRaises(UxcError):parse_uxc(bytes(r))
    def test_size_cap(self):
        with self.assertRaises(UxcError):parse_uxc(resource(),20)
    def test_odd_size(self):
        with self.assertRaises(UxcError):parse_uxc(resource()[:-1])
    def test_invalid_budget_type(self):
        for budget in (None,True,1.5,-1,0):
            with self.assertRaises(UxcError):parse_uxc(resource(),budget)
    def test_group_outside_canonical_id(self):
        with self.assertRaises(UxcError):parse_uxc(resource(group=0x800))

if __name__ == "__main__":unittest.main()
