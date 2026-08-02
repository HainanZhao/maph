# Cycle 184 correction preregistration: actual slope shift

<!-- research-freeze-v1
{
  "cycle": 184,
  "failure_rule": ["Withhold the original deformation wording if it identifies alpha_j with z^j rather than z^j-1.", "Promote only a corrected shifted-numerator deformation with all original residual, determinant, and box-scale checks rerun."],
  "formula_families": ["alpha_j=z^j-1", "left rational slope (B-V)/V approximating r-1", "right rational slope (B^2-V^2)/V^2 approximating r^2-1", "common-denominator numerator-shift cancellation in F"],
  "input_paths": ["artifacts/cycle-184-ray-box-determinant-orbit-v1.json", "conventions/ray_box_determinant_orbit_v1.py", "proof/cycle_seal_v1.py", "../../tools/preregistration_check.py"],
  "parameters": {"affected_claim":{"kind":"expression","rationale":"Name the mismatch precisely.","value":"alpha_j=z^j in the nonrational deformation"},"corrected_slopes":{"kind":"expression","rationale":"Use the pinned phase convention.","value":"A_left/V=(B-V)/V, A_right/V^2=(B^2-V^2)/V^2"}},
  "pre_execution": {"git_head":"85c98ce9dc986f408907cdee4dc68bb911862d68","git_state":"correction preregistration and narrative created before executable correction code","timestamp_utc":"2026-08-02T14:32:00Z"},
  "resource_caps":{"candidate_engine_count":{"kind":"integer","rationale":"Containment and one shift repair only.","value":1},"new_executable_code":{"kind":"not_applicable","justification":"The correction specification precedes code.","rationale":"Preflight precedes correction replay code."}},
  "schema":"research-preregistration-freeze-v1",
  "selection_rule":["The original artifact stays immutable; its LCM algebra and subcritical scale must be separated from the corrected phase wording."]
}
-->

## Amendment log

- 2026-08-02: corrected the pre-execution commit hash before any executable
  code; the initial value was an incorrect transcription.
