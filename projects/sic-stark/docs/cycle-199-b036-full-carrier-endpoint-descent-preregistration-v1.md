# Cycle 199 / B036 preregistration: quotient-level Abel--Poincare continuation

Amendment, 2026-08-03: the initial direct-quotient cut was rejected.  A
Poincare/Zak construction sums the alias fibre, so unequal individual
equation-(66) values are not an obstruction.  The rejected cut is retained in
`discovery/cycle-199-b036-direct-quotient-cut.md`; this is still the sole live
Cycle-199 specification.

The actual question is whether the source-prescribed full alias sum admits a
canonical Abel continuation along the attracting geodesic and supplies a
source-derived intertwiner to the Cycle-198 endpoint functional.  The block
must either build that full construction or isolate an exact failure of its
specified ingredients.  It may not replace the sum by a centered alias.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 199,
  "parameters": {
    "full_source_poincare_family": {
      "kind": "expression",
      "value": "Put beta=(5+sqrt(21))/2, omega(tau)=24*tau-5, Q(tau)=omega(tau)+1, D(tau)=4*tau-1, alpha_(a,b,z)(tau)=D(tau)*(4*b-5*a)/3+2*D(tau)*z, N_(a,z)=a+2-6*z, K_(a,b,z)(tau)=Gamma_M(alpha_(a,b,z),N_(a,z);tau)*Gamma_M(-alpha_(a,b,z),4-N_(a,z);tau), and g_(a,b,z)(tau)=exp(pi*i*alpha_(a,b,z)*Q(tau)/(24*omega(tau))). Let Xi_(a,b,z) be the full equation-(66) character, including exp(pi*i*alpha_(a,b,z)*(2*y-Q)/(24*omega(tau))); its transform is R_(a,b,z)=24*Gamma_M(Q,0)*K_(a,b,z). For (a,b) in (Z/6Z)^2 and r in {0,1,2}, define the C198-phase Poincare amplitude Pfull_(a,b,r)(tau,u)=sum_(k in Z)u^abs(k)*R_(a,b,r+3k)(tau), initially only in the common interior lens chamber with 0<u<1, and Pfull_(a,b)=sum_(r=0)^2 Pfull_(a,b,r). Separately define the ordinary-Fourier diagnostic Pord_(a,b,r)(tau,u)=sum_(k in Z)u^abs(k)*g_(a,b,r+3k)*R_(a,b,r+3k). The weights u^abs(k) are the fixed symmetric Abel weights on the helical deck group Z; no row-dependent or fitted weight is allowed.",
      "rationale": "Pfull is the transform of the full equation-(66) character and is the only family compared to C198. Pord retains the Cycle-157 gauge as a separately labeled diagnostic; the two families may never be conflated."
    },
    "source_character_and_coverage": {
      "kind": "expression",
      "value": "For each alias set n=5*(N_(a,z)-2) mod 24 and ell=b-6*z. Verify exactly that 4*ell-n=4*b-5*a+6*z and (-n,ell) mod 6=(a,b). Every one of the 24 N labels must occur in the full 36-row carrier, and every row must retain all three r classes. Capital Gamma_M(Q,0) is an explicit factor of the equation-(66) transformed amplitude and is never merged with the AFK phase.",
      "rationale": "The source quotient, rather than a selected lift, fixes the complete characteristic carrier."
    },
    "interior_identity_and_transform_rule": {
      "kind": "expression",
      "value": "In the stated common interior chamber, prove the Poincare sums are absolutely and locally uniformly convergent at u=1 by the two-base source ratio, so equation (66) may be summed termwise there. The full-phase transformed amplitude is exactly Pfull_(a,b)=24*Gamma_M(Q,0)*sum_(r,k)Gamma_M(alpha_(a,b,r+3k),N_(a,r+3k))*Gamma_M(-alpha_(a,b,r+3k),4-N_(a,r+3k)); Pord is separately the same sum with g inserted. No termwise identification of aliases and no centered replacement is permitted. Any claimed quotient-to-T_6 map J_tau must be derived from the full-phase Fourier/Poincare rule before endpoint specialization, be linear and source-defined on all 36 rows, and satisfy J_tau(Pfull_(a,b))=chi_(a,b) without a selected alias or fitted scalar.",
      "rationale": "The interior domain is the only legitimate origin for a continuation; keeping full-phase and ordinary Fourier amplitudes distinct makes the missing source intertwiner testable."
    },
    "endpoint_abel_continuation": {
      "kind": "expression",
      "value": "Use the attracting A_6 geodesic gamma(s) already fixed by the project, s>0, and the canonical Abel paths u_lambda(s)=exp(-lambda*s) for every lambda in the closed interval [1/2,2]. A positive endpoint result requires a source-derived meromorphic or distributional continuation of Pfull, with an explicit regular part and every finite collision residue from Cycles 194--195 retained, whose limit as s downarrow 0 exists, is finite, and is independent of lambda on that whole interval. It must then prove J_gamma(s)(Pfull_(a,b)(gamma(s),u_lambda(s))) tends to the Cycle-198 value L_src(chi_(a,b)) for all 36 rows. Pord may only diagnose the separately ordinary Fourier packet. A finite set of numerical Abel paths can only falsify a candidate or provide OBSERVED evidence; it cannot establish this condition.",
      "rationale": "The Abel parameter is tied to the active geodesic and must be path-independent, preventing a post-result summation prescription."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A positive result proves only the stated full-carrier source Poincare continuation and its exact all-36 compatibility with the Cycle-198 functional. It still does not identify an AFK cocycle or ray logarithm, prove fusion continuity, Stark algebraicity, or TCC unless those separate identities are subsequently proved. A negative result may reject only the declared symmetric-geodesic Abel/Poincare family or a precisely isolated source-intertwiner condition; it cannot reject all meromorphic, contour, residue, distributional, or non-Abel continuations.",
      "rationale": "The construction is a required interface step, not a shortcut to the downstream arithmetic claims."
    },
    "forbidden_data_and_normalization": {
      "kind": "expression",
      "value": "Retain the capital Gamma_M normalization and its source -q alias multiplier. Keep Xi/Pfull (the full equation-(66) phase) distinct from the g-weighted Pord ordinary Fourier packet exactly as audited in Cycle 157. Keep the AFK phase separate and unevaluated. Do not use ray labels, selected exponents, SIC outcome data, a preferred alias, fitted weights or scalars, a post-result counterterm, or a principal-value convention not derived from the declared Abel/Poincare family.",
      "rationale": "This prevents the full C198 character from being silently replaced by the ordinary Fourier coefficient."
    }
  },
  "resource_caps": {
    "finite_character_rows": {"kind":"integer","value":36,"rationale":"The complete dimension-six Zak character grid."},
    "source_discrete_labels": {"kind":"integer","value":24,"rationale":"The full source Z/24Z carrier."},
    "helical_residue_classes_per_row": {"kind":"integer","value":3,"rationale":"The full Poincare fibre splits only by z modulo 3."},
    "abel_rate_interval": {"kind":"expression","value":"lambda in [1/2,2]","rationale":"A fixed compact family detects dependence on the radial Abel approach without fitting a rate."},
    "diagnostic_interior_points": {"kind":"integer","value":3,"rationale":"The fixed geodesic points s=1/20,1/10,1/5 are diagnostic checks of the interior construction only."},
    "diagnostic_abel_rates": {"kind":"integer","value":5,"rationale":"The fixed rates 1/2,3/4,1,3/2,2 may falsify, but never prove, path independence."},
    "tail_terms_per_direction": {"kind":"integer","value":2048,"rationale":"Fixed cap for any certified interior or diagnostic Abel tail calculation."},
    "arb_precision_bits": {"kind":"integer","value":512,"rationale":"Certified numerical diagnostics use Arb balls rather than floating-point recognition."},
    "wall_seconds": {"kind":"integer","value":300,"rationale":"All-row exact ledgers plus bounded certified diagnostics."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov arXiv:1910.11747v4 equation (66), equations (5)--(15), and true Gamma_M divisors",
    "the source helical quotient and Pontryagin restriction from scripts/dimension_six_helical_zak.py",
    "the two-base interior Poincare packet and ordinary Fourier gauge from scripts/dimension_six_two_base_lens.py and scripts/dimension_six_cycle157_fourier_normalization_audit.py",
    "the finite anti-residue census and combination from Cycles 194--195",
    "the C198 analytic-frequency functional on T_6 and the separately pinned AFK phase bookkeeping"
  ],
  "selection_rule": [
    "Enumerate every (a,b) in {0,...,5}^2 and all three r classes before evaluating any packet; each class uses the complete bilateral k sum with the fixed u^abs(k) weight.",
    "Derive the full equation-(66) character ratio, the separately ordinary-Fourier gauge ratio, the two-base kernel ratio, and the interior tail criterion from the frozen formulas; do not infer an identity from numerical agreement.",
    "A candidate source intertwiner J must be written before endpoint data are inspected and be verified symbolically on all 36 rows.  An output that merely lists summed values without J fails the bridge test.",
    "For any certified diagnostic, use only the five frozen Abel rates and three frozen interior points, record every failed tail or pole, and treat numerical observations as non-proof.",
    "Accept endpoint compatibility only after a proof of the complete lambda-interval limit and exact all-36 equality with L_src; otherwise classify the precise missing continuation or intertwiner condition."
  ],
  "failure_rule": [
    "Failure of interior local uniform convergence, termwise source transform, source-defined J, finite residue accounting, lambda-independent endpoint control, or all-36 C198 compatibility leaves the D6 amplitude gate open and records the exact failed condition.",
    "A divergent or incompatible Abel diagnostic rejects only the declared symmetric-geodesic Abel/Poincare candidate unless a separate theorem proves a broader obstruction.",
    "Do not turn a raw endpoint contour value, a one-mode continuation, a fitted finite part, numerical convergence, or an unproved coefficient-to-ray relation into an AFK, fusion, Stark, or TCC claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T04:03:06Z",
    "git_head": "4298f0ea4b516b029c5ed46671cbb312045fcdde",
    "git_state": "DIRTY only from the concurrent repository-wide PROGRAM migration and unrelated projects/tools, plus this amended live C199 specification and its contained direct-quotient discovery note. This block freezes only the listed SIC--Stark mathematical inputs and does not use PROGRAM.md as an input."
  },
  "input_paths": [
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "artifacts/cycle-197-b034-gaussian-abel-tail-v1.json",
    "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json",
    "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
    "artifacts/cycle-193-b030-helical-theta-amplitude-v1.json",
    "scripts/dimension_six_helical_zak.py",
    "scripts/dimension_six_alias_normalization.py",
    "scripts/dimension_six_two_base_lens.py",
    "scripts/dimension_six_cycle157_fourier_normalization_audit.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
