# Cycle 249 / B086 preregistration: common chamber for positive-`F3` jets

Cycle 248's live formal calculation made the necessary coordinate pullback
explicit but did not freeze a convergent ordinary-gamma product chamber. This
block tests that missing analytic prerequisite only. It does not promote the
unsealed C248 calculation or assert a cross-sign law.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 249,
  "parameters": {
    "regularization": {
      "kind": "expression",
      "value": "Freeze K=Q(sqrt(21)), t_+=55+12*sqrt(21), t_-=55-12*sqrt(21), and at both real embeddings w_sigma=t_sigma+i. For every C228 A/C period coefficient pair alpha=a1*w_sigma+a2 and beta=b1*w_sigma+b2, freeze the ordinary-gamma product bases q=exp(2*pi*i*alpha/beta) and qtilde=exp(-2*pi*i*beta/alpha). No limit epsilon->0, other tilt, branch, or meromorphic continuation is allowed.",
      "rationale": "A fixed common upper tilt gives a concrete source-product domain rather than the unit-circle endpoint excluded by the C248 review."
    },
    "retained_factors": {
      "kind": "expression",
      "value": "Freeze all eight C228 ordinary-gamma factors: four ordered A factors and four ordered C factors, with their exact argument slopes and period pairs. Test each factor at both embeddings; no factor may be omitted because the jet representation requires every ordered edge factor.",
      "rationale": "The desired chamber must work simultaneously for both positive F3 paths and both embeddings."
    },
    "criterion": {
      "kind": "expression",
      "value": "Accept the common chamber only if every exact determinant det(alpha,beta)=a1*b2-a2*b1 is positive and the identity Im(alpha/beta)=det(alpha,beta)/|beta|^2 proves |q|<1, while Im(beta/alpha)<0 proves |qtilde|<1, at each embedding. Then derive from the pinned q-product that G(mu)=mu*gamma(c*mu;alpha,beta) is holomorphic with nonzero leading coefficient and has absolutely convergent degree-0:3 Lambert-series coefficients. Falsify on the first failed determinant, base inequality, or leading-coefficient condition.",
      "rationale": "This is exactly the analytic hypothesis missing from C248's formal jet display."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A passing result supplies only a fixed-tilt common q-product chamber and factorwise analytic jets for the C228 A/C residuals. It does not validate C248's path representation beyond its stated coordinate bookkeeping, take a real-endpoint limit, derive a negative-k or cross-sign law, or imply a packet map, current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "The chamber is a prerequisite, not the missing interface."
    }
  },
  "resource_caps": {
    "residual_blocks": {"kind": "integer", "value": 2, "rationale": "C228 A and C only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "All retained factors."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both real embeddings are required."},
    "tilts": {"kind": "integer", "value": 1, "rationale": "w_sigma=t_sigma+i only."},
    "jet_degrees": {"kind": "integer", "value": 4, "rationale": "Degrees zero through three only."},
    "floating_point": {"kind": "not_applicable", "justification": "Determinants and chamber inequalities are exact; no endpoint sampling may replace them.", "rationale": "Numerical product evaluation cannot establish the common domain."},
    "wall_seconds": {"kind": "integer", "value": 180, "rationale": "Exact eight-factor, two-embedding chamber audit."}
  },
  "formula_families": ["C228 A/C ordered ordinary-gamma factors", "ordinary hyperbolic-gamma q-product", "exact quadratic-field embeddings", "Lambert-series derivative expansion"],
  "selection_rule": ["Compute every determinant from its frozen coefficient pair before any q-product statement.", "Use only w_sigma=t_sigma+i and both embeddings.", "If all base inequalities pass, derive only the degree-0:3 factorwise analytic jet formulas; leave every path composition and cross-sign conclusion out of this block."],
  "failure_rule": ["Do not change tilt, omit a factor or embedding, use a numerical q estimate, select a radial limit, invoke a meromorphic continuation, or infer an endpoint value after a failed chamber inequality.", "Do not claim a C248 representation seal, a negative-k/cross-sign law, source authorization beyond the frozen products, a canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:14:07Z", "git_head": "33c77fcd43d3232a4826b173123990ddcee6fc14", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "proof/verify_cycle_245_a_principal_coefficients.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a fixed-tilt analytic-domain certificate, not a
cross-sign or endpoint theorem.
