# C108 frozen-seed preflight: no executable input

**`OBSERVED` source/preflight containment, 2026-08-06 UTC.**  C108's selected
four-vertex-border equation requires a frozen, independently valid order-278
Seidel matrix \(S_{70}\).  No such input is present in the repository or
identified by the checked primary route.

## Evidence

1. The sealed C101 record establishes a complete no-hit for the *public
   n=70 six-block placement* across all \(2^{19}\) signed completions at
   \(q=7\).  That record therefore cannot supply a valid normalized
   \(278\times278\) Seidel seed.
2. Wesley, *Lower Bounds for Book Ramsey Numbers*, arXiv:2410.03625, Theorem
   2, gives its infinite 2-block construction only when
   \(2n-1\equiv1\pmod4\) is a prime power.  At \(n=70\),
   \(2n-1=139\equiv3\pmod4\), so the stated theorem does not provide the
   required seed.  The source describes the same asymmetric
   \(R(B_{n-1},B_n)\) target, but its stated prime-power hypothesis fails at
   \(n=70\), so it furnishes no seed for this border.

Primary source: <https://arxiv.org/html/2410.03625v1#Thm2>.

## Consequence

`CONJECTURED` C108's border equations remain a reusable design *conditional
on a supplied valid seed*, but no executable C108 cycle is opened, no budget
ordinal is consumed, and no SAT/UNSAT claim is made.  A valid seed must be
provided or independently source-verified before this design may be selected
again.  Do not reconstruct a seed from C101's rejected sign family or replace
the missing input with a free graph search.
