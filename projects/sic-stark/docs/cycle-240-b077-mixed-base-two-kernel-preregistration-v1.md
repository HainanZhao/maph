# Cycle 240 / B077 preregistration: mixed-base two-kernel composition

Cycle 239 excludes the literal rarefied beta kernel, but does not test the
smallest proposed construction: Fourier-transform the first two ordinary
gamma factors of a C228 word and close their convolution by Faddeev's
two-kernel main integral relation.  This cycle tests the exact common-period
condition before any contour or Fubini claim is made.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":240,
  "parameters":{
    "endpoint_field":{"kind":"expression","value":"Freeze beta^2-5*beta+1=0, beta>1, t=omega1/omega2=24*beta-5, and hence t^2-110*t+1=0. Work in Q(t), reducing every quadratic expression by t^2=110*t-1.","rationale":"This is the pinned d=6 period ratio and permits exact proportionality tests."},
    "frozen_two_factor_pairs":{"kind":"expression","value":"Freeze the first two C228 factors for both starts. A has P_A=((t+5)/24,1) and Q_A=(t,(1-115*t)/24). C has P_C=((t-5)/24,1) and Q_C=(t,(1+115*t)/24), where each ordered pair is an ordinary-gamma period pair and both arguments are mu/24.","rationale":"These are the smallest retained two-factor subwords, with no new factor or period choice."},
    "source_composition":{"kind":"expression","value":"Freeze Faddeev arXiv:1201.6464 equations (FTD) and (MIR). FTD Fourier-transforms one gamma for one normalized period system (omega,omega') with omega*omega'=-1/4; MIR closes a two-kernel ratio only when every displayed gamma has that same period system. Scaling and swapping one ordinary-gamma period pair are allowed only when they produce literally the same unordered period system; no modular or sign conversion is supplied by FTD/MIR.","rationale":"This is the proposed smallest source-based two-kernel construction and its indispensable common-period hypothesis."},
    "acceptance_boundary":{"kind":"expression","value":"Advance only if, for one frozen A/C pair, exact ordered or swapped proportionality supplies one common Faddeev period system. Only then may a later block freeze transform order, auxiliary convolution variable, contours, and Fubini domination. If all proportionality tests fail, seal that the FTD/MIR two-kernel closure is unavailable before those later analytic steps. Do not infer failure of a new mixed-base theorem.","rationale":"The common system is logically prior to the source transform and prevents an invented convolution identity."}
  },
  "resource_caps":{
    "residual_starts":{"kind":"integer","value":2,"rationale":"A and C only."},
    "factors_per_start":{"kind":"integer","value":2,"rationale":"The first C228 pair only."},
    "period_systems_per_factor":{"kind":"integer","value":1,"rationale":"Each factor retains its pinned ordered pair."},
    "proportionality_modes":{"kind":"integer","value":2,"rationale":"Ordered and swapped equality only."},
    "source_identity_count":{"kind":"integer","value":2,"rationale":"FTD and MIR from one Faddeev source."},
    "floating_point":{"kind":"not_applicable","justification":"All endpoint-field and determinant computations are exact in Q(t).","rationale":"Numerical near-equality cannot supply a common source period system."},
    "wall_seconds":{"kind":"integer","value":180,"rationale":"Exact two-pair proportionality audit."}
  },
  "formula_families":[
    "Faddeev arXiv:1201.6464 equations (FTD) and (MIR)",
    "Cycle-228 exact first ordinary-gamma factor pairs",
    "Exact Q(t) ordered/swapped period-pair proportionality"
  ],
  "selection_rule":[
    "Reduce the endpoint field relation before each determinant comparison.",
    "Test both ordered and swapped pair proportionality for A and C.",
    "Do not specify an auxiliary contour, Fubini interchange, or transformed output unless a common source system first passes."
  ],
  "failure_rule":[
    "Do not identify a negative period with a positive one, invoke an unprinted modular transformation, or use a source factorization that creates new residual words.",
    "Do not add complementary factors, choose a different endpoint, or replace the fixed C228 subword after a failed determinant.",
    "Do not claim a general mixed-base no-go, an AFK consequence, fusion, Stark, or TCC."
  ],
  "pre_execution":{"timestamp_utc":"2026-08-03T08:48:00Z","git_head":"b1e2dc8ed4e893b9c315042792e3e423d5c0c627","git_state":"Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":[
    "artifacts/cycle-228-b065-f3-square-residual-block-v1.json",
    "proof/verify_cycle_228_f3_square_residual_block.py",
    "artifacts/cycle-239-b076-rarefied-beta-embedding-v1.json",
    "proof/verify_cycle_239_rarefied_beta_embedding.py",
    "../../tools/preregistration_check.py"
  ]
}
-->

Claim boundary: failure would rule out only the proposed direct Faddeev
FTD/MIR closure of this two-factor subword.  A new mixed-base composition
theorem, different integral identity, and all downstream dimension-six claims
remain open.
