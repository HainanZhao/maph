#!/usr/bin/env python3
"""Exact graded positive-F3 jet representation audit for Cycle 250/B087."""
from __future__ import annotations

import json
from fractions import Fraction as F
from typing import TypeAlias

try:
    from .verify_cycle_226_signed_product_groupoid import AugmentedState, NODES, edge_inventory, f3, node_name, transition
    from .verify_cycle_228_f3_square_residual_block import blocks
    from .verify_cycle_249_common_jet_chamber import audit as chamber_audit
except ImportError:  # pragma: no cover
    from verify_cycle_226_signed_product_groupoid import AugmentedState, NODES, edge_inventory, f3, node_name, transition
    from verify_cycle_228_f3_square_residual_block import blocks
    from verify_cycle_249_common_jet_chamber import audit as chamber_audit


RANK = 4
EDGE_SCALE = 24
RETURN_SCALE = EDGE_SCALE**2
Pair: TypeAlias = tuple[F, F]
Word: TypeAlias = tuple[str, ...]
Polynomial: TypeAlias = dict[Word, F]
Jet: TypeAlias = list[Polynomial]
Matrix: TypeAlias = list[list[Polynomial]]


def vadd(left: Pair, right: Pair) -> Pair:
    return (left[0] + right[0], left[1] + right[1])


def vscale(value: F, vector: Pair) -> Pair:
    return (value * vector[0], value * vector[1])


def p_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for word, coefficient in right.items():
        result[word] = result.get(word, F(0)) + coefficient
        if result[word] == 0:
            del result[word]
    return result


def p_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            # Concatenation is intentional: factor atoms are never sorted or
            # commuted.  This is the ordered path algebra absent from C235.
            word = left_word + right_word
            result[word] = result.get(word, F(0)) + left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def p_scale(poly: Polynomial, scalar: F) -> Polynomial:
    return {word: scalar * coefficient for word, coefficient in poly.items() if scalar * coefficient}


def jet_mul(left: Jet, right: Jet) -> Jet:
    output: Jet = [{} for _ in range(RANK)]
    for degree in range(RANK):
        for left_degree in range(degree + 1):
            output[degree] = p_add(output[degree], p_mul(left[left_degree], right[degree - left_degree]))
    return output


def jet_scale(jet: Jet, scalar: F) -> Jet:
    return [p_scale(coefficient, scalar) for coefficient in jet]


def jet_pull(jet: Jet, scale: int) -> Jet:
    return [p_scale(coefficient, F(scale**degree)) for degree, coefficient in enumerate(jet)]


def toeplitz(jet: Jet) -> Matrix:
    return [[jet[row - col] if row >= col else {} for col in range(RANK)] for row in range(RANK)]


def diagonal(scale: int) -> Matrix:
    return [[{(): F(scale**row)} if row == col else {} for col in range(RANK)] for row in range(RANK)]


def matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    output: Matrix = [[{} for _ in range(RANK)] for _ in range(RANK)]
    for row in range(RANK):
        for col in range(RANK):
            for pivot in range(RANK):
                output[row][col] = p_add(output[row][col], p_mul(left[row][pivot], right[pivot][col]))
    return output


def matrix_scale(matrix: Matrix, scalar: F) -> Matrix:
    return [[p_scale(entry, scalar) for entry in row] for row in matrix]


def render_polynomial(poly: Polynomial) -> str:
    if not poly:
        return "0"
    terms = []
    for word, coefficient in poly.items():
        atom = "*".join(word) if word else "1"
        terms.append(f"({coefficient})*{atom}")
    return " + ".join(terms)


def render_matrix(matrix: Matrix) -> list[list[str]]:
    return [[render_polynomial(entry) for entry in row] for row in matrix]


def spec(c: F, alpha: Pair, beta: Pair) -> dict[str, object]:
    return {"c": c, "alpha": alpha, "beta": beta}


