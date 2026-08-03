# Cycle 202 / B039 preregistration: normal derivative target weight

Cycle 201 leaves open the source normal derivative of the rank-36 regular
germ, which is rate-covariant rather than rate-invariant. This block tests the
first exact compatibility condition for using it: can a source-linear,
rate-independent map send that weight-one datum to the nonzero rate-zero C198
endpoint values? The target values remain exactly those frozen in Cycle 198.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 202,
  "parameters": {
    "normal_datum": {
      "kind": "expression",
      "value": "Use the Cycle-201 germ G_lambda=(B,lambda*R). Define its normal derivative R=d/dlambda G_lambda at lambda=0, equivalently the coefficient lim_(lambda->0) lambda^(-1)(G_lambda-B). Under a regulator reparametrization lambda->q*lambda with q in {2,3,5}, the corresponding normal datum is R_q=q*R.",
      "rationale": "The derivative is source-defined by the two-scale expansion but is explicitly weight one, not an invariant boundary value."
    },
    "target_weight": {
      "kind": "expression",
      "value": "For all 36 Cycle-198 characters chi_(a,b), the source endpoint value L_src(chi_(a,b)) is frozen, finite, and nonzero, and has regulator weight zero because neither its meromorphic equation-(66) definition nor its T_6 argument includes the auxiliary Abel rate.",
      "rationale": "A direct amplitude bridge must respect both the source normal-coordinate action and the already sealed endpoint functional."
    },
    "functional_class": {
      "kind": "expression",
      "value": "A direct normal-data bridge is a complex-linear J:E_reg->T_6 independent of the Abel rate and required to satisfy J(R_(a,b))=L_src(chi_(a,b)) on all 36 rows. Test this equality after every q in {2,3,5}; no q-dependent J, division by q, fitted scalar, or target-dependent renormalization is permitted.",
      "rationale": "This is the smallest rate-covariant source-linear bridge class left by Cycle 201."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A no-go rejects only direct complex-linear rate-independent maps from the normal derivative to the fixed C198 endpoint values. It leaves a theorem-derived target weight, a nonlinear map, a paired covariant target, a higher-germ construction, non-Abel continuation, AFK identification, fusion, Stark, and TCC open. A positive result would still prove only the stated direct bridge, not those later claims.",
      "rationale": "The rate mismatch is a specific covariance test, not a universal obstruction."
    }
  },
  "resource_caps": {
    "character_rows": {"kind":"integer","value":36,"rationale":"Complete source and target grids."},
    "normal_datum_rank": {"kind":"integer","value":36,"rationale":"Cycle-200 off-support packet rank."},
    "regulator_dilation_probes": {"kind":"integer","value":3,"rationale":"q in {2,3,5}."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact all-row covariance ledger."}
  },
  "formula_families": [
    "Cycle-200 first off-support Abel-coordinate coefficient",
    "Cycle-201 two-scale regulator dilation action",
    "Cycle-198 nonzero source endpoint functional on T_6"
  ],
  "selection_rule": [
    "Enumerate every one of the 36 source normal packets and their C198 targets before testing a dilation.",
    "Use each q in {2,3,5}; compare q*J(R_(a,b)) with the same fixed target value on every row.",
    "Record the nonzero target condition and the exact contradiction rather than selecting a compensating scalar."
  ],
  "failure_rule": [
    "If the normal datum has weight one while targets have weight zero, a direct rate-independent linear equality is false on every nonzero target row; seal only that class.",
    "A q-dependent J, a division by q, or a post-result target rescaling is outside this block and cannot be called a solution.",
    "Do not promote a covariance ledger to an AFK, fusion, Stark, or TCC claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:20:00Z",
    "git_head": "3b948e5d06f05398a96d72a76d87771ff432935c",
    "git_state": "DIRTY from the concurrent repository-wide PROGRAM header migration and unrelated projects/tools, plus this live Cycle-202 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
    "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "proof/verify_cycle_201_two_scale_germ_covariance.py",
    "proof/verify_cycle_200_regular_residue_jet.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
