# Cycle 243 / B080 preregistration: two-chamber divisor crossing

Cycle 242 excludes one shared linear cone contour, not separately admissible
chambers. This block tests the next proposed construction: connect canonical
Galois-equivariant A and C chamber normals and decide whether the connection
has a finite, completely accounted residue crossing ledger.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 243,
  "parameters": {
    "chamber_normals": {
      "kind": "expression",
      "value": "Freeze the C242 normal form u=t_sigma+h. Use u_A=1/230, inside A's exact interval (0,1/115), and u_C=6, inside C's exact interval (5,infinity). Thus h_{sigma,A}=u_A-t_sigma and h_{sigma,C}=u_C-t_sigma at each of the two Minkowski embeddings.",
      "rationale": "These are rational, source-period-derived interior representatives with a Galois-equivariant rule, not fitted contours."
    },
    "deformation_class": {
      "kind": "expression",
      "value": "Admit every continuous deformation of the fixed affine-linear normal whose scalar u joins u_A to u_C. A finite Picard-Lefschetz-type continuation is admissible only if it has finitely many uncancelled divisor crossings with an exact residue ledger. Any path must cross u=1/115 by the intermediate value theorem.",
      "rationale": "It is the broadest continuous connection of the frozen chamber-normal class while making the finite-residue claim checkable."
    },
    "divisor_family": {
      "kind": "expression",
      "value": "Freeze the ordinary gamma divisor convention from C229. In the A word retain the second and third factors, which have the common pole family mu_N=N*(115*t-1), N>=1. Audit all eight A/C factors for zeros at this exact family. Use t^2-110*t+1=0 only after coefficient comparison in the Q-basis (t,1).",
      "rationale": "This is an infinite source-derived family whose cone side changes at the forced crossing."
    },
    "acceptance_boundary": {
      "kind": "expression",
      "value": "Advance to a finite-residue two-chamber contour only if every side-changing mu_N is cancelled except finitely many, with exact multiplicity. If infinitely many N remain uncancelled, seal failure of finite-residue continuation and do not infer failure of a renormalized infinite-residue, nonlinear, or other contour construction.",
      "rationale": "An infinite crossing cannot be represented by the proposed finite Picard-Lefschetz ledger."
    }
  },
  "resource_caps": {
    "embeddings": {"kind": "integer", "value": 2, "rationale": "The two Minkowski embeddings only."},
    "residual_factors": {"kind": "integer", "value": 8, "rationale": "All four A and four C factors are required for cancellation."},
    "pole_families": {"kind": "integer", "value": 1, "rationale": "One forced A two-factor ray is sufficient."},
    "deformation_classes": {"kind": "integer", "value": 1, "rationale": "Continuous scalar-u normal deformations only."},
    "residue_modes": {"kind": "integer", "value": 1, "rationale": "Finite exact ledger only."},
    "floating_point": {"kind": "not_applicable", "justification": "All family and multiplicity statements are exact over Q(t).", "rationale": "Numerical poles cannot certify an infinite crossing family."},
    "wall_seconds": {"kind": "integer", "value": 240, "rationale": "Exact all-eight-factor family audit."}
  },
  "formula_families": ["Cycle-229 ordinary hyperbolic-gamma divisor convention", "Cycle-228 exact A/C residual words", "Cycle-242 affine-linear normal form and chamber intervals", "exact Q(t) divisor-family comparison"],
  "selection_rule": ["Use only the frozen A2/A3 pole ray and compare it against zeros of every A/C factor.", "Prove the forced normal crossing before using the divisor family.", "Record every congruence class of N which can cancel and its exact multiplicity."],
  "failure_rule": ["Do not truncate N, discard coincident poles, replace an infinite family by sampled values, or assert cancellation without an exact factor-by-factor comparison.", "Do not turn failure of a finite-residue ledger into a no-go for renormalized infinite residue sums, nonlinear contours, a mixed-base identity, AFK, fusion, Stark, or TCC.", "Do not choose factor-dependent chamber endpoints or alter the upper tilt after seeing crossings."],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T10:24:00Z",
    "git_head": "0f6f295ed5b8d5f7ab8544bc293b68637b1f0b37",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-229-b066-f3-square-divisor-v1.json", "proof/verify_cycle_229_f3_square_divisor.py", "artifacts/cycle-242-b079-minkowski-common-contour-v1.json", "proof/verify_cycle_242_minkowski_common_contour.py", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: an infinite uncancelled family would obstruct only the frozen
finite-residue deformation class. It would not settle a regularized infinite
sum or any downstream identity.
