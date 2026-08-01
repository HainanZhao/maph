#!/usr/bin/env python3
"""Build the deterministic, OBSERVED Cycle-2 G0 evidence-coverage audit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
ARTIFACTS = PROJECT / "artifacts"
OUTPUT = ARTIFACTS / "g0-dependency-evidence-matrix-v2.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def ev(*names: str) -> list[str]:
    return list(names)


# Each item reports the status already asserted by the cited artifacts.  This
# script does not promote a status: the complete audit artifact is OBSERVED.
NODES = (
    ("SOURCE-MANIFEST", False, "No: byte metadata is not an exponent derivation.", (),
     ev("source-manifest-verification-v2.json"),
     ev("Metadata inventory does not establish mathematical source authority or upstream completeness."),
     "OBSERVED is appropriate; no mathematical conclusion is implied."),
    ("GM-T1.1", True, "No reproof; two independent application audits are required where transferred.",
     ev("baseline-route-a-v3.json", "cycle-1-route-b-baseline.json", "cycle-1-route-reconciliation-v3.json"),
     ev("guth-maynard-source-metadata-v1.json", "source-manifest-verification-v2.json"),
     ev("Published theorem is not re-proved; applications remain conditional on its hypotheses."),
     "Published-statement and conditional exact-algebra labels remain bounded as written."),
    ("GM-ZD-TYPE-SPLIT", True, "Yes: independent Section-13.1 label-level application audits.",
     ev("cycle-2-stream-b-route-a-v3.json", "cycle-2-stream-b-route-b-v1.json", "cycle-2-stream-b-route-reconciliation-v2.json"),
     ev("g0-theorem-dependency-graph-v1.json", "cycle-2-stream-a-source-metadata-v1.json"), (),
     "PROVED only as the narrow pinned-source Stream-B transfer, not a reproof of GM."),
    ("EXT-MP-L24", True, "Yes: both routes must check that MP covers GM's Type-II use.",
     ev("cycle-2-stream-b-route-a-v3.json", "cycle-2-stream-b-route-b-v1.json", "cycle-2-stream-b-route-reconciliation-v2.json"),
     ev("cycle-2-stream-a-source-metadata-v1.json", "source-manifest-verification-v2.json"), (),
     "PROVED narrowly in Stream B; MP Lemma 24 itself is not re-proved."),
    ("GM-ZD-SMOOTH-SEPARATE", True, "Yes: smoothing, separation, local count, and height translation need two routes.",
     ev("cycle-2-stream-b-route-a-v3.json", "cycle-2-stream-b-route-b-v1.json", "cycle-2-stream-b-route-reconciliation-v2.json"),
     ev("guth-maynard-source-metadata-v1.json", "source-manifest-verification-v2.json"), (),
     "PROVED only as a source/application audit in the narrow Stream-B boundary."),
    ("GM-ZD-APPLY-T1.1", True, "Yes: powered coefficients, shells, normalization, threshold, and k regimes need two routes.",
     ev("cycle-2-stream-b-route-a-v3.json", "cycle-2-stream-b-route-b-v1.json", "cycle-2-stream-b-route-reconciliation-v2.json"),
     ev("guth-maynard-source-metadata-v1.json", "source-manifest-verification-v2.json"), (),
     "PROVED as a reconciled exact/pinned application audit, not a proof of Theorem 1.1."),
    ("EXT-MVT", True, "Yes: precise mean-value input and residual comparison need independent coverage.",
     ev("cycle-2-stream-b-route-a-v3.json", "cycle-2-stream-b-route-b-v1.json", "cycle-2-stream-b-route-reconciliation-v2.json"),
     ev("cycle-2-stream-a-source-metadata-v1.json", "source-manifest-verification-v2.json"), (),
     "PROVED narrowly in Stream B; no mean-value theorem is re-proved."),
    ("INGHAM", True, "Two exact downstream uses must agree; Huxley's frozen restatement is the source substitute.",
     ev("baseline-route-a-v3.json", "cycle-1-route-b-baseline.json", "cycle-1-route-reconciliation-v3.json"),
     ev("classical-zero-density-source-metadata-v1.json", "source-manifest-verification-v2.json"),
     ev("Original Ingham page is inaccessible; source authority is the recorded Huxley restatement."),
     "PROVED only for the reachable restated range and its exact conditional uses."),
    ("HUXLEY", True, "Two exact downstream uses must agree; direct source inspection supplies the theorem statement.",
     ev("baseline-route-a-v3.json", "cycle-1-route-b-baseline.json", "cycle-1-route-reconciliation-v3.json"),
     ev("classical-zero-density-source-metadata-v1.json", "source-manifest-verification-v2.json"), (),
     "PROVED only for the inspected statement/range and conditional uses."),
    ("GM-T1.2", True, "Yes for displayed exponent and all case boundaries; no analytic reproof is claimed.",
     ev("theorem-1-2-case-split-route-a-v4.json", "cycle-1-route-b-v3-theorem-1-2-case-split.json", "cycle-1-route-reconciliation-v3.json"),
     ev("guth-maynard-source-metadata-v1.json", "source-manifest-verification-v2.json"),
     ev("Analytic proof is outside the exact exponent audit."),
     "PROVED only conditional on the cited GM, zero-detection, and mean-value inputs."),
    ("GM-ENV-30-13", True, "Yes: crossover and envelope branches require independent exact arithmetic.",
     ev("baseline-route-a-v3.json", "cycle-1-route-b-baseline.json", "cycle-1-route-reconciliation-v3.json"),
     ev("guth-maynard-source-metadata-v1.json", "classical-zero-density-source-metadata-v1.json", "source-manifest-verification-v2.json"),
     ev("Only exponent arithmetic is closed; the upstream analytic chain is not re-proved."),
     "PROVED as exact conditional crossover arithmetic."),
    ("EXT-EXPLICIT-FORMULA", True, "Yes for G0: both routes must pin archival source, conventions, and endpoint transfer.",
     ev("cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-explicit-formula-source-closure-v2.json", "cycle-2-stream-c-source-ledger-v3.json", "source-manifest-verification-v2.json"),
     ev("Route A v3 pins only ledger v1, not the licensed Kedlaya von-Mangoldt proof unit; six Route-A formula/convention labels remain OBSERVED."),
     "Route-B closure is PROVED narrowly, but this global two-route node remains OBSERVED."),
    ("EXT-NEAR-ONE-DENSITY", True, "Yes: a single pinned branch/range/convention must agree in both routes.",
     ev("cycle-2-stream-c-route-a-v3.json", "cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-source-ledger-v3.json", "source-manifest-verification-v2.json"), (),
     "PROVED for the individually pinned node within the reported reconciliation scope."),
    ("EXT-VK-ZERO-FREE", True, "Yes: all-height completion and 5/7 weakening must agree in both routes.",
     ev("cycle-2-stream-c-route-a-v3.json", "cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-source-ledger-v3.json", "source-manifest-verification-v2.json"), (),
     "PROVED for the frozen finite-/high-height bridge, inside its no-new-theorem boundary."),
    ("EXT-LOCAL-PAIR-KERNEL", False, "Yes: multiplicity-inclusive local zero correlation/count is required in both routes.",
     ev("cycle-2-stream-c-route-a-v3.json", "cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-source-ledger-v3.json", "source-manifest-verification-v2.json"), (),
     "PROVED only as the reported HSW/Bui local-kernel transfer."),
    ("GM-C1.3", True, "Yes: all labeled uniform boundary, truncation, epsilon, range, and error conversions need both routes.",
     ev("cycle-2-stream-c-route-a-v3.json", "cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-source-ledger-v3.json", "cycle-2-stream-c-explicit-formula-source-closure-v2.json"),
     ev("17/30 arithmetic agrees, but Route-A explicit-formula authority gap prevents full theorem-path closure."),
     "Exact boundary agreement is PROVED; full Stream-C/G0 closure is OBSERVED and withheld."),
    ("GM-C1.4", True, "Yes: all labeled almost-all delta/T/epsilon/L2/remainder/exceptional-set conversions need both routes.",
     ev("cycle-2-stream-c-route-a-v3.json", "cycle-2-stream-c-route-b-v4.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("cycle-2-stream-c-source-ledger-v3.json", "cycle-2-stream-c-explicit-formula-source-closure-v2.json"),
     ev("2/15 arithmetic agrees, but Route-A explicit-formula authority gap prevents full theorem-path closure."),
     "Exact boundary agreement is PROVED; full Stream-C/G0 closure is OBSERVED and withheld."),
    ("G0-FULL-RECONSTRUCTION", False, "Yes: every promoted dependency and downstream label needs genuinely independent route coverage.",
     ev("cycle-1-route-reconciliation-v3.json", "cycle-2-stream-b-route-reconciliation-v2.json", "cycle-2-stream-c-two-route-reconciliation-v1.json"),
     ev("g0-theorem-dependency-graph-v1.json", "source-manifest-verification-v2.json"),
     ev("EXT-EXPLICIT-FORMULA lacks Route-A v4 archival-source/convention coverage.", "Per-route 60-second/256-MiB G0 resource evidence is not recorded for every current Stream-B/Stream-C route."),
     "OBSERVED OPEN. This audit does not declare G0 PASS."),
)


def classify(name: str) -> str:
    if name.startswith("source-manifest-"):
        return "SOURCE-MANIFEST"
    if name in {"guth-maynard-source-metadata-v1.json", "classical-zero-density-source-metadata-v1.json", "cycle-2-stream-a-source-metadata-v1.json", "g0-theorem-dependency-graph-v1.json"}:
        return "SOURCE-AND-LOCATOR-FREEZE"
    if name.startswith("baseline-") or name.startswith("theorem-1-2-") or name.startswith("cycle-1-"):
        return "C1-EXACT-ARITHMETIC"
    if name.startswith("cycle-2-mit-sword-official-bitstream-audit-"):
        return "EXT-EXPLICIT-FORMULA"
    if "stream-b" in name:
        return "SB-SECTION-13.1-TRANSFER"
    if "stream-c" in name:
        return "SC-SECTION-13.2-TRANSFER"
    raise RuntimeError(f"unclassified artifact: {name}")


def timing_paths(value: Any, prefix: str = "") -> list[str]:
    if isinstance(value, dict):
        found = []
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else key
            found += [path] if key == "wall_time_ns" else []
            found += timing_paths(item, path)
        return found
    if isinstance(value, list):
        return [p for i, item in enumerate(value) for p in timing_paths(item, f"{prefix}[{i}]")]
    return []


def without_timing(value: Any) -> Any:
    """Canonical identity for a known mutable replay record, never a proof hash."""
    if isinstance(value, dict):
        return {key: without_timing(item) for key, item in value.items() if key != "wall_time_ns"}
    if isinstance(value, list):
        return [without_timing(item) for item in value]
    return value


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()


def source_manifest_v2_state() -> dict[str, str]:
    """Check coverage without changing the previous manifest artifact."""
    from build_source_manifest_v2 import ARTIFACT as manifest_file
    from build_source_manifest_v2 import build as build_manifest
    from build_source_manifest_v2 import encoded as encode_manifest

    try:
        current = encode_manifest(build_manifest())
    except RuntimeError as error:
        return {"status": "STALE_OR_INCOMPLETE", "detail": str(error), "epistemic_status": "OBSERVED"}
    return {
        "status": "CURRENT" if manifest_file.is_file() and manifest_file.read_bytes() == current else "STALE_OR_INCOMPLETE",
        "detail": "byte-for-byte current" if manifest_file.is_file() and manifest_file.read_bytes() == current else "manifest bytes differ from current source inventory",
        "epistemic_status": "OBSERVED",
    }


def build() -> dict[str, Any]:
    files = sorted(path for path in ARTIFACTS.glob("*.json") if path != OUTPUT)
    inventory, timing = [], []
    for path in files:
        data = json.loads(path.read_text())
        name = path.name
        paths = timing_paths(data)
        identity = ({"stable_content_sha256_excluding_wall_time_ns": canonical_sha256(without_timing(data)), "raw_byte_identity": "NONDETERMINISTIC_TIMING_ARTIFACT"} if paths else {"sha256": sha256(path)})
        inventory.append({"file": name, **identity, "declared_epistemic_status": data.get("epistemic_status", "UNLABELED_LEGACY_METADATA"), "evidence_node": classify(name), "epistemic_status": "OBSERVED"})
        if paths:
            is_perf = name == "cycle-2-stream-c-route-a-v3-performance.json"
            known = name in {"cycle-2-stream-b-route-a-v2.json", "cycle-2-stream-c-route-a-v2.json"}
            legacy_reconciliation_input = name == "cycle-2-stream-c-route-a-v1.json"
            timing.append({"file": name, "paths": paths, "classification": "isolated non-mathematical performance observation" if is_perf else ("historical mutable-timing defect in a mathematical artifact" if known else "mutable timing embedded in a replay artifact"), "containment_or_gap": "Expected: timing is isolated from the deterministic mathematical artifact." if is_perf else ("UNCONTAINED: Stream-C two-route reconciliation v1 records this legacy raw hash, so a successful v1 replay can stale that reconciliation certificate; issue a versioned timing-free reconciliation correction." if legacy_reconciliation_input else ("Contained by canonical semantic identity and later correction/reconciliation; raw bytes are not mathematical identity." if known else "No global raw-byte reproducibility promotion may rely on this artifact without a timing-free canonical identity.")), "epistemic_status": "OBSERVED"})
    inherited = {row["id"] for row in json.loads((ARTIFACTS / "g0-theorem-dependency-graph-v1.json").read_text())["nodes"]}
    node_ids = {row[0] for row in NODES}
    if inherited - node_ids:
        raise RuntimeError(f"omitted inherited nodes: {sorted(inherited-node_ids)}")
    matrix = []
    for ident, inherited_node, required, route, source, gaps, validity in NODES:
        for filename in list(route) + list(source):
            if not (ARTIFACTS / filename).is_file():
                raise RuntimeError(f"{ident} references absent evidence {filename}")
        matrix.append({"id": ident, "inherited_graph_node": inherited_node, "required_two_route_evidence": required, "two_route_evidence": route, "source_hypothesis_evidence": source, "open_gaps": gaps, "reported_tag_validity": validity, "epistemic_status": "OBSERVED"})
    source_manifest_state = source_manifest_v2_state()
    if source_manifest_state["status"] != "CURRENT":
        next(row for row in matrix if row["id"] == "SOURCE-MANIFEST")["open_gaps"].append("Source-manifest v2 is stale or incomplete: " + source_manifest_state["detail"])
    global_gaps = ["Route A v4 must independently pin the archival explicit-formula source/proof unit and its six formula/convention labels.", "Explicit per-route resource evidence for the G0 60-second/256-MiB condition is still required.", "Cycle-2 Stream-C two-route reconciliation v1 depends on the raw timed Route-A v1 byte hash and needs a versioned timing-free correction for suite-stable replay."]
    if source_manifest_state["status"] != "CURRENT":
        global_gaps.append("Source-manifest v2 is not current against the direct source inventory; issue a versioned metadata correction before relying on its coverage.")
    return {"artifact_id": "g0-dependency-evidence-matrix-v2", "schema": 2, "epistemic_status": "OBSERVED", "claim_boundary": "Deterministic coverage audit of prior Cycle-1/Cycle-2 records. It reports prior labels without revalidating mathematics and does not declare G0 PASS.", "inventory_scope": {"included": "every JSON artifact directly under artifacts/ at build time, except this self-referential output", "self_exclusion": OUTPUT.name, "source_manifest_v2_included": True, "source_manifest_v2_state": source_manifest_state, "epistemic_status": "OBSERVED"}, "artifact_inventory": inventory, "nodes": matrix, "open_global_gaps": global_gaps, "historical_nondeterministic_timing_artifacts": timing, "verification": {"algorithm": "SHA-256", "builder": "proof/audit_g0_dependency_evidence_v2.py", "builder_sha256": sha256(Path(__file__).resolve()), "epistemic_status": "OBSERVED"}}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(), indent=2, sort_keys=True) + "\n").encode()
    if args.write:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(PROJECT)}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_bytes() != payload:
        print("G0 dependency evidence matrix is stale; rerun with --write", file=sys.stderr)
        return 1
    print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
