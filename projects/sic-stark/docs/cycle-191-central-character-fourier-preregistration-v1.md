# Cycle 191 preregistration: central-character restriction of the beta Fourier transform

Use the published continuous--discrete beta Fourier transform as an actual
operator, rather than reindexing its raw output.  Its discrete
\(\mathbb Z/24\) Fourier character has a canonical two-central-character
block decomposition.  Test whether that decomposition supplies the
all-characteristic selection and finite phase data needed before any analytic
operator or boundary claim.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 191,
  "parameters": {
    "source_transform": {
      "kind": "expression",
      "value": "Use Sarkissian--Spiridonov arXiv:1910.11747v4 degeneration (66), specialized as in the frozen d=6 paper to (p,k,r,s)=(-115,24,5,24), g=Q=omega1+omega2, l=0. Its discrete Fourier character is omega_24^(n*m) with n=5*(N-2) mod 24; retain the continuous Fourier character and capital Gamma_M normalization.",
      "rationale": "This is a published continuous--discrete Fourier identity, genuinely outside the T1,T2,H recurrence-only class."
    },
    "central_character_blocks": {
      "kind": "expression",
      "value": "In C[Z/24], for j mod 6 and epsilon in Z/2 define v_j^epsilon=e_(2j)+(-1)^epsilon e_(2j+12). Restrict the source character chi_n(m)=omega_24^(n*m) to these two canonical level-six blocks. No other support, coefficient, or block is admitted.",
      "rationale": "They are the two central-character variants of the level-24 two-point block, not a fitted finite basis."
    },
    "source_label_rule": {
      "kind": "expression",
      "value": "For raw frequency (a,b) mod 6 and alias z, N_z=a+2-6z, ell_z=b-6z, n_z=5*(N_z-2) mod24, and epsilon=a mod2. The frozen helical Zak restriction is (-n_z,ell_z)=(a,b) mod6.",
      "rationale": "It is the source-defined all-alias label rule, including the forced central character."
    },
    "afk_comparison": {
      "kind": "expression",
      "value": "Compare the resulting selected level-six character, its two-point Fourier phase, and the retained Gamma_M inversion normalization against the frozen AFK characteristic p=(a,b), source line gamma_M(mu_p,m_p)=shin_A^(p/6), and AFK phase Phi_p. The test may establish only selection/phase compatibility; it may not infer analytic operator restriction or a cocycle equality without an explicit amplitude identity.",
      "rationale": "Separates the finite Fourier selection problem from the still-open amplitude/operator theorem."
    }
  },
  "resource_caps": {
    "characteristic_grid": {"kind":"integer","value":36,"rationale":"Every d=6 source characteristic is checked."},
    "aliases_per_characteristic": {"kind":"integer","value":25,"rationale":"Use z=-12,...,12 for the bounded all-alias census before the symbolic proof."},
    "central_character_blocks": {"kind":"integer","value":2,"rationale":"Only epsilon=0,1 is admitted."},
    "block_basis_vectors": {"kind":"integer","value":12,"rationale":"Six basis vectors in each of two blocks."},
    "discrete_fourier_modes": {"kind":"integer","value":24,"rationale":"The full source discrete transform is audited."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"The selection and phase audit is exact finite algebra."},
    "wall_seconds": {"kind":"integer","value":30,"rationale":"The finite character census is bounded."},
    "floating_point": {"kind":"not_applicable","justification":"No numerical boundary or amplitude claim is authorized.","rationale":"This is an exact source-transform restriction test."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov continuous--discrete beta Fourier transform",
    "two-central-character restriction of C[Z/24]",
    "d=6 helical Zak label descent",
    "capital Gamma_M normalization and AFK/Ishibashi inversion phase"
  ],
  "selection_rule": [
    "Prove the block-character restriction formula for all 24 discrete modes before applying the source label rule.",
    "Check all 36 characteristics and the 25 frozen aliases each, then prove alias independence symbolically.",
    "Advance only if the source transform selects the forced epsilon=a mod2 block and the full finite phase ledger agrees with the corresponding AFK characteristic without fitted coefficients; otherwise contain the failed block-restriction class.",
    "Treat finite selection/phase compatibility as a prerequisite only: exact analytic operator preservation, source-to-AFK amplitude equality, and every boundary claim remain separately required."
  ],
  "failure_rule": [
    "A failed selection or phase check excludes only the declared two-central-character restriction of the published beta Fourier transform. It does not exclude another contour identity, a different analytic operator completion, a real-multiplication boundary theorem, fusion continuity, or TCC.",
    "Do not replace the full 24-mode transform with a chosen single mode, add a third block or fitted coefficients, discard Gamma_M normalization or AFK wrap signs, use ray labels or selected exponents, or make an equal-base or unit-circle substitution."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T03:00:00Z",
    "git_head": "1d4bcec5f14c1efca44f41974d83d56d194e221c",
    "git_state": "CLEAN before Cycle 191 preregistration"
  },
  "input_paths": [
    "AGENTS.md",
    "artifacts/cycle-190-balanced-helical-reflection-v1.json",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "scripts/dimension_six_helical_zak.py",
    "scripts/dimension_six_heisenberg_descent.py",
    "scripts/dimension_six_inversion_phase.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
