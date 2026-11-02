"""Unit tests for α6700 Customizer targets and backend logic."""
import unittest

from apps.a6700_customizer.targets import (
    ALL_FTP_TARGETS,
    ALL_TARGETS,
    APPFW_SIZE,
    TARGET_ENGLISH,
    TARGET_FILE,
    TARGET_FTP_GALLERY_MENUS,
    TARGET_FTP_NETWORK_SETTINGS,
    TARGET_FTP_PLAYBACK_KEY,
    build_target_spans,
)


class TestCustomizerTargets(unittest.TestCase):
    def test_target_file(self):
        self.assertEqual(TARGET_FILE, "/usr/lib/appFw.so")
        self.assertEqual(APPFW_SIZE, 89027992)

    def test_english_target(self):
        self.assertEqual(TARGET_ENGLISH.offset, 0x023080F8)
        self.assertEqual(len(TARGET_ENGLISH.preimage), 4)
        self.assertEqual(len(TARGET_ENGLISH.patched), 4)
        self.assertEqual(TARGET_ENGLISH.preimage, bytes.fromhex("f4179f1a"))
        self.assertEqual(TARGET_ENGLISH.patched, bytes.fromhex("34008052"))

    def test_ftp_playback_key_target(self):
        self.assertEqual(TARGET_FTP_PLAYBACK_KEY.offset, 0x03F17CE4)
        self.assertEqual(TARGET_FTP_PLAYBACK_KEY.preimage, b"\x00")
        self.assertEqual(TARGET_FTP_PLAYBACK_KEY.patched, b"\x01")

    def test_ftp_counts(self):
        self.assertEqual(len(TARGET_FTP_NETWORK_SETTINGS), 9)
        self.assertEqual(len(TARGET_FTP_GALLERY_MENUS), 81)
        # 1 playback key + 9 network settings + 81 gallery menus = 91 targets
        self.assertEqual(len(ALL_FTP_TARGETS), 91)
        # 1 english + 91 ftp = 92 targets
        self.assertEqual(len(ALL_TARGETS), 92)

    def test_all_targets_bounds(self):
        for t in ALL_TARGETS:
            self.assertGreaterEqual(t.offset, 0)
            self.assertLess(t.offset + len(t.patched), APPFW_SIZE)
            self.assertEqual(len(t.preimage), len(t.patched))

    def test_spans_grouping(self):
        spans = build_target_spans(ALL_TARGETS)
        # Verify 7 spans
        self.assertEqual(len(spans), 7)
        # Verify all targets accounted for
        total_targets_in_spans = sum(len(s.targets) for s in spans)
        self.assertEqual(total_targets_in_spans, len(ALL_TARGETS))

        # Verify max span size <= 128 KiB (safe USB Senser write block)
        for s in spans:
            self.assertLessEqual(s.length, 0x20000)
            # Verify each target within its span
            for t in s.targets:
                self.assertGreaterEqual(t.offset, s.offset)
                self.assertLessEqual(t.offset + len(t.patched), s.offset + s.length)


if __name__ == "__main__":
    unittest.main()
