"""Frozen conventions for the fixed-ray character-aware P7-3 reduction.

The ambient complete ray-class character group is used only to make Fourier
identities exact.  The selected P7 family remains the primitive, exact-finite-
conductor family fixed in the P7 preregistration.
"""
from __future__ import annotations


SCHEMA_VERSION = "p7-fixed-ray-colour-diagonalization-v1"
GATE_ID = "P7-3-IDEAL-CUBIC-ENERGY"
FIELD = "K=Q(i), O_K=Z[i]"
SHELL = "Q<N(f)<=2Q, Q>=8; f is the exact finite conductor"
ARCHIMEDEAN_TYPE = "trivial; the Thorner large-sieve parameter is m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
RESOURCE_LIMITS = {
    "wall_seconds_strictly_less_than": 60,
    "rss_kib_strictly_less_than": 262144,
}

# These are exact finite checks, frozen before the replay.  They are not a
# numerical search and use only integer/Fraction arithmetic.
EXACT_CHECKS = {
    "fourier_projector_group_order": 2,
    "coloured_cubic_group_order": 2,
    "coloured_energy_group_order": 3,
    "coloured_energy_progression_length": 4,
    "one_height_group_order": 5,
    "completion_group_order": 3,
    "completion_diagonal_scale": 7,
    "shell_Q_values": (8, 16, 32),
    "fallback_threshold_powers": (2, 4, 4),
}

SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
        "locators": "selected primitive family and frozen P7-3 gate boundary",
    },
    "p7_ray_orthogonality_v1": {
        "path": "artifacts/p7-ray-orthogonality-v1.json",
        "sha256": "d4ad1fb81ac2cac49f94fb73616b5134f96fadd86e44f0a94975683b2db0387d",
        "locators": "complete ambient ray group, primitive projector, and common-ideal L2 boundary",
    },
    "p7_norm_status_v3": {
        "path": "artifacts/p7-norm-aggregation-v3-status-correction.json",
        "sha256": "32d3f2a5ffc8c62e985c7b3c156ddd9c0b00b23908d837b583d806e2c0e05aa8",
        "locators": "fixed-character norm collapse and N<=T^C normalization scope",
    },
    "p7_common_ideal_cubic_v1": {
        "path": "artifacts/p7-common-ideal-cubic-v1.json",
        "sha256": "5363288906df50df18e96afec0760c1fa8bfec912e61bbf05fa60492c77957f2",
        "locators": "labelled ideal Gram/cubic identity and fixed-modulus coloured energy",
    },
    "p7_common_ideal_cubic_v3": {
        "path": "artifacts/p7-common-ideal-cubic-v3-test-correction.json",
        "sha256": "caf4055315ccdcb265263c8594f3511108522494793093ef2cbcf0adf290c0dd",
        "locators": "latest preserved test-correction boundary for the P7-3 predecessor chain",
    },
    "guth_maynard_tex": {
        "path": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
        "locators": (
            "matrix/spectral reduction lines 477--739; additive energy lines 252--275; "
            "refined S3 bound lines 1684--1699; energy discussion lines 1778--1822"
        ),
    },
}

NON_PROMOTION = (
    "No Hecke large-value, zero-density, detector, or prime-ideal interval theorem.",
    "No assertion that the coloured primitive cubic excess has the Guth--Maynard bound.",
    "No assertion that primitive character selection can be completed to all characters at subpower cost.",
    "No assertion for varying fields, angular characters, or a common ray group across conductors.",
)
