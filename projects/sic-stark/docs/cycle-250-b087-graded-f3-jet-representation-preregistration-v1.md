# Cycle 250 / B087 preregistration: graded positive-`F3` jet representation

C249 supplies the fixed upper chamber missing from C248. This block rebuilds
the proposed positive-path action from the source factors, including the
degree-dependent normalization forced by the intermediate coordinate change.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 250,
  "parameters": {
    "source_paths": {
      "kind": "expression",
      "value": "Freeze m=0, starts A=(-115,24,5,24) and C=(115,24,-5,24), and only the two source-defined paths A-F3-C-F3-A and C-F3-A-F3-C. Derive every one-edge period map, affine coordinate mu_1=24*mu_0, label 0, and ordered two-factor residual from C226; derive the two-edge return (576*omega1,576*omega2;576*mu_0,0) and compare all four pulled factors exactly with C228. No negative-k edge or reordered factor is admitted.",
      "rationale": "These are the minimal source paths isolated by C227 and the complete residual blocks frozen by C228."
    },
    "analytic_factor_jets": {
      "kind": "expression",
      "value": "Freeze C249's two-embedding chamber w_sigma=t_sigma+i. For each factor gamma(c*mu;alpha,beta), derive G(mu)=mu*gamma(c*mu;alpha,beta) modulo mu^4 from the pinned q-product. Write [mu^r]G=c^(r-1)*K_r(alpha,beta), r=0,1,2,3, where K_r is explicitly defined by the nonzero q-Pochhammer leading term and the convergent S1,S2,S3 logarithmic derivatives. Coefficients are source formulas, not independent symbols.",
      "rationale": "The c^(r-1) homogeneity makes the 24-coordinate pullback exact while C249 supplies convergence."
    },
    "graded_transfer": {
      "kind": "expression",
      "value": "For a tail path v of length n with local normalized jet J_v(nu)=nu^(2n)*R_v(nu) mod nu^4, freeze the prepended positive-F3 transfer T_e^(n)=24^(-2n)*M_(h_e)*P_24, where h_e=mu^2*H_e, M is ordered truncated multiplication, and P_24 f(mu)=f(24*mu). Use noncommutative ordered factor words when checking matrices. For each frozen two-edge path test T_first^(1)*T_second^(0)=M_(mu^4*R_full)*P_576 exactly through degree three, including the forced 24^(-2) factor.",
      "rationale": "This is the actual graded semidirect law; omitting the degree normalization or commuting factors would reproduce C248's invalid prototype."
    },
    "acceptance": {
      "kind": "expression",
      "value": "Accept only if both A/C source derivations reproduce all four C228 factors in order, every K_r is tied to its exact q-product formula in C249's chamber, and both 4-by-4 ordered matrix identities hold coefficientwise with the exact 24 and 576 weights. Otherwise record the first exact state, factor, coefficient, or matrix mismatch and do not change rank, tilt, paths, or normalization.",
      "rationale": "A passing result is a source-specific finite-rank representation rather than generic power-series algebra."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A passing result constructs only the fixed-tilt graded representation of the two positive F3 path fragments. It does not take an endpoint limit, produce tilt independence, derive a negative-k or cross-sign Gamma_M law, define a packet map or canonical current, or imply a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "The representation is enlarged positive-path state, not the missing signed interface."
    }
  },
  "resource_caps": {
    "starts": {"kind": "integer", "value": 2, "rationale": "A and C only."},
    "edges_per_path": {"kind": "integer", "value": 2, "rationale": "The positive F3 square only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "Four ordered factors per start."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both C249 embeddings."},
    "jet_rank": {"kind": "integer", "value": 4, "rationale": "Degrees zero through three."},
    "matrix_identities": {"kind": "integer", "value": 2, "rationale": "One ordered identity per start."},
    "floating_point": {"kind": "not_applicable", "justification": "All state, coefficient, and matrix identities are exact in the convergent source formulas.", "rationale": "Numerical gamma values cannot establish functoriality."},
    "wall_seconds": {"kind": "integer", "value": 300, "rationale": "Exact two-path degree-three representation audit."}
  },
  "formula_families": ["Sarkissian--Spiridonov positive-F3 factorization", "C228 A/C residual blocks", "C249 fixed-chamber ordinary-gamma jets", "graded truncated-jet multiplication and affine pullback"],
  "selection_rule": ["Derive the second edge in its local periods and coordinate before pulling it to mu_0.", "Represent coefficient products by ordered words and never sort factor atoms.", "Compare the graded operator matrix with the direct four-factor C228 matrix coefficientwise at both starts."],
  "failure_rule": ["Do not omit the 24^(-2n) normalization, replace a K_r by a free symbol, commute or reorder factors, alter the fixed tilt, add a negative-k edge, or infer an endpoint value.", "Do not claim a cross-sign law, packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:20:37Z", "git_head": "33c77fcd43d3232a4826b173123990ddcee6fc14", "git_state": "Dirty only from concurrent repository-wide workflow changes and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["docs/cycle-248-b085-filtered-f3-jet-representation-preregistration-v1.md", "artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "proof/verify_cycle_226_signed_product_groupoid.py", "artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json", "proof/verify_cycle_227_augmented_transport_normal_forms.py", "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "proof/verify_cycle_249_common_jet_chamber.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a fixed-tilt positive-path representation test, not a
signed or endpoint theorem.
