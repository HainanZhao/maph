# Cycle 200 / B037 preregistration: source regular-plus-residue jet

Cycle 199 proved that the literal full-phase symmetric Abel boundary has only
delta support and loses `b`. This block asks whether the same *source* family,
before support-only collapse, forces a regular-plus-residue jet that retains
enough all-row information. It is not permitted to choose a counterterm,
coefficient, alias, or target map after inspecting the 36 target values.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 200,
  "parameters": {
    "source_family": {
      "kind": "expression",
      "value": "Use exactly the Cycle-199 full equation-(66)-phase three-class character comb. On each m=4h channel set u_lambda(s)=exp(-lambda*s) for lambda in [1/2,2], rho_h,s(Lambda)=exp(-pi*r_gamma(s)*Lambda/2), and A_u(rho)=(1-u^2)/((1-u*rho)*(1-u/rho)). Retain the full character Xi_(a,b,r+3k), including its continuous alpha-dependent phase, and the canonical paired i0 pole orientation from Cycle 199.",
      "rationale": "The candidate must be a refinement of the sealed source family, not a new fitted summation method."
    },
    "jet_family": {
      "kind": "expression",
      "value": "Derive the source Laurent/Taylor distributional expansion at s=0 of the paired regular-plus-residue object before any comparison to T_6. Audit all derivative distributions delta^(j)(Lambda) for j in {0,1,2,3,4,5}; retain a j only if its coefficient is forced by that expansion or source covariance. The displayed candidate order cap is five because six distinct b labels require a polynomial jet of degree at least five in the full-character phase; this is a rank necessity, not an assertion that the source supplies such a jet.",
      "rationale": "It separates an exact source-forced coefficient from a post-result jet fit and makes the first rank-capable order finite."
    },
    "all_row_rank_test": {
      "kind": "expression",
      "value": "For every (a,b) in (Z/6Z)^2, every r in {0,1,2}, and every m=4h with h in {0,...,5}, evaluate the exact full-character Taylor data through order five at Lambda=0. Compute the exact row-rank of each source-forced retained jet set. A rank below 36 fails the all-36 interface prerequisite; rank 36 is only a necessary source-data condition and does not define J or prove amplitude equality.",
      "rationale": "Cycle 199's rank-six collapse was a failure before any arithmetic comparison, so this block must preserve the same all-row discipline."
    },
    "regular_part_rule": {
      "kind": "expression",
      "value": "The regular part, each finite collision residue, and every Laurent coefficient are taken from the declared source family. No finite part, subtraction, rescaling by an s-dependent factor, or combination of plus/minus boundary values is admissible unless derived symbolically from the frozen Abel/Poincare formula and its A_6 orientation. A source-forced coefficient may be zero; zero does not license replacement by a nonzero normalized jet.",
      "rationale": "The missing bridge is a construction problem, not permission to normalize the desired answer into existence."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A positive result establishes only the source Laurent/Taylor coefficient ledger and any proved rank property of its regular-plus-residue endpoint object. It does not establish a Zak intertwiner J, C198 amplitude equality, AFK identification, ray logarithms, fusion continuity, Stark algebraicity, or TCC. A negative result rejects only the exact declared full-phase symmetric Abel regular-plus-residue jet family through order five; it does not reject higher-order, non-Abel, or another source-derived continuation.",
      "rationale": "The block tests one genuinely new engine while keeping all downstream claims quarantined."
    }
  },
  "resource_caps": {
    "character_rows": {"kind":"integer","value":36,"rationale":"The complete C198 target grid."},
    "source_labels": {"kind":"integer","value":24,"rationale":"The retained full source carrier."},
    "residue_classes": {"kind":"integer","value":3,"rationale":"The complete Cycle-199 helical residue family."},
    "pinching_channels": {"kind":"integer","value":6,"rationale":"Exactly m=0 mod 4 from Cycle 199."},
    "maximum_derivative_order": {"kind":"integer","value":5,"rationale":"The first possible degree for six b labels; higher orders are outside this block."},
    "abel_rate_interval": {"kind":"expression","value":"lambda in [1/2,2]","rationale":"The frozen Cycle-199 radial family."},
    "wall_seconds": {"kind":"integer","value":300,"rationale":"Exact symbolic ledger and bounded test suite."}
  },
  "formula_families": [
    "Cycle-199 full equation-(66) character ratio and canonical A_6 paired i0 orientation",
    "the exact rational Abel kernel A_u(rho) and distributional Laurent/Taylor expansion",
    "the complete 24-mode carrier and C198 distinct 36-character target ledger",
    "the finite anti-residue constraints of Cycles 194--195"
  ],
  "selection_rule": [
    "Derive the paired regular-plus-residue distribution from the frozen rational Abel kernel before multiplying by or comparing full-character Taylor data.",
    "Enumerate every a,b,r,h and every derivative order 0 through 5; do not select a phase channel, alias, order, or coefficient because it improves rank.",
    "For every source-forced nonzero coefficient, calculate exact rank and give an explicit collision witness if it is below 36.",
    "Only if a source-forced jet has rank 36 may the block formulate, but not fit, a subsequent source-defined J problem."
  ],
  "failure_rule": [
    "If no source-forced coefficient through order five retains rank 36, seal the exact scoped regular-plus-residue jet obstruction and leave the D6 interface gate open.",
    "If an expansion needs an unproved finite part, s-dependent renormalization, or a coefficient not fixed by the source, classify that condition as missing rather than treating a candidate jet as a construction.",
    "Do not promote rank, a formal distribution, or numerical agreement to an equation-(66) endpoint amplitude, AFK value, fusion, Stark, or TCC result."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:15:00Z",
    "git_head": "4298f0ea4b516b029c5ed46671cbb312045fcdde",
    "git_state": "DIRTY from concurrent repository-wide PROGRAM migration and unrelated projects/tools, plus sealed Cycle 199 and this live Cycle-200 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json",
    "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
    "proof/verify_cycle_199_full_phase_abel_boundary.py",
    "proof/verify_cycle_199_abel_character_comb.py",
    "proof/verify_cycle_199_abel_pole_geometry.py",
    "proof/verify_cycle_199_full_theta_carrier.py",
    "scripts/dimension_six_helical_zak.py",
    "scripts/dimension_six_alias_normalization.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
