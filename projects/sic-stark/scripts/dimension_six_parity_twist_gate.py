#!/usr/bin/env python3
"""Archimedean parity gate for twists of the d=6 mixed character."""


def add_mod_two(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (left[0] ^ right[0], left[1] ^ right[1])


def main() -> None:
    mixed_parity = (0, 1)
    even_dirichlet_restriction = (0, 0)
    odd_dirichlet_restriction = (1, 1)

    even_twist = add_mod_two(mixed_parity, even_dirichlet_restriction)
    odd_twist = add_mod_two(mixed_parity, odd_dirichlet_restriction)
    reachable = {even_twist, odd_twist}

    assert reachable == {(0, 1), (1, 0)}
    assert (1, 1) not in reachable
    assert (0, 0) not in reachable

    print("TARGET_ARCHIMEDEAN_PARITY=[0,1]")
    print("DIRICHLET_RESTRICTION_PARITIES=[[0,0],[1,1]]")
    print("SCALAR_TWIST_REACHABLE_PARITIES=[[0,1],[1,0]]")
    print("TOTALLY_ODD_PARITY_REACHABLE=0")
    print("TOTALLY_EVEN_PARITY_REACHABLE=0")
    print("TOTALLY_ODD_STARK_THEOREM_APPLIES_AFTER_SCALAR_TWIST=0")


if __name__ == "__main__":
    main()
