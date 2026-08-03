#!/usr/bin/env python3
"""Exact state-completeness audit for Cycle 226/B063.

The raw F2/F3 matrix maps form a four-node square.  This verifier keeps the
period basis, affine argument, discrete label, and both ordinary-gamma
residuals attached to each arrow.  It deliberately distinguishes a formal
matrix substitution at k<0 from a source-authorized functional identity.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


State = tuple[int, int, int, int]  # (p, k, r, s)
Pair = tuple[int, int]  # coefficients in the frozen (omega1, omega2) basis


NODES: dict[str, State] = {
    "A": (-115, 24, 5, 24),
    "B": (-5, -24, 115, -24),
    "C": (115, 24, -5, 24),
    "D": (5, -24, -115, -24),
}
POSITIVE_REPRESENTATIVES: dict[str, State] = {
    "A": NODES["A"],
    "B": (5, 24, -115, 24),
    "C": NODES["C"],
    "D": (-5, 24, 115, 24),
}


def add(left: Pair, right: Pair) -> Pair:
    return (left[0] + right[0], left[1] + right[1])


def scale(integer: int, pair: Pair) -> Pair:
    return (integer * pair[0], integer * pair[1])


def f2(state: State) -> State:
    p, k, r, s = state
    return (-r, -s, -p, -k)


def f3(state: State) -> State:
    p, k, r, s = state
    return (-p, s, -r, k)


def node_name(state: State) -> str:
    for name, candidate in NODES.items():
        if candidate == state:
            return name
    raise AssertionError(f"state escaped frozen raw orbit: {state}")


def residuals(kind: str, state: State) -> list[str]:
    """Transcribe, without scalarization, the two gamma factors in (16)/(17)."""
    p, k, r, _s = state
    first_label = f"{k}+m" if kind == "F2" else "m"
    second_label = f"{k}-({p})*m" if kind == "F2" else f"-({p})*m"
    return [
        f"gamma((mu+({first_label})*omega2)/({k}); (omega1+({r})*omega2)/({k}), omega2)",
        f"gamma((mu+({second_label})*omega1)/({k}); omega1, (omega2+({p})*omega1)/({k}))",
    ]


@dataclass(frozen=True)
class AugmentedState:
    raw: State
    periods: tuple[Pair, Pair]
    # Argument is a*mu+b*m*omega2 in the initial coordinates.  Its label is
    # retained separately because the first F2/F3 move sets it to zero.
    argument: tuple[int, int]
    label: str


def transition(current: AugmentedState, kind: str) -> AugmentedState:
    p, _k, r, s = current.raw
    one, two = current.periods
    if kind == "F2":
        target = f2(current.raw)
        new_periods = (add(scale(p, one), two), add(one, scale(r, two)))
        multiplier = -s
    elif kind == "F3":
        target = f3(current.raw)
        new_periods = (add(one, scale(r, two)), add(scale(p, one), two))
        multiplier = s
    else:
        raise AssertionError(f"unknown generator {kind}")

    # The source affine argument is +/-s*(mu+m*omega2) and has label zero.
    # After one move that label is zero, so subsequent moves multiply the
    # already transported argument; no scalarization is used here.
    a, b = current.argument
    if current.label == "m":
        b += 1
    else:
        assert current.label == "0"
    return AugmentedState(
        raw=target,
        periods=new_periods,
        argument=(multiplier * a, multiplier * b),
        label="0",
    )


def edge_inventory() -> dict[str, object]:
    rows = []
    for source_name, source in NODES.items():
        p, k, r, s = source
        for kind, target_fn, argument in (
            ("F2", f2, f"{-s}*(mu+m*omega2)"),
            ("F3", f3, f"{s}*(mu+m*omega2)"),
        ):
            target = target_fn(source)
            source_product_defined = k > 0
            rows.append(
                {
                    "edge": f"{source_name}-{kind}->{node_name(target)}",
                    "kind": kind,
                    "source_raw_state": list(source),
                    "target_raw_state": list(target),
                    "source_k": k,
                    "source_product_domain": "k>0" if source_product_defined else "k<0",
                    "source_product_definition_available": source_product_defined,
                    "target_positive_representative": list(POSITIVE_REPRESENTATIVES[node_name(target)]),
                    "period_map": (
                        [p, 1], [1, r]
                    ) if kind == "F2" else ([1, r], [p, 1]),
                    "affine_argument": argument,
                    "target_label": 0,
                    "ordinary_gamma_residuals": residuals(kind, source),
                    "residuals_scalarized": False,
                }
            )
    assert len(rows) == 8
    defined = [row for row in rows if row["source_product_definition_available"]]
    undefined = [row for row in rows if not row["source_product_definition_available"]]
    assert len(defined) == 4
    assert len(undefined) == 4
    assert all(len(row["ordinary_gamma_residuals"]) == 2 for row in rows)
    return {
        "epistemic_status": "PROVED",
        "directed_edge_count": len(rows),
        "edges": rows,
        "source_defined_edge_count": len(defined),
        "formal_negative_k_edge_count": len(undefined),
        "source_defined_edges": [row["edge"] for row in defined],
        "unavailable_inverse_or_negative_k_edges": [row["edge"] for row in undefined],
        "conclusion": "Only the four arrows with source k=24 have a source-defined rarefied-product input under the frozen convention. The four arrows sourced at B or D require a negative-k product and are formal matrix substitutions, not source-authorized factorization identities.",
    }


def raw_loop_audit() -> dict[str, object]:
    """Test all twelve preregistered raw loops on the augmented state."""
    words = {
        "F2_square": ("F2", "F2"),
        "F3_square": ("F3", "F3"),
        "alternating_square": ("F2", "F3", "F2", "F3"),
    }
    start_periods = ((1, 0), (0, 1))
    rows = []
    for start_name, start_raw in NODES.items():
        for loop_name, word in words.items():
            current = AugmentedState(start_raw, start_periods, (1, 0), "m")
            for generator in word:
                current = transition(current, generator)
            raw_closed = current.raw == start_raw
            fully_closed = (
                raw_closed
                and current.periods == start_periods
                and current.argument == (1, 0)
                and current.label == "m"
            )
            assert raw_closed
            assert not fully_closed
            rows.append(
                {
                    "start": start_name,
                    "raw_loop": loop_name,
                    "word": " then ".join(word),
                    "raw_matrix_returns": raw_closed,
                    "final_periods": {
                        "omega1": list(current.periods[0]),
                        "omega2": list(current.periods[1]),
                    },
                    "final_affine_argument": {
                        "mu_coefficient": current.argument[0],
                        "m_omega2_coefficient": current.argument[1],
                    },
                    "final_label": current.label,
                    "augmented_state_returns": fully_closed,
                }
            )
    assert len(rows) == 12
    assert all(row["raw_matrix_returns"] for row in rows)
    assert all(not row["augmented_state_returns"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "loop_count": len(rows),
        "loops": rows,
        "raw_loop_count": len(rows),
        "augmented_closed_loop_count": 0,
        "conclusion": "Every frozen raw matrix loop changes at least periods, affine argument, or label. Therefore the four-node raw orbit is not a state-complete factorization groupoid on which a loop cochain could be imposed.",
    }


def construction_boundary_audit() -> dict[str, object]:
    edges = edge_inventory()
    loops = raw_loop_audit()
    assert edges["source_defined_edge_count"] == 4
    assert loops["augmented_closed_loop_count"] == 0
    return {
        "epistemic_status": "PROVED",
        "negative_raw_nodes_have_positive_representatives": True,
        "complete_eight_edge_source_interface_available": False,
        "complete_twelve_loop_interface_available": False,
        "signed_product_groupoid_constructed": False,
        "reason": "A positive representative may support a new local product definition, but it does not supply the missing negative-k factorization arrows. Moreover, the preregistered raw loops do not close in the period/argument/label state required by the factorization formulas. Assigning an edge constant here would be a fitted datum rather than a cochain on a closed source groupoid.",
    }


def run() -> dict[str, object]:
    edges = edge_inventory()
    loops = raw_loop_audit()
    boundary = construction_boundary_audit()
    assert edges["directed_edge_count"] == 8
    assert loops["loop_count"] == 12
    assert not boundary["signed_product_groupoid_constructed"]
    return {
        "schema": "sic-stark-cycle-226-signed-product-groupoid-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the frozen four raw F2/F3 states, all eight displayed edge interfaces and all twelve raw matrix loops were tracked with periods, affine arguments, labels, and both ordinary-gamma residuals retained. Only the four k=24 source edges have a source-defined rarefied-product input; the four edges sourced at k=-24 lack one. Independently, none of the twelve raw matrix loops closes in the augmented period/argument/label state. Thus the proposed four-node state-complete signed-product groupoid cannot be constructed from the frozen interface. This does not rule out an enlarged signed-period/affine groupoid, a new signed-k product theorem, a source cross-sign law, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "edge_inventory": edges,
        "raw_loop_audit": loops,
        "construction_boundary_audit": boundary,
        "gate_outcome": {
            "four_node_signed_product_groupoid": "FALSIFIED_BY_UNCLOSED_AUGMENTED_LOOPS_AND_MISSING_NEGATIVE_K_ARROWS",
            "remaining_design_problem": "Enlarge the state space by the exact period-basis, affine-argument, and label transport semigroup; then construct a signed-k product and edge cochains on that enlarged groupoid before asserting any loop relation or affine E comparison.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
