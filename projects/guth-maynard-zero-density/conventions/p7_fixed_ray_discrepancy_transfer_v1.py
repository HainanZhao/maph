"""Frozen conventions for the P7 fixed-ray discrepancy transfer.

The complete ray-class group is used only in the exact Parseval identity.
The selected sample remains primitive with its exact finite conductor, and
every polynomial below retains the zero-extension convention.
"""
from __future__ import annotations


SCHEMA_VERSION = "p7-fixed-ray-discrepancy-transfer-v1"
GATE_ID = "P7-3-IDEAL-CUBIC-ENERGY"
FIELD = "K=Q(i), O_K=Z[i]"
SHELL = "Q<N(f)<=2Q, Q>=8; f is the exact finite conductor"
ARCHIMEDEAN_TYPE = "trivial; the Thorner large-sieve parameter is m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
SAMPLING_RADIUS = "Delta=1/4; all local windows are closed intervals of radius Delta"
RESOURCE_LIMITS = {
    "wall_seconds_strictly_less_than": 60,
    "rss_kib_strictly_less_than": 262144,
}

# Exact, finite algebra checks frozen before the builder.  They are not a
# numerical search and use only integers/Fractions.
EXACT_CHECKS = {
    "formal_transfer_weights": (2, 3),
    "progression_length": 5,
    "fibre_colours": 3,
    "fibre_blocks": 4,
    "exponent_loss_ratio": 16,
    "budget_group_order": 2,
    "budget_a3": 5,
    "budget_delta": 1,
}

SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
        "locators": "selected exact-conductor primitive Q(i) family and P7-3 gate boundary",
    },
    "p7_ray_orthogonality_v1": {
        "path": "artifacts/p7-ray-orthogonality-v1.json",
        "sha256": "d4ad1fb81ac2cac49f94fb73616b5134f96fadd86e44f0a94975683b2db0387d",
        "locators": "P7-2 projector, zero extension, and checked Thorner Theorem 2.1 specialization",
    },
    "p7_fixed_ray_colour_v1": {
        "path": "artifacts/p7-fixed-ray-colour-diagonalization-v1.json",
        "sha256": "426681db11b09b52dad029a2e0a5931e430a5a5224d55c8f4ca5908b26564027",
        "locators": "fixed-ray Fourier blocks, coloured energy boundary, and exact-conductor selection",
    },
    "p7_selected_gram_excess_v1": {
        "path": "artifacts/p7-selected-gram-excess-v1.json",
        "sha256": "fac0f8bb8206ce7d0b008363ab9715859e4b5ed2d9932af5f86b684c52c2db5a",
        "locators": "delta_2 Parseval identity and class-average cubic perturbation inequality",
    },
    "p7_norm_status_v3": {
        "path": "artifacts/p7-norm-aggregation-v3-status-correction.json",
        "sha256": "32d3f2a5ffc8c62e985c7b3c156ddd9c0b00b23908d837b583d806e2c0e05aa8",
        "locators": "a_Q(i)(n)<=tau(n) norm-collapse scope and N<=T^C subpower normalization",
    },
    "thorner_2019_rendered": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.rendered.txt",
        "sha256": "69cdec98f836569683371d73972bc6541fcf33c6ec902c384dbecb3273eb2bb3",
        "locators": "Theorem 2.1, rendered lines 650--719 / printed pp.883--884",
    },
    "zaman_tex": {
        "path": "artifacts/sources/p7-hecke-v1/zaman-1502.05679v4/Explicit_estimates_for_the_zeros_of_Hecke_L-functions.tex",
        "sha256": "9440e5d28903d641df03e261c5d9f497bfc7f63062d279b082d6077ad8eaf620",
        "locators": "lines 101--110 (ray group) and 298--303 (zero extension and conductor divides modulus)",
    },
    "guth_maynard_tex": {
        "path": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
        "locators": "selected cubic subtraction lines 477--739 and refined S3 source shape lines 1684--1764",
    },
}

NON_PROMOTION = (
    "No selected primitive cubic estimate of Guth--Maynard source shape is proved.",
    "No Hecke large-value, zero-density, detector, or prime-ideal interval theorem is proved.",
    "No assertion that per-character separation controls the required uncoloured difference sampling statistic.",
    "No assertion that the finite combinatorial sharpness models are detector or zero examples.",
    "No assertion for a common ray group across different exact conductors.",
)
