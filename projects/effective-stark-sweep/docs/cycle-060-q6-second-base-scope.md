# Cycle 060 — \(\mathbb Q(\sqrt6)\) second-base scope halt

**Audited:** 2026-07-30T05:55:15Z  
**Case:** `RQ-000129`  
**Verdict:** `BLOCKED_THEOREM_SCOPE_RESISTANCE`  
**Promotion:** none

## Exact reconstruction

The independent imaginary base is
\[
k=\mathbb Q(\sqrt{-3}),\qquad w_k=6.
\]
The character field has polynomial
\[
x^8-2x^6+5x^4-4x^2+1,
\]
signature \([0,4]\), class number one, `bnfcertify=1`, and
\[
e=|\mu(E)|=12.
\]
Its exact ray data are
\[
\operatorname{Cl}_{\mathfrak m}(k)\simeq C_4\times C_2,\qquad
H=\begin{pmatrix}4&2\\0&1\end{pmatrix},
\]
with inverse character pair
\[
[1,1],\ [3,1].
\]
The first thirty exact Dirichlet coefficients of `[1,1]` equal the
source coefficients.  The inverse is separated already at \(n=3\):
\[
a_3(\mathrm{source})=a_3([1,1])=-i,\qquad
a_3([3,1])=+i.
\]
Thus the exact source label selects `[1,1]` without numerical
recognition.

The order-four generator acts on the free unit lattice by
\[
\begin{pmatrix}
-1&0&0\\
0&0&-1\\
0&1&0
\end{pmatrix},
\]
and the anti-unit lattice is
\[
\begin{pmatrix}
0&0\\1&0\\0&1
\end{pmatrix}.
\]
The general-\(e\) scaling is \(e/2=6\).  An exact search in the common
degree-16 normal closure found precisely the four expected secondary
coordinate directions
\[
(-1,0),\ (0,-1),\ (0,1),\ (1,0),
\]
raised to the sixth power.  Across the two complex conjugations and
all exact field inclusions, it produced 256 identities, 64 for each
direction, satisfying
\[
\boxed{q_8^3=q_{12}^2},\qquad
q_e=\varepsilon_e\overline{\varepsilon_e}.                 \tag{1}
\]
Equation (1) is the root-free same-normalized-packet relation forced
by
\[
\frac{\log q_8}{8}=\frac{\log q_{12}}{12}.
\]
This is an exact algebraic alignment of the two candidate orbits.  It
is not an analytic Stark identification.

## The scope failure

The conductor is
\[
\mathfrak p_2^3,\qquad
\mathfrak p_2=(2,[2,0]^t),
\]
with **one** distinct finite conductor prime.  Consequently the
natural set consisting of the complex place and conductor primes has
\[
|S|=2.
\]
The general-\(e\) theorem banked in Cycle 059 explicitly assumes
\(|S|\ge3\) in order to invoke Stark's global-unit clause.  Therefore
it cannot promote the \(\mathbb Q(\sqrt{-3})\) route as written.
The exact global units found in the lattice search do not repair this
logical gap: without an applicable theorem or an analytic
identification, calling one of them the Stark unit would be circular.

This is the mandated theorem-scope resistance.  Work halted before
Arb.  `RQ-000129` remains
`THEOREM_CANDIDATE_NOT_YET_VERIFIED`.

## What would be required to reopen the case

One of the following must be proved and pre-registered first:

1. an \(|S|=2\) Engine-C lemma in the appropriate \(S\)-unit lattice,
   including exact control of the finite valuation; or
2. an auxiliary-prime enlargement to \(|S|\ge3\), with its Euler
   factor carried exactly through the source/CM reinduction and packet
   normalization.

Neither modification is implicit in the banked theorem, and neither
is attempted here.

## Reproducibility record

- Scope audit:
  `scripts/q6_norm8_second_base_scope.gp`, SHA-256
  `5b7555f53bac16317bb990551e81b22a956eb01519dff0114b7a64b07d072e0a`.
- Normalized bridge:
  `scripts/q6_norm8_second_base_bridge_search.gp`, SHA-256
  `9ccdc7aa73fff1f7fe1858b7fffbe5a37e3b7a875e409ee73c2f53b6dbf6929f`.
- Scope transcript SHA-256:
  `96ec3779d40241e41256fd5e6040d7f23a9ea36900e501b5e323b1223b0c737a`.
- Bridge transcript SHA-256:
  `d28f45618f9fcaa34c969eda140061615f443c5a115ee1326883f6a15919bcef`.
- The first bridge search parser failure is preserved, SHA-256
  `4ba7b4ee7f116d6a2f5a00121120b2e5654e50fcce27fd7fb04cb22e1b9a09af`.
- General-\(e\) theorem record SHA-256:
  `1067e3cd00cbbb5a33c55b698353a3554d991090f6c4e4997e8d5ebebdf68233`.

All algebraic identities above are `VERIFIED`.  The statement that
either candidate is the analytic Stark packet is deliberately not
made.