def derive_path_factors(start: str) -> dict[str, object]:
    p, k, r, s = NODES[start]
    assert k == s == 24
    first_periods = (F(1), F(r))
    second_periods = (F(p), F(1))
    target_raw = f3(NODES[start])
    target = node_name(target_raw)
    target_p, target_k, target_r, target_s = target_raw
    assert target_k == target_s == 24

    first_local = [
        spec(F(1, 24), vscale(F(1, 24), first_periods), (F(0), F(1))),
        spec(F(1, 24), (F(1), F(0)), vscale(F(1, 24), second_periods)),
    ]
    return_first = vadd(first_periods, vscale(F(target_r), second_periods))
    return_second = vadd(vscale(F(target_p), first_periods), second_periods)
    assert return_first == (F(RETURN_SCALE), F(0))
    assert return_second == (F(0), F(RETURN_SCALE))
    second_local = [
        spec(F(1, 24), vscale(F(1, 24), return_first), second_periods),
        spec(F(1, 24), first_periods, vscale(F(1, 24), return_second)),
    ]
    second_pulled = [
        spec(F(EDGE_SCALE) * item["c"], item["alpha"], item["beta"]) for item in second_local
    ]
    return {
        "start": start,
        "target": target,
        "first_period_map": [first_periods, second_periods],
        "return_period_map": [return_first, return_second],
        "first_local": first_local,
        "second_local": second_local,
        "second_pulled": second_pulled,
        "all_pulled": first_local + second_pulled,
    }


def block_specs(start: str) -> list[dict[str, object]]:
    output = []
    for item in blocks()[start]:
        output.append(
            spec(
                F(str(item["argument_mu"])),
                tuple(F(str(value)) for value in item["alpha"]),  # type: ignore[arg-type]
                tuple(F(str(value)) for value in item["beta"]),  # type: ignore[arg-type]
            )
        )
    return output


def atom_definitions(label: str, alpha: Pair, beta: Pair) -> dict[str, str]:
    alpha_text = f"{alpha[0]}*omega1+{alpha[1]}*omega2"
    beta_text = f"{beta[0]}*omega1+{beta[1]}*omega2"
    a = f"2*pi*i/({alpha_text})"
    b = f"2*pi*i/({beta_text})"
    q = f"exp(2*pi*i*({alpha_text})/({beta_text}))"
    qt = f"exp(-2*pi*i*({beta_text})/({alpha_text}))"
    k0 = f"-({qt};{qt})_infinity/(({b})*({q};{q})_infinity)"
    l1 = f"-({b})/2-({a})*S1({qt};{qt})+({b})*S1({q};{q})"
    l2 = f"-({b})^2/12-({a})^2*S2({qt};{qt})+({b})^2*S2({q};{q})"
    l3 = f"-({a})^3*S3({qt};{qt})+({b})^3*S3({q};{q})"
    return {
        f"K_{label}_0": k0,
        f"K_{label}_1": f"({k0})*({l1})",
        f"K_{label}_2": f"({k0})*(({l2})+({l1})^2)/2",
        f"K_{label}_3": f"({k0})*(({l3})+3*({l1})*({l2})+({l1})^3)/6",
    }


def factor_jet(label: str, item: dict[str, object]) -> tuple[Jet, dict[str, str]]:
    c = item["c"]
    alpha = item["alpha"]
    beta = item["beta"]
    assert isinstance(c, F) and isinstance(alpha, tuple) and isinstance(beta, tuple)
    definitions = atom_definitions(label, alpha, beta)
    # The q-product derivation gives [mu^r]G=c^(r-1)K_r(alpha,beta).
    jet = [{(f"K_{label}_{degree}",): c ** (degree - 1)} for degree in range(RANK)]
    return jet, definitions


def chamber_rows() -> dict[str, dict[str, object]]:
    chamber = chamber_audit()
    assert chamber["epistemic_status"] == "PROVED"
    assert chamber["status"] == "COMMON_FIXED_UPPER_CHAMBER_FOR_C228_JETS"
    return {row["factor"]: row for row in chamber["factors"]}


