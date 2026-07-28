#!/usr/bin/env python3
"""Exact duality ledger for the legitimate d=6 helical Zak quotient.

The two general-gamma functional shifts

    e1=(omega1,5),  e2=(omega2,-1)

generate a dense subgroup after projection to R x Z/24, so they do not
define an ordinary topological Zak lattice.  The AFK grid only requires
their difference

    T=e1-e2=(Delta,6),  Delta=omega1-omega2.

The cyclic subgroup <T> is discrete and cocompact in
G=R x Z/24.  On X=G/<T>, the translations

    v_a=(0,-4),  v_b=(Delta/6,1)

generate a subgroup H isomorphic to (Z/6)^2.

A character of G is indexed by (xi,n), n mod 24:

    chi_(xi,n)(y,m)=exp(2*pi*i*xi*y)*omega_24^(n*m).

It descends to X exactly when xi*Delta+n/4 is an integer ell.  Its
restriction to H has finite frequencies

    (p_a,p_b)=(-n,ell) mod 6.

This gives the exact Pontryagin-dual map needed for the finite Zak
descent.  It also exposes the remaining alias sum: each finite frequency
collects four discrete beta modes and infinitely many continuous modes.
"""

from __future__ import annotations

import json


DISCRETE_LEVEL = 24
DIMENSION = 6


