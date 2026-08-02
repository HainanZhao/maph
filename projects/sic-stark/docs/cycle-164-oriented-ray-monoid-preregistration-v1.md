# Cycle 164 preregistration: oriented ray-monoid section

## Question and boundary

Can characteristic-dependent conductor lowering turn all 36 frozen
dimension-six characteristics into reduced ray objects whose labels admit a
single, arithmetic-Frobenius-oriented coordinate in the full ray group?

This cycle tests an exact finite state-space construction only. It does not
define an additive coefficient-to-logarithm operation, a finite part, an AFK
cocycle identification, a Stark identity, fusion continuity, or a
dimension-six TCC identity. A successful finite prototype is a necessary
construction step, not an operational interface theorem.

The manifest below is the sole frozen specification. In plain terms, it
lowers the conductor of each positive-lift principal ideal, projects the
oriented full-ray generator into that lowered ray group, and uses the
predeclared least compatible exponent as the common (C_6) coordinate.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 164,
  "parameters": {
    "dimension": {
      "kind": "integer",
      "value": 6,
      "rationale": "The Cycle-163 fixed-full-ray obstruction and both frozen orientation anchors are dimension-six data."
    },
    "field": {
      "kind": "symbolic",
      "value": "K=Q(beta), beta^2-5*beta+1=0, discriminant 21",
      "rationale": "This is the Cycle-163 convention-pinned real quadratic field."
    },
    "characteristic_domain": {
      "kind": "expression",
      "value": "(a,b) in {0,1,2,3,4,5}^2 in lexicographic order",
      "rationale": "The construction must be total on the same frozen 36-row domain, including (0,0)."
    },
    "positive_lift": {
      "kind": "expression",
      "value": "p*(a,b)=max{p in Z: p congruent a (mod 6), b*(5-sqrt(21))/2-p>0}; gamma(a,b)=b*beta-p*",
      "rationale": "This preserves the selected-embedding and principal-representative convention used in Cycle 163."
    },
    "full_modulus": {
      "kind": "expression",
      "value": "m=(6) with exactly the selected real place beta'=(5-sqrt(21))/2 in the ray modulus",
      "rationale": "The candidate common coordinate source is the existing oriented full ray group."
    },
    "conductor_lowering": {
      "kind": "expression",
      "value": "c=m+(gamma); m_ab=m/c; a_ab=(gamma)/c, represented by exact integral ideals",
      "rationale": "Ideal sum removes precisely the common finite divisor before defining the reduced ray object."
    },
    "orientation": {
      "kind": "expression",
      "value": "G6=Cl_{m infinity_2}; g=[(4*beta+1)] is the arithmetic-Frobenius-oriented generator; target coordinate is g^e in this fixed C6",
      "rationale": "The target orientation is fixed independently of every row result."
    },
    "transition_and_section": {
      "kind": "expression",
      "value": "pi_ab:G6->Cl_{m_ab infinity_2} is computed by the images of g^e; e_ab=min{e in {0,...,5}:pi_ab(g^e)=[a_ab]}; lambda_ab=g^e_ab",
      "rationale": "This gives a deterministic, outcome-blind tie rule and one common oriented C6 target."
    },
    "orientation_anchors": {
      "kind": "expression",
      "value": "lambda_(3,5)=g^1 and lambda_(3,4)=g^2",
      "rationale": "These are the two eligible Cycle-163 labels that the construction must preserve exactly."
    },
    "full_modulus_recovery": {
      "kind": "expression",
      "value": "For every row with c=(1), lambda_ab must equal the direct full-ray discrete log of (gamma)",
      "rationale": "The new state space must extend rather than overwrite its fixed-full-modulus subdomain."
    }
  },
  "resource_caps": {
    "row_count": {
      "kind": "integer",
      "value": 36,
      "rationale": "Exhaustive finite domain; no adaptive row selection is allowed."
    },
    "candidate_exponents_per_row": {
      "kind": "integer",
      "value": 6,
      "rationale": "The predeclared common target is C6, so every membership test exhausts exactly six exponents."
    },
    "wall_seconds": {
      "kind": "integer",
      "value": 60,
      "rationale": "The prototype is finite exact ideal/ray arithmetic and must not expand into an unbounded search."
    },
    "pari_gp_version": {
      "kind": "text",
      "value": "2.15.4",
      "rationale": "Pinned project pipeline for byte-level replay of discrete ray data."
    },
    "floating_point": {
      "kind": "not_applicable",
      "justification": "All positivity, norms, ideal operations, and ray-class coordinates are exact; no numerical threshold is used.",
      "rationale": "A floating-point branch could change conductor or section membership and is prohibited."
    }
  },
  "formula_families": [
    "exact selected-embedding positivity via integer comparison after squaring positive sides",
    "principal-ideal conductor lowering c=(6)+(gamma), m_ab=(6)/c, a_ab=(gamma)/c",
    "PARI bnrinit and bnrisprincipal exact finite ray-class coordinates at one selected real place",
    "oriented source-generator image enumeration and least-exponent section in C6"
  ],
  "selection_rule": [
    "Enumerate every characteristic in frozen lexicographic order before inspecting a row result.",
    "Use only the positive lift, ideal formulas, selected real place, generator g, and least e in 0..5 stated above.",
    "Choose no modulus, generator, place, branch, or tie rule from an observed ray label, packet value, or anchor outcome."
  ],
  "failure_rule": [
    "Fail this named minimal-lift ray-monoid section if G6 is not the frozen oriented C6, a reduced ray group or transition image is undefined, any row has no e in 0..5, either anchor has the wrong exponent, or a full-modulus row fails direct-log recovery.",
    "A failure confines only this conductor-lowering section; it is not a TCC, Stark, AFK-interface, or global ray-monoid no-go.",
    "A pass establishes only the exact finite state-space totality and preserves no analytic interface claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T00:00:00Z",
    "git_head": "6e4b04439ea887b427787e533e75d11f9c3fa3ea",
    "git_state": " M ../../AGENTS.md\n?? discovery/cycle-164-oriented-ray-monoid-working-ledger.md\n?? docs/cycle-164-oriented-ray-monoid-preregistration-v1.md"
  },
  "input_paths": [
    "AGENTS.md",
    "PLAN.md",
    "artifacts/cycle-163-spectral-ray-interface-v1.json",
    "artifacts/cycle-163-spectral-ray-interface-v2.json",
    "docs/cycle-163-spectral-ray-interface-preregistration-v1.md",
    "proof/verify_cycle_163_fixed_full_ray_selector.py",
    "scripts/dimension_six_ray_recon.gp",
    "scripts/dimension_six_shintani_cycle.py",
    "discovery/audit_tcc_sweep_d12_conductor_lowering_corrected_v2.py",
    "docs/effective-stark-sweep-context-v1.md",
    "../../tools/preregistration_check.py"
  ]
}
-->
