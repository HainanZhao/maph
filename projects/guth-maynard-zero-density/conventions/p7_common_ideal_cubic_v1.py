"""Frozen conventions for the P7-3 common-ideal cubic/energy bridge."""
from __future__ import annotations


SCHEMA_VERSION = "p7-common-ideal-cubic-v1"
GATE_ID = "P7-3-IDEAL-CUBIC-ENERGY"
FIELD = "K=Q(i), O_K=Z[i]"
SHELL = "Q<N(f)<=2Q, Q>=8; f is the exact finite conductor"
ARCHIMEDEAN_TYPE = "trivial; the Thorner large-sieve parameter is m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
RESOURCE_LIMITS = {"wall_seconds_strictly_less_than": 60, "rss_kib_strictly_less_than": 262144}

# The P7-3 sample is coloured: a point keeps its exact conductor and its
# character.  Equal heights for different colours are allowed and must not be
# silently identified.
SAMPLE_CONVENTION = (
    "x=(f_x,chi_x,t_x), with chi_x primitive of exact finite conductor f_x; "
    "W is a finite subset of these labelled points. Separation is imposed "
    "inside each fixed (f,chi) fibre unless a new global-separation argument "
    "is supplied."
)

SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
        "locators": "selected family and the frozen P7-3 pass/fail boundary",
    },
    "p7_ray_orthogonality_v1": {
        "path": "artifacts/p7-ray-orthogonality-v1.json",
        "sha256": "d4ad1fb81ac2cac49f94fb73616b5134f96fadd86e44f0a94975683b2db0387d",
        "locators": "exact primitive projector and the common-ideal L2 boundary",
    },
    "p7_norm_status_v3": {
        "path": "artifacts/p7-norm-aggregation-v3-status-correction.json",
        "sha256": "32d3f2a5ffc8c62e985c7b3c156ddd9c0b00b23908d837b583d806e2c0e05aa8",
        "locators": "repeated-norm witness and N<=T^C normalization scope",
    },
    "guth_maynard_tex": {
        "path": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
        "locators": (
            "Theorem 1.1 lines 62--79; additive energy lines 252--275; "
            "cubic trace lines 608--730; R(v) and S3 lines 1025--1065; "
            "refined S3 bound lines 1680--1698"
        ),
    },
}

NON_PROMOTION = (
    "No common-sample ideal cubic/energy inequality, Hecke large-value theorem, zero-density theorem, detector, or prime-ideal interval theorem.",
    "No verbatim application of the Guth--Maynard integer Poisson/cubic argument to the joint primitive (chi,t) sample.",
    "No claim that the scoped obstruction excludes a character-aware, coloured, or conductor-by-conductor cubic theorem.",
    "No assertion for angular characters, varying fields, or varying discriminants.",
)
