"""Pure, synthetic-only candidate guards. No filesystem or device executor.

Review references are required fixture attestations, not proofs about real code.
Every result remains device-ineligible, including an otherwise valid result.
"""

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Mapping, Sequence


class CandidateError(ValueError):
    """A synthetic plan failed a required precondition."""


@dataclass(frozen=True)
class ComponentIdentity:
    component: str
    size: int
    sha256: str


@dataclass(frozen=True)
class ProtectedRange:
    component: str
    start: int
    end: int
    reason: str


@dataclass(frozen=True)
class Edit:
    component: str
    offset: int
    expected: bytes
    replacement: bytes
    address_type: str = "file_offset"


@dataclass(frozen=True)
class ReviewFacts:
    instruction_boundaries: str
    control_flow: str
    address_mapping: str
    protected_regions: str
    unselected_records: str
    storage_size: str


@dataclass(frozen=True)
class SyntheticProfile:
    profile_id: str
    fixture_version: str
    tool_revision: str
    components: tuple[ComponentIdentity, ...]
    protected_ranges: tuple[ProtectedRange, ...] = ()
    profile_status: str = "SYNTHETIC_ONLY"
    model: str = "SYNTHETIC"
    region: str = "SYNTHETIC"


@dataclass(frozen=True)
class FixtureIdentity:
    profile_id: str
    fixture_version: str
    model: str = "SYNTHETIC"
    region: str = "SYNTHETIC"


@dataclass(frozen=True)
class Candidate:
    """Immutable synthetic bytes and canonical manifest, never a write request."""

    objects: tuple[tuple[str, bytes], ...]
    manifest_json: str
    profile: SyntheticProfile
    edits: tuple[Edit, ...]
    review: ReviewFacts

    @property
    def device_eligible(self) -> bool:
        return False


_LABEL = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")
_SHA = re.compile(r"[0-9a-f]{64}\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")


def _label(value: object, field: str) -> str:
    if not isinstance(value, str) or not _LABEL.fullmatch(value):
        raise CandidateError(f"invalid {field}")
    if "unknown" in value.lower() or "unverified" in value.lower():
        raise CandidateError(f"unknown {field}")
    return value


