# Cycle 253 / B090 preregistration: direct hyperbolic-gamma continuation

This block uses a direct hyperbolic-gamma theorem, rather than another
q-product convention, to test the signed-period bridge left open by C252.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 253,
  "parameters": {
    "primary_theorem": {
      "kind": "expression",
      "value": "Freeze Stokman, Hyperbolic beta integrals, Adv. Math. 190 (2005), Appendix: the integral definition of Ruijsenaars' Gamma_h for Re(a_plus),Re(a_minus)>0; its meromorphic continuation in the argument; Proposition Shintani giving the q-product quotient for Im(a_plus/a_minus)>0; symmetry under swapping periods; and the subsequent statement that the associated tau-shifted factorial extends meromorphically to (z,tau) in C x (C minus R_{>=0}). Check the displayed hypotheses and normalization directly against Sarkissian--Spiridonov arXiv:1910.11747v4 equation (13).",
      "rationale": "This is a distinct integral/meromorphic engine with an explicit parameter domain and normalization."
    },
    "parameter_path": {
      "kind": "expression",
      "value": "For each factor set r=alpha/beta and tau_h=-beta/alpha=-1/r. C249 has Im(r)>0. Orientation reversal alpha->-alpha sends r to -r and tau_h to -tau_h. Freeze the path in the simply connected slit domain C minus R_{>=0}; accept path independence only from Stokman's meromorphic continuation on that exact domain. Endpoints are evaluated at w_sigma=t_sigma+i for both embeddings.",
      "rationale": "The slit fixes the branch and avoids C252's disconnected-definition defect."
    },
    "normalization_match": {
      "kind": "expression",
      "value": "Center z_h=-i*(mu-(alpha+beta)/2). Derive in the positive chamber that Sarkissian--Spiridonov gamma(mu;alpha,beta)=E(alpha,beta,mu)/Gamma_h(alpha,beta;z_h), where E is exactly the two exponential factors in Stokman's Shintani product. Continue this same normalized expression along the frozen slit path. At the negative-alpha endpoint use period symmetry and Stokman's opposite-sign product, deriving the endpoint formula rather than inserting C252's candidate by definition.",
      "rationale": "Matching on the source chamber fixes the analytic continuation uniquely."
    },
    "target_test": {
      "kind": "expression",
      "value": "Compare the continued factor at (-alpha,beta) with the corresponding C251 target factor at (alpha,beta), preserving argument and label. First compare their beta-shift quotients as meromorphic functions of mu. If they differ nontrivially, reject the direct cross-sign target map for all affected factors and stop before degree-0:3 coefficient comparison; no quotient correction, elliptic multiplier, scalar, or branch change may be added.",
      "rationale": "A canonical continuation is useful only if it lands in the declared target normalization without a fitted transition function."
    },
    "acceptance": {
      "kind": "expression",
      "value": "Accept only if the theorem hypotheses hold at both embeddings, the normalized source formula continues path-independently, and all eight continued factors equal their opposite A/C target factors as meromorphic functions before the ordered C250 jet matrices are compared. Falsify the direct bridge on the first exact nonconstant shift or divisor mismatch.",
      "rationale": "Functional equations distinguish meromorphic functions before any numerical or truncated-jet comparison."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "Passing would construct the direct signed-period ordinary-gamma bridge and authorize a later full Gamma_M/interface lift. Failure excludes only this canonical path-independent continuation as the uncorrected A/C target map. It does not exclude a separately sourced transition operator, another full Gamma_M theorem, AFK, fusion, Stark, or dimension-six TCC.",
      "rationale": "This is the second of the final three closeout blocks."
    }
  },
  "resource_caps": {
    "primary_theorems": {"kind": "integer", "value": 1, "rationale": "Stokman's hyperbolic-gamma continuation package only."},
    "continuation_paths": {"kind": "integer", "value": 1, "rationale": "The fixed slit-domain homotopy class."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "Every C251 reflected factor."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both C249 embeddings."},
    "jet_degree": {"kind": "integer", "value": 3, "rationale": "C250's full graded jet rank if the function-level target test passes."},
    "floating_point": {"kind": "not_applicable", "justification": "Parameter-domain signs, product normalization, and shift quotients are exact.", "rationale": "A sampled match cannot establish meromorphic equality."},
    "wall_seconds": {"kind": "integer", "value": 1200, "rationale": "Bounded theorem-hypothesis and eight-factor symbolic audit."}
  },
  "formula_families": ["Stokman Appendix integral Gamma_h and Proposition Shintani", "Stokman tau-shifted-factorial meromorphic continuation", "Sarkissian--Spiridonov equation (13) ordinary gamma", "C249 common chamber", "C251 reflected A/C states", "C250 graded jets"],
  "selection_rule": ["Prove the positive-chamber normalization match before continuing it.", "Check the slit-domain endpoints for all factors and embeddings.", "Compare meromorphic shift quotients before any jets or correction factor."],
  "failure_rule": ["Do not switch theorem, slit, centering, normalization, branch, target, or add a quotient correction after execution.", "Do not infer a no-go for separately sourced signed-period operators, the full Gamma_M interface, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:44:30Z", "git_head": "b35c06bb90867ab3f991b2ba6f57dcbdd905eba1", "git_state": "Dirty from the existing repository-wide PROGRAM migration and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-249-b086-common-jet-chamber-v1.json", "proof/verify_cycle_249_common_jet_chamber.py", "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "proof/verify_cycle_250_graded_f3_jet_representation.py", "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "proof/verify_cycle_251_residue_dual_cross_sign.py", "artifacts/cycle-252-b089-reciprocal-negative-alpha-v1.json", "proof/verify_cycle_252_reciprocal_negative_alpha.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this tests whether the canonical theorem-backed continuation
itself lands in the declared A/C target normalization.
