# P7 — finite ray-class Hecke family over \(\mathbb Q(i)\), preregistration v1

## Boundary and status

`OBSERVED`: this document selects and freezes one prospective P7 transfer
family:

\[
 K=\mathbb Q(i),\qquad
 \mathcal F(Q)=\{(\mathfrak f,\chi):Q<N\mathfrak f\leq2Q,
 \ \chi\text{ is a primitive finite ray-class character of exact conductor }
 \mathfrak f\}.
\]

Here \(Q\geq8\), the lower shell endpoint is strict, and the upper endpoint
is inclusive. The archimedean type is exactly trivial. There are no real
places of \(\mathbb Q(i)\), and no angular Groessencharacter parameter is
included. Characters are counted as distinct characters on ideals; this does
not quotient by conjugation, inversion, Galois action, or ideal
representatives. Each exact-conductor pair is counted once.

This is `PREREGISTERED_UNEXECUTED`. It proves no zero-density improvement,
no transfer of Guth--Maynard, no zero-free region, no prime-ideal
short-interval result, and no bounded-gap result. It does not start a theorem
search or a hostile audit. Angular characters, varying fields, varying
discriminants, and higher-degree/automorphic families are deferred.

## Frozen L-function and zero conventions

For an integral ideal \(\mathfrak a\), extend \(\chi(\mathfrak a)\) by zero
when \((\mathfrak a,\mathfrak f)\ne1\), and use

\[
 L(s,\chi)=\sum_{\mathfrak a}\frac{\chi(\mathfrak a)}{(N\mathfrak a)^s}
 =\prod_{\mathfrak p}\left(1-\frac{\chi(\mathfrak p)}{(N\mathfrak p)^s}\right)^{-1}.
\]

Only nontrivial zeros of the uncompleted \(L(s,\chi)\) are counted:

\[
 N(\sigma,T,\chi)=\#\{\rho:\ 0<\Re\rho<1,\
 \sigma\leq\Re\rho<1,\ |\Im\rho|\leq T\},
\]

with multiplicity, \(1/2\leq\sigma<1\), and \(T\geq2\). The frozen family
sum is

\[
 N_{\mathcal F}(\sigma,T;Q)=
 \sum_{Q<N\mathfrak f\leq2Q}\sum_{\chi\ \mathrm{primitive}\bmod\mathfrak f}
 N(\sigma,T,\chi).
\]

## Source ledger and prior-work boundary

The replay pins the primary-source bytes, source archives where available,
and the following locators.

| Source | Checked locator | Limited role here |
|---|---|---|
| Zaman, arXiv:1502.05679v4 | TeX 68--91, 225--253, 295--303; PDF pp.1, 3--4, 6 | ray-class definitions, exact conductor, and prior near-one density context |
| Thorner--Zaman, arXiv:1510.08086v1 | Theorem 1.1, TeX 441--449 / PDF p.4; TeX 468--472; TeX 1162--1166 | prior log-free density, detector/large-sieve mechanism, and induction comparison |
| Thorner, *Math. Res. Lett.* 26 (2019), 875--901 | Theorems 2.1/2.3, PDF pp.9--11; primitive embedding, PDF p.21; abstract, PDF p.1 | existing Hecke large-sieve/density, Bombieri--Vinogradov, and bounded-gap work |

`OBSERVED`: the preceding results are conceded as prior work. In particular,
this program claims neither an improvement of the Thorner--Zaman log-free
density estimate nor a replacement of Thorner's Bombieri--Vinogradov or
bounded-gap applications. BGL is a rejected comparison only: no definition,
theorem, or inference below relies on it.

## First falsifiable gate: norm aggregation

Grouping by absolute norm gives

\[
 A_\chi(n)=\sum_{N\mathfrak a=n}\chi(\mathfrak a),\qquad
 |A_\chi(n)|\leq a_K(n)=\sum_{d\mid n}\chi_{-4}(d)\leq\tau(n).
\]

Thus a fixed-character norm-collapsed polynomial has coefficients bounded by
\(N^{o(1)}\) on a length-\(N\) block. That alone does **not** make the loss
harmless for the desired family theorem: the target inequality and all
epsilon bookkeeping must still be checked. Nor does it identify a common
polynomial for all characters.

The gate fixes an exact, independent type-mismatch witness before any search:
at \(Q=8\), the moduli \((3)\) and \((1+i)^4\) have norms \(9\) and \(16\),
so both lie in the shell. Each associated ray-class quotient after dividing
by \(\mu_4\) has a unique nontrivial character of exact displayed conductor.
For

\[
 17=(4+i)(4-i),
\]

the former character has value \(-1\) on both prime ideals and the latter
has value \(+1\) on both. Therefore the preselected calculation is

\[
 A_{\chi_{(3)}}(17)=-2,\qquad A_{\chi_{(1+i)^4}}(17)=2.
\]

The future gate must verify this calculation and separately prove stability
under the divisor normalization. If verified, the result is only
`PASS_TYPE_MISMATCH`: a theorem for one fixed coefficient vector cannot be
applied verbatim to the joint collection of \((\chi,t)\) samples. It is not
a no-go theorem for a character-aware large-value inequality, nor does it
rule out applying a fixed-polynomial estimate separately and then paying a
separately audited family cost.

## Dependency graph and frozen gates

```text
P7-0 source/family conventions
  -> P7-1 norm aggregation (first falsifiable gate)
       -> P7-2 complete and primitive ray-class orthogonality
            -> P7-3 ideal-indexed cubic trace and energy
                 -> P7-4 zero detector and tail
                 -> P7-5 prime-ideal short-interval bridge
P7-4 -------------------------------------> P7-5
```

- `P7-2` must derive the primitive projector rather than replace it with
  complete-character orthogonality.
- `P7-3` must account for distinct ideals of equal norm, ideal products and
  ratios, the common \((\chi,t)\) sample space, and the exact diagonal.
- `P7-4` must pin a detector, all length and smoothness ranges, the ideal-sum
  tail, principal/pole treatment, and low-height conventions.
- `P7-5` must check an explicit formula, exceptional zeros, prime powers,
  and every interval uniformity condition before it may name an exponent
  \(\theta\) for \([x,x+x^\theta]\).

Every gate is currently `UNEXECUTED`. A failure contains its own table and
does not refute an untried character-aware route. No gate outcome can be
promoted to a paper claim without a later paper-stage audit.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_hecke_qi_preregistration_v1.py --check
python3 -m unittest tests/test_p7_hecke_qi_preregistration_v1.py -v
```

The sealed artifact records source, conventions, document, and builder hashes,
plus resource caps (60 seconds and 256 MiB). It refuses optimized Python and
does not have a command that executes a theorem search.
