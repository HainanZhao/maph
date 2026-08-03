# Cycle 244 / B081 preregistration: constructed Abel residue current

The cited beta theorem does not provide this current. This block constructs it
openly from the A residual word and tests only its distributional boundary and
normalization dependence; source authorization remains outside the claim.

Amendment — 2026-08-03: corrected the frozen Git commit hash before any
discovery, proof, test, or replay executable was created or run.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 244,
  "parameters": {
    "current_state": {
      "kind": "expression",
      "value": "Freeze R_A(mu)=product of the four ordered C228 A ordinary-gamma factors. For N>=1 with 12 not dividing N, set mu_N=N*(115*t-1), and let kappa_N be the coefficient of (mu-mu_N)^(-2) in R_A. The constructed Minkowski support is v_N=(sigma_+(mu_N),sigma_-(mu_N)); coefficients are the ordered pair (sigma_+(kappa_N),sigma_-(kappa_N)) as a formal two-component coefficient line.",
      "rationale": "C243 proves this is an infinite uncancelled double-pole family; this defines a candidate state without asserting a source A-to-C integrand."
    },
    "abel_dissection": {
      "kind": "expression",
      "value": "For 0<rho<1 and residues r=1,...,11, freeze J_{rho,r}=sum_{M>=0} rho^(12*M+r) kappa_{12*M+r} delta_{v_{12*M+r}}. Work in vector-valued distributions on compactly supported smooth test functions on R^2, and set J_r at rho=1 by the same locally finite sum if proved locally finite.",
      "rationale": "The twelve dissection is fixed before any boundary observation and compact-test-function topology makes the proposed distributional continuation checkable."
    },
    "galois_invariant": {
      "kind": "expression",
      "value": "Freeze Gal(K/Q) to swap the two Minkowski coordinates and the two coefficient-line components. Acceptance requires every support ray and every residue class current to be equivariant under that swap.",
      "rationale": "This is the only inherited symmetry used by the constructed current."
    },
    "normalization_falsifier": {
      "kind": "expression",
      "value": "Test the full family kappa_N -> lambda^N*kappa_N for lambda>0. If it preserves support, Galois swap, 12-dissection, local finiteness, and rho-to-one distributional existence but changes the rho=1 current, then the frozen construction has no intrinsic regulator normalization. Do not select lambda.",
      "rationale": "A non-fitted Abel construction cannot conceal an arbitrary exponential regulator."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A successful local-finiteness proof establishes only a constructed vector-valued distribution current. A surviving lambda deformation withholds source compatibility, contour identity, B-Fourier covariance, AFK, fusion, Stark, and TCC consequences.",
      "rationale": "The construction is a falsifiable prototype, not a source theorem."
    }
  },
  "resource_caps": {
    "residual_words": {"kind": "integer", "value": 1, "rationale": "C228 A only; C is not inserted into the state."},
    "pole_families": {"kind": "integer", "value": 1, "rationale": "The C243 mu_N family only."},
    "dissection_classes": {"kind": "integer", "value": 11, "rationale": "The nonzero classes modulo 12 only."},
    "coefficient_deformations": {"kind": "integer", "value": 1, "rationale": "The one-parameter lambda^N normalization falsifier."},
    "topologies": {"kind": "integer", "value": 1, "rationale": "Compact-test-function distributions only."},
    "floating_point": {"kind": "not_applicable", "justification": "Support properness and the normalization ambiguity are exact.", "rationale": "Numerics cannot establish a distributional boundary or canonicity."},
    "wall_seconds": {"kind": "integer", "value": 240, "rationale": "Exact support, symmetry, and deformation audit."}
  },
  "formula_families": ["Cycle-228 A residual word", "Cycle-229/C243 ordinary-gamma divisor families", "Cycle-241 Minkowski embeddings", "locally finite vector-valued distribution currents"],
  "selection_rule": ["Prove the support ray is proper in both real Minkowski coordinates before taking rho to one.", "Use all eleven nonzero residue classes, with no fitted weights or discarded class.", "Test lambda^N ambiguity symbolically and use a compactly supported witness to distinguish currents."],
  "failure_rule": ["Do not call rho source-supplied, replace a formal coefficient line by numerically fitted gamma values, choose lambda, use a non-locally-finite topology, or add C factors to the frozen A current.", "Do not infer a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T11:02:00Z",
    "git_head": "d2305fa09d2a571ac2d992c298ac937e8d3bb6eb",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-229-b066-f3-square-divisor-v1.json", "proof/verify_cycle_229_f3_square_divisor.py", "artifacts/cycle-243-b080-two-chamber-crossing-v1.json", "proof/verify_cycle_243_two_chamber_crossing.py", "artifacts/cycle-239-b076-rarefied-beta-embedding-v1.json", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a constructed current only. Its source compatibility
and every analytic identity remain separately open.
