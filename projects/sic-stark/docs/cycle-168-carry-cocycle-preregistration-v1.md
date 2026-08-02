# Cycle 168 preregistration: canonical carry-cocycle completion

Can a standard, independently specified state-dependent `C6` cocycle
representative complete the sealed torsor graph to an associative algebra that
preserves frozen Shintani transport?

The family below is fixed before evaluation. It contains bilinear twists plus
the two canonical coordinate-carry cocycles; it excludes arbitrary
coboundaries derived from the observed graph defect. A pass remains only a
finite algebra construction, not a coefficient-to-logarithm map, AFK
identification, Stark identity, fusion theorem, or TCC.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 168,
  "parameters": {
    "base_and_transport": {
      "kind": "expression",
      "value": "X=(Z/6Z)^2; Y=XxC6; s and d are the sealed Cycle-166 graph and transport; T_tilde(x,e)=(Tx,e+d(x))",
      "rationale": "The full fibre and frozen transport remain fixed."
    },
    "cocycle_family": {
      "kind": "expression",
      "value": "B_(M,r0,r1)(x,y)=x^T M y+r0 floor((x0+y0)/6)+r1 floor((x1+y1)/6) mod 6, for M in Mat_2(Z/6Z), r0,r1 in Z/6Z",
      "rationale": "This is the canonical normalized bilinear-plus-coordinate-carry 2-cocycle representative family; no graph-derived coboundary is included."
    },
    "product": {
      "kind": "expression",
      "value": "delta_(x,e) star_B delta_(y,f)=delta_(x+y,e+f+B(x,y)); J(delta_x)=delta_(x,s(x))",
      "rationale": "The source and graph conventions are unchanged."
    },
    "identities": {
      "kind": "expression",
      "value": "require normalized cocycle associativity; J(delta_x delta_y)=J(delta_x) star_B J(delta_y); and T_tilde(u star_B v)=T_tilde(u) star_B T_tilde(v) on basis pairs",
      "rationale": "Associativity, graph multiplicativity, and transport are independently checked."
    },
    "fixed_probe_pairs": {
      "kind": "expression",
      "value": "((1,0),(1,0)), ((1,0),(0,1)), ((0,1),(1,0)), ((0,1),(0,1)), ((5,0),(1,0)), ((0,5),(0,1))",
      "rationale": "These six preselected pairs determine respectively M00,M01,M10,M11,r0,r1, so a graph-compatible family member is uniquely determined before any full check."
    }
  },
  "resource_caps": {
    "cocycle_candidates": {
      "kind": "integer",
      "value": 46656,
      "rationale": "This exhausts six parameters over Z/6Z."
    },
    "base_pairs": {
      "kind": "integer",
      "value": 1296,
      "rationale": "A surviving candidate receives the full exact basis-pair audit."
    },
    "probe_pairs": {
      "kind": "integer",
      "value": 6,
      "rationale": "The fixed identifying probes permit an exact rejection of every nonmatching candidate without a redundant full replay."
    },
    "wall_seconds": {
      "kind": "integer",
      "value": 30,
      "rationale": "The finite candidate census must remain bounded."
    },
    "floating_point": {
      "kind": "not_applicable",
      "justification": "All equations are exact modular integer identities.",
      "rationale": "Numerical fitting would not define a frozen cocycle."
    }
  },
  "formula_families": [
    "Cycle-166 torsor graph and transport",
    "canonical coordinate-carry normalized C6 2-cocycles",
    "exact associativity, graph, and transport identities"
  ],
  "selection_rule": [
    "Enumerate all 46,656 parameter tuples in lexicographic order and reject a tuple at its first failed fixed graph probe.",
    "For every tuple surviving all six probes, check normalized associativity, graph multiplicativity, and transport covariance on all 1,296 ordered X-pairs.",
    "Report every surviving tuple; do not introduce an arbitrary coboundary, change probes, or fit a cocycle after seeing the graph defect."
  ],
  "failure_rule": [
    "If no tuple survives the full test, falsify only the canonical bilinear-plus-coordinate-carry C6 cocycle family.",
    "A pass is only a finite associative torsor algebra and does not prove a coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC.",
    "Failure does not rule out other state-dependent cocycles, nonlocal products, higher fibres, or analytic operations."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T16:29:01Z",
    "git_head": "0f9a2c1bda400a507fa70602463de88cede2706f",
    "git_state": "?? docs/cycle-168-carry-cocycle-preregistration-v1.md"
  },
  "input_paths": [
    "AGENTS.md",
    "PLAN.md",
    "artifacts/cycle-166-fibre-torsor-v1.json",
    "artifacts/cycle-167-bilinear-convolution-v1.json",
    "discovery/cycle-166-fibre-torsor-prototype-v1.json",
    "proof/verify_cycle_166_fibre_torsor.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