def path_audit(start: str, chamber: dict[str, dict[str, object]]) -> dict[str, object]:
    derived = derive_path_factors(start)
    expected = block_specs(start)
    assert derived["all_pulled"] == expected

    edge_rows = {row["edge"]: row for row in edge_inventory()["edges"]}
    target = derived["target"]
    first_edge = edge_rows[f"{start}-F3->{target}"]
    second_edge = edge_rows[f"{target}-F3->{start}"]
    assert first_edge["source_product_definition_available"]
    assert second_edge["source_product_definition_available"]

    direct_factor_jets = []
    first_factor_jets = []
    second_local_factor_jets = []
    definitions: dict[str, str] = {}
    for position, item in enumerate(expected, 1):
        label = f"{start}{position}"
        row = chamber[label]
        assert row["argument_slope"] == str(item["c"])
        assert row["alpha"] == [str(value) for value in item["alpha"]]
        assert row["beta"] == [str(value) for value in item["beta"]]
        jet, factor_definitions = factor_jet(label, item)
        definitions.update(factor_definitions)
        direct_factor_jets.append(jet)
        if position <= 2:
            first_factor_jets.append(jet)
    for offset, item in enumerate(derived["second_local"], 3):
        label = f"{start}{offset}"
        jet, factor_definitions = factor_jet(label, item)
        # K_r depends only on alpha,beta, so the direct and local formulas
        # have exactly the same atom definition; only c^(r-1) changes.
        assert factor_definitions == {key: definitions[key] for key in factor_definitions}
        second_local_factor_jets.append(jet)

    h_first = jet_mul(first_factor_jets[0], first_factor_jets[1])
    h_second_local = jet_mul(second_local_factor_jets[0], second_local_factor_jets[1])
    direct = direct_factor_jets[0]
    for factor in direct_factor_jets[1:]:
        direct = jet_mul(direct, factor)
    graded = jet_mul(h_first, jet_scale(jet_pull(h_second_local, EDGE_SCALE), F(1, EDGE_SCALE**2)))
    assert graded == direct

    d24 = diagonal(EDGE_SCALE)
    d576 = diagonal(RETURN_SCALE)
    first_operator_at_tail_one = matrix_scale(matrix_mul(toeplitz(h_first), d24), F(1, EDGE_SCALE**2))
    second_operator_at_tail_zero = matrix_mul(toeplitz(h_second_local), d24)
    composed_operator = matrix_mul(first_operator_at_tail_one, second_operator_at_tail_zero)
    direct_operator = matrix_mul(toeplitz(direct), d576)
    assert composed_operator == direct_operator

    return {
        "start": start,
        "source_path": [first_edge["edge"], second_edge["edge"]],
        "derived_factor_specs_equal_C228_in_order": True,
        "ordered_factor_labels": [f"{start}{position}" for position in range(1, 5)],
        "local_coordinate_law": "mu_1=24*mu_0; mu_2=576*mu_0",
        "graded_transfer_law": "T_e^(n)=24^(-2*n)*M_(h_e)*P_24",
        "two_edge_normalization": "24^(-2)",
        "jet_identity_holds_degree_0_to_3": True,
        "matrix_identity": "T_first^(1)*T_second^(0)=M_(mu^4*R_full)*P_576",
        "matrix_identity_holds": True,
        "direct_multiplier_matrix": render_matrix(toeplitz(direct)),
        "source_coefficient_definitions": definitions,
    }


def audit() -> dict[str, object]:
    chamber = chamber_rows()
    paths = [path_audit(start, chamber) for start in ("A", "C")]
    assert all(path["matrix_identity_holds"] for path in paths)
    return {
        "epistemic_status": "PROVED",
        "status": "GRADED_POSITIVE_F3_JET_REPRESENTATION_CONSTRUCTED",
        "regularization": "Both embeddings at w_sigma=t_sigma+i, as certified by C249/B086",
        "ordered_path_algebra": "Coefficient monomials concatenate in source factor order and are never sorted or commuted.",
        "paths": paths,
        "representation": {
            "objects": "pole-order-graded rank-four analytic jet spaces J_v=nu^(2*length(v))*R_v(nu) mod nu^4",
            "arrows": "T_e^(n)=24^(-2*n)*M_(h_e)*P_24",
            "positive_A_C_edges_intertwined": True,
            "negative_k_or_cross_sign_law_derived": False,
        },
        "conclusion": "The two frozen positive F3 paths define a source-specific, coordinate-aware graded rank-four jet representation in C249's fixed chamber. The forced 24^(-2n) normalization makes each two-edge operator equal the direct C228 four-factor operator with P_576. This supplies no negative-k, cross-sign, endpoint, or tilt-independent law.",
        "claim_boundary": "This proves only the fixed-tilt graded representation of the A/C positive F3 path fragments. It does not take an endpoint limit, establish tilt independence, derive a negative-k or cross-sign Gamma_M law, define a packet map or canonical current, or imply a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
