# Cycle 185 correction preregistration: shifted exponential convention

## Frozen correction question

Cycle 185 used the product identity for `z^ell` after the project had fixed
the ray slope as `alpha_ell=z^ell-1`.  Preserve the original artifact,
withhold its unshifted curvature claim, and test whether the shifted numerator
`B_ell=A_ell+U_ell` restores a correctly stated exactifier without changing
the mass-only AP-free no-go.

<!-- research-freeze-v1
{
  "cycle": 185,
  "failure_rule": [
    "Seal a correction that withholds the original unshifted curvature claim if alpha_-*alpha_+!=alpha_0^2 under the pinned phase convention.",
    "Promote the shifted-numerator calculation only if its exact product expansion, v^2 divisibility, and retained pair-determinant syzygy are checked in exact arithmetic.",
    "Do not relabel the abstract AP-free occupancy as an actual-exponential configuration."
  ],
  "formula_families": [
    "pinned phase alpha_ell=exp(2*pi*ell/Delta)-1 and z_ell=1+alpha_ell=exp(2*pi*ell/Delta)",
    "arithmetic-progression identity z_(ell-r)*z_(ell+r)=z_ell^2",
    "shifted numerators B_i=A_i+U_i and corrected integer K_plus=U_0^2*B_-*B_+-U_-*U_+*B_0^2",
    "C185 mass/capacity/stable-shell AP-free occupancy boundary",
    "C183 primitive pair determinants retained under the numerator shift"
  ],
  "input_paths": [
    "artifacts/cycle-185-three-label-curvature-v1.json",
    "conventions/three_label_curvature_v1.py",
    "proof/cycle_seal_v1.py",
    "../../tools/preregistration_check.py"
  ],
  "parameters": {
    "affected_claim": {
      "kind": "expression",
      "rationale": "The source record must remain immutable while this correction names precisely the invalid assertion.",
      "value": "alpha_(ell-r)*alpha_(ell+r)=alpha_ell^2 for alpha_ell=z^ell-1"
    },
    "corrected_invariant": {
      "kind": "expression",
      "rationale": "The actual geometric identity applies only after the pinned +1 shift.",
      "value": "K_plus=U_0^2*(A_-+U_-)*(A_++U_+)-U_-*U_+*(A_0+U_0)^2"
    },
    "retained_state": {
      "kind": "symbolic",
      "rationale": "The correction may not discard C183 pair-determinant or fibre state.",
      "value": "(N_i,U_i,A_i,B_i,primitive pair determinants, fibres,residuals,labels,stable shells)"
    }
  },
  "pre_execution": {
    "git_head": "07c6b68886c369f044a1a9c47fcd66702c3d77ad",
    "git_state": "clean worktree; correction preregistration and correction narrative created before executable correction code",
    "timestamp_utc": "2026-08-02T14:18:58Z"
  },
  "resource_caps": {
    "candidate_engine_count": {
      "kind": "integer",
      "rationale": "This is containment plus one exact shifted repair, not a new exploratory branch.",
      "value": 1
    },
    "new_executable_code": {
      "kind": "not_applicable",
      "justification": "The initial correction is a convention comparison and exact symbolic specification; executable code follows only after this freeze validates.",
      "rationale": "Preflight precedes correction replay code."
    }
  },
  "schema": "research-preregistration-freeze-v1",
  "selection_rule": [
    "The original artifact is immutable and its unshifted K claim is withheld regardless of whether K_plus works.",
    "A shifted identity counts only as a corrected local exactifier; it does not reopen density promotion or defeat the C185 AP-free occupancy no-go."
  ]
}
-->

