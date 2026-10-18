"""Synthetic OFF-01..07/09 coverage; no real firmware fixtures or target proof."""

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import unittest

from tools.candidate_guards import (
    CandidateError, ComponentIdentity, Edit, FixtureIdentity, ProtectedRange,
    ReviewFacts, SyntheticProfile, build_candidate, identify, invert_candidate,
)


class CandidateGuardTests(unittest.TestCase):
    def setUp(self):
        self.sources = {"ap": b"HEAD|look-a|recipe-b|TAIL", "cp": b"CP|curve-a|calibration"}
        self.profile = SyntheticProfile(
            "synthetic-pair", "synthetic-v1", "a" * 40,
            tuple(identify(k, v) for k, v in self.sources.items()),
            (ProtectedRange("ap", 19, 23, "fixture trailer"),
             ProtectedRange("cp", 11, 22, "fixture protected data")),
        )
        self.fixture = FixtureIdentity("synthetic-pair", "synthetic-v1")
        self.review = ReviewFacts(*(f"fixture-review-{i}" for i in range(6)))
        self.edits = (Edit("ap", 5, b"look-a", b"look-x"), Edit("cp", 3, b"curve-a", b"curve-x"))

    def build(self, *, profile=None, sources=None, edits=None, review=None, fixture=None):
        return build_candidate(profile if profile is not None else self.profile,
                               sources if sources is not None else self.sources,
                               edits if edits is not None else self.edits,
                               review if review is not None else self.review,
                               fixture_identity=fixture if fixture is not None else self.fixture)

    def test_off01_deterministic_bytes_manifest_independent_of_input_order(self):
        first = self.build()
        second = self.build(sources=dict(reversed(list(self.sources.items()))),
                            edits=tuple(reversed(self.edits)),
                            profile=replace(self.profile, components=tuple(reversed(self.profile.components)),
                                            protected_ranges=tuple(reversed(self.profile.protected_ranges))))
        self.assertEqual(first.objects, second.objects)
        self.assertEqual(first.manifest_json, second.manifest_json)
        manifest = json.loads(first.manifest_json)
        self.assertEqual(manifest["kind"], "synthetic-only-candidate")
        self.assertFalse(first.device_eligible)
        self.assertFalse(manifest["device_eligible"])
        self.assertFalse(manifest["camera_access_performed"])

    def test_off02_changed_source_byte_outside_edit_refused(self):
        sources = dict(self.sources, ap=b"h" + self.sources["ap"][1:])
        with self.assertRaisesRegex(CandidateError, "whole-object identity mismatch: ap"):
            self.build(sources=sources)

    def test_off03_target_unverified_profile_refused(self):
        path = Path(__file__).resolve().parents[1] / "profiles" / "ilce6700.UNVERIFIED.json"
        with self.assertRaisesRegex(CandidateError, "unknown profile"):
            self.build(profile=json.loads(path.read_text(encoding="utf-8")))

    def test_off03_actual_target_profile_refused(self):
        for field, value in (("model", "ILCE-6700"), ("region", "Japan"),
                             ("profile_status", "VERIFIED"), ("fixture_version", "UNKNOWN")):
            with self.subTest(field=field), self.assertRaises(CandidateError):
                self.build(profile=replace(self.profile, **{field: value}))

    def test_off03_wrong_fixture_model_version_region_or_profile_refused(self):
        for field, value in (("model", "other"), ("region", "other"),
                             ("fixture_version", "synthetic-v2"), ("profile_id", "synthetic-other")):
            with self.subTest(field=field), self.assertRaisesRegex(CandidateError, "identity mismatch"):
                self.build(fixture=replace(self.fixture, **{field: value}))

    def test_missing_review_facts_refused_individually(self):
        for field in self.review.__dataclass_fields__:
            with self.subTest(field=field), self.assertRaisesRegex(CandidateError, "explicit review"):
                self.build(review=replace(self.review, **{field: "UNKNOWN"}))
        with self.assertRaisesRegex(CandidateError, "explicit fixture review"):
            self.build(review={})

    def test_missing_whole_object_identity_or_duplicate_component_refused(self):
        bad = replace(self.profile.components[0], sha256="")
        for components in ((), (bad,), (self.profile.components[0], self.profile.components[0])):
            with self.subTest(components=components), self.assertRaises(CandidateError):
                self.build(profile=replace(self.profile, components=components))

    def test_tool_revision_must_be_explicit_and_pinned(self):
        for revision in ("main", "UNKNOWN", "a" * 7, "g" * 40):
            with self.subTest(revision=revision), self.assertRaises(CandidateError):
                self.build(profile=replace(self.profile, tool_revision=revision))

    def test_off04_truncation_missing_extra_and_mixed_pair_refused(self):
        cases = [dict(self.sources, cp=self.sources["cp"][:-1]),
                 {"ap": self.sources["ap"]}, dict(self.sources, resource=b"extra"),
                 dict(self.sources, cp=b"CP|curve-z|calibration")]
        for sources in cases:
            with self.subTest(sources=sources), self.assertRaises(CandidateError):
                self.build(sources=sources)

    def test_off05_negative_boolean_out_of_bounds_or_size_change_refused(self):
        cases = [Edit("ap", -1, b"a", b"b"), Edit("ap", True, b"a", b"b"),
                 Edit("ap", len(self.sources["ap"]), b"a", b"b"),
                 Edit("ap", 5, b"look-a", b"x"), Edit("ap", 5, b"", b""),
                 Edit("ap", 5, b"look-a", b"look-a")]
        for edit in cases:
            with self.subTest(edit=edit), self.assertRaises(CandidateError):
                self.build(edits=(edit,))

    def test_off05_overlap_refused_even_if_expected_windows_are_valid(self):
        with self.assertRaisesRegex(CandidateError, "overlapping edits"):
            self.build(edits=(self.edits[0], Edit("ap", 8, b"k-a", b"k-y")))

    def test_off05_adjacent_edits_are_bounded_and_allowed(self):
        candidate = self.build(edits=(Edit("ap", 5, b"look", b"LOOK"),
                                     Edit("ap", 9, b"-a", b"-x")))
        self.assertEqual(dict(candidate.objects)["ap"][5:11], b"LOOK-x")

    def test_address_type_not_silently_translated(self):
        for address_type in ("virtual_address", "runtime_process_address", "", "UNKNOWN"):
            with self.subTest(address_type=address_type), self.assertRaisesRegex(CandidateError, "file_offset"):
                self.build(edits=(replace(self.edits[0], address_type=address_type),))

    def test_expected_bytes_and_unknown_component_refused(self):
        for edit in (replace(self.edits[0], expected=b"look-q"),
                     replace(self.edits[0], component="unknown")):
            with self.subTest(edit=edit), self.assertRaises(CandidateError):
                self.build(edits=(edit,))

    def test_protected_intersection_and_malformed_ranges_refused(self):
        with self.assertRaisesRegex(CandidateError, "protected range"):
            self.build(edits=(Edit("cp", 11, b"c", b"X"),))
        for region in (ProtectedRange("ap", -1, 2, "invalid"),
                       ProtectedRange("ap", 0, 999, "invalid"),
                       ProtectedRange("missing", 0, 1, "invalid")):
            with self.subTest(region=region), self.assertRaises(CandidateError):
                self.build(profile=replace(self.profile, protected_ranges=(region,)))
        with self.assertRaisesRegex(CandidateError, "overlapping protected"):
            self.build(profile=replace(self.profile, protected_ranges=(
                ProtectedRange("ap", 0, 3, "one"), ProtectedRange("ap", 2, 4, "two"))))

    def test_off06_reapply_full_or_partly_applied_candidate_refused(self):
        candidate = self.build()
        for sources in (dict(candidate.objects), dict(self.sources, ap=dict(candidate.objects)["ap"])):
            with self.subTest(sources=sources), self.assertRaisesRegex(CandidateError, "already-applied"):
                self.build(sources=sources)

    def test_off07_exact_inverse_whole_component_set_and_protected_equality(self):
        candidate = self.build()
        restored = dict(invert_candidate(candidate, dict(candidate.objects)))
        self.assertEqual(restored, self.sources)
        for region in self.profile.protected_ranges:
            self.assertEqual(restored[region.component][region.start:region.end],
                             self.sources[region.component][region.start:region.end])
        manifest = json.loads(candidate.manifest_json)
        self.assertTrue(all(manifest["preservation"].values()))

    def test_off07_inverse_rejects_stale_or_partial_candidate_sources(self):
        candidate = self.build()
        for sources in (self.sources, dict(candidate.objects, cp=b"different")):
            with self.subTest(sources=sources), self.assertRaises(CandidateError):
                invert_candidate(candidate, sources)

    def test_off09_unselected_recipe_and_component_byte_equality(self):
        sources = dict(self.sources, resource=b"recipe-0|recipe-1|recipe-2")
        profile = replace(self.profile, components=tuple(identify(k, v) for k, v in sources.items()))
        candidate = self.build(profile=profile, sources=sources)
        output = dict(candidate.objects)
        self.assertEqual(output["resource"], sources["resource"])
        self.assertEqual(output["ap"][12:], sources["ap"][12:])
        self.assertEqual(output["ap"][:5], sources["ap"][:5])

    def test_input_immutability_and_no_partial_output_on_failure(self):
        before = dict(self.sources)
        with self.assertRaises(CandidateError):
            self.build(edits=(self.edits[0], replace(self.edits[1], expected=b"curve-q")))
        self.assertEqual(self.sources, before)
        candidate = self.build()
        with self.assertRaises(FrozenInstanceError):
            candidate.manifest_json = "forged"
        self.assertEqual(self.sources, before)


if __name__ == "__main__":
    unittest.main()
