"""Frozen conventions for the P7 selected-Gram cubic-excess reduction.

This is a fixed-field, finite-ray-class algebraic reduction.  The complete
ambient character group is used only for exact Fourier conjugation; selected
rows retain their primitive exact-conductor labels and zero extension.
"""
from __future__ import annotations


SCHEMA_VERSION = "p7-selected-gram-excess-v1"
GATE_ID = "P7-3-IDEAL-CUBIC-ENERGY"
FIELD = "K=Q(i), O_K=Z[i]"
SHELL = "Q<N(f)<=2Q, Q>=8; f is the exact finite conductor"
ARCHIMEDEAN_TYPE = "trivial; the Thorner large-sieve parameter is m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
RESOURCE_LIMITS = {
    "wall_seconds_strictly_less_than": 60,
    "rss_kib_strictly_less_than": 262144,
}

# Exact finite checks, frozen before the builder is written.  They use only
# integer/Fraction arithmetic and are not a numerical search.
EXACT_CHECKS = {
    "excess_sharpness_n": 11,
    "pinching_rank_one_size": 5,
    "class_average_group_order": 2,
    "class_average_selected_indices": (0, 3),
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
        "locators": "exact primitive projector, zero extension, and Thorner Theorem 2.1 shell specialization",
    },
    "p7_common_ideal_cubic_v3": {
        "path": "artifacts/p7-common-ideal-cubic-v3-test-correction.json",
        "sha256": "caf4055315ccdcb265263c8594f3511108522494793093ef2cbcf0adf290c0dd",
        "locators": "latest common-ideal Gram/cubic predecessor correction",
    },
    "p7_fixed_ray_colour_diagonalization_v1": {
        "path": "artifacts/p7-fixed-ray-colour-diagonalization-v1.json",
        "sha256": "426681db11b09b52dad029a2e0a5931e430a5a5224d55c8f4ca5908b26564027",
        "locators": "fixed-ray Fourier selection, completion barrier, and the aggregate cross-conductor definition corrected here",
    },
    "guth_maynard_tex": {
        "path": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
        "locators": (
            "spectral trace subtraction lines 477--739; R(v)/S3 lines 1025--1065; "
            "refined S3 bound lines 1684--1764"
        ),
    },
    "thorner_2019_rendered": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.rendered.txt",
        "sha256": "69cdec98f836569683371d73972bc6541fcf33c6ec902c384dbecb3273eb2bb3",
        "locators": "Theorem 2.1, rendered lines 650--715 / printed pp.883--884",
    },
}

NON_PROMOTION = (
    "No selected primitive cubic estimate of Guth--Maynard source shape is proved.",
    "No Hecke large-value, zero-density, detector, or prime-ideal interval theorem is proved.",
    "No claim that the raw L2 large sieve controls the centred Gram variance at the needed scale.",
    "No claim that the finite PSD countermodels are P7 detector or zero examples.",
    "No assertion for varying fields, angular characters, or a common ray group across conductors.",
)
