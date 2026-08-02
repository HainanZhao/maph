# Cycle 175 preregistration: affine eligibility grid or discrepancy bank

## Question and boundary

Starting from a massed Cycle-166 canonical affine parent fibre, pull back the
*entire* parameter set through Cycle-167 eligibility and Cycle-174 capacity
classification. The permitted result is a breadth–depth transport grid or a
fully labelled range/residue/capacity-discrepancy bank. No target-local packet,
actual population lower bound, recurrence, density, or interval claim is
preregistered.

## Frozen full-fibre ledger

For the retained finite parameter set `N`, set `h(n)=h0+r n`, and freeze
the source/target range intersection

```text
M={n in N: H<=h(n)<=2H and H<=q h(n)/a<=2H}.
```

Let `g0=gcd(a,r)`. If `g0` fails to divide `h0`, retain the complete parent
fibre as a residue obstruction. Otherwise freeze the unique class

```text
n=n0 (mod m),       m=a/g0,
N_elig={n in M:n=n0 (mod m)}.                        (1)
```

Retain the exact breadth `b=|N_elig|`, capacity ratio `qK/H`, and its unique
Cycle-174 dyadic class. Define the signed modular discrepancy

```text
Disc=n_elig-|M|/m.                                   (2)
```

No density assumption on `N` is allowed.

## Gates

1. Prove (1) including zero slope, both range cuts, and every complete row
   label. Prove every eligible row gives the exact C167 edge and inherits one
   common Cycle-174 capacity class.
2. Prove the exact grid ledger: `b` distinct beta-preserving transport edges,
   each with the same depth/capacity state, and fixed bounded slack only in
   the saturated class.
3. If `b` is below a preregistered breadth threshold, retain either the
   insoluble residue condition, an explicitly small range intersection `M`,
   or the signed modular discrepancy (2); do not call this a population
   bound or drop the parent fibre.
4. Construct a finite high-parent fibre avoiding its unique eligible residue
   class, proving parent multiplicity alone cannot force breadth.

## Falsifier and advance condition

The falsifier is a parameter row omitted from all range/residue/capacity
classes, a claimed common capacity class with varying `qK/H`, or a
parent-multiplicity-to-breadth implication without an explicit discrepancy
hypothesis. Advance only with an exact grid/discrepancy classifier.
