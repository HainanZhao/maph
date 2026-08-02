# Cycle 169 preregistration: equivariant defect coboundary

Can the Cycle-166 graph defect be removed by a `T`-invariant normalized gauge?
This is the finite action-groupoid cohomology test: ordinary coboundarity is
not informative because the graph already supplies an ordinary cochain.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 169,
  "parameters": {
    "action_groupoid": {
      "kind": "expression",
      "value": "X=(Z/6Z)^2 with T(a,b)=(5a+b,-a) mod 6; the action groupoid has arrows x->Tx",
      "rationale": "This is the frozen finite transport action."
    },
    "defect": {
      "kind": "expression",
      "value": "D(x,y)=s(x+y)-s(x)-s(y) mod 6, where s is the sealed Cycle-166 anchor-normalized graph",
      "rationale": "D is the fixed graph multiplicativity defect, not a candidate product."
    },
    "cochains_and_normalization": {
      "kind": "expression",
      "value": "C1_T={h:X->C6 | h(0)=0, h(Tx)=h(x) for all x, h(3,5)=0, h(3,4)=0}; delta h(x,y)=h(x+y)-h(x)-h(y)",
      "rationale": "T-invariance and the two fixed anchor normalizations are imposed before solving, so h=s is not admissible by construction."
    },
    "cohomology_test": {
      "kind": "expression",
      "value": "solve delta h=D on all XxX over C6 by CRT into exact F2 and F3 linear systems; independently verify any lifted C6 solution on all equations",
      "rationale": "The test is a full action-equivariant coboundary decision, not an unrestricted fitted cochain search."
    }
  },
  "resource_caps": {
    "base_elements": {"kind": "integer", "value": 36, "rationale": "The full characteristic state space is required."},
    "defect_equations": {"kind": "integer", "value": 1296, "rationale": "Every ordered pair is imposed."},
    "prime_fields": {"kind": "integer", "value": 2, "rationale": "CRT uses only F2 and F3."},
    "wall_seconds": {"kind": "integer", "value": 30, "rationale": "The finite exact linear-algebra decision is bounded."},
    "floating_point": {"kind": "not_applicable", "justification": "All maps and linear systems are exact modular arithmetic.", "rationale": "Numerical ranks cannot decide a cohomology class."}
  },
  "formula_families": ["Cycle-166 graph/transport", "T-invariant normalized action-groupoid 1-cochains", "CRT exact coboundary equations"],
  "selection_rule": ["Use all 36 states and all 1,296 defect equations.", "A solution must satisfy both prime-field systems and the original C6 equations with every normalization.", "Do not use s itself, change the anchor normalizations, or introduce a graph-derived gauge."],
  "failure_rule": ["If either prime-field system is inconsistent, or no lifted normalized T-invariant C6 cochain verifies all equations, prove only that D is nontrivial in this normalized T-invariant coboundary quotient.", "If a solution exists, prove only its finite cohomological statement, not an additive coefficient map, AFK interface, Stark identity, fusion theorem, or TCC.", "A negative result does not rule out non-equivariant gauges, altered normalizations, larger groupoids, higher fibres, or analytic operations."],
  "pre_execution": {"timestamp_utc": "2026-08-02T16:32:48Z", "git_head": "d526eb66c88220ef91c672a5b92761f301b8a71f", "git_state": "?? docs/cycle-169-equivariant-coboundary-preregistration-v1.md"},
  "input_paths": ["AGENTS.md", "PLAN.md", "artifacts/cycle-166-fibre-torsor-v1.json", "artifacts/cycle-168-carry-cocycle-v1.json", "discovery/cycle-166-fibre-torsor-prototype-v1.json", "proof/verify_cycle_166_fibre_torsor.py", "../../tools/preregistration_check.py"]
}
-->
