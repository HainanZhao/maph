"""Frozen scope for the executed P7-1 norm-aggregation gate.

This module deliberately does *not* repeat the prospective character values
from the P7 preregistration.  The two proof routes calculate them from the
residue rings instead of importing them as expected constants.
"""
from __future__ import annotations


SCHEMA_VERSION = "p7-norm-aggregation-v1"
GATE_ID = "P7-1-NORM-AGGREGATION"
FIELD = "Q(i)"
RING = "Z[i]"
Q = 8
SHELL = "Q<N(f)<=2Q"
MODULI = ("(3)", "(1+i)^4=(4) up to a unit")
SPLIT_PRIME = 17
SPLIT_FACTORIZATION = "17=(4+i)(4-i)"

# Zaman, §1 and §2.1, is the frozen primary source for the ray-class,
# conductor, ideal-series, and Euler-product conventions.  GM Theorem 1.1 is
# the precisely stated single-polynomial estimate whose epsilon bookkeeping is
# checked here; it is not asserted for the Hecke family.
SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
    },
    "zaman_tex": {
        "path": "artifacts/sources/p7-hecke-v1/zaman-1502.05679v4/Explicit_estimates_for_the_zeros_of_Hecke_L-functions.tex",
        "sha256": "9440e5d28903d641df03e261c5d9f497bfc7f63062d279b082d6077ad8eaf620",
        "locators": "§1, lines 101--110; §2.1, lines 298--309",
    },
    "guth_maynard_tex": {
        "path": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
        "locators": "Theorem 1.1, TeX lines 62--79; reduction to N<T, lines 447--457",
    },
}

RESOURCE_LIMITS = {"wall_seconds_strictly_less_than": 60, "rss_kib_strictly_less_than": 262144}

GM_THEOREM_1_1 = {
    "coefficient_hypothesis": "|b_n|<=1",
    "sample_hypothesis": "1-separated t_r in [0,T]",
    "bound": "R<=T^(o(1)) (N^2 V^-2 + N^(18/5)V^-4 + T N^(12/5)V^-4)",
    "threshold_powers": (2, 4, 4),
    "height_length_condition_for_absorption": "N<=T^C for a fixed C; the GM proof's nontrivial reduction uses N<T",
}

NON_PROMOTION = (
    "This gate proves no Hecke-family large-value theorem, density theorem, or prime-ideal result.",
    "Different A_chi block only verbatim common-coefficient import to joint (chi,t) samples.",
    "The result does not rule out a character-aware, ideal-indexed, or separately summed method with its own accounting.",
)
