# Cycle 197 / B034 preregistration: Gaussian Abel test for the vertical tail

Cycle 196 eliminates finite pole crossings on the central contour.  This
block tests the most canonical scalar regularization of the remaining
imaginary-infinity obstruction: the even Gaussian Abel factor.  It is a
falsifiable engine, not a declaration that a Gaussian prescription is the
desired endpoint distribution.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 197,
  "parameters": {
    "fixed_endpoint_contour": {
      "kind": "expression",
      "value": "At beta=(5+sqrt(21))/2, set omega=24*beta-5=55+12*sqrt(21), Q=omega+1, and use y=Re(Q)/2+i*lambda, lambda in R. Retain the Cycle-196 zero finite-crossing and zero anti-jump vector; no contour displacement is allowed.",
      "rationale": "The source central contour and finite jump rule are already fixed independently of the tail test."
    },
    "gaussian_abel_family": {
      "kind": "expression",
      "value": "For epsilon>0, multiply the central-contour integrand by exp(epsilon*(y-Re(Q)/2)^2)=exp(-epsilon*lambda^2). The test space is the 36 frozen real endpoint Fourier components indexed by (a,b) in (Z/6Z)^2, with centered alpha proportional to 4b-5a in {-3,-2,-1,0,1,2}; no frequency-dependent regulator or analytic continuation of alpha is allowed.",
      "rationale": "This is the canonical even heat/Abel cutoff on the fixed vertical coordinate and an all-component, not selected-row, test."
    },
    "asymptotic_failure_criterion": {
      "kind": "expression",
      "value": "Use the published g=Q asymptotic: after the quadratic Gamma_M terms cancel, the endpoint integrand has a nonzero constant tail times exp(-B*alpha*lambda), B=2*pi/(24*omega)>0. For every alpha!=0, the growing tail under the Gaussian cutoff has Laplace scale exp(B^2*alpha^2/(4*epsilon)). The Gaussian rule fails if this exact scale is present for every nonzero component; alpha=0 modes are reported separately and may not rescue a uniform 36-component prescription.",
      "rationale": "A source asymptotic is converted into an explicit regulator falsifier without fitting a tail subtraction."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A positive result would require a finite epsilon->0 limit for all 36 components under this one regulator. A negative result may state only that the fixed scalar even Gaussian Abel family does not give a uniform raw real-frequency endpoint continuation. It may not exclude a tilted/Fresnel, frequency-continued, renormalized, or other distributional construction.",
      "rationale": "The test distinguishes one concrete regularization from the still-open endpoint theorem."
    }
  },
  "resource_caps": {
    "endpoint_components": {"kind":"integer","value":36,"rationale":"Full characteristic grid."},
    "nonzero_frequency_components": {"kind":"integer","value":30,"rationale":"The exact 6+30 centered-frequency split."},
    "zero_frequency_components": {"kind":"integer","value":6,"rationale":"Reported separately, never extrapolated."},
    "regulator_families": {"kind":"integer","value":1,"rationale":"Only the prescribed even Gaussian family."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Laplace divergence is exact symbolic asymptotics."},
    "wall_seconds": {"kind":"integer","value":30,"rationale":"Finite lattice and exact exponent ledger."},
    "floating_point": {"kind":"not_applicable","justification":"Numerical cutoff instability cannot prove or disprove the prescribed epsilon limit.","rationale":"The criterion is the exact positive 1/epsilon exponent."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov endpoint Gamma_M asymptotics at g=Q",
    "Cycle-196 central contour and pole-free geometry",
    "the all-36 centered d=6 Fourier-frequency ledger",
    "exact Gaussian Laplace asymptotics"
  ],
  "selection_rule": [
    "Enumerate every (a,b) mod6 and use its centered frequency; report all six zero modes separately.",
    "For alpha!=0, derive the sign-independent positive exponent B^2*alpha^2/(4*epsilon) from the growing tail, retaining the nonzero source tail coefficient as a named factor.",
    "Call the Gaussian family failed only if all 30 nonzero components have this positive exponent and no fitted subtraction is introduced.",
    "Do not promote a result to endpoint continuation unless all 36 prescribed limits are actually finite."
  ],
  "failure_rule": [
    "Failure excludes only the one fixed, even, scalar Gaussian Abel family on raw real endpoint frequencies. It does not exclude a different contour, Fresnel rule, analytic-frequency continuation, finite-part subtraction, distributional construction, AFK evaluation, fusion, or TCC.",
    "A zero-mode observation may not be used to claim a uniform 36-component endpoint rule.",
    "Do not choose a regulator after inspecting a component, fit a tail coefficient/counterterm, alter the fixed central contour, use selected exponents, s, d, or ray labels, or claim an RM-boundary, Stark/fusion/TCC consequence."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T03:13:41Z",
    "git_head": "e40637624f96b3013ad701ebf9f225ee3571c2e0",
    "git_state": "DIRTY only from concurrent repository-wide PROGRAM migration and unrelated projects/tools. This block freezes the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-196-b033-endpoint-contour-geometry-v1.json",
    "proof/verify_cycle_196_endpoint_contour_geometry.py",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
