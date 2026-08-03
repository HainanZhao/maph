# Cycle 248 / B085 preregistration: filtered positive-`F3` jet representation

This block tests a source-defined finite-rank representation of the positive
`F3` path fragment.  It does not assert a signed-`k` continuation.  Its point
is to retain the pole-order filtration that makes individual residual edges
well-defined, rather than centralizing an entire residual word.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 248,
  "parameters": {
    "source_states_and_edges": {
      "kind": "expression",
      "value": "Freeze m=0 and the two source-defined positive F3 edges A->C and C->A of Cycle 226, including their exact period bases, affine arguments, label 0, and two ordered ordinary-gamma residual factors per edge. Freeze only the length-0, length-1, and length-2 alternating positive paths A, A-F3, A-F3-F3 and C, C-F3, C-F3-F3. No negative-k arrow, new path, or relabeling is admitted.",
      "rationale": "These are the smallest partial paths on which a pole-order-filtered edge action can be defined from the cited source products."
    },
    "filtered_jet_state": {
      "kind": "expression",
      "value": "For a frozen partial path u with ordered residual product R_u(mu) and p(u)=2*length(u), freeze J_u=mu^(p(u))*R_u(mu) modulo mu^4, represented in the ordered basis (1,mu,mu^2,mu^3). For an appended source-defined F3 edge e with two-factor residual H_e(mu), freeze its candidate map J_u->J_(u e) as multiplication by h_e(mu)=mu^2*H_e(mu) modulo mu^4. The four jet coefficients and all factor order are state, not scalars to be discarded.",
      "rationale": "C229's pole audit implies that an unnormalized single edge changes pole order; normalization by the exact edge order is the minimal stable filtration."
    },
    "transport_and_intertwining": {
      "kind": "expression",
      "value": "Freeze C227's positive F3^2 return data: ordered periods are 576 times the starting ordered pair, affine argument is 576*mu at m=0, and label remains 0. On the jet basis freeze D_576(f)(mu)=f(576*mu), with weights (1,576,576^2,576^3). Derive, rather than posit, every edge multiplication matrix and each ordered two-edge composite. Test the exact source-state comparison and the semidirect relation D_576 M_h D_576^(-1)=M_(h(576*mu)) modulo mu^4. An A/C intertwiner exists only if the two source-defined edge maps and their composites satisfy these frozen state and weight rules with no factor reordering or scalarization.",
      "rationale": "This is a noncentral representation test: dilation acts on each residual-jet multiplier, unlike C235's commuting monomial extension."
    },
    "acceptance": {
      "kind": "expression",
      "value": "Accept only a PROVED filtered positive-F3 jet representation if every normalized one-edge multiplier is regular at mu=0 with nonzero leading coefficient; its 4-by-4 lower-triangular Toeplitz matrix is derived from the frozen source product; ordered composition equals multiplication of the corresponding truncated source jets; and both length-two paths match the frozen 576 period/argument/label transport and semidirect dilation rule. Otherwise record the first exact failure and do not introduce a replacement jet, a gauge, a sign law, or a different path.",
      "rationale": "The construction is useful only if it is a genuine source-derived finite-rank action, not a renamed residual word."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A passing result constructs only the filtered positive-F3 jet representation of the specified source path fragment. It does not derive a negative-k or cross-sign Gamma_M law unless that follows from a later separately preregistered source identity; it does not define a packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "The missing cross-sign interface is not promoted merely by retaining its positive-path jet data."
    }
  },
  "resource_caps": {
    "starts": {"kind": "integer", "value": 2, "rationale": "A and C only."},
    "partial_paths_per_start": {"kind": "integer", "value": 3, "rationale": "Lengths 0, 1, and 2 only."},
    "positive_edges": {"kind": "integer", "value": 2, "rationale": "A->C and C->A only."},
    "ordinary_gamma_factors_per_edge": {"kind": "integer", "value": 2, "rationale": "Retain both source residual factors."},
    "jet_rank": {"kind": "integer", "value": 4, "rationale": "Truncation modulo mu^4."},
    "matrix_entries_per_edge": {"kind": "integer", "value": 16, "rationale": "One 4-by-4 multiplication matrix for each edge."},
    "dilation_weights": {"kind": "integer", "value": 4, "rationale": "Degrees 0 through 3."},
    "floating_point": {"kind": "not_applicable", "justification": "Regularity, Laurent coefficients, matrices, and transport are exact symbolic statements.", "rationale": "Numerical gamma values cannot establish a source representation."},
    "wall_seconds": {"kind": "integer", "value": 300, "rationale": "Exact two-edge filtered-jet audit."}
  },
  "formula_families": ["Sarkissian--Spiridonov equation (17) positive-F3 residual products", "ordinary hyperbolic-gamma product/Laurent expansion at zero", "Cycle-226 exact augmented F3 state", "Cycle-227 576-scale normal form", "truncated regular-jet multiplication"],
  "selection_rule": ["Derive the pole order and normalized edge jet from each complete two-factor source residual before multiplying paths.", "Keep A/C order, period bases, affine argument, label, and all four factors through every composition.", "Use exactly the stipulated degree-3 truncation and D_576 action; record the first mismatch as the outcome."],
  "failure_rule": ["Do not treat an unnormalized pole-producing edge as an endomorphism, commute residual factors, discard a nonconstant jet coefficient, choose a gauge, extend to a negative-k edge, invoke reflection, change path length, or change the truncation after inspection.", "Do not infer a cross-sign law, packet cocycle, canonical current, source authorization beyond the frozen positive edges, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:03:28Z", "git_head": "33c77fcd43d3232a4826b173123990ddcee6fc14", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "proof/verify_cycle_226_signed_product_groupoid.py", "artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json", "proof/verify_cycle_227_augmented_transport_normal_forms.py", "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-229-b066-f3-square-divisor-v1.json", "proof/verify_cycle_229_f3_square_divisor.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a finite, positive-source-path representation test; a
passing result is not a cross-sign continuation.
