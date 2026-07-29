# Phase-0 literature and state-of-practice audit

Date: 2026-07-29

Status: primary-source review plus frozen source snapshots; not
exhaustive. The broad universal novelty claim remains `OPEN`.

## Primary mathematical source

Dick, Kuo, and Sloan, *High-dimensional integration: the
quasi-Monte Carlo way*, Acta Numerica 2013:

- Theorem 3.5 gives the generic RKHS squared worst-case-error formula.
- Theorem 5.3 relates shift-averaged error to a shift-invariant kernel.
- Lemma 5.5, equation (5.13), gives the product-weight rank-1 lattice
  formula used here.
- Algorithm 5.6 states exact CBC as sequential minimization over unit
  components.

Source:
<https://web.maths.unsw.edu.au/~josefdick/preprints/DKS2013_Acta_Num_Version.pdf>

## Fast CBC

Nuyens and Cools' fast CBC work gives \(O(dN\log N)\)-type construction
for structured shift-invariant spaces, replacing the original
quadratic candidate evaluation. The composite-\(N\) group structure
must be treated explicitly; it is not interchangeable with the
prime-\(N\) cyclic case.

Sources:

- <https://doi.org/10.1090/S0025-5718-06-01785-6>
- <https://doi.org/10.1016/j.jco.2005.07.002>

The project's CRT three-representation architecture is not yet
validated against those algorithms. In particular, a residue layout
that makes pointwise updates cheap does not automatically preserve the
fast convolution layout.

## Public vector tables

Frances Kuo's UNSW page publishes fixed and extensible lattice
generating vectors and identifies four recommended extensible rules.
The page states that the vectors were constructed by CBC minimization
of shift-averaged worst-case errors in weighted unanchored Sobolev
spaces. It also records the weight models.

Source: <https://web.maths.unsw.edu.au/~fkuo/lattice/index.html>

Phase 0 freezes one fixed \(N=1024\), \(\gamma_j=1/j^2\) file because
its convention is legible and a complete exact prefix audit is cheap.
The stronger proposal phrase “tables actually in production use” is
not yet evidenced. Public recommendation and practical use are
different claims.

## Current construction software

LatNet Builder constructs rank-1 lattices and digital nets and supports
multiple figures of merit, weights, and search methods.

Source: <https://umontreal-simul.github.io/latnetbuilder/>

Cycle 001 inspected LatNet Builder commit
`39dd60fceb0c86a6124b701072d91f8e3aed73df` and QMCPy commit
`a774f3a1297b982f2544742e8c691e035c9fc0a7`. In the former, the lattice
merit type is `double`, Bernoulli kernels use binary64 constants, the
fast inner product uses double-precision FFTW, and the argmin is an
ordinary `<` branch. QMCPy preserves integer generating vectors but did
not expose an exact/interval merit or certified CBC path. Its LatNet
Builder linker was marked under reconstruction.

Sources:

- <https://github.com/umontreal-simul/latnetbuilder>
- <https://github.com/QMCSoftware/QMCSoftware>

This supports only the snapshot-scoped statement that no arithmetic
certification path was found in those audited revisions. It does not
establish that every current tool or published table uses unverified
binary64 arithmetic.

## Application boundary

Preintegration can smooth kinks or jumps under explicit monotonicity
and regularity conditions, and has been demonstrated for a digital
Asian option. Later work shows that smoothing generally fails when the
needed monotonicity fails.

Sources:

- <https://arxiv.org/abs/1712.00920>
- <https://arxiv.org/abs/2112.11621>
- <https://arxiv.org/abs/2212.11493>

This supports the proposal's conservative pilot boundary: certifying a
rule merit is only one factor in an RKHS error inequality. The
integrand norm and the validity/error of preprocessing remain separate
obligations.

## Remaining novelty questions

1. Do other maintained QMC packages expose reproducible high-precision
   or interval-certified merit evaluation?
2. Are any public vector tables shipped with exact error values,
   interval enclosures, or replayable certificates?
3. Does published “rigorous upper bound” software certify arithmetic
   rounding, or only the analytic inequality?
4. Which table formats record enough normalization metadata for a
   meaningful independent audit?
5. Has exact/CRT CBC branch certification already been attempted under
   another name?
