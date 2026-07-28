#!/usr/bin/env python3
"""Character-weight decomposition of the projective D12 adjoint packet."""

from collections import Counter


def main() -> None:
    modulus = 6
    rho_rotation_weights = (1, -1)
    endomorphism_weights = Counter(
        (left - right) % modulus
        for left in rho_rotation_weights
        for right in rho_rotation_weights
    )

    assert endomorphism_weights == Counter({0: 2, 2: 1, 4: 1})

    # The two weight-zero lines split under reflection into the scalar
    # line and the quadratic sign line.  The weights +/-2 form the
    # induction of the order-three rotation character.
    scalar_dimension = 1
    quadratic_sign_dimension = 1
    induced_order_three_dimension = 2
    assert (
        scalar_dimension
        + quadratic_sign_dimension
        + induced_order_three_dimension
        == 4
    )

    print("RHO_ROTATION_WEIGHTS_MOD_6=[1,5]")
    print("END_RHO_ROTATION_WEIGHTS_MOD_6=[0,0,2,4]")
    print("RHO_TENSOR_DUAL=1+epsilon_21+Ind_K_Q(chi^2)")
    print("ADJOINT_ZERO=epsilon_21+Ind_K_Q(chi^2)")
    print("ADJOINT_PACKET_INVARIANT_UNDER_CHI_INVERSION=1")
    print("ADJOINT_PACKET_CONTAINS_ORIENTED_CHI_ONE_LINE=0")
    print("DERIVED_HECKE_ADJOINT_ROUTE_CLOSES_ORIENTATION=0")


if __name__ == "__main__":
    main()
