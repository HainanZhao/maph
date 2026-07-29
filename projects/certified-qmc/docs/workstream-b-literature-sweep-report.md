# Workstream B primary-literature sweep report

## Result

The frozen six-paper perimeter contains numerical figures of merit, but
none is attached to the frozen UNSW `lattice-29102` or
`lattice-39102` vectors.

The classification count is therefore zero:

- papers inspected: 6;
- papers printing numerical merits or FOMs: 4;
- papers attaching such a value to a frozen vector: 0;
- exact-minus-published subtractions: 0.

Together with the Cycle 011 site survey, this closes the classification
branch for the frozen perimeter.  A new paper or table cannot enter
silently; it requires a new prospective perimeter amendment.

## Paper dispositions

### Kuo–Joe 2002

The paper's construction has numerical experiments, including
composite moduli and \(\gamma_j=j^{-2}\).  The author thesis version
containing the corresponding construction and numerical chapters uses
test moduli near \(10^3\), \(2\cdot10^3\), and products of distinct
primes.  It does not identify the later public `lattice-29102` family or
the standard \(2^{10},\ldots,2^{20}\) ladder.

Disposition: `CONTEXT_ONLY`.

### Kuo 2003

The journal article establishes optimal convergence rates.  The
corresponding thesis chapter and numerical rate experiments use prime
moduli, not the frozen powers-of-two public vectors.

Disposition: `THEORY_ONLY_FOR_THIS_SWEEP`.

### Nuyens–Cools 2006

Tables 2–4 print worst-case errors for independent 100-dimensional
fast-CBC experiments at prime and selected composite moduli.  The paper
explicitly discusses double versus long-double differences, but none of
those rows identifies a frozen public vector from the UNSW
powers-of-two family.

Disposition: `CONTEXT_ONLY`; potentially useful model-class evidence,
not a Workstream B classification target.

### LatticeBuilder 2016 and LatNet Builder 2022

Both papers print numerical experimental results.  Their values belong
to lattices, polynomial lattices, Sobol points, or digital nets
generated within the stated examples.  Neither paper identifies a value
with the frozen UNSW vector.

Disposition: `CONTEXT_ONLY`.

### Dick–Kuo–Sloan 2013

The survey develops the relevant merit formulas and points readers to
the UNSW generating-vector repository.  It does not supply a numerical
merit table for `lattice-29102` or `lattice-39102`.

Disposition: `REPOSITORY_LINK_WITHOUT_MERIT_TABLE`.

## Formal fork

For the frozen web-plus-literature perimeter,
\(B_{\rm alg}(\mathcal M)\), the three-way external classification, and
the unfinished composition of \(T_{\rm eval}(\mathcal M)\) no longer
sit on the Workstream B critical path.  The exact formatting component,
reference radix-two proof, and sensitivity variants remain banked.
Completing the full model-class envelope is optional appendix work
unless a new merit-bearing target is prospectively frozen.

Workstream B is now a supply workstream:

> publish the missing figures of merit for the distributed generating
> vectors, with exact or enclosed values and independently replayable
> certificates.

This is not a universal claim about every QMC publication.  It is a
complete negative result only over the explicitly frozen distribution
sites and six-paper primary-literature perimeter.
