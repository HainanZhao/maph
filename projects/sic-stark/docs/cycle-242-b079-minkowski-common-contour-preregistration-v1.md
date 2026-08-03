# Cycle 242 / B079 preregistration: Minkowski common-contour cone

This block tests the first analytic prerequisite left open by Cycle 241. It
does **not** presume that lattice self-duality supplies a special-function
transform. The test is the canonical Galois-equivariant upper tilt of the two
C228 residual words and a fixed affine-linear cone-separation class which
gives both Minkowski components their own contour normal.

Amendment — 2026-08-03: corrected the frozen Git commit hash before any
discovery, proof, test, or replay executable was created or run.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 242,
  "parameters": {
    "minkowski_endpoint": {
      "kind": "expression",
      "value": "Freeze K=Q(sqrt(21)), t_+=55+12*sqrt(21), t_-=55-12*sqrt(21), and the two embeddings sigma_+, sigma_-. For each sigma use t_sigma(epsilon)=t_sigma+i*epsilon, epsilon>0, extending both embeddings trivially over the common scalar i.",
      "rationale": "Cycle 241 fixes this real quadratic Minkowski setting; the common i-tilt is the source-side upper-half-plane regularization to test, not a fitted continuation."
    },
    "residual_words": {
      "kind": "expression",
      "value": "Freeze exactly C228's four ordered A factors and four ordered C factors, with positive argument coefficients 1/24, 1/24, 1, 1. At either embedding write every period as a*t_sigma(epsilon)+b using its C228 affine coefficient pair. No factor is inserted, removed, commuted, reflected, or rescaled.",
      "rationale": "The candidate must retain the actual heterogeneous residual words."
    },
    "contour_class": {
      "kind": "expression",
      "value": "For each embedding independently admit every fixed affine-linear cone normal L_{sigma,h}(z)=Re(z)+(h/epsilon)Im(z), h in R, and its contour L_{sigma,h}(mu)=0. Acceptance requires one h_+ and one h_- for which L is strictly positive on every A and C period generator at the corresponding embedding.",
      "rationale": "The normal permits finite first-order tilt compensation while forbidding an after-the-fact, factor-dependent contour."
    },
    "exact_failure_witness": {
      "kind": "expression",
      "value": "Use the A second/third period pair (t,(1-115*t)/24) and the C first/fourth period (t-5)/24. For u=t_sigma+h, positivity would require 0<u<1/115 and u>5 simultaneously. If this exact contradiction holds at both embeddings, stop before asymptotic/tail, Fourier-covariance, or integral-identity claims.",
      "rationale": "It is a finite symbolic falsifier of the preregistered shared-contour class."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A failure excludes only a common fixed affine-linear pole/zero cone separator for paired A/C residual words under this upper tilt. It does not exclude a contour for one word alone, a nonlinear or factor-dependent contour, another regularization, a mixed-base identity, AFK, fusion, Stark, or TCC.",
      "rationale": "The cone condition is an analytic entry gate, not a general no-go theorem."
    }
  },
  "resource_caps": {
    "embeddings": {"kind": "integer", "value": 2, "rationale": "The two real embeddings of K only."},
    "residual_words": {"kind": "integer", "value": 2, "rationale": "C228 A and C only."},
    "period_generators": {"kind": "integer", "value": 16, "rationale": "Four period pairs per word and two embeddings."},
    "tilt_family": {"kind": "integer", "value": 1, "rationale": "One common upper tilt with independently chosen finite normals per embedding."},
    "contour_classes": {"kind": "integer", "value": 1, "rationale": "Fixed affine-linear cone separators only."},
    "floating_point": {"kind": "not_applicable", "justification": "The witness is an exact rational interval contradiction.", "rationale": "Numerical near-separation cannot establish a contour class."},
    "wall_seconds": {"kind": "integer", "value": 180, "rationale": "Exact two-embedding finite cone audit."}
  },
  "formula_families": ["Cycle-228 exact ordinary-gamma residual period pairs", "Cycle-241 Q(sqrt(21)) Minkowski embeddings and B-Fourier framework", "upper-half-plane period regularization and linear divisor-cone separation"],
  "selection_rule": ["Evaluate every period generator under both frozen embeddings and the same upper tilt.", "Permit independent h_+ and h_- but require each to work for both A and C in that embedding.", "Derive the acceptance or failure condition directly from the displayed affine periods before any tail calculation."],
  "failure_rule": ["Do not reverse a period, use a factor-dependent tilt or normal, replace a negative period by its absolute value, or invoke an unprinted special-function identity.", "After a cone-separation failure, do not make an asymptotic, temperedness, Fourier-covariance, mixed-base, AFK, fusion, Stark, or TCC claim.", "Do not call the scoped failure a no-go for nonlinear contours, one-word contours, other regularizations, or new mixed-base constructions."],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T10:08:00Z",
    "git_head": "8fc880e5a4ca2922eaf1058ce33be8738013e7fc",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-241-b078-minkowski-self-duality-v1.json", "proof/verify_cycle_241_minkowski_self_duality.py", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: a passing cone condition would be only an entry condition for
later distributional and Fourier analysis; a failure is scoped to the stated
paired-word, common affine-linear contour class.
