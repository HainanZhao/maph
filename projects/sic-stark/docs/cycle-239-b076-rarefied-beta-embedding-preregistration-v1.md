# Cycle 239 / B076 preregistration: rarefied beta embedding

Cycle 238 excludes only the one-kernel Faddeev Fourier transform.  This cycle
tests one genuinely multi-kernel source theorem: Sarkissian--Spiridonov,
*General modular quantum dilogarithm and beta integrals*, arXiv:1910.11747v4,
the rarefied hyperbolic beta theorem (their equation (42), labelled
`integral`).  It asks whether either exact C228 residual word can be an
instance of that theorem's kernel, without adding factors or identifying
different source period systems.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":239,
  "parameters":{
    "source_identity":{"kind":"expression","value":"Freeze S--S arXiv:1910.11747v4, theorem/equation (42): for one fixed normalized rarefied gamma Gamma_M(mu,m;omega1,omega2), the sum over m in Z_k+nu and contour integral of product_{j=1}^6 Gamma_M(a_j plus/minus mu,n_j plus/minus m) divided by Gamma_M(plus/minus 2mu,plus/minus 2m), with sum a_j=omega1+omega2 and sum n_j=r-1, equals product_{ell<j} Gamma_M(a_ell+a_j,n_ell+n_j).","rationale":"This is the single cited multi-kernel beta/star-triangle identity; it fixes one M, one ordered period pair, twelve numerator factors organized into six plus/minus pairs, a denominator, balancing, and an integral/sum output."},
    "frozen_residuals":{"kind":"expression","value":"Freeze exactly the A and C four-factor ordered ordinary-gamma blocks of C228, including every argument coefficient and ordered period pair. The C228 block may be rewritten only using a displayed S--S equation-(17) identity, retaining every resulting Gamma_M factor, period system, and affine argument. No factor may be inserted, deleted, commuted, normalized away, or supplied by an uncited composition theorem.","rationale":"The question is embedding the extant residual word, not completing a larger kernel by design."},
    "necessary_embedding_conditions":{"kind":"expression","value":"For either block to embed, derive from the frozen source formula a common normalized Gamma_M lens datum (M;omega1,omega2), one common integration coordinate, six exact plus/minus argument pairs, an exact realization of the Gamma_M(plus/minus 2mu,plus/minus 2m) denominator, a balancing assignment, and a contour/domain compatible with the theorem. Failure of any condition contains this identity as a direct residual-word engine; it does not rule out a different multi-kernel theorem or a new composition theorem.","rationale":"Each item is explicit in the cited theorem and must be checked before its evaluation can be invoked."},
    "acceptance_boundary":{"kind":"expression","value":"Advance only if one complete source-authorized assignment satisfies every necessary condition and maps the theorem's displayed output to the required reversed word with all bases, arguments, discrete labels, and multipliers retained. Otherwise seal a scoped no-embedding result for this theorem only. Do not assert an AFK, fusion, Stark, or TCC consequence.","rationale":"A formal resemblance or a partial two-factor match is not an application of the beta integral."}
  },
  "resource_caps":{
    "residual_blocks":{"kind":"integer","value":2,"rationale":"The frozen A and C C228 blocks only."},
    "factors_per_block":{"kind":"integer","value":4,"rationale":"Every factor remains in scope."},
    "source_identity_count":{"kind":"integer","value":1,"rationale":"One concrete source theorem, equation (42), is tested."},
    "identity_kernel_numerator_factors":{"kind":"integer","value":12,"rationale":"Six displayed plus/minus pairs in the frozen beta kernel."},
    "floating_point":{"kind":"not_applicable","justification":"Period bases, slopes, pairing arity, and balancing equations are exact symbolic data.","rationale":"Numerics cannot establish a source-identity embedding."},
    "wall_seconds":{"kind":"integer","value":300,"rationale":"Exact factor/base/pairing census and theorem-hypothesis audit."}
  },
  "formula_families":[
    "Sarkissian--Spiridonov arXiv:1910.11747v4 equations (17), (42), and the stated balancing/contour hypotheses",
    "Cycle-228 exact A/C ordinary-gamma residual blocks",
    "Exact period-system, affine-argument, and plus/minus-pair matching"
  ],
  "selection_rule":[
    "First transcribe the beta theorem's fixed-M, fixed-period, paired-kernel, denominator, balancing, and contour data.",
    "Then derive any C228-to-Gamma_M grouping solely from the cited equation (17), retaining its target lens data.",
    "Test all required conditions for both A and C before drawing the scoped conclusion."
  ],
  "failure_rule":[
    "Do not complete the beta kernel by adding complementary Gamma_M factors, choose a balancing relation after inspection, identify merely proportional or modularly related bases without a cited source theorem, or cancel a missing partner by a fitted scalar.",
    "Do not replace the cited identity by a composition, degeneration, or star-triangle form absent from the frozen source statement.",
    "Do not claim a general multi-kernel no-go, a signed extension, AFK covariance, fusion, Stark, or TCC."
  ],
  "pre_execution":{"timestamp_utc":"2026-08-03T08:35:00Z","git_head":"6a0ad5b11604c6c7561dd5391f0b0ade2f63a854","git_state":"Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":[
    "artifacts/cycle-228-b065-f3-square-residual-block-v1.json",
    "proof/verify_cycle_228_f3_square_residual_block.py",
    "artifacts/cycle-238-b075-faddeev-fourier-dualization-v1.json",
    "proof/verify_cycle_238_faddeev_fourier_dualization.py",
    "../../tools/preregistration_check.py"
  ]
}
-->

Claim boundary: a failed audit would establish only that this displayed,
common-period rarefied beta integral does not directly embed either frozen
residual word.  Other multi-kernel identities, an actually cited composition,
and every downstream dimension-six claim remain open.
