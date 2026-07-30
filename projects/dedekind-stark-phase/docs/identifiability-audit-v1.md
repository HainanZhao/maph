# Identifiability audit

Frozen: 2026-07-30 UTC.

## Question

Can the five certified Engine-C packets be used as independent response
values when fitting a formula for

\[
\delta(\chi)=\arg L'(0,\chi)-\arg c(\eta)\pmod{\pi/2},
\]

where \(c(\eta)\) is the coefficient attached to a canonical weak Stark
solution?

## Verdict

**No, not with the comparison objects presently in the archive.**

The Engine-C computation starts with the same complex \(L'(0,\psi)\)
that supplies the proposed left-hand phase. It Fourier-inverts those
values, isolates a unit vector in a CM unit lattice, and proves an exact
bridge from its positive norms to the original one-place packet. This
is a valid proof of the packet identity. It is not an independent
construction of a coefficient \(c(\eta)\) against which the phase of
that same \(L'\)-value may be fitted.

Consequently:

- the ten route records are legitimate convention and route-invariance
  controls;
- their raw \(L'\)-phases are legitimate negative controls for the
  overly strong claim that the phase itself is quarter-turn quantized;
- setting \(c(\eta)\) equal to a coefficient reconstructed from those
  same \(L'\)-values would force the desired defect by construction;
- any Dedekind-sum fit performed before an independent \(c(\eta)\)
  exists would therefore be circular.

## Why the second CM route does not cure the problem

Each case has two theorem-independent CM descent routes. Their exact
agreement is strong evidence that the Fourier, character, and Artin
conventions are coherent. But both routes still consume the common
original \(L'\)-data. Independence of theorem base is not statistical
independence of the proposed response variable.

## Scope mismatch with Roblot's construction

The descent fields in these Engine-C proofs are imaginary quadratic.
Roblot's index-formula construction is formulated for a totally real
base and explicitly excludes the complex-quadratic-base case. The
relevant next object must instead be built on the original cyclic
quartic extension over the real quadratic field. Its hypotheses must
be checked there; quartic CM descent on another base does not imply
them.

## Recovery gate

For each of the five controls:

1. reconstruct the original cyclic-quartic subextension over the real
   quadratic base;
2. check Roblot's hypotheses (A1)--(A3) directly;
3. construct the index-formula weak solution without reading the
   certified packet, the Engine-C unit, or the analytic \(L'\)-value;
4. freeze its generator and orientation conventions;
5. only then open the analytic value and form the defect.

The admissible Dedekind--Rademacher feature family and the fifty-row
holdout remain blocked until at least one such independently
constructed defect exists.

