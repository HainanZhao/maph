# Cycle 189 preregistration: regularized sign-reflected Jacobi--lens interface

Test the sign-reflected packet in a real interior domain, then attempt its
first source-defined AFK identification. The Chen--Chen--Gu expansion gives
the continuation; Kopp's Jacobi-to-modular cocycle identity is the only
permitted elliptic-coordinate map. The earlier untranslated (z=0) census
remains a scoped control, not a no-go theorem.

Amendment 1 follows the companion review: the interior regularization,
removable (r=1) finite part, and (t\to1^-) limit are now exact. The
remaining live test is the full characteristic Jacobi-to-modular map before
any unit-circle or spectral claim.

Amendment 2 tests the smallest factorwise lift from the existing helical
packet to that map: one forced (omega_2=1) gamma shift. It is a scoped
prototype for a later periodization transform, not a substitute for one.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 189,
  "parameters": {
    "continuation_source": {
      "kind": "expression",
      "value": "Chen--Chen--Gu arXiv:math/0701062, Theorem 2.1 / equation (2.1), official TeX SHA-256 3d902b7d9c0beb6cd6f36e0c66c0213b1cc76ad9302e7311b9f4e3525e3df9a6; it expands _2psi_2(a,b;c,d;q,z) into two _2phi_1 terms when |cd/(ab)|<|z|<1 and |bq/d|<1.",
      "rationale": "The named continuation identity and its strict interior hypotheses."
    },
    "regularized_packet": {
      "kind": "expression",
      "value": "w=exp(2*pi*i/6), 0<t<1, |q|<r<|q|^(-1), a=x, b=t*w^2*x, c=-q*t*w^2*x, d=-q*x, z=-r*q; use the ordered r->1 then t->1^- limit for the raw _2psi_2(x,w^2*x;-q*w^2*x,-q*x;q,-q).",
      "rationale": "This has cd/(ab)=q^2, |z|=r|q|, |bq/d|=t and isolates the removable (r;q)_infty singularity."
    },
    "boundary_and_branch": {
      "kind": "expression",
      "value": "Use convergent q-Pochhammer branches for 0<t<1 and |q|<r<|q|^(-1). First prove cancellation in the full two-term expression, then r->1 through real r>1, then t->1^-. Only subsequently may a two-base modular continuation approach beta along the attracting A6 geodesic. Never make an equal-base off-boundary substitution.",
      "rationale": "Pins the order of continuation and prohibits the known collapsed-boundary shortcut."
    },
    "jacobi_lens_map": {
      "kind": "expression",
      "value": "With A=((115,-24),(24,-5)) and omega=24*tau-5, gamma_M(mu,m;omega,1)=sigma_{(0,m+1),A}((mu+m)/24,tau). Capital Gamma_M=Z(m)*exp(-pi*i*B_2,2(mu;omega,1)/48)*gamma_M and that factor is retained.",
      "rationale": "Kopp arXiv:2411.06763v3 equations (1)--(3), source SHA-256 4f3d0b359502e575e28c6be8259ed0ac45422f94ff91a9f6f3caf7a4f1504bcc; Sarkissian--Spiridonov arXiv:1910.11747v4 equations (5)--(8), source SHA-256 69a140cfd4af010a7ffcf0643e1df211f4675a88c2480e1b868c77bca4520941."
    },
    "source_defined_afk_map": {
      "kind": "expression",
      "value": "For p=(p1,p2) in (Z/6Z)^2, r_p=p/6, kappa_p=(I-A)r_p=(-19*p1+4*p2,-4*p1+p2), m_p=kappa_(p,2)-1, mu_p(tau)=4*(p2*tau-p1)-m_p. Test gamma_M(mu_p,m_p)=sigma_(kappa_p,A)(<r_p,(tau,1)>,tau)=shin_A^(r_p)(tau) using Kopp's Jacobi-to-modular cocycle identity; keep AFK's phase Phi_t(p) separate.",
      "rationale": "A complete source-defined characteristic map, distinct from the deliberately falsified untranslated z=0 class."
    },
    "raw_factor_alignment": {
      "kind": "expression",
      "value": "For the frozen helical gamma factor alpha_z=(4*tau-1)*((4*b-5*a)/3+2*z), N_z=a+2-6*z, compare to mu_p=(4*tau-1)*p2+1, m_p=-4*p1+p2-1. The only constant omega_2 shift that can match continuous coefficients is (alpha_z,N_z)->(alpha_z+1,N_z-1). Require exact equality with (mu_p,m_p) for a,b,p in (Z/6Z)^2 and arbitrary integer z; eliminate z symbolically.",
      "rationale": "This is the smallest source-defined raw-factor-to-AFK prototype. It tests one necessary shift rather than fitting an alias or introducing ray data."
    }
  },
  "resource_caps": {
    "symbolic_parameter_cases": {"kind":"integer","value":2,"rationale":"The displayed regularization and its c,d interchange only."},
    "characteristic_grid": {"kind":"integer","value":36,"rationale":"Test every canonical characteristic; report p=0 separately."},
    "frequency_grid": {"kind":"integer","value":36,"rationale":"Test all residue-frequency pairs before symbolic elimination of the alias integer."},
    "factor_orientations": {"kind":"integer","value":2,"rationale":"The frozen kernel has the alpha,N and -alpha,4-N gamma factors."},
    "regularization_limit": {"kind":"integer","value":2,"rationale":"Only r->1 then t->1^- is allowed."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Only exact symbolic divisor and cocycle algebra is authorized."},
    "wall_seconds": {"kind":"integer","value":30,"rationale":"The prototype is finite exact arithmetic."},
    "floating_point": {"kind":"not_applicable","justification":"No numerical recognition or enclosure claim is authorized.","rationale":"The interface must first be defined exactly."}
  },
  "formula_families": [
    "Chen--Chen--Gu _2psi_2-to-_2phi_1 expansion",
    "q-Pochhammer continuation and Heine transformation",
    "Sarkissian--Spiridonov gamma_M and Gamma_M normalization",
    "Kopp Jacobi cocycle and Jacobi-to-modular identity",
    "AFK normalized ghost overlap definition"
  ],
  "selection_rule": [
    "Verify every Chen--Chen--Gu hypothesis before its use; record the raw direct failure |bq/d|=1.",
    "Verify all Pochhammer arguments, the r=1 cancellation, the finite-part derivative, and the t->1^- transform exactly before an RM claim.",
    "For every p, verify kappa_p, mu_p, the lower gamma/Jacobi equality, and the Kopp Jacobi-to-modular identity before applying the separate AFK phase.",
    "For the raw-factor prototype, compare tau coefficients first; if they force the omega_2 shift, eliminate the arbitrary alias integer exactly and report any surviving or impossible congruence without selecting an alias.",
    "Only an exact AFK cross-orbit relation or a rigorous enclosure with a preregistered strict margin advances the D6 interface gate."
  ],
  "failure_rule": [
    "A failed continuation, divisor, normalization, full-grid kappa_p/mu_p, or source-identity check contains this route only; it is not a no-go for another completion, interface, fusion theorem, or TCC.",
    "Do not call the Chen--Chen--Gu formula Slater's, use raw |bq/d|=1 as an interior theorem hypothesis, or substitute Bailey--Daum +q for -q.",
    "Do not erase Gamma_M's explicit normalization, fit phases or character data, use ray labels or selected exponents, or treat multiplier weights as spectral coefficients."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T01:20:00Z",
    "git_head": "4282bd47a214e14527748e6ab915891d3b400f16",
    "git_state": "CLEAN before initial Cycle 189 preregistration; Amendment 1 follows companion review in the same live cycle"
  },
  "input_paths": [
    "AGENTS.md",
    "artifacts/cycle-188-stabilizer-covariance-v1.json",
    "proof/verify_cycle_188_stabilizer_covariance.py",
    "scripts/dimension_six_alias_hypergeometric.py",
    "scripts/dimension_six_slater_reduction.py",
    "scripts/dimension_six_ss_evaluation_audit.py",
    "scripts/dimension_six_two_base_lens.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
