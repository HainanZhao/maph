# SIC--Stark research cycle 94: rational Artin induction cannot orient

Date: 2026-07-28

## Challenged shortcut

The faithful ray character has order six, and
\(\zeta_6+\zeta_6^{-1}=1\).  This suggests trying Stark's proved theorem
for rational Artin characters after induction or rationalization.

The shortcut fails for a precise representation-theoretic reason.

Let \(G=C_6=\langle g\rangle\), and write
\(\chi_k(g)=\zeta_6^k\).  The rational irreducible character packets are

\[
 \chi_0,\qquad
 \chi_3,\qquad
 \chi_1+\chi_5,\qquad
 \chi_2+\chi_4.
\]

Every one is fixed by inversion \(g\mapsto g^{-1}\).  Their rational
span therefore contains the primitive even packet

\[
 \chi_1+\chi_5
\]

but not the primitive odd packet

\[
 \chi_1-\chi_5.
\]

The first determines the conjugation-invariant modulus information.  The
second is exactly the orientation needed to distinguish the certified
Artin order from its reversal.

## Exact certificate

The script

```text
scripts/dimension_six_rational_induction_gate.py
```

performs exact linear algebra over \(\mathbf Q\).  It verifies

```text
RATIONAL_CHARACTER_BASIS_RANK=4
PRIMITIVE_EVEN_PACKET_IN_RATIONAL_SPAN=1
PRIMITIVE_ODD_PACKET_IN_RATIONAL_SPAN=0
RATIONAL_ARTIN_INDUCTION_CAN_ORIENT_CHI_1=0
```

Equivalently, the functional

\[
 f\longmapsto f(g)-f(g^{-1})
\]

annihilates every rational-valued character but not
\(\chi_1-\chi_5\).

## Consequence

Stark's rational-character theorem explains why the already-certified
absolute value is unconditional.  It cannot prove

\[
 L'_S(0,\chi_1)
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2
\]

because the imaginary, inversion-odd component of this equality is
invisible to rational Artin induction.

This excludes every proposed proof that uses only permutation
characters, rational zeta quotients, and rational regulator relations.