def quadratic_multiply(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    """Multiply a+b*beta using beta^2=5*beta-1."""

    constant_left, beta_left = left
    constant_right, beta_right = right
    return (
        constant_left * constant_right - beta_left * beta_right,
        (
            constant_left * beta_right
            + beta_left * constant_right
            + 5 * beta_left * beta_right
        ),
    )


def finite_frequency(discrete_mode: int, helical_integer: int) -> tuple[int, int]:
    return (
        (-discrete_mode) % DIMENSION,
        helical_integer % DIMENSION,
    )


def beta_discrete_mode(dual_label: int) -> int:
    return (5 * (dual_label - 2)) % DISCRETE_LEVEL


def beta_label_for_first_frequency(first_frequency: int, lift: int) -> int:
    """Return one of four N mod 24 labels above p_a."""

    return (first_frequency + 2 + DIMENSION * lift) % DISCRETE_LEVEL


def main() -> None:
    omega_one = (-5, 24)
    omega_two = (1, 0)
    delta = (-6, 24)
    d_parameter = (-1, 4)
    assert delta == tuple(6 * value for value in d_parameter)
    assert quadratic_multiply(d_parameter, d_parameter) == tuple(
        3 * value for value in omega_one
    )
    assert quadratic_multiply(d_parameter, delta) == tuple(
        18 * value for value in omega_one
    )

    # Work in coordinates (continuous coefficient of Delta, m mod 24).
    period = (1, 6)
    a_step = (0, -4)
    # b_step has continuous coefficient 1/6; store numerator over six.
    b_step_numerator = (1, 6)

    # Six steps close exactly by the helical period.
    assert (6 * a_step[0], 6 * a_step[1] % 24) == (0, 0)
    assert (
        b_step_numerator[0],
        b_step_numerator[1] % 24,
    ) == period

    # Independence of v_a and v_b in X.
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            # If i*v_a+j*v_b=n*T, the continuous coordinate forces
            # j=6n.  In the fundamental range j=0, hence n=0 and then
            # -4i=0 mod24 forces i=0.
            if first == 0 and second == 0:
                continue
            assert not (
                second == 0
                and (-4 * first) % DISCRETE_LEVEL == 0
            )

    restriction_records = []
    for discrete_mode in range(DISCRETE_LEVEL):
        for helical_integer in range(-6, 12):
            first_frequency, second_frequency = finite_frequency(
                discrete_mode,
                helical_integer,
            )
            # chi(v_a)=omega_24^(-4n)=omega_6^(-n).
            a_exponent_mod_six = (-discrete_mode) % DIMENSION
            # Descent gives xi*Delta=ell-n/4.  On v_b the continuous
            # factor exp(2pi*i*(ell-n/4)/6) cancels omega_24^n,
            # leaving omega_6^ell.
            b_exponent_mod_six = helical_integer % DIMENSION
            assert (
                first_frequency,
                second_frequency,
            ) == (a_exponent_mod_six, b_exponent_mod_six)
            restriction_records.append(
                {
                    "discrete_mode_n": discrete_mode,
                    "helical_integer_ell": helical_integer,
                    "finite_frequency": [
                        first_frequency,
                        second_frequency,
                    ],
                }
            )

    alias_records = []
    for first_frequency in range(DIMENSION):
        labels = [
            beta_label_for_first_frequency(first_frequency, lift)
            for lift in range(4)
        ]
        assert len(set(labels)) == 4
        modes = [beta_discrete_mode(label) for label in labels]
        assert all(
            (-mode) % DIMENSION == first_frequency
            for mode in modes
        )
        assert len(set(modes)) == 4
        for second_frequency in range(DIMENSION):
            base_alpha_coefficient_over_D = (
                4 * second_frequency - 5 * first_frequency,
                3,
            )
            for lift in range(4):
                dual_label = beta_label_for_first_frequency(
                    first_frequency,
                    lift,
                )
                raw_discrete_mode = 5 * (dual_label - 2)
                for continuous_lift in range(-4, 5):
                    helical_integer = (
                        second_frequency + 6 * continuous_lift
                    )
                    alpha_numerator_over_d = (
                        4 * helical_integer - raw_discrete_mode
                    )
                    alias_index_numerator = (
                        alpha_numerator_over_d
                        - (4 * second_frequency - 5 * first_frequency)
                    )
                    assert alias_index_numerator % 6 == 0
                    alias_index = alias_index_numerator // 6
                    # alpha/D=s/3=base/3+2*z.
                    assert (
                        3 * alpha_numerator_over_d
                        == (
                            3
                            * (4 * second_frequency - 5 * first_frequency)
                            + 18 * alias_index
                        )
                    )
            alias_records.append(
                {
                    "finite_frequency": [
                        first_frequency,
                        second_frequency,
                    ],
                    "beta_N_lifts_mod_24": labels,
                    "beta_discrete_modes_mod_24": modes,
                    "helical_integer_family": (
                        f"{second_frequency}+6*t, t in Z"
                    ),
                    "alpha_alias_family": (
                        "alpha=D*(4*p_b-5*p_a)/3+2*D*z, z in Z"
                    ),
                    "base_alpha_coefficient_over_D": list(
                        base_alpha_coefficient_over_D
                    ),
                    "three_step_alias_translation": (
                        "(alpha,N)->(alpha+Delta,N+6)"
                    ),
                    "finite_alias_count": 4,
                    "continuous_alias_count": "infinite",
                }
            )
    assert len(alias_records) == DIMENSION * DIMENSION

    result = {
        "schema": "sic-stark-dimension-six-helical-zak-v1",
        "ambient_group": "G=R x Z/24",
        "invalid_dense_subgroup": (
            "<(omega1,5),(omega2,-1)> is not a topological lattice"
        ),
        "helical_period": "T=(Delta,6), Delta=omega1-omega2",
        "helical_cyclic_subgroup_is_discrete_and_cocompact": True,
        "quotient": "X=G/<T>",
        "finite_subgroup_generators": {
            "v_a": "(0,-4)",
            "v_b": "(Delta/6,1)",
        },
        "finite_subgroup": "(Z/6)^2",
        "dual_descent_condition": "xi*Delta+n/4=ell in Z",
        "restricted_character_map": "(xi,n,ell)->(-n,ell) mod 6",
        "restriction_records": restriction_records,
        "beta_mode_map": "n=5*(N-2) mod 24",
        "real_multiplication_identity": (
            "omega1/Delta=D/18, D=(omega1-omega2)/6"
        ),
        "finite_frequency_aliases": alias_records,
        "single_beta_mode_equals_finite_transform": False,
        "remaining_alias_identity": (
            "For each (p_a,p_b), sum the four N lifts and all "
            "ell=p_b+6t Fourier values.  Exact reindexing combines them "
            "into alpha=D*(4p_b-5p_a)/3+2D*z; three z-steps equal the "
            "helical translation (Delta,6).  Determine the resulting "
            "three-class automorphy sum and reduce it to the AFK finite "
            "convolution coefficient."
        ),
        "conclusion": (
            "A rigorous compact Zak quotient exists, but it is generated "
            "by the helical difference period T, not by both irrational "
            "functional shifts.  Its dual restriction gives the AFK "
            "frequency map exactly.  The remaining proof is an explicit "
            "alias-summation theorem, not a one-mode specialization of "
            "the beta integral."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
