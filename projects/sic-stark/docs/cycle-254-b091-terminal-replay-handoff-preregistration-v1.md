# Cycle 254 / B091 preregistration: terminal replay and handoff

This is the final SIC--Stark research block. It independently replays the
strongest signed-period result and either closes dimension six or freezes the
project with a minimal handoff.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 254,
  "parameters": {
    "independent_replay": {
      "kind": "expression",
      "value": "Re-derive without importing the C253 verifier: (i) the exact C251 orientation relation R(alpha)=-alpha_target and R(beta)=beta_target for all eight factors; (ii) Stokman's slit parameter tau_h=-beta/alpha and its half-plane change; (iii) the theorem-normalized negative-alpha endpoint product; and (iv) the continued and target beta-shift quotients. The replay passes only if all eight rows at both embeddings reproduce the nonconstant 1-X^(-1) versus 1-X mismatch.",
      "rationale": "The terminal decision must not rely on running the same implementation twice."
    },
    "transition_inventory": {
      "kind": "expression",
      "value": "Audit only sealed C221--C226, C235--C237, and C251--C253 for an already source-derived nonconstant transition operator. A survivor must act on all eight ordered factors with exact periods, argument, and labels; have beta cocycle T(z+beta)/T(z)=-X and alpha cocycle T(z+alpha)/T(z)=(1-Y)*(1-q*Y), where X=exp(2*pi*i*z/alpha) and Y=exp(2*pi*i*z/beta); preserve reflection/double-sign normalization; and be source-authorized rather than fitted as target/continuation quotient.",
      "rationale": "These are the exact necessary cocycles of T=target/continuation and the complete relevant frozen candidate family."
    },
    "terminal_rule": {
      "kind": "expression",
      "value": "Record A_CLOSED only if a surviving source transition yields the full Gamma_M interface and the existing exact downstream replay proves dimension-six TCC in this run. Otherwise record C_FROZEN, seal the strongest positive theorem and obstruction, update PROGRAM.md to terminal state, generate the optional intentional-handoff STATUS.md, and stop the project. Do not open another engine or cycle.",
      "rationale": "This enforces the user-authorized three-cycle closeout without weakening the proof boundary."
    },
    "handoff": {
      "kind": "expression",
      "value": "If frozen, STATUS.md contains only the terminal state, pointers to PROGRAM.md and the C254 artifact, and exact recovery/replay commands. It must not duplicate the strategy, historical narrative, or result ledger.",
      "rationale": "The handoff remains useful without recreating status-report overhead."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "C_FROZEN means dimension-six TCC is not proved under the completed B091 closeout and no already sealed source transition closes the identified interface. It is a project stop and handoff classification, not a universal impossibility theorem for TCC or future mathematics.",
      "rationale": "A finite terminal audit cannot prove universal nonexistence."
    }
  },
  "resource_caps": {
    "independent_replays": {"kind": "integer", "value": 1, "rationale": "One independent implementation."},
    "sealed_transition_records": {"kind": "integer", "value": 12, "rationale": "C221--C226, C235--C237, and C251--C253."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "Every reflected A/C factor."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both fixed C249 embeddings."},
    "new_transition_engines": {"kind": "integer", "value": 0, "rationale": "C254 is replay and closeout, not another speculative cycle."},
    "floating_point": {"kind": "not_applicable", "justification": "All orientation, cocycle, source-scope, and terminal checks are exact.", "rationale": "Numerics cannot close the bridge."},
    "wall_seconds": {"kind": "integer", "value": 1200, "rationale": "Independent replay and bounded sealed-record inventory."}
  },
  "formula_families": ["Stokman hyperbolic-gamma continuation", "Sarkissian--Spiridonov ordinary gamma shifts", "C228/C251 exact A/C factor states", "C221--C226 signed-product corrections", "C235--C237 retained-word/reflection routes", "C253 target mismatch"],
  "selection_rule": ["Run the independent all-eight replay first.", "Test every frozen candidate against both required cocycles and full source/state scope.", "Attempt downstream closure only for a genuine survivor; otherwise freeze and hand off."],
  "failure_rule": ["Do not fit T as target/continuation, relax source authorization, omit a failed candidate, open a new engine, create C255, or extend the budget.", "Do not state a universal no-go; preserve the exact positive continuation theorem and scoped obstruction."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:48:31Z", "git_head": "2fe9fc7e776f715397e5c0abc03b668dc5e79adc", "git_state": "Dirty from the existing repository-wide PROGRAM migration and unrelated work; this terminal cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-221-b058-tilde-inversion-v1.json", "artifacts/cycle-222-b059-z-label-cocycle-v1.json", "artifacts/cycle-223-b060-explicit-signed-product-v1.json", "artifacts/cycle-224-b061-shift-cohomology-v1.json", "artifacts/cycle-225-b062-reflection-root-branch-v1.json", "artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "artifacts/cycle-235-b072-meromorphic-loop-holonomy-v1.json", "artifacts/cycle-236-b073-ordered-word-dualization-v1.json", "artifacts/cycle-237-b074-reflection-partner-reachability-v1.json", "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "artifacts/cycle-252-b089-reciprocal-negative-alpha-v1.json", "artifacts/cycle-253-b090-direct-hyperbolic-continuation-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "proof/verify_cycle_253_direct_hyperbolic_continuation.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is the terminal finite-record classification, not a
universal mathematical no-go.
