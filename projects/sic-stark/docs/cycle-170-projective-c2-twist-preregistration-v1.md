# Cycle 170 preregistration: projective scalar-twist barrier

Can the actual scalar kernel of the dimension-six projectivization supply a
nontrivial projective character twist for the order-three transport action?

The scalar kernel is the certified `C2` on which the target has eigenvalue
`-1`; the acting transport group is `C3`. This tests that fixed extension,
not an invented larger fibre.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 170,
  "parameters": {
    "acting_and_central_groups": {"kind":"expression","value":"Q=C3=<t|t^3=1>; Z=C2={0,1}; Z embeds in the C6 fibre as 1->3","rationale":"Q is the frozen order-three Shintani return and Z is the certified projective scalar kernel."},
    "projective_data": {"kind":"expression","value":"target scalar eigenvalue on Z is -1; projective CM characters are +1, from Cycle 109","rationale":"This fixes the only allowed scalar character source."},
    "twist_and_extension_test": {"kind":"expression","value":"enumerate all normalized Z-valued 2-cocycles c on Q and all homomorphisms chi:Q->Z; test cocycle law, coboundary status, and whether a nontrivial chi exists","rationale":"A projective central extension or scalar character can alter the transport only through these frozen finite objects."},
    "defect_relation": {"kind":"expression","value":"the Cycle-169 F2 obstruction is the relevant scalar reduction; a C2 twist advances only if it is nontrivial before any graph data are used","rationale":"This prevents fitting a scalar correction to the observed defect."}
  },
  "resource_caps": {"normalized_2cochain_entries":{"kind":"integer","value":4,"rationale":"Only c(1,1),c(1,2),c(2,1),c(2,2) vary."},"candidate_2cochains":{"kind":"integer","value":16,"rationale":"All normalized Z-valued 2cochains are enumerated."},"group_triples":{"kind":"integer","value":27,"rationale":"Every cocycle identity is checked."},"character_maps":{"kind":"integer","value":2,"rationale":"Both images of the generator are checked."},"wall_seconds":{"kind":"integer","value":30,"rationale":"The exact finite extension test is bounded."},"floating_point":{"kind":"not_applicable","justification":"All group laws are finite modular arithmetic.","rationale":"No numerical multiplier fitting is permitted."}},
  "formula_families":["Cycle-109 scalar C2 kernel","C3 central C2 extensions","normalized group cohomology and characters"],
  "selection_rule":["Enumerate every normalized 2cochain and both generator images.","Call an extension nontrivial only if its cocycle class is not a normalized coboundary.","Do not change the central group, transport order, or fit a cochain to Cycle-169 defect values."],
  "failure_rule":["If every normalized C2 2-cocycle is a coboundary and every C3->C2 character is trivial, prove only that the actual scalar kernel supplies no nontrivial projective transport twist.","A pass would prove only a finite projective extension construction, not a coefficient-to-logarithm map, AFK interface, Stark identity, fusion theorem, or TCC.","Failure does not rule out non-scalar, nonprojective, larger-groupoid, wild-local, or analytic engines."],
  "pre_execution":{"timestamp_utc":"2026-08-02T16:36:32Z","git_head":"bd3ad0f5c37df714819b326be65d5a6496abde7d","git_state":"?? docs/cycle-170-projective-c2-twist-preregistration-v1.md"},
  "input_paths":["AGENTS.md","PLAN.md","artifacts/cycle-169-equivariant-coboundary-v1.json","docs/sic-stark-cycle109.md","scripts/dimension_six_projective_cm_gate.gp","../../tools/preregistration_check.py"]
}
-->
