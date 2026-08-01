# P7-2 — ray-class projector and L2 large-sieve gate

## Outcome and boundary

`PROVED`: for the selected finite-order, trivial-infinity ray-class family
over \(K=\mathbb Q(i)\), complete ray-class orthogonality and the exact
finite-conductor projector have the formulas below, including the required
ideal-coprimality indicator. `PROVED`: Thorner's published Theorem 2.1 has
the displayed \(m=0\), dyadic-shell L2 specialization for one common
ideal-indexed coefficient function.

This closes only `P7-2-RAY-CLASS-ORTHOGONALITY` in the scoped sense recorded
by the replay. It proves no cubic-energy or large-value inequality, no
Hecke zero-density estimate, no detector, and no prime-ideal interval
theorem. It is a lightweight source/algebra/replay result; no hostile audit
was initiated.

## Exact ray-class indexing and projector

For a nonzero integral ideal \(\mathfrak f\subset\mathbb Z[i]\), write

\[
  \mathrm{Cl}(\mathfrak f)=I(\mathfrak f)/P_{\mathfrak f},\qquad
  X(\mathfrak f)=\operatorname{Hom}(\mathrm{Cl}(\mathfrak f),\mathbb C^\times).
\]

Zaman's definitions (source TeX lines 101--110 and 298--303) identify these
with the finite ray-class characters and give each such character a unique
finite conductor \(\mathfrak d\mid\mathfrak f\). Values on integral ideals
not coprime to the modulus are extended by zero. There are no real-place
conditions for \(\mathbb Q(i)\).

For integral ideals \(\mathfrak a,\mathfrak b\) with
\((\mathfrak a\mathfrak b,\mathfrak f)=1\), finite abelian-character
orthogonality gives

\[
 C_{\mathfrak f}(\mathfrak a,\mathfrak b)
 :=\sum_{\chi\in X(\mathfrak f)}
   \chi(\mathfrak a)\overline{\chi(\mathfrak b)}
 =|\mathrm{Cl}(\mathfrak f)|
   \mathbf 1_{[\mathfrak a]_{\mathfrak f}=[\mathfrak b]_{\mathfrak f}}.
\]

Let \(P_{\mathfrak d}\) sum only characters of exact finite conductor
\(\mathfrak d\). Unique primitivity then partitions the complete kernel:

\[
 C_{\mathfrak f}(\mathfrak a,\mathfrak b)
 =\sum_{\mathfrak d\mid\mathfrak f}
 P_{\mathfrak d}(\mathfrak a,\mathfrak b)
 \quad ((\mathfrak a\mathfrak b,\mathfrak f)=1).
\]

Ideal Möbius inversion yields the primitive formula, valid with the frozen
zero extension for all integral \(\mathfrak a,\mathfrak b\):

\[
 P_{\mathfrak f}^{0}(\mathfrak a,\mathfrak b)
 =\mathbf1_{(\mathfrak a\mathfrak b,\mathfrak f)=1}
   \sum_{\mathfrak d\mid\mathfrak f}\mu_K(\mathfrak f/\mathfrak d)
   |\mathrm{Cl}(\mathfrak d)|
   \mathbf1_{[\mathfrak a]_{\mathfrak d}=[\mathfrak b]_{\mathfrak d}}.
\]

The outside coprimality factor is material: omitting it incorrectly assigns a
nonzero complete kernel to ideals on which the selected character convention
is zero. The replay checks the underlying Möbius convolution exactly on
representative prime-ideal divisor lattices.

## Source-scoped large sieve

Thorner, *Math. Res. Lett.* 26 (2019), Theorem 2.1 (PDF pp.9--10; printed
pp.883--884), states Duke's Hecke large sieve. Its relevant hypotheses are:
a single function \(c(\mathfrak a)\) on integral ideals with

\[
 \|c\|_2^2=\sum_{N\mathfrak a\leq N}|c(\mathfrak a)|^2,
\]

primitive narrow ray-class characters \(\xi\bmod\mathfrak q\), and the
torsion-free Hecke parameters \(\mathbf m\) with
\(\|\mathbf m\|_\infty\leq T\). For \(n_K=2\), take the source conductor
cutoff \(R=2Q\), retain only the nonnegative subcollection
\(Q<N\mathfrak f\leq2Q\), and fix the sole parameter to \(m=0\). This is
exactly the selected trivial-infinity family, and \(\lambda_0=1\). Thus for
\(Q\geq8\), \(T\geq2\), and common finite-support ideal coefficients,

\[
 \sum_{Q<N\mathfrak f\leq2Q}\ \sum_{\chi\;\mathrm{primitive}\bmod\mathfrak f}
 \int_{-T}^{T}\left|\sum_{N\mathfrak a\leq N}
 c(\mathfrak a)\chi(\mathfrak a)(N\mathfrak a)^{-it}\right|^2dt
 \ll_K (N+4Q^2T^2)(\log(2QT))^A\|c\|_2^2.
\]

`PROVED`: this is a restriction of the cited nonnegative source sum, not a
new large sieve. The conductor is indexed exactly once because the source
star sum is primitive and the P7 family indexes a pair by its exact finite
conductor.

## Common-coefficient boundary

The quoted theorem's \(c(\mathfrak a)\) is fixed before summing over
\(\mathfrak f,\chi,m,t\). If it is grouped by norm, then

\[
 b_\chi(n)=\sum_{N\mathfrak a=n}c(\mathfrak a)\chi(\mathfrak a),
\]

which generally varies with \(\chi\). P7-1 already proved this variation for
the basic coefficients at norm \(17\). The ideal-form large sieve remains
available when the \(b_\chi\) genuinely come from one common \(c\), but it
does not license a theorem for arbitrary independently selected
\(b_\chi(n)\), nor a verbatim common-integer-polynomial Guth--Maynard
import. Likewise, the signed primitive Möbius projector is an identity, not
a positive family large-sieve estimate.

`OBSERVED`: P7-3 remains open: it must formulate an ideal-indexed common
sample cubic/energy inequality which handles repeated norms and the
character-coupled terms. This gate neither rules that route out nor supplies
its missing estimate.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_ray_orthogonality_v1.py --check
python3 -m unittest tests/test_p7_ray_orthogonality_v1.py -v
```
