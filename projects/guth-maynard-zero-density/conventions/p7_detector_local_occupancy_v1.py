"""Frozen conventions for the P7 detector-side local-occupancy reduction.

This file concerns selected primitive, exact-finite-conductor rows only.  It
does not complete a character, inflate its modulus, or change its extension
by zero on non-coprime ideals.
"""
from __future__ import annotations

from fractions import Fraction


SCHEMA_VERSION = "p7-detector-local-occupancy-v1"
GATE_ID = "P7-3-IDEAL-CUBIC-ENERGY"
FIELD = "K=Q(i), O_K=Z[i], D_K=4, n_K=2"
SHELL = "Q<N(f)<=2Q, Q>=8; every selected chi is primitive of exact finite conductor f"
ARCHIMEDEAN_TYPE = "trivial; the Thorner large-sieve parameter is m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
SAMPLING_RADIUS = Fraction(1, 4)
SOBLEV_RADIUS = Fraction(1, 4)
LOCAL_ZERO_CENTER_REAL_PART = Fraction(21, 20)
LOCAL_ZERO_CIRCLE_RADIUS = Fraction(3, 4)
RESOURCE_LIMITS = {
    "wall_seconds_strictly_less_than": 60,
    "rss_kib_strictly_less_than": 262144,
}

# Exact finite checks frozen before replay.  They are algebraic/combinatorial
# checks, not a search for zeros or detector data.
EXACT_CHECKS = {
    "colours": 3,
    "blocks": 4,
    "joint_threshold_squared": 7,
    "joint_mass": 21,
}

SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
        "locators": "selected exact-finite-conductor primitive Q(i) family and P7-3 boundary",
    },
    "p7_ray_orthogonality_v1": {
        "path": "artifacts/p7-ray-orthogonality-v1.json",
        "sha256": "d4ad1fb81ac2cac49f94fb73616b5134f96fadd86e44f0a94975683b2db0387d",
        "locators": "exact primitive indexing, zero extension, and m=0 Thorner specialization",
    },
    "p7_fixed_ray_colour_v1": {
        "path": "artifacts/p7-fixed-ray-colour-diagonalization-v1.json",
        "sha256": "426681db11b09b52dad029a2e0a5931e430a5a5224d55c8f4ca5908b26564027",
        "locators": "|X(f)|<=N(f)<=2Q and shell family bound sum_f|X(f)|<12Q^2",
    },
    "p7_selected_gram_excess_v1": {
        "path": "artifacts/p7-selected-gram-excess-v1.json",
        "sha256": "fac0f8bb8206ce7d0b008363ab9715859e4b5ed2d9932af5f86b684c52c2db5a",
        "locators": "selected time projection and the exact cubic discrepancy budget context",
    },
    "p7_fixed_ray_discrepancy_transfer_v1": {
        "path": "artifacts/p7-fixed-ray-discrepancy-transfer-v1.json",
        "sha256": "c943ef3b946c2a1392f226a080711a24b094d9e4cddbb141b2290375afeecc96",
        "locators": "D_Delta definition, fixed-ray transfer, and cubic-budget target",
    },
    "thorner_2019_rendered": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.rendered.txt",
        "sha256": "69cdec98f836569683371d73972bc6541fcf33c6ec902c384dbecb3273eb2bb3",
        "locators": "Theorem 2.1, printed pp.883--884: primitive Hecke large sieve",
    },
    "thorner_zaman_lfzd_tex": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1/LFZD_manuscript.tex",
        "sha256": "e77007c73da81c239fa009f6fce8befbc72989a0fd28f2ec4ff6952ff098f8f2",
        "locators": "FunctionalEquation and ZerosInCircle-Classical, source TeX lines 580--586 and 668--699",
    },
}

NON_PROMOTION = (
    "No P7 zero detector, large-value theorem, selected cubic estimate, zero-density theorem, or prime-ideal interval theorem is proved.",
    "No actual Hecke zero configuration is asserted by the finite coloured-block obstruction model.",
    "No completion to imprimitive characters, conductor inflation, or change to the frozen zero extension is used.",
    "No claim that the existing joint L2 inequality gives a subpower local occupancy bound without a common detector lower bound.",
    "No claim that controlling D_Delta alone supplies the separate averaged-block A_0 cubic input.",
)
