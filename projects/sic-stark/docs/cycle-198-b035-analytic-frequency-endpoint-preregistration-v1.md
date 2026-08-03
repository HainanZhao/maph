# Cycle 198 / B035 preregistration: analytic-frequency endpoint functional

The raw endpoint contour has no common real-frequency convergence strip.
This block tests a different, source-defined object: the unique meromorphic
continuation of the published two-gamma transform, restricted to a fixed
finite-dimensional space of endpoint exponential characters.  A successful
test defines only that regularized transform functional; it does not identify
its values with AFK data or prove fusion.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 198,
  "parameters": {
    "endpoint_and_source_identity": {
      "kind": "expression",
      "value": "Set beta=(5+sqrt(21))/2, omega=24*beta-5=55+12*sqrt(21), Q=omega+1, D=(omega-1)/6, and c=Q/2. Use Sarkissian--Spiridonov arXiv:1910.11747v4 equation (66), specialized to (p,k,r,s)=(-115,24,5,24), g=Q, l=0: the continuous-discrete transform of K_Q(y,m)=Gamma_M(y,m)Gamma_M(Q-y,-m), with character exp(pi*i*m*437*(2*N-4)/24) exp(pi*i*alpha*(2*y-Q)/(24*omega)), has meromorphic value 24*Gamma_M(Q,0)*Gamma_M(alpha,N)*Gamma_M(-alpha,4-N). Capital Gamma_M is retained throughout.",
      "rationale": "This is the published continuation rule whose uniqueness and endpoint regularity are being tested, not a fitted tail subtraction."
    },
    "characteristic_state_space": {
      "kind": "expression",
      "value": "For each (a,b) in {0,...,5}^2 set r_ab=4*b-5*a; let sigma_ab be its unique representative in {-3,-2,-1,0,1,2}; set z_ab=(sigma_ab-r_ab)/6, N_ab=a+2-6*z_ab, and alpha_ab=D*sigma_ab/3. Let T_6 be the 36-dimensional complex vector space with basis chi_ab(lambda,m)=exp(pi*i*m*437*(2*N_ab-4)/24)*exp(pi*i*alpha_ab*(2*(c+i*lambda)-Q)/(24*omega)), lambda in R and m in Z/24Z, with coefficient norm ||sum u_ab chi_ab||_1=sum |u_ab|. These are entire exponential-type characters; no additional frequency, alias, or selected row is admitted.",
      "rationale": "The centered helical lift freezes both the continuous and discrete labels before evaluating the source transform."
    },
    "continuation_and_uniqueness_rule": {
      "kind": "expression",
      "value": "Define L_src first by the published integral identity in its nonempty convergence chamber and then by its joint meromorphic continuation in the source parameters. On T_6 set L_src(chi_ab)=24*Gamma_M(Q,0)*Gamma_M(alpha_ab,N_ab)*Gamma_M(-alpha_ab,4-N_ab), only if that endpoint is outside every true pole and zero divisor needed for finiteness and nonzero normalization. Uniqueness means equality with the source transform on a nonempty open subset of the same connected meromorphic parameter domain; the meromorphic identity theorem then forbids adding an entire function, delta term, principal-value choice, or counterterm invisible to the raw endpoint contour.",
      "rationale": "This distinguishes analytic continuation inherited from the source theorem from an arbitrary hyperfunction representative."
    },
    "divisor_and_endpoint_acceptance": {
      "kind": "expression",
      "value": "Audit all 36 pairs against the published true divisors. For Gamma_M(mu,m), true poles are mu=-j*omega-(24*n+5*j+m), j>=0 and 24*n+5*j+m>=0; true zeros are mu=(-115*(m+j+1)+24*n)*omega+(j+1), j>=0 with the displayed omega coefficient positive. Accept a unique finite endpoint functional only if Gamma_M(Q,0), Gamma_M(alpha_ab,N_ab), and Gamma_M(-alpha_ab,4-N_ab) are finite and nonzero for every row and the helical labels reproduce the frozen source character. Otherwise report the exact singular rows or label mismatch and leave the endpoint gate open.",
      "rationale": "A named continuation is insufficient unless every requested characteristic is evaluable without a post-result finite part."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A positive result proves only a unique source-derived analytic-frequency linear functional on T_6 and finite nonzero values for its 36 fixed basis characters. It is not the raw Lebesgue contour integral, a general Fourier-hyperfunction theorem, an AFK amplitude match, a helical alias sum, a ray map, fusion continuity, Stark algebraicity, or TCC. The capital-Gamma_M transform value and the separate AFK phase may not be conflated.",
      "rationale": "The block closes one endpoint-definition gate without skipping the amplitude and arithmetic interfaces."
    }
  },
  "resource_caps": {
    "characteristic_rows": {"kind":"integer","value":36,"rationale":"The full frozen characteristic grid."},
    "discrete_kernel_labels": {"kind":"integer","value":24,"rationale":"The complete source Z/24Z transform, not a selected mode."},
    "gamma_factors_per_value": {"kind":"integer","value":3,"rationale":"The two frequency factors and fixed Gamma_M(Q,0)."},
    "continuation_rules": {"kind":"integer","value":1,"rationale":"Only continuation inherited from source equation (66)."},
    "numeric_samples": {"kind":"integer","value":0,"rationale":"Divisor avoidance and label matching are exact."},
    "wall_seconds": {"kind":"integer","value":60,"rationale":"Finite exact all-row ledger and deterministic replay."},
    "floating_point": {"kind":"not_applicable","justification":"Numerical samples cannot establish meromorphic uniqueness or divisor avoidance.","rationale":"All acceptance conditions are symbolic."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov arXiv:1910.11747v4 equation (66) and true Gamma_M divisors",
    "the frozen d=6 beta-kernel specialization and continuous-discrete Fourier character",
    "the all-36 centered helical characteristic lift",
    "uniqueness of meromorphic continuation on a connected domain"
  ],
  "selection_rule": [
    "Enumerate all 36 characteristics and derive sigma, z, N, and alpha without row selection or fitted shifts.",
    "Verify the source discrete character modulo 24 and the centered continuous character exactly for every row.",
    "Audit both frequency Gamma_M factors and the fixed Gamma_M(Q,0) against the published true divisors.",
    "Call the functional unique only through agreement with equation (66) on its source convergence chamber and meromorphic continuation on the same connected domain.",
    "Accept the endpoint rule only if all 36 prescribed values are finite and nonzero without a new finite-part choice."
  ],
  "failure_rule": [
    "Any divisor hit, source-character mismatch, disconnected continuation domain, or need for an added entire/distributional term leaves this endpoint gate open and is reported row by row.",
    "A positive analytic-frequency functional does not prove equality with the AFK characteristic values, preservation by helical periodization, a coefficient-to-ray map, fusion continuity, Stark algebraicity, or TCC.",
    "Do not fit a counterterm, choose a hyperfunction representative after inspecting the rows, discard capital Gamma_M normalization, absorb the AFK phase, use selected exponents, SIC s or d variables beyond the frozen characteristic formula, or use ray labels."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T03:23:50Z",
    "git_head": "128da66a927a7889185d8d937aa4cd4cc8dd0b22",
    "git_state": "DIRTY only from the concurrent repository-wide PROGRAM migration and unrelated projects/tools, plus the user-directed removal of the redundant PROGRAM budget counter. This block freezes only the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-197-b034-gaussian-abel-tail-v1.json",
    "artifacts/cycle-189-regularized-jacobi-lens-interface-v1.json",
    "scripts/dimension_six_beta_fourier.py",
    "scripts/dimension_six_beta_kernel_match.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "docs/sic-stark-cycle146.md",
    "../../tools/preregistration_check.py"
  ]
}
-->
