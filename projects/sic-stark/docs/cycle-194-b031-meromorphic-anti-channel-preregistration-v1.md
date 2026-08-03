# Cycle 194 preregistration: meromorphic anti-channel periodization

Cycle 193 proves that the minimal 18-dimensional fibre loses the odd
antisymmetric directions, but it does not say that the source beta kernel
lacks them.  This block tests the opposite possibility with a source-defined
construction: use the principal parts of the actual two-gamma kernel to force
the missing `B_(1,-)` fibre, then periodize that meromorphic channel only in
the interior two-base chamber where the published factorization supplies
locally uniform bilateral tails.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 194,
  "parameters": {
    "forced_anti_fibre": {
      "kind": "expression",
      "value": "Let A=B_(1,-) with basis e_(1+2j)-e_(13+2j), j mod 6. Let Pi_A be its exact orthogonal projection in C[Z/24]. This is the sole added fibre: it is admitted only if the source kernel K_Q(y,m)=Gamma_M(y,m)*Gamma_M(Q-y,-m) has a nonzero odd antisymmetric principal part in every canonical pair N=1,3,...,11 at y=-N.",
      "rationale": "A is the unique Cycle-192 Fourier-stable complement to V. Principal parts make its inclusion source-forced rather than a fitted fourth block."
    },
    "principal_part_rule": {
      "kind": "expression",
      "value": "For every odd canonical N in {1,3,...,11}, compare K_Q(y,N) and K_Q(y,N+12) at y=-N using the published true Gamma_M pole/zero divisors. The anti-channel is the coefficient of the simple principal part of Pi_A K_Q there. It is accepted only when the first term has a true pole and every other gamma factor in the comparison is finite nonzero; no numerical residue or normalization fitting is allowed.",
      "rationale": "This is a fixed source-local extraction rule that can carry the six directions discarded by Pi_V."
    },
    "interior_spectral_periodization": {
      "kind": "expression",
      "value": "In the frozen interior two-base chamber, apply the published beta transform first and periodize the A-projected spectral RHS R_N(alpha)=24*Gamma_M(Q,0)*Gamma_M(alpha,N)*Gamma_M(-alpha,4-N) along N_z=a+2-6z and alpha_z=D*(4b-5a)/3+2D*z, D=(omega1-omega2)/6, separately for z mod 3. First solve the exact collision lattice of true poles under z->z+3. If aliases share a pole, derive the source functional-equation ratio of their residues and test the resulting bilateral residue series with the strict interior tail criterion; termwise principal parts are forbidden unless the collision audit proves isolation. The boundary and any fused value are excluded.",
      "rationale": "The periodization is the source-defined helical alias sum, not a formal summation at the real-multiplication endpoint."
    },
    "transform_and_amplitude_boundary": {
      "kind": "expression",
      "value": "Derive F_24(A)=A from the sealed block action and verify that Pi_A records the individual odd difference R_N-R_(N+12) rather than averaging it away. A positive result is only an interior meromorphic anti-channel and source amplitude carrier. It must retain capital Gamma_M normalization and the AFK phase separately, and may not identify the channel with an AFK cocycle, a completed alias value, or an RM boundary value.",
      "rationale": "This tests a non-finite, source-forced polarization change while preserving the claim boundary."
    }
  },
  "resource_caps": {
    "discrete_level": {"kind":"integer","value":24,"rationale":"The source beta level and full graded closure."},
    "minimal_fibre_dimension": {"kind":"integer","value":18,"rationale":"Cycle-193 fibre retained for comparison."},
    "added_anti_fibre_dimension": {"kind":"integer","value":6,"rationale":"Exactly B_(1,-), no further enlargement."},
    "full_source_fibre_dimension": {"kind":"integer","value":24,"rationale":"V direct-sum A exhausts the four two-point blocks."},
    "principal_part_pairs": {"kind":"integer","value":6,"rationale":"Odd canonical pairs only."},
    "characteristics": {"kind":"integer","value":36,"rationale":"All rows remain in scope; no selected row or exponent."},
    "alias_classes": {"kind":"integer","value":3,"rationale":"Exactly z mod 3 under the helical period."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Divisors, projections, and tail-rule logic are exact."},
    "wall_seconds": {"kind":"integer","value":60,"rationale":"Bounded symbolic divisor and alias ledger only."},
    "floating_point": {"kind":"not_applicable","justification":"No endpoint approximation, numerical residue, or amplitude fit is allowed.","rationale":"The claimed result is interior meromorphic structure only."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov true Gamma_M divisors and degenerate beta transform",
    "source interior two-base 24-factor continuation and helical alias classes",
    "Cycle-192 level-24 block Fourier action",
    "Cycle-193 V/A fibre projection and raw beta amplitude convention",
    "AFK capital-Gamma normalization and phase bookkeeping"
  ],
  "selection_rule": [
    "Prove the physical-kernel principal-part witnesses at all six odd canonical pairs before declaring A source-forced.",
    "Use all 36 characteristics for parity/alias coverage and all three z classes. The interior periodization may be called meromorphic only on a chamber with the frozen local-uniform tail condition and an exact collision/residue-orbit audit; do not take a boundary limit.",
    "A positive result requires exact A preservation by F_24 and exact retention of R_N-R_(N+12) in every odd pair. A negative result may be promoted only for the declared principal-part/interior-periodization class, with its explicit failing witness."
  ],
  "failure_rule": [
    "Nonzero local principal parts alone, or local uniform convergence away from poles, do not prove convergence of a coincident-pole residue orbit, a beta-kernel Poincare theorem outside the interior chamber, an AFK identity, a ray map, an RM boundary value, fusion, or TCC.",
    "Failure of the declared channel excludes only the one A-valued principal-part construction with the frozen source periodization. It does not exclude another distributional completion, contour/residue transform, a larger non-block fibre, an alias-sum identity, AFK evaluation, boundary theorem, fusion, or TCC.",
    "Do not add any fibre beyond A, fit a residue or transfer entry, use selected exponents, SIC s/d variables, ray labels, endpoint continuation, or discard capital Gamma_M normalization or AFK phase."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T02:37:48Z",
    "git_head": "d778d5ea29eef33b979f88ff501c1a4d50cd000e",
    "git_state": "DIRTY: concurrent repository-wide PROGRAM migration and unrelated project/tooling edits. This block freezes only the listed mathematical sources and does not use PROGRAM.md as an input."
  },
  "input_paths": [
    "artifacts/cycle-193-b030-helical-theta-amplitude-v1.json",
    "proof/verify_cycle_192_graded_fourier_polarization.py",
    "proof/verify_cycle_193_helical_theta_amplitude.py",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "scripts/dimension_six_helical_zak.py",
    "scripts/dimension_six_interior_factorization_audit.py",
    "scripts/dimension_six_two_base_lens.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
