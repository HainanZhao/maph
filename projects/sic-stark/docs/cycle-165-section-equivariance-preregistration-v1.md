# Cycle 165 preregistration: section-equivariant operation class

## Question and boundary

Can the sealed conductor-lowered section support an outcome-blind,
pointwise label-respecting linear operation from the formal 36-characteristic
additive module that intertwines the Shintani action with any target action
on its oriented (C_6) labels?

This is an exact prerequisite test for one named operation class. It does not
evaluate a continuous packet, choose a logarithm branch, define a finite part,
identify an AFK cocycle, or make a Stark or TCC claim. A failure rejects only
the stated section-equivariant pointwise class; a pass would still not supply
the missing analytic operation.

The manifest below is the sole frozen specification. It asks whether the
existing characteristic action can descend through the already-fixed section
without inspecting an additive coefficient or target ray value.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 165,
  "parameters": {
    "dimension": {
      "kind": "integer",
      "value": 6,
      "rationale": "The formal characteristic module and sealed target are both frozen at dimension six."
    },
    "input_module": {
      "kind": "expression",
      "value": "V=Q[X], X=(Z/6Z)^2, basis delta_(a,b) in lexicographic order",
      "rationale": "This is the formal finite-characteristic input underlying the 36 additive coefficients, so the test requires no numerical packet evaluation."
    },
    "shintani_action": {
      "kind": "expression",
      "value": "T(a,b)=(5a+b,-a) mod 6 and T_*(delta_x)=delta_(T x)",
      "rationale": "This is the convention-pinned period-one Shintani action already used in Cycles 163--164."
    },
    "sealed_section": {
      "kind": "expression",
      "value": "lambda:X->C6 is the Cycle-164 least-exponent section with lambda(x)=e iff the sealed ray object maps to g^e",
      "rationale": "The labels, place, generator, and tie rule are immutable Cycle-164 output, not selected in this cycle."
    },
    "operation_class": {
      "kind": "expression",
      "value": "A:V->Q[C6], A(delta_x)=delta_(lambda(x)); U_u(delta_e)=delta_(u(e)) for a set map u:C6->C6",
      "rationale": "This is the minimally outcome-blind pointwise label-respecting linear pushforward; allowing every set map makes the descent test stronger than an affine or group-automorphism-only test."
    },
    "compatibility_identity": {
      "kind": "expression",
      "value": "A composed with T_* equals U_u composed with A on every basis vector delta_x",
      "rationale": "Exact intertwining is the frozen necessary condition for this operation class to respect the Shintani transport through the sealed section."
    },
    "target_actions": {
      "kind": "integer",
      "value": 46656,
      "rationale": "Every set map C6->C6 is included: 6^6=46,656; no post-result restriction to convenient target actions is allowed."
    },
    "logarithm_branch": {
      "kind": "not_applicable",
      "justification": "The frozen test remains in the formal group-ring stage and evaluates no logarithm or analytic continuation.",
      "rationale": "Introducing a branch would enlarge the named operation class after the finite descent question."
    },
    "finite_part": {
      "kind": "not_applicable",
      "justification": "No boundary limit or continuous coefficient is evaluated in this exact finite prerequisite test.",
      "rationale": "A finite-part prescription belongs only to a later surviving analytic operation class."
    }
  },
  "resource_caps": {
    "characteristic_rows": {
      "kind": "integer",
      "value": 36,
      "rationale": "The complete frozen domain must be checked, not a chosen orbit or fibre."
    },
    "target_action_maps": {
      "kind": "integer",
      "value": 46656,
      "rationale": "Exhaustive target-action enumeration closes the declared finite class."
    },
    "wall_seconds": {
      "kind": "integer",
      "value": 30,
      "rationale": "The finite exact table and 6^6 action census require no unbounded search."
    },
    "floating_point": {
      "kind": "not_applicable",
      "justification": "All objects are finite sets, integer residues, and exact basis maps.",
      "rationale": "Numerical fitting would defeat the outcome-blind operation-class test."
    }
  },
  "formula_families": [
    "formal finite-characteristic module Q[(Z/6Z)^2]",
    "Cycle-164 least-exponent section lambda into the oriented C6",
    "period-one Shintani action T(a,b)=(5a+b,-a) mod 6",
    "pointwise section pushforward and exhaustive finite target-action descent"
  ],
  "selection_rule": [
    "Read lambda only from the sealed Cycle-164 prototype; do not alter a label, fibre, generator, or tie rule.",
    "Test every x in X and every u:C6->C6; do not choose a surviving submodule, fibre, or target action after observing a collision.",
    "Do not inspect a continuous packet, a Stark logarithm, or an AFK target value when deciding the operation or compatibility rule."
  ],
  "failure_rule": [
    "Falsify the named pointwise label-respecting section-equivariant operation class if no u:C6->C6 satisfies A T_*=U_u A, equivalently if equal lambda labels have unequal successor labels under T.",
    "A passing census establishes only descent for this formal class and does not define a logarithm, finite part, AFK cocycle, analytic continuation, Stark identity, or TCC identity.",
    "A failure is not a no-go for non-pointwise, non-fibrewise, nonlinear, or analytically regularized coefficient-to-logarithm operations."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T16:03:37Z",
    "git_head": "0a54005cc90d11c8c2d71cae7248fc31a1da1575",
    "git_state": " M ../../AGENTS.md\n?? discovery/cycle-165-section-equivariance-working-ledger.md\n?? docs/cycle-165-section-equivariance-preregistration-v1.md"
  },
  "input_paths": [
    "AGENTS.md",
    "PLAN.md",
    "artifacts/cycle-163-spectral-ray-interface-v1.json",
    "artifacts/cycle-164-oriented-ray-monoid-section-v1.json",
    "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json",
    "proof/verify_cycle_164_oriented_ray_monoid_section.py",
    "scripts/dimension_six_shintani_cycle.py",
    "scripts/dimension_six_tcc_beta_frequency.py",
    "docs/sic-stark-cycle157.md",
    "certificates/dimension-six-cycle157-fourier-normalization-audit.json",
    "../../tools/preregistration_check.py"
  ]
}
-->
