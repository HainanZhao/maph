#!/usr/bin/env python3
"""Assemble the proxy-clean theorem paper independently of census counts."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper/effective-stark-sweep-draft.md"
OUTPUT = ROOT / "paper/effective-stark-results-paper.md"
SEAL = ROOT / "artifacts/results-paper-scope-seal-v1.json"

HEADINGS = [
    "First new theorem: an order-six instance",
    "Second order-six theorem",
    "New theorem candidates and exponent economics",
    "Uniform Engine A after deduplication",
    "Theorem-value portfolio",
    "Two routes from disjoint theorem bases",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(source: str, heading: str) -> str:
    marker = f"## {heading}\n"
    start = source.index(marker)
    next_heading = source.find("\n## ", start + len(marker))
    if next_heading < 0:
        next_heading = len(source)
    return source[start:next_heading].strip()


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    selected = [section(source, heading) for heading in HEADINGS]
    no_go_start = source.index(
        "**Lemma (absolute-abelian one-place obstruction).**"
    )
    no_go_end = source.index(
        "\n## Census result and containment correction", no_go_start
    )
    no_go = source[no_go_start:no_go_end].strip()

    header = r"""# Certified archimedean Stark packets beyond the classical cases

**Results-paper scope:** FROZEN; independent of census population counts.

## Abstract

We give unconditional, replayable identifications of archimedean Stark
packets over real quadratic fields through three theorem bases: quadratic
analytic class-number formulae, Shintani's index-two algebraicity theorem
with explicit height rigidity, and CM descent to Stark's imaginary-quadratic
rank-one theorem.  The results include the first order-six and order-ten
instances in a frozen literature perimeter, two independent proofs of one
quartic packet, a uniform Engine-A reduction, and a no-go lemma excluding an
absolutely abelian fourth engine.  Every displayed packet is supported by
exact field and Artin-label computations and by Arb enclosures with explicit
height margins.  No census frequency, frontier count, or conductor-trend
claim is used.

## Claim boundary and theorem bases

The results below depend only on proxy-clean case bundles.  Engine A uses an
exact norm-kernel regulator index and the mixed-signature analytic
class-number formula.  Engine B uses genuine two-route field reconstruction,
printed divisor exponents, certified analytic enclosures, Sturm isolation,
and Voutier rigidity.  Engine C constructs the actual splitting closure and
uses exact linear reinduction, the global-unit clause with \(|S|\ge3\), and
oriented Arb lattice inversion.  Numerical cross-checks never enter a proof.

The theorem corpus comprises the seven reproduction anchors and 25 promoted
census case identities.  The R-13 audit found no PROXY predicate in any
case-level theorem chain.  Population completeness and all W4 statistics are
reserved for a separate census paper after genuine reconstruction v5.
"""
    method = r"""## Completeness lemma for the theorem taxonomy

""" + no_go + r"""

## Reproducibility and containment

Every result is tagged only after a replayable case bundle closes.  R-13 marks
every deciding computational predicate GENUINE or PROXY; no `VERIFIED_*` tag
may depend on a proxy.  A post hoc audit found an unmarked conjugation proxy in
the census classification layer, but not in any promoted theorem chain.  The
results paper is consequently invariant under every possible outcome of the
241-row B recovery, 252-row C completeness screen, and 8,200-row index rerun.

The principal machine-readable entry points are:

- `data/q7-p7-case-v1.json` for the first order-six theorem;
- `data/q33-p11-order10-case-v1.json` for the order-ten theorem;
- `data/rq000458-dual-case-v1.json` for the disjoint-route quartic packet;
- `artifacts/engine-c-w3-tranche-01-verified-v1.json` for the first generic
  Engine-C closure;
- `artifacts/engine-c-e6-tranche-01-verified-v1.json` for the elevated
  \(e=6\) controls;
- `artifacts/proxy-scope-and-tag-audit-v1.json` and
  `artifacts/predicate-provenance-ledger-r13-v1.json` for the claim-boundary
  audit.
"""
    output = (
        header.strip()
        + "\n\n"
        + "\n\n".join(selected)
        + "\n\n"
        + method.strip()
        + "\n"
    )
    OUTPUT.write_text(output, encoding="utf-8")
    payload = {
        "schema": "effective-stark-results-paper-scope-seal-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_SCOPE_SEPARATION",
        "paper": str(OUTPUT.relative_to(ROOT)),
        "paper_sha256": sha(OUTPUT),
        "included_source_sections": HEADINGS,
        "excluded_claim_families": [
            "census population counts",
            "FRONTIER taxonomy counts",
            "FRONTIER share versus conductor norm",
            "odd-index landscape",
            "C census completeness",
        ],
        "invariance": (
            "the paper's theorem statements cannot change under any "
            "outcome of recovery tracks a-c"
        ),
        "source_hashes": {
            str(SOURCE.relative_to(ROOT)): sha(SOURCE),
            "scripts/assemble_results_paper.py": sha(Path(__file__)),
        },
    }
    SEAL.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
