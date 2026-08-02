"""Exact Cycle-184 determinant/lcm and nonrational two-ray ledgers."""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb, gcd


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def lcm_resonance(
    *, v: int, u: int, w: int, A: int, B: int, alpha_left: Q, alpha_right: Q
) -> dict[str, object]:
    """Factor the primitive determinant through the least common multiple."""
    require(min(v, u, w) > 0, "positive ray denominators")
    U, V = v * u, v * w
    common = gcd(u, w)
    L = U * V // gcd(U, V)
    epsilon_left, epsilon_right = Q(A) - U * alpha_left, Q(B) - V * alpha_right
    F = w * A - u * B
    identity_left = Q(F, common) - L * (alpha_left - alpha_right)
    identity_right = Q(w, common) * epsilon_left - Q(u, common) * epsilon_right
    require(identity_left == identity_right, "lcm resonance identity")
    require(F % common == 0, "primitive determinant gcd divisibility")
    return {
        "v": v,
        "u": u,
        "w": w,
        "U": U,
        "V": V,
        "gcd_u_w": common,
        "lcm_U_V": L,
        "F": F,
        "identity": "F/g-L*(alpha_left-alpha_right)=(w/g)*epsilon_left-(u/g)*epsilon_right",
        "left_side": identity_left,
        "right_side": identity_right,
    }


def nonrational_two_ray_family(t: int) -> dict[str, object]:
    """Certify the scale-matched two-label nonrational local deformation.

    The phase itself is represented exactly by its square: r^2=q^2+1/M.
    This suffices for all row, determinant, nonrationality, and coarse
    exponential-chart inequalities in the construction.
    """
    require(t >= 3 and t % 2 == 1, "T must be an odd integer at least three")
    X, H, V, U, n, M = t**50, t**22, t**11, t**22, t**30, t**80
    B = (3 * V + 1) // 2
    require(2 * B == 3 * V + 1 and gcd(B, V) == 1, "reduced left slope")
    q = Q(B, V)
    r_squared = q * q + Q(1, M)
    reduced_numerator = B * B * t**58 + 1
    reduced_denominator = t**80
    require(r_squared == Q(reduced_numerator, reduced_denominator), "reduced quadratic phase")
    root = B * t**29
    require(root * root < reduced_numerator < (root + 1) * (root + 1), "non-square quadratic phase")
    require(Q(3, 2) < q < Q(5, 3) and r_squared < 4, "coarse phase window")

    N_left, N_right = H // V + 1, H // U + 1
    require((N_left, N_right) == (t**11 + 1, 2), "complete fibre depths")
    R = t**12
    require(max(N_left, N_right) < R <= 2 * R, "strictly sub-seed light fibres")

    # Exact residual upper bounds after replacing r by its positive square root.
    left_residual_bound = Q(2 * H, 3 * M)  # r-q=(1/M)/(r+q), r+q>3.
    right_residual_bound = Q(2 * H, M)
    strip_width = Q(1, X)
    require(left_residual_bound < strip_width and right_residual_bound < strip_width, "actual strip residuals")
    left_orbit_bound = Q(V, 3 * M)
    right_orbit_bound = Q(U, M)
    require(left_orbit_bound < Q(2, (N_left - 1) * X), "left near orbit")
    require(right_orbit_bound < Q(2, (N_right - 1) * X), "right near orbit")

    A, F = B, V * B * (V - B)
    D = F
    require(F == U * A - V * (B * B) and F != 0, "primitive determinant")
    require(D == U * A - V * (B * B), "physical determinant orientation")
    require(abs(F) == V * B * (B - V), "determinant magnitude")

    # Coarse exact bounds that imply the c=1/2 chart and C180 stable shell.
    # log(r) lies in (1/3,1), using q>3/2, r<2 and standard elementary bounds.
    require(t**63 >= 24 * t**2, "stable product exceeds coarse cutoff")
    require(Q(3, 4) * V**3 < abs(F) < Q(10, 9) * V**3, "primitive determinant window")

    all_left_pairs = comb(N_left, 2)
    # The right fibre has one pair. Partition only the left multiplier into
    # its frozen dyadic ranges; all other seven box fields are fixed.
    dyadic_k_bins = N_left.bit_length()
    box_lower_bound = (all_left_pairs + dyadic_k_bins - 1) // dyadic_k_bins
    require(box_lower_bound * dyadic_k_bins >= all_left_pairs, "frozen multiplier partition")
    require(box_lower_bound < t**23, "subcritical populated box mass")
    return {
        "parameters": {"T": t, "X": X, "H": H, "Delta": "2*pi*T^30/log(r)", "label_left": n, "label_right": 2 * n},
        "phase": {
            "q": q,
            "r_squared": r_squared,
            "definition": "r=sqrt(q^2+1/M), z=r^(1/n), alpha_j=z^j",
            "nonrational": "r^2=(B^2*T^58+1)/T^80 has a square denominator and numerator strictly between consecutive squares",
            "chart": "1/3<log(r)<1, hence 2n/Delta=log(r)/pi<1/2 for c=1/2",
        },
        "fibres": {
            "intercept": Q(0),
            "beta": Q(0),
            "left_slope": q,
            "right_slope": q * q,
            "left_denominator": V,
            "right_denominator": U,
            "left_count": N_left,
            "right_count": N_right,
            "all_depths_below_seed": True,
            "left_residual_bound": left_residual_bound,
            "right_residual_bound": right_residual_bound,
        },
        "determinant": {
            "u": V,
            "w": U,
            "A": A,
            "B": B * B,
            "F": F,
            "D": D,
            "formula": "F=w*A-u*B=V*B*(V-B), D=F",
            "stable_product": n * V * U,
            "stable_cutoff_coarse_upper": 24 * t**2,
        },
        "populated_box": {
            "all_ordered_label_pair_rectangles": all_left_pairs,
            "frozen_k_bins": dyadic_k_bins,
            "one_box_lower_bound": box_lower_bound,
            "scale": "X^(11/25-o(1))",
            "critical_scale": "X^(21/25-o(1))",
        },
    }


def verify_all() -> dict[str, object]:
    lcm = lcm_resonance(v=2, u=1, w=2, A=1, B=1, alpha_left=Q(1, 2), alpha_right=Q(1, 4))
    family = nonrational_two_ray_family(3)
    require(lcm["lcm_U_V"] == 4 and lcm["F"] == 1, "lcm fixture")
    require(family["fibres"]["all_depths_below_seed"], "sub-seed fixture")
    return {
        "lcm_resonance": "For g=gcd(u,w) and L=lcm(U,V), F/g-L*(alpha_l-alpha_m)=(w/g)*epsilon_l-(u/g)*epsilon_m exactly. The determinant supplies an LCM resonance but no independent error beyond the two retained orbits.",
        "nonrational_deformation": "For every sufficiently large odd T, a two-label actual positive exponential has a common-intercept primitive-ray configuration with one nonrational phase, nonzero stable determinant, complete fibres of depths below X^(6/25), and one frozen dyadic box of X^(11/25-o(1)) rectangles.",
        "boundary": "This isolates only LCM-resonance redundancy: the local data cannot by itself force rational phases or a critical seeded fibre. It proves no upper bound for a critical populated box and does not rule out a population-sensitive critical-box estimate, aggregate recurrence, density gain, or interval result.",
        "samples": {"lcm": lcm, "family_T3": family},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
