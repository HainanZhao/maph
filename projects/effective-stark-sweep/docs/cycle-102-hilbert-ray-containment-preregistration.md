# Cycle 102 — first Hilbert/ray containment control

The first exact Cohen--Roblot comparison target is the v5 Engine-B
normal closure B5-079, with canonical member RQ-001262 over
(mathbb Q(sqrt{35})).  Cohen--Roblot's class-number-two entry gives
the Hilbert field

\[
 H = \mathbb Q(\sqrt{35},\sqrt5)=\mathbb Q(\sqrt5,\sqrt7),
\]

represented by the polynomial (x^4-24x^2+4).  The frozen question is
whether this field is an exact subfield of the B5-079 normal closure
defined by its v5 normal-closure polynomial.

The route uses PARI's exact number-field inclusion test and records an
explicit embedding when inclusion holds.  A negative result means only
that this ray normal closure does not contain this Hilbert field.  It
does not compare Stark units or settle the remaining three bases.
