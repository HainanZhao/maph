# Roblot phase clarification: certified and uncertified branches

Recorded: 2026-07-31 UTC.

## Setup and convention

Let \(K/k\) be cyclic quartic with
\(G=\langle\gamma\rangle\), let \(\tau=\gamma^2\), and choose the
primitive odd character \(\chi\) by \(\chi(\gamma)=i\). Let \(S\)
satisfy Roblot's hypotheses (A1)--(A3), and let
\(\bar\eta\in\bar U_K^-\) be the weak solution supplied by
Roblot's Theorem 6.1. Put

\[
c_\chi(\eta)=\frac12\sum_{g\in G}\chi(g)\log|\eta^g|_w.
\]

For a trivial group-ring unit \(h\), the convention is

\[
c_\chi(h\bar\eta)=\chi(h)c_\chi(\bar\eta).
\tag{1}
\]

Roblot's theorem proves
\(\lvert c_\chi(\eta)\rvert=\lvert L'_{K/k,S}(0,\chi)\rvert\),
uniqueness of \(\bar\eta\) up to a trivial unit, and the abelianity
condition for \(K(\sqrt\eta)/k\).

## Lemma A: certified Stark cases

Assume that the rank-one Stark unit \(\bar\epsilon\) for
\((K/k,S,w)\) has been proved to exist with the convention

\[
L'_{K/k,S}(0,\chi)=c_\chi(\epsilon).
\tag{2}
\]

Then there is a trivial group-ring unit \(h\) such that
\(\bar\eta=h\bar\epsilon\), and

\[
\boxed{\frac{L'_{K/k,S}(0,\chi)}{c_\chi(\eta)}
       =\chi(h)^{-1}\in\mu_4.}
\tag{3}
\]

### Proof

The proved Stark unit satisfies Roblot's index properties (P1) and
(P2). By the uniqueness clause of Roblot's Theorem 6.1, it and
\(\bar\eta\) differ by a trivial unit:
\(\bar\eta=h\bar\epsilon\). Equation (1), followed by (2), gives

\[
c_\chi(\eta)=\chi(h)L'_{K/k,S}(0,\chi).
\]

A trivial unit acts as a signed Galois element; its primitive quartic
character value belongs to \(\mu_4\). Rearrangement proves (3).

Thus phase quantization in a case whose Stark packet is already proved
is a theorem consequence and a convention/label consistency check,
not new evidence for algebraicity.

## Lemma B: uncertified Stark cases

Under the same cyclic-quartic and (A1)--(A3) hypotheses, the following
are equivalent:

1. the rank-one Stark conjecture holds for \((K/k,S,w)\);
2. there exists a trivial unit \(h\) such that
   \[
   L'_{K/k,S}(0,\chi)=c_\chi(h\bar\eta);
   \tag{4}
   \]
3. the phase ratio is quartically quantized:
   \[
   \frac{L'_{K/k,S}(0,\chi)}{c_\chi(\eta)}
   \in\mu_4.
   \tag{5}
   \]

Here (5) is understood with the generator, place, Fourier convention,
and Artin orientation fixed before evaluating either side.

### Proof

The implication \(1\Rightarrow2\) is Lemma A, and
\(2\Rightarrow3\) follows from (1).

For \(3\Rightarrow2\), every element of \(\mu_4\) occurs as
\(\chi(h)\) for a trivial unit \(h\), so choose \(h\) with
\(\chi(h)=L'/c_\chi(\eta)\). Equation (4) follows. Its conjugate gives
the identity for \(\bar\chi\), the only other odd character of \(C_4\).
The even characters have the rank-zero term in this one-place
signature, so Fourier inversion supplies the full rank-one logarithmic
identity. Roblot's weak solution is a global unit under these
hypotheses and already satisfies the abelian square-root condition;
these properties are preserved by a trivial-unit action. Hence
\(h\bar\eta\) satisfies the rank-one Stark conjecture.

## Epistemic consequence

- Lemma A is `PROVED` from the rank-one Stark identity plus Roblot
  Theorem 6.1.
- Lemma B is `PROVED` as an equivalence. It does **not** prove
  quantization in an uncertified row.
- A rigorous numerical census can falsify (5) by separating the two
  complex balls from all four rotations. Ball overlap with a rotation
  is only `CERTIFIED_NUMERICAL_CONSISTENCY`, never a proof of (5).

## Source map

The source is X.-F. Roblot, *Index formulae for Stark units and their
solutions*, arXiv:1112.2820:

- (A1)--(A3): p. 2;
- the weak absolute-value conclusion and uniqueness up to a trivial
  unit: Theorem 6.1;
- the general weak determinant statement: Proposition 4.1;
- comparison of two index-formula solutions by group-ring units:
  Corollary 4.5.

The exact sign in (1)--(3) follows the phase project's frozen
\(\chi(g)\), right-action convention and must be inverted if the
opposite Artin convention is used.
