"""Frozen conventions for the P7-2 ray-class projector and L2 gate."""
from __future__ import annotations


SCHEMA_VERSION = "p7-ray-orthogonality-v1"
GATE_ID = "P7-2-RAY-CLASS-ORTHOGONALITY"
FIELD = "K=Q(i)"
RING = "O_K=Z[i]"
DEGREE = 2
SHELL = "Q<N(f)<=2Q, Q>=8; f is the exact finite conductor"
ARCHIMEDEAN_TYPE = "trivial: the source large-sieve parameter m is fixed to m=0"
IDEAL_EXTENSION = "chi(a)=0 when (a,f)!=1"
RESOURCE_LIMITS = {"wall_seconds_strictly_less_than": 60, "rss_kib_strictly_less_than": 262144}

# Source Theorem 2.1 is quoted through the pinned publisher text.  The source
# calls the conductor cutoff Q; this gate calls it R to avoid conflict with
# the selected dyadic-shell parameter Q.
THORNER_2019_LARGE_SIEVE = {
    "source": "J. Thorner, Math. Res. Lett. 26 (2019), Theorem 2.1, PDF pp.9--10 (printed pp.883--884)",
    "statement": "For c on integral ideals with ||c||_2^2=sum_{Na<=N}|c(a)|^2, sum_{Nq<=R} sum_{xi mod q}^* sum_{||m||_infty<=T} integral_{-T}^T |sum_{Na<=N} c(a)xi lambda_m(a)(Na)^(-it)|^2 dt << (N+R^2 T^n_K)(log(RT))^A ||c||_2^2.",
    "checked_specialization": "K=Q(i), n_K=2, R=2Q, m=0, Q>=8, T>=2, and c is one finitely supported coefficient function on integral ideals.",
    "conclusion": "sum_{Q<Nf<=2Q} sum_{chi primitive mod f} integral_{-T}^T |sum_{Na<=N} c(a)chi(a)(Na)^(-it)|^2 dt <<_K (N+4Q^2T^2)(log(2QT))^A ||c||_2^2.",
    "scope_limit": "It is an L2 large sieve for common ideal coefficients c(a). It is not a cubic/large-value theorem and it does not accept arbitrary character-dependent norm coefficients b_chi(n).",
}

SOURCES = {
    "p7_preregistration_v2": {
        "path": "artifacts/p7-hecke-qi-preregistration-v2.json",
        "sha256": "fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9",
        "locators": "selected family and P7-2 pass/fail boundary",
    },
    "p7_norm_aggregation_v2": {
        "path": "artifacts/p7-norm-aggregation-v2-correction.json",
        "sha256": "200f4328c72e2af2ffe08a9fd3b9901bbbf6b2977c18a34e20a20fb020f033d0",
        "locators": "P7-1 common-coefficient type mismatch and exact witness",
    },
    "zaman_tex": {
        "path": "artifacts/sources/p7-hecke-v1/zaman-1502.05679v4/Explicit_estimates_for_the_zeros_of_Hecke_L-functions.tex",
        "sha256": "9440e5d28903d641df03e261c5d9f497bfc7f63062d279b082d6077ad8eaf620",
        "locators": "lines 101--110 (ray group); lines 298--303 (conductor, primitive, zero extension)",
    },
    "thorner_2019_pdf": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.pdf",
        "sha256": "463bd56afd679444e4cf3417228230e9996b1202daeac47c3b436b4b2776d1b3",
        "locators": "Theorem 2.1, PDF pp.9--10 (printed pp.883--884)",
    },
    "thorner_2019_rendered": {
        "path": "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.rendered.txt",
        "sha256": "69cdec98f836569683371d73972bc6541fcf33c6ec902c384dbecb3273eb2bb3",
        "locators": "lines 650--756 (Theorem 2.1 and its notation)",
    },
}

NON_PROMOTION = (
    "No new Hecke zero-density, cubic-energy, detector, prime-ideal interval, or bounded-gap theorem.",
    "The exact primitive projector is not by itself a positive large-sieve bound after modulus summation.",
    "The cited L2 large sieve applies only to a common ideal coefficient function, not to arbitrary b_chi(n).",
    "The fixed m=0 specialization excludes angular characters; no angular-family assertion is made.",
)
