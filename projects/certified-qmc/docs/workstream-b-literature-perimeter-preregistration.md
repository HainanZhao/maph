# Workstream B primary-literature perimeter

Frozen: 2026-07-29T06:29:00Z

## Purpose

The public distribution sites inspected in Cycle 011 contain vectors,
not numerical merit columns.  Before declaring that classification has
lost its object, this bounded sweep checks the primary papers most
likely to print worst-case errors or figures of merit associated with
the frozen UNSW vector family.

Bibliographic metadata was resolved before this freeze.  No paper body
had been inspected for numerical merit values, no such value had been
acquired, and no exact-minus-published subtraction had occurred.

## Frozen papers

1. F. Y. Kuo and S. Joe, “Component-by-component construction of good
   lattice rules with a composite number of points,” *Journal of
   Complexity* 18 (2002), 943–976,
   DOI `10.1006/jcom.2002.0650`.
2. F. Y. Kuo, “Component-by-component constructions achieve the
   optimal rate of convergence for multivariate integration in
   weighted Korobov and Sobolev spaces,” *Journal of Complexity* 19
   (2003), 301–320, DOI `10.1016/S0885-064X(03)00006-2`.
3. D. Nuyens and R. Cools, “Fast algorithms for
   component-by-component construction of rank-1 lattice rules in
   shift-invariant reproducing kernel Hilbert spaces,” *Mathematics of
   Computation* 75 (2006), 903–920,
   DOI `10.1090/S0025-5718-06-01785-6`.
4. P. L'Ecuyer and D. Munger, “LatticeBuilder: A General Software Tool
   for Constructing Rank-1 Lattice Rules,” *ACM Transactions on
   Mathematical Software* 42 (2016), Article 15,
   DOI `10.1145/2754929`.
5. P. L'Ecuyer, P. Marion, M. Godin, and F. Puchhammer, “A Tool for
   Custom Construction of QMC and RQMC Point Sets,” *Monte Carlo and
   Quasi-Monte Carlo Methods 2020* (2022), 51–70,
   DOI `10.1007/978-3-030-98319-2_3`.
6. J. Dick, F. Y. Kuo, and I. H. Sloan, “High-dimensional
   integration: The quasi-Monte Carlo way,” *Acta Numerica* 22 (2013),
   133–288, DOI `10.1017/S0962492913000044`.

The machine-readable freeze is
`data/workstream-b-literature-perimeter.json`.

## Admission rule

Classification revives only when a paper prints a numerical merit or
worst-case-error value tied unambiguously to a frozen public vector and
the modulus, dimension, weights, kernel normalization, and displayed
precision are recoverable.

Theoretical rate bounds, application errors, timings, and merits for
unrelated example-generated vectors do not qualify.

## Gate

The inspection records only presence, attachment, normalization
recoverability, and lexical precision.  External subtraction remains
forbidden.  A qualifying value requires a source-specific
\(T_{\rm format}\), complete \(T_{\rm eval}(\mathcal M)\), sensitivity
freeze, and prospective authorization before it is compared.

The perimeter closes after these six papers.  Expansion requires a new
timestamped amendment.
