# Cycle 193 preregistration: helical theta lift and odd-polarization amplitudes

Cycle 192 proves a finite 18-dimensional graded Fourier closure but expressly
does not establish a continuous state space or an amplitude theorem.  This
block constructs the smallest source-derived continuous Poincare/Zak section
class from that closure.  It then asks a narrower, falsifiable question: does
the resulting fibrewise projection retain the individual beta-transform
amplitudes required before an all-36 AFK comparison can even begin?

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 193,
  "parameters": {
    "continuous_section_space": {
      "kind": "expression",
      "value": "Let G=R x Z/24, T=(Delta,6), and V=B_(0,+) direct-sum B_(0,-) direct-sum B_(1,+) in C[Z/24], with the Cycle-192 two-point bases. For eta in {+1,-1} and f in Schwartz(R) tensor V, define P_eta f(y,m)=sum_(q in Z) eta^q f(y+q*Delta,m+6q). The admitted continuous sections are finite sums of these P_eta f, interpreted as smooth theta sections with P_eta f(y+Delta,m+6)=eta^(-1)P_eta f(y,m). Their Fourier images are the corresponding tempered dual theta distributions on chi_(xi,n)(T)=eta^(-1).",
      "rationale": "This is a source-derived helical periodization of the exact compact quotient, with the 18D closure imposed before—not fitted after—the transform."
    },
    "continuous_transform_and_sampling": {
      "kind": "expression",
      "value": "Use the full continuous-discrete Fourier transform whose discrete factor is F_24 and whose continuous character is the published beta character. Prove its exact preservation of Schwartz(R) tensor V and its Poincare/Poisson transport to the declared dual theta distributions. The sampled fibre is exactly V; no scalarization of the B_(1,+) boundary-twisted three-shift is admitted.",
      "rationale": "This separates genuine continuous Fourier preservation from the Cycle-192 finite necessary condition."
    },
    "source_beta_amplitudes": {
      "kind": "expression",
      "value": "For the published d=6 beta specialization define R_N(alpha)=24*Gamma_M(Q,0)*Gamma_M(alpha,N)*Gamma_M(-alpha,4-N), N in Z/24. Retain capital Gamma_M and the AFK phase as separate factors. For every canonical N=0,...,11, compare R_N and R_(N+12) at alpha=-N using the published true pole/zero divisors. The proof may use only the frozen d=6 periods with omega_2=1 and omega_1/omega_2 irrational.",
      "rationale": "The beta identity supplies these raw continuous-transform amplitudes without ray data, fitted characters, or selected exponents."
    },
    "admitted_amplitude_family": {
      "kind": "expression",
      "value": "Let iota exchange e_N and e_(N+12). Test only a fixed fibrewise complex-linear, iota-equivariant amplitude operation A on the declared V-valued dual theta fibre: it may depend symbolically on alpha and on the fixed AFK phase/capital-Gamma normalization, but has no fitted entries, row dependence, nonlocal alpha action, derivative, contour, residue, selected exponent, SIC s/d variable, or ray label. A positive result must recover each individual raw R_N contribution for all odd N, before any alias summation or AFK identity is claimed.",
      "rationale": "This is the first non-finite, continuous state-space test, while keeping a checkable amplitude boundary."
    }
  },
  "resource_caps": {
    "discrete_level": {"kind":"integer","value":24,"rationale":"Published beta transform and sealed closure level."},
    "graded_blocks": {"kind":"integer","value":3,"rationale":"Exactly B_(0,+), B_(0,-), and B_(1,+)."},
    "sampled_fibre_dimension": {"kind":"integer","value":18,"rationale":"The sealed minimal closure; no added block is permitted."},
    "odd_polarization_pairs": {"kind":"integer","value":6,"rationale":"The six pairs (N,N+12) with odd canonical N=1,3,...,11."},
    "characteristics": {"kind":"integer","value":36,"rationale":"All AFK characteristics remain in scope; no row selection is permitted."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"The preservation and divisor tests are symbolic/exact."},
    "wall_seconds": {"kind":"integer","value":60,"rationale":"Finite exact ledger and deterministic structural checks only."},
    "floating_point": {"kind":"not_applicable","justification":"No recognition, numerical divisor test, or fitted amplitude is allowed.","rationale":"All claimed conclusions must follow from exact Fourier/Poincare identities and the published divisors."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov continuous--discrete beta Fourier identity",
    "helical Poincare/Zak transform on (R x Z/24)/<(Delta,6)>",
    "Cycle-192 Z2-graded level-24 Fourier closure",
    "published true pole/zero divisors of Gamma_M",
    "AFK capital-Gamma normalization and phase bookkeeping"
  ],
  "selection_rule": [
    "Derive P_eta quasiperiodicity and Fourier/Poisson transport for every Schwartz seed, then derive F_24-invariance of V from the sealed block maps; do not infer either from a finite sample.",
    "Compute the orthogonal fibre projection Pi_V exactly. A negative amplitude result is admissible only if Pi_V identifies an odd pair and the divisor ledger proves the two corresponding raw R values are distinct meromorphic functions.",
    "Audit all 36 characteristics only for coverage of the even/odd source labels. Do not claim that a raw R_N is an AFK cocycle value, a completed alias sum, an RM boundary value, fusion continuity, Stark data, or TCC.",
    "A positive result requires a source-defined fixed iota-equivariant A which recovers every odd raw R_N without accessing a discarded V-perpendicular component."
  ],
  "failure_rule": [
    "A successful Schwartz/theta Fourier statement does not put the meromorphic beta kernel itself in that Schwartz domain and does not prove a periodized beta identity; that requires a separate convergence or distributional-continuation proof.",
    "A projection/divisor mismatch excludes only fixed fibrewise complex-linear iota-equivariant recovery of individual odd raw beta amplitudes from the declared V-projected theta fibre. It does not exclude a larger fibre, a nonlocal alpha operator, derivatives, contours, residues, a new analytic identity, an alias-sum identity, AFK evaluation, RM boundary, fusion, or TCC.",
    "Do not add B_(1,-), replace the p=1 twisted three-shift by a scalar, fit transfer entries, discard the capital Gamma_M normalization or AFK phase, use selected exponents, SIC s/d variables, or ray labels."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T02:25:23Z",
    "git_head": "b404b1e32b5ee64db060fc002a87ff4e85135c07",
    "git_state": "DIRTY: concurrent repository-wide PROGRAM migration and unrelated projects/tooling edits. This block freezes only the listed mathematical sources and does not use PROGRAM.md as an input."
  },
  "input_paths": [
    "artifacts/cycle-192-graded-fourier-polarization-v1.json",
    "proof/verify_cycle_192_graded_fourier_polarization.py",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "scripts/dimension_six_helical_zak.py",
    "scripts/dimension_six_line_bundle_duality.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
