# Cycle 196 / B033 preregistration: endpoint contour geometry and finite jumps

Cycle 195 supplies six nonzero finite anti-residue germs.  Before choosing an
Abel or distributional finite part at real multiplication, this block tests
whether the source kernel has any finite pole crossings at all along the
attracting endpoint path.  The result distinguishes a finite residue-jump
problem from the known obstruction at imaginary infinity.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 196,
  "parameters": {
    "endpoint_path_and_strip": {
      "kind": "expression",
      "value": "Use beta=(5+sqrt(21))/2 and gamma(s)=(beta+beta^(-1)s^2+i*sqrt(21)*s)/(1+s^2) for 0<=s<=1. Set omega_1(s)=24*gamma(s)-5, omega_2=1, Q(s)=omega_1(s)+1, and c(s)=Re(Q(s))/2. The sole contour family is C_s={c(s)+i*lambda:lambda in R}.",
      "rationale": "This is the attracting half-axis near beta, where Re(omega_1)>0 and the source pole cones have a fixed real separation."
    },
    "true_pole_and_jump_rule": {
      "kind": "expression",
      "value": "For K_Q(y,m)=Gamma_M(y,m)Gamma_M(Q-y,-m), use the source true-pole divisors y=-j*omega_1-l and y=Q+j*omega_1+l, with j,l>=0 after the exact 24n+5j+m>=0 condition. A finite residue jump is recorded only if a true pole crosses C_s as s decreases in [0,1]. The six Cycle-195 anti germs are represented by their source poles y=-N, N=1,3,...,11, and use the same crossing rule.",
      "rationale": "It fixes every candidate finite crossing and its sign before any endpoint finite-part assertion."
    },
    "regular_part_state_space": {
      "kind": "expression",
      "value": "For each m mod24 and real Fourier frequency alpha, define only the symmetric contour truncation I_T(s;alpha,m)=integral_{c(s)-iT}^{c(s)+iT} exp(pi*i*alpha*(2y-Q(s))/(24*omega_1(s)))K_Q(y,m)dy/(i*sqrt(omega_1(s))). No limit T->infinity, Abel regulator, fitted counterterm, or identification with the beta transform is admitted unless separately proved by the frozen acceptance condition.",
      "rationale": "The truncation makes the regular part explicit while not silently assuming the known divergent endpoint integral converges."
    },
    "strict_acceptance": {
      "kind": "expression",
      "value": "A positive result requires an exact all-m true-pole cone separation for every 0<=s<=1, proof that C_s has zero finite crossings, and the resulting zero finite-jump vector for all six anti germs. An endpoint continuation is proved only if an additional source-derived T->infinity or specified distributional limit is established; otherwise it must be reported OPEN with imaginary infinity as the sole remaining obstruction.",
      "rationale": "Finite pole geometry alone cannot be mislabeled as endpoint regularity."
    }
  },
  "resource_caps": {
    "discrete_labels": {"kind":"integer","value":24,"rationale":"All kernel labels, not selected characteristics."},
    "anti_residue_germs": {"kind":"integer","value":6,"rationale":"All sealed B_(1,-) finite germs."},
    "path_interval_endpoints": {"kind":"integer","value":2,"rationale":"The closed attracting segment s=0,1 is handled symbolically."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Cone separation is exact real-part algebra."},
    "wall_seconds": {"kind":"integer","value":30,"rationale":"Finite symbolic divisor/crossing ledger."},
    "floating_point": {"kind":"not_applicable","justification":"A plot or endpoint sample cannot prove no crossings or a distributional limit.","rationale":"Only exact path and source divisors are authorized."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov true Gamma_M pole divisors",
    "the A_6 attracting real-multiplication geodesic",
    "the source two-gamma beta kernel and its Fourier phase",
    "Cycle-195 finite anti-residue germs"
  ],
  "selection_rule": [
    "Use every m mod24 and both kernel factors. Keep the true-pole inequality; an affine lattice point without it is not a crossing candidate.",
    "Record a crossing only from an equality of its real coordinate with c(s); show the side of every source pole for the entire closed path.",
    "Report the six anti-pole locations and their jump vector separately from the regular contour truncation.",
    "Call the endpoint continuation OPEN unless the stated T->infinity/distributional limit is actually established."
  ],
  "failure_rule": [
    "A finite crossing or separation failure contains only this fixed central-contour path; it does not exclude a tilted contour, a different source distribution, endpoint continuation, AFK evaluation, fusion, or TCC.",
    "Zero finite crossings do not prove a convergent vertical integral, a finite-part limit, nonzero endpoint amplitude, AFK identity, ray map, fusion, Stark, or TCC.",
    "Do not fit a contour displacement, residue sign, Abel regulator, counterterm, AFK map, selected exponent, s, d, or ray label; do not identify q and q_tilde off the endpoint."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T03:08:44Z",
    "git_head": "4653be8463a39a1fbacc6c2a8429a70c52524a40",
    "git_state": "DIRTY only from concurrent repository-wide PROGRAM migration and unrelated projects/tools. This block freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json",
    "proof/verify_cycle_195_finite_anti_residue_sum.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "scripts/dimension_six_beta_fourier.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
