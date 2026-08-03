# Cycle 205 / B042 preregistration: source Mellin/b-pairing

Cycle 204 left one concrete missing operation: a source-derived Mellin or
b-pairing. This block uses the frozen two-scale asymptotic to derive the
unique local Mellin pole and its regulator weight. It must not choose a
nonlocal Mellin evaluation, contour, or finite part after seeing target data.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 205,
  "parameters": {
    "local_source_asymptotic": {
      "kind": "expression",
      "value": "Use exactly G_lambda(s)=B+lambda*s*R+O(s^2) from the Cycle-200/Cycle-201 two-scale germ, with B the rate-zero boundary sector and R the rank-36 regular packet. The local b-Mellin transform is M_lambda(z)=integral_0^1 s^(z-1)*(G_lambda(s)-B) ds, initially where it converges and then continued only by the displayed frozen asymptotic. Its leading local term is lambda*R/(z+1), so the forced pole is z=-1 with residue lambda*R.",
      "rationale": "This asks the source asymptotic, not a selected contour, what homogeneity a local Mellin residue has."
    },
    "candidate_operations": {
      "kind": "expression",
      "value": "Audit only: (i) the z=-1 local residue, (ii) its Laurent finite coefficient determined by the displayed leading term, and (iii) a rate-independent linear combination with the retained boundary B. No evaluation at another Mellin point, cutoff-dependent finite part, global s-integral, division by lambda, or target-fitted counterterm is admissible unless forced by an equation-(66) theorem in the frozen inputs.",
      "rationale": "It gives the proposed Mellin engine a real falsification target without pretending a global b-integral is already present."
    },
    "all_row_target_rule": {
      "kind": "expression",
      "value": "On all 36 rows, compare the forced local residue/finite coefficient weights with the frozen finite nonzero C198 values. A direct complex-linear rate-independent equality to T_6 requires weight zero. If the rank-36 term retains weight one, only B can survive an invariant linear map, and its rank cap is 30.",
      "rationale": "The local Mellin operation is only useful if it crosses the exact all-row interface boundary."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A negative result rejects only the local b-Mellin residue and finite coefficient forced by the stated asymptotic, plus their rate-independent linear combinations with B. It does not exclude an equation-(66) global Mellin theorem, another source pairing, covariant target, nonlinear/higher-germ/non-Abel continuation, AFK, fusion, Stark, or TCC. A positive result establishes only the stated Mellin bridge.",
      "rationale": "It records exactly whether the first natural b-pairing candidate exists, without globalizing an unproved integral."
    }
  },
  "resource_caps": {
    "character_rows": {"kind":"integer","value":36,"rationale":"Full source/target grid."},
    "boundary_rank_cap": {"kind":"integer","value":30,"rationale":"Sealed symmetric b-boundary cap."},
    "mellin_candidates": {"kind":"integer","value":3,"rationale":"Only the frozen local residue, coefficient, and B combination."},
    "regulator_dilation_probes": {"kind":"integer","value":3,"rationale":"q in {2,3,5}."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact local Laurent/rank ledger."}
  },
  "formula_families": [
    "Cycle-200 two-scale source expansion",
    "Cycle-201 regulator action",
    "Cycle-204 b-normal category and source-pairing boundary",
    "Cycle-198 finite nonzero T_6 endpoint functional"
  ],
  "selection_rule": [
    "Derive the local Mellin pole from the frozen leading asymptotic before inspecting any target row.",
    "Enumerate all 36 rows and q in {2,3,5} for each candidate operation.",
    "Treat a nonlocal Mellin evaluation or finite part as absent unless an exact equation-(66) source theorem supplies it."
  ],
  "failure_rule": [
    "If the forced local residue or coefficient has rate weight one, it cannot directly equal the fixed weight-zero C198 targets under a rate-independent linear map.",
    "A division by lambda, chosen Mellin point, cutoff, contour, or target-fitted subtraction is outside the block and cannot count as a Mellin bridge.",
    "Do not promote a local Mellin ledger to a Zak map, AFK, fusion, Stark, or TCC claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T08:05:00Z",
    "git_head": "75be801b30b02a38da2ea6c7d667146ccbae88b2",
    "git_state": "DIRTY from the concurrent repository-wide PROGRAM header migration and unrelated projects/tools, plus this live Cycle-205 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-204-b041-log-normal-bundle-v1.json",
    "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
    "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "proof/verify_cycle_204_log_normal_bundle.py",
    "proof/verify_cycle_201_two_scale_germ_covariance.py",
    "proof/verify_cycle_200_regular_residue_jet.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
