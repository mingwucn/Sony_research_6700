"""Unit tests for α6700 Customizer targets and backend logic."""
import unittest

from apps.a6700_customizer.targets import (
    ALL_FTP_TARGETS,
    ALL_TARGETS,
    APPFW_SIZE,
    TARGET_ENGLISH,
    TARGET_FILE,
    TARGET_FTP_PLAYBACK_KEY,
    UnexpectedTargetState,
    target_needs_change,
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

    def test_ftp_network_settings_count(self):
        # 1 playback key + 9 network settings = 10 targets
        self.assertEqual(len(ALL_FTP_TARGETS), 10)

    def test_all_targets_bounds(self):
        for t in ALL_TARGETS:
            self.assertGreaterEqual(t.offset, 0)
            self.assertLess(t.offset + len(t.patched), APPFW_SIZE)
            self.assertEqual(len(t.preimage), len(t.patched))

    def test_exact_stock_to_patched_transitions(self):
        for target in ALL_TARGETS:
            with self.subTest(target=target.name):
                self.assertTrue(target_needs_change(target, target.preimage, target.patched))
                self.assertFalse(target_needs_change(target, target.patched, target.patched))

    def test_exact_patched_to_stock_transitions(self):
        for target in ALL_TARGETS:
            with self.subTest(target=target.name):
                self.assertTrue(target_needs_change(target, target.patched, target.preimage))
                self.assertFalse(target_needs_change(target, target.preimage, target.preimage))

    def test_unknown_or_truncated_source_fails_closed(self):
        for target in ALL_TARGETS:
            with self.subTest(target=target.name):
                with self.assertRaises(UnexpectedTargetState):
                    target_needs_change(target, b"\\xff" * len(target.preimage), target.patched)
                with self.assertRaises(UnexpectedTargetState):
                    target_needs_change(target, b"", target.preimage)

    def test_invalid_destination_fails_closed(self):
        with self.assertRaises(ValueError):
            target_needs_change(TARGET_ENGLISH, TARGET_ENGLISH.preimage, b"\\xff" * 4)


if __name__ == "__main__":
    unittest.main()