def _reference(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateError(f"missing explicit review fact: {field}")
    if value.strip().lower() in {"unknown", "unverified", "todo", "none"}:
        raise CandidateError(f"missing explicit review fact: {field}")
    return value


def identify(component: str, data: bytes) -> ComponentIdentity:
    """Identify an immutable synthetic object; this cannot identify a camera."""
    _label(component, "component")
    if not isinstance(data, bytes) or not data:
        raise CandidateError("source must be nonempty immutable bytes")
    return ComponentIdentity(component, len(data), hashlib.sha256(data).hexdigest())


def _identity_record(item: ComponentIdentity) -> dict:
    return {"component": item.component, "size": item.size, "sha256": item.sha256}


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _validate_profile(profile: SyntheticProfile) -> dict[str, ComponentIdentity]:
    if not isinstance(profile, SyntheticProfile):
        raise CandidateError("unknown profile; only SyntheticProfile is accepted")
    if (profile.profile_status != "SYNTHETIC_ONLY" or
            profile.model != "SYNTHETIC" or profile.region != "SYNTHETIC"):
        raise CandidateError("wrong model/region/profile status; target profiles are refused")
    if not _label(profile.profile_id, "profile id").startswith("synthetic-"):
        raise CandidateError("profile id must explicitly identify a synthetic fixture")
    if not _label(profile.fixture_version, "fixture version").startswith("synthetic-"):
        raise CandidateError("wrong or unknown synthetic fixture version")
    if not isinstance(profile.tool_revision, str) or not _REVISION.fullmatch(profile.tool_revision):
        raise CandidateError("tool revision must be an explicit full lowercase Git revision")
    if not isinstance(profile.components, tuple) or not profile.components:
        raise CandidateError("missing immutable component identity set")
    identities = {}
    for item in profile.components:
        if not isinstance(item, ComponentIdentity):
            raise CandidateError("invalid component identity")
        _label(item.component, "component")
        if item.component in identities:
            raise CandidateError("duplicate component identity")
        if type(item.size) is not int or item.size <= 0:
            raise CandidateError("component size must be a positive integer")
        if not isinstance(item.sha256, str) or not _SHA.fullmatch(item.sha256):
            raise CandidateError("missing exact whole-object SHA-256")
        identities[item.component] = item
    if not isinstance(profile.protected_ranges, tuple):
        raise CandidateError("protected ranges must be immutable")
    for region in profile.protected_ranges:
        if not isinstance(region, ProtectedRange) or region.component not in identities:
            raise CandidateError("unknown protected component")
        if (type(region.start) is not int or type(region.end) is not int or
                not 0 <= region.start < region.end <= identities[region.component].size):
            raise CandidateError("invalid protected range bounds")
        _reference(region.reason, "protected range reason")
    previous = {}
    for region in sorted(profile.protected_ranges, key=lambda r: (r.component, r.start)):
        if region.start < previous.get(region.component, 0):
            raise CandidateError("overlapping protected ranges")
        previous[region.component] = region.end
    return identities


def _verify_sources(sources: Mapping[str, bytes], identities: dict[str, ComponentIdentity]) -> None:
    if not isinstance(sources, Mapping) or set(sources) != set(identities):
        raise CandidateError("missing, extra or mixed component set")
    for name in sorted(identities):
        if identify(name, sources[name]) != identities[name]:
            raise CandidateError(f"whole-object identity mismatch: {name}; already-applied sources refused")


def _validate_review(review: ReviewFacts) -> dict[str, str]:
    if not isinstance(review, ReviewFacts):
        raise CandidateError("missing explicit fixture review facts")
    return {name: _reference(getattr(review, name), name) for name in (
        "instruction_boundaries", "control_flow", "address_mapping", "protected_regions",
        "unselected_records", "storage_size")}


def _ordered_edits(edits: Sequence[Edit], identities: dict[str, ComponentIdentity],
                   protected: tuple[ProtectedRange, ...]) -> tuple[Edit, ...]:
    if not isinstance(edits, (tuple, list)) or not edits:
        raise CandidateError("missing bounded edits")
    for item in edits:
        if not isinstance(item, Edit) or item.component not in identities:
            raise CandidateError("unknown edited component")
        if item.address_type != "file_offset":
            raise CandidateError("only explicit file_offset addresses are supported")
        if type(item.offset) is not int or item.offset < 0:
            raise CandidateError("negative or noninteger edit offset")
        if (not isinstance(item.expected, bytes) or not isinstance(item.replacement, bytes)
                or not item.expected or len(item.expected) != len(item.replacement)):
            raise CandidateError("edit must have nonempty equal-length immutable byte strings")
        end = item.offset + len(item.expected)
        if end > identities[item.component].size:
            raise CandidateError("edit exceeds object bounds")
        if item.expected == item.replacement:
            raise CandidateError("no-op edit refused")
        for region in protected:
            if (region.component == item.component and
                    item.offset < region.end and region.start < end):
                raise CandidateError("edit intersects protected range")
    ordered = tuple(sorted(edits, key=lambda e: (e.component, e.offset)))
    previous = {}
    for item in ordered:
        if item.offset < previous.get(item.component, 0):
            raise CandidateError("overlapping edits")
        previous[item.component] = item.offset + len(item.expected)
    return ordered


def _apply(sources: Mapping[str, bytes], edits: tuple[Edit, ...]) -> tuple[tuple[str, bytes], ...]:
    # All expected windows are checked against the original, before constructing output.
    for item in edits:
        if sources[item.component][item.offset:item.offset + len(item.expected)] != item.expected:
            raise CandidateError(f"expected bytes mismatch: {item.component}")
    buffers = {name: bytearray(data) for name, data in sources.items()}
    for item in edits:
        buffers[item.component][item.offset:item.offset + len(item.expected)] = item.replacement
    return tuple((name, bytes(buffers[name])) for name in sorted(buffers))


def _edit_record(item: Edit) -> dict:
    return {"component": item.component, "address_type": item.address_type,
            "offset": item.offset, "expected_hex": item.expected.hex(),
            "replacement_hex": item.replacement.hex()}


def build_candidate(profile: SyntheticProfile, sources: Mapping[str, bytes],
                    edits: Sequence[Edit], review: ReviewFacts, *,
                    fixture_identity: FixtureIdentity) -> Candidate:
    """Return a deterministic in-memory fixture plan after all-or-nothing checks.

    No profile path is loaded. UNVERIFIED and actual target profiles are refused.
    The caller's tool revision and review references are recorded, not certified.
    """
    identities = _validate_profile(profile)
    if not isinstance(fixture_identity, FixtureIdentity) or fixture_identity != FixtureIdentity(
            profile.profile_id, profile.fixture_version, profile.model, profile.region):
        raise CandidateError("fixture model/version/region/profile identity mismatch")
    _verify_sources(sources, identities)
    reviews = _validate_review(review)
    ordered = _ordered_edits(edits, identities, profile.protected_ranges)
    # Freeze the mapping before processing; bytes themselves are immutable.
    source_copy = dict(sources)
    _verify_sources(source_copy, identities)
    objects = _apply(source_copy, ordered)
    output = dict(objects)
    inverse = tuple(Edit(e.component, e.offset, e.replacement, e.expected, e.address_type)
                    for e in ordered)
    if dict(_apply(output, inverse)) != source_copy:
        raise CandidateError("exact inverse failed")
    for name, original in source_copy.items():
        changed = {i for e in ordered if e.component == name
                   for i in range(e.offset, e.offset + len(e.expected))}
        if len(original) != len(output[name]) or any(
                original[i] != output[name][i] for i in range(len(original)) if i not in changed):
            raise CandidateError("unselected byte preservation failed")
    for region in profile.protected_ranges:
        if source_copy[region.component][region.start:region.end] != output[region.component][region.start:region.end]:
            raise CandidateError("protected byte preservation failed")
    before = [_identity_record(identities[name]) for name in sorted(identities)]
    after = [_identity_record(identify(name, data)) for name, data in objects]
    manifest = {
        "schema_version": 1, "kind": "synthetic-only-candidate", "evidence_class": "offline-tested",
        "device_eligible": False, "camera_access_performed": False,
        "profile_id": profile.profile_id, "model": profile.model,
        "fixture_version": profile.fixture_version, "region": profile.region,
        "tool_revision_claim": profile.tool_revision,
        "baseline_set_sha256": hashlib.sha256(_canonical(before).encode("ascii")).hexdigest(),
        "before": before, "after": after,
        "edits": [_edit_record(e) for e in ordered],
        "inverse_edits": [_edit_record(e) for e in inverse], "review_references": reviews,
        "protected_ranges": [{"component": p.component, "start": p.start, "end": p.end,
                              "reason": p.reason} for p in sorted(
                                  profile.protected_ranges, key=lambda p: (p.component, p.start))],
        "preservation": {"size_invariant": True, "unselected_bytes_equal": True,
                         "protected_bytes_equal": True, "exact_inverse_verified": True},
    }
    return Candidate(objects, _canonical(manifest), profile, ordered, review)


def invert_candidate(candidate: Candidate, sources: Mapping[str, bytes]) -> tuple[tuple[str, bytes], ...]:
    """Check the complete candidate set before constructing its exact inverse."""
    if not isinstance(candidate, Candidate):
        raise CandidateError("unknown candidate")
    identities = {name: identify(name, data) for name, data in candidate.objects}
    _verify_sources(sources, identities)
    inverse = tuple(Edit(e.component, e.offset, e.replacement, e.expected, e.address_type)
                    for e in candidate.edits)
    restored = _apply(dict(sources), inverse)
    expected = _validate_profile(candidate.profile)
    _verify_sources(dict(restored), expected)
    return restored
