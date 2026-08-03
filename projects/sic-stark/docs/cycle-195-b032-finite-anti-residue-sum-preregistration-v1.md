# Cycle 195 / B032 preregistration: finite anti-residue combination

Cycle 194 v2 shows that the source-forced odd `B_(1,-)` channel has six
finite, rather than infinite, coincident true-pole orbits.  This block tests
the one source-defined operation still required before any endpoint analysis:
combine every orbit with the published gamma functional equations and decide
whether its total residue is identically zero as a meromorphic interior
function.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 195,
  "parameters": {
    "finite_true_pole_state_space": {
      "kind": "expression",
      "value": "For each canonical odd N in {1,3,5,7,9,11}, use precisely the Cycle-194-v2 true-pole orbit (z,j,n)=(-3k,k,-k), m=N+18k, with 0<=k<=N. Its residue coordinates are all referred to the common alpha_0=-N pole. No affine collision point outside this source-admissible set is a summand.",
      "rationale": "This incorporates the corrected Sarkissian--Spiridonov true-pole condition 24n+5j+m>=0 before combining residues."
    },
    "source_combination_rule": {
      "kind": "expression",
      "value": "Let c_(N,0) be the nonzero simple residue of the k=0 summand. For 1<=k<=N, define c_(N,k)=c_(N,k-1)/M_(N,k), where M_(N,k) is the exact threefold helical Gamma_M functional-equation multiplier obtained from the published shifts (mu,m)->(mu+omega_1,m+5) and (mu,m)->(mu+1,m-1), evaluated at the shared pole. The only combined residue is C_N=sum_(k=0)^N c_(N,k). No numerical residue, fitted scalar, or reordered/infinite sum is allowed.",
      "rationale": "The recurrence is source-defined and is used only on the finite true-pole orbit certified by v2."
    },
    "formal_cusp_test": {
      "kind": "expression",
      "value": "Use q=exp(2*pi*i*tau), q_tilde=exp(-2*pi*i/omega_1), t=q_tilde^(-1/24), and the frozen source multiplier variables x_1=q^(-k), x_2=w*q^k, a_1=zeta_24^(5k+19N)*t^(k-N-24), a_2=zeta_24^(4+5N+19k)*t^(-k+N-24). Clear only the source denominator factors. Test the exact q-adic order of each c_(N,k)/c_(N,0), and accept noncancellation only if C_N/c_(N,0) has constant coefficient 1 in the resulting meromorphic formal ring for every N.",
      "rationale": "A distinct positive q-adic order is an exact nonidentity certificate; it is not an all-point nonvanishing or endpoint statement."
    },
    "cancellation_and_boundary_scope": {
      "kind": "expression",
      "value": "Audit the reflected Gamma_M pole and zero divisors at every finite summand, record all denominators excluded from the meromorphic domain, and report cancellation only for the six finite combined residues. Do not select a contour, take an RM limit, impose q=q_tilde, identify an AFK cocycle, or construct an endpoint finite part in this cycle.",
      "rationale": "The finite combination is a necessary source-local input to a later distributional or contour continuation, not that continuation itself."
    }
  },
  "resource_caps": {
    "canonical_odd_orbits": {"kind":"integer","value":6,"rationale":"All six B_(1,-) coordinates."},
    "maximum_orbit_depth": {"kind":"integer","value":11,"rationale":"The largest corrected orbit has k=0,...,11."},
    "true_pole_summands": {"kind":"integer","value":42,"rationale":"The fixed total 2+4+6+8+10+12."},
    "functional_equation_steps_per_depth": {"kind":"integer","value":3,"rationale":"One alias period shifts the discrete label by 18, assembled from three source r=5 shifts modulo 24 with the fixed omega_2 correction."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Only exact formal/divisor algebra is authorized."},
    "wall_seconds": {"kind":"integer","value":60,"rationale":"Finite symbolic ledger and exact formal-order audit."},
    "floating_point": {"kind":"not_applicable","justification":"No numerical residue, nonzero sample, or endpoint approximation can establish the declared meromorphic identity criterion.","rationale":"The acceptance condition is a formal constant coefficient."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov true Gamma_M pole/zero divisors and functional equations",
    "corrected Cycle-194 finite collision orbit",
    "source two-base helical multiplier with q, q_tilde, and t retained separately",
    "exact finite meromorphic residue sums and q-adic valuation"
  ],
  "selection_rule": [
    "Use every N and every certified depth k; enforce 24n+5j+m>=0 before including any summand.",
    "Verify that the reflected factor is finite nonzero for every included summand and record the source denominators in every recurrence ratio.",
    "Promote noncancellation only when all six normalized finite sums have formal constant coefficient exactly one after the fixed source recurrence; report every denominator locus and no all-point conclusion.",
    "If a numerator cancellation occurs, retain the exact N and normalized finite polynomial as the scoped falsifier; do not alter an orbit, ordering, or normalization."
  ],
  "failure_rule": [
    "A cancellation or failed functional-equation/divisor check contains only this finite source recurrence construction; it does not exclude another residue transform, distributional completion, endpoint continuation, AFK evaluation, fusion theorem, or TCC.",
    "A nonzero meromorphic finite combined residue does not prove all-point nonvanishing, a convergent Poincare series, an endpoint distribution, an AFK identity, a ray map, fusion, Stark, or TCC.",
    "Do not restore the v1 infinite tail, add a fibre, fit a scalar/counterterm, identify q and q_tilde off the boundary, use selected exponents, s, d, or ray labels, or suppress capital Gamma_M normalization or the AFK phase."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T03:02:25Z",
    "git_head": "9daaa666e524dab95cceb190ea6fc41b42b20c04",
    "git_state": "DIRTY only from concurrent repository-wide PROGRAM migration and unrelated projects/tools. This block freezes the listed SIC--Stark mathematical inputs and treats Cycle 194 v2 as authoritative over v1 for the collision orbit."
  },
  "input_paths": [
    "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
    "proof/verify_cycle_194_meromorphic_anti_channel_v2.py",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "scripts/dimension_six_two_base_lens.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
