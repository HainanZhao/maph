# Unitary leakage fingerprints of three four-mode dark mechanisms

This note challenges the assumption that classifying exact Fourier
amplitude zeros is, by itself, a physically compelling thesis.  The
answer is negative: an infinite arithmetic family need not be more
robust than an isolated zero.  A more physical invariant is the
*directional leakage fingerprint* under calibrated, unitary
perturbations.

The exact calculations are reproduced with:

```console
python3 scripts/analyze_unitary_leakage.py
```

The script uses the Python standard library and the repository's exact
integer phase histogram.  It performs no floating-point zero tests.

## 1. Normalization and perturbation model

Let

\[
F_4(j,k)=\frac{i^{jk}}2,
\qquad
\mathcal A_{r,s}(U)
=
\frac{\operatorname{per}U[r,s]}
{\sqrt{\prod_jr_j!\prod_ks_k!}}.
\]

Write \(Z_{r,t}\in\mathbb Z[i]\) for the permanent obtained from the
unnormalized matrix \(2F_4\), with its rows and columns repeated
according to \(t\) and \(r\).  If \(N=\sum r_j=\sum s_j\), then

\[
\mathcal A_{r,t}(F_4)
=
\frac{Z_{r,t}}
{2^N\sqrt{\prod_jr_j!\prod_kt_k!}}.
\]

Append a tunable two-mode unitary after the Fourier multiport:

\[
\begin{aligned}
U^{X}_{pq}(\epsilon)&=e^{i\epsilon X_{pq}}F_4,&
X_{pq}&=|p\rangle\langle q|+|q\rangle\langle p|,\\
U^{Y}_{pq}(\epsilon)&=e^{i\epsilon Y_{pq}}F_4,&
Y_{pq}&=-i|p\rangle\langle q|+i|q\rangle\langle p|.
\end{aligned}
\]

These are the two phase quadratures of a lossless beam splitter.
Second quantization replaces \(X_{pq}\) by
\(\widehat X_{pq}=b_p^\dagger b_q+b_q^\dagger b_p\), and similarly for
\(Y\).

Let

\[
D_{r,s}=2^N\sqrt{\prod_jr_j!\prod_ks_k!}.
\]

For a dark target, direct use of the Fock ladder factors gives the
exact tangent formulas

\[
\boxed{
\mathcal A_X'(0)
=\frac{i}{D_{r,s}}\left(
s_qZ_{r,s+e_p-e_q}+s_pZ_{r,s-e_p+e_q}
\right)
}
\tag{1}
\]

and

\[
\boxed{
\mathcal A_Y'(0)
=\frac{1}{D_{r,s}}\left(
s_pZ_{r,s-e_p+e_q}-s_qZ_{r,s+e_p-e_q}
\right).
}
\tag{2}
\]

Terms with a negative occupation are omitted.  The square roots from
the ladder operators cancel exactly against the changed Fock-state
normalization; this is why (1)--(2) contain integer multiplicities.
If the derivative is nonzero, then

\[
P_{r,s}(\epsilon)
=|\mathcal A'(0)|^2\epsilon^2+O(\epsilon^3).
\tag{3}
\]

Higher derivatives can be computed without radicals.  Starting at
\(s\), moving one particle out of a mode of current occupation \(n\)
contributes the integer \(n\), and a \(Y\)-move additionally contributes
\(+i\) or \(-i\) according to its orientation.  Summing the resulting
Gaussian-integer weights times \(Z_{r,t}\) gives the common-denominator
numerator of
\(\langle s|\widehat G^kF_4|r\rangle\).  This is the exact recurrence
implemented by the reproduction script.

## 2. Three exact fingerprints

In the table, an entry \(c\,\epsilon^{2k}\) means
\(P(\epsilon)=c\,\epsilon^{2k}+O(\epsilon^{2k+1})\).
“Exact” means zero for every rotation angle, not merely a vanishing
first derivative.

### 2.1 Cyclic selection-rule zero

Take

\[
r=(1,1,1,1),\qquad s=(3,1,0,0).
\]

The cyclic rule allows only outputs satisfying
\(\sum_j j s_j=0\pmod4\).  The target has sum \(1\), and is dark.

| pair \(pq\) | \(X_{pq}\) | \(Y_{pq}\) |
|---|---:|---:|
| 01 | \(3\epsilon^2/8\) | \(3\epsilon^2/8\) |
| 02 | exact | exact |
| 03 | \(3\epsilon^2/8\) | \(3\epsilon^2/8\) |
| 12 | exact | exact |
| 13 | exact | exact |
| 23 | exact | exact |

The four exact rows hold for an arbitrary \(U(2)\) on the indicated
pair, not just the \(X\) and \(Y\) axes.  Such a unitary preserves the
total occupation in its pair.  The reachable modular sums are:

\[
\begin{array}{c|c}
02&1+2n_2\in\{1,3\}\pmod4\\
12&1\text{ or }2\pmod4\\
13&1\text{ or }3\pmod4\\
23&1\pmod4.
\end{array}
\]

None is allowed.  This is a proved selection-rule protection.

### 2.2 Parity/reflection family

For the smallest odd member, take

\[
r=s=(0,1,2,1).
\]

The leakage table is:

| pair \(pq\) | \(X_{pq}\) | \(Y_{pq}\) |
|---|---:|---:|
| 01 | \(\epsilon^2/64\) | \(\epsilon^2/64\) |
| 02 | \(\epsilon^2/4\) | \(\epsilon^2/4\) |
| 03 | \(\epsilon^2/64\) | \(\epsilon^2/64\) |
| 12 | \(\epsilon^2/64\) | \(25\epsilon^2/64\) |
| 13 | \(\epsilon^2/4\) | exact |
| 23 | \(\epsilon^2/64\) | \(25\epsilon^2/64\) |

The \(Y_{13}\) protection extends to every odd member

\[
r=s=(0,a,2a,a),\qquad a\ \text{odd}.
\tag{4}
\]

This statement is proved, rather than inferred from finite data.  Set
\(x=x_1,y=x_2,z=x_3\), \(u=x+z\), and \(v=x-z\).  With
\(c=\cos\epsilon\), \(d=\sin\epsilon\),
\(\alpha=c+d\), and \(\beta=c-d\), the two rotated Fourier row forms
satisfy

\[
L'_1L'_3
=
\alpha\beta(y^2+v^2)
+i(\alpha^2-\beta^2)yv,
\qquad
L_2=y-u.
\tag{5}
\]

The desired amplitude is proportional to

\[
[x^ay^{2a}z^a]
\left(A(y^2+v^2)+Byv\right)^a(y-u)^{2a},
\tag{6}
\]

where \(A=\alpha\beta\) and \(B=i(\alpha^2-\beta^2)\).
The functional \([x^az^a]\) is invariant under \(x\leftrightarrow z\),
which sends \(v\mapsto-v\).  It therefore kills every term containing
an odd power of \(v\), including all contributions with an odd number
of \(Byv\) factors.

Choose \(2h\) factors \(Byv\) in any surviving contribution.  After
choosing \(k-h\) factors \(v^2\) from the remaining \(a-2h\) factors,
the central coefficient is a symmetric weight times

\[
K_{a,k}
=[x^az^a](x-z)^{2k}(x+z)^{2a-2k}.
\]

Its weight is proportional to

\[
\binom{a-2h}{k-h}\binom{2a}{2k},
\]

which is invariant under \(k\leftrightarrow a-k\).  Substituting
\(z\mapsto-z\) proves

\[
K_{a,a-k}=(-1)^aK_{a,k}.
\]

For odd \(a\), every \(k\) term cancels its \(a-k\) partner.  Hence
(6) is identically zero for all \(\epsilon\), proving the exact
\(Y_{13}\) protection in (4).

The script separately checks the finite cases \(a=1,3,5,7\) by exact
Krylov moments.  Those checks reproduce the theorem but are not used
as its proof.

### 2.3 An isolated \(N=11\) affine-root zero

Use the line-\(B\) event

\[
r=(0,1,3,7),\qquad s=(1,3,3,4).
\]

| pair \(pq\) | \(X_{pq}\) | \(Y_{pq}\) |
|---|---:|---:|
| 01 | \(595\epsilon^2/8192\) | \(455\epsilon^2/16384\) |
| 02 | \(315\epsilon^2/16384\) | \(315\epsilon^2/8192\) |
| 03 | \(875\epsilon^2/16384\) | \(315\epsilon^2/16384\) |
| 12 | \(315\epsilon^2/16384\) | \(315\epsilon^4/8192\) |
| 13 | \(315\epsilon^2/16384\) | \(315\epsilon^2/16384\) |
| 23 | \(35\epsilon^2/4096\) | \(35\epsilon^2/4096\) |

The quartic \(Y_{12}\) entry is exact.  The two first-neighbour root
permanents are

\[
Z_{r,(1,2,4,4)}
=Z_{r,(1,4,2,4)}
=241920,
\]

so (2) vanishes because \(s_1=s_2=3\).  At second order the exact
common-denominator moment is

\[
\langle s|\widehat Y_{12}^{\,2}F_4|r\rangle
\quad\longleftrightarrow\quad
2903040(1-i).
\]

Including the Taylor factor \(1/2!\) and Fock normalization gives

\[
P_{r,s}^{Y_{12}}(\epsilon)
=\frac{315}{8192}\epsilon^4+O(\epsilon^5).
\]

Thus this isolated root has an accidentally flat tangent direction,
but it is not protected along the full one-parameter rotation.

## 3. A compact experimental discriminator

Probe four calibrated axes on the same four-mode device:

| mechanism | \(X_{12}\) | \(Y_{12}\) | \(X_{13}\) | \(Y_{13}\) |
|---|---:|---:|---:|---:|
| cyclic | exact | exact | exact | exact |
| parity, \(a=1\) | \(\epsilon^2/64\) | \(25\epsilon^2/64\) | \(\epsilon^2/4\) | exact |
| isolated \(N=11\) | \(315\epsilon^2/16384\) | \(315\epsilon^4/8192\) | \(315\epsilon^2/16384\) | \(315\epsilon^2/16384\) |

This distinguishes the mechanisms by directional power-law exponents
and exact null axes.  A scalar “robustness” measured along one
perturbation does not: the isolated root is flatter than the infinite
parity family along \(Y_{12}\).

A practical first experiment should use only the four-photon cyclic
and parity events.  Prepare the two inputs, implement \(F_4\), append a
phase-programmable mixer on modes \(1,2\) or \(1,3\), scan signed small
\(\epsilon\), and use photon-number-resolving detection for the target
events.  Fit a common background plus the predicted quadratic
curvature.  The \(N=11\) row is a longer-term test because preparing
the occupation \((0,1,3,7)\) with adequate indistinguishability is much
harder than programming the four-mode unitary.

This setup is realistic in architecture: Fourier suppression has
already been measured in integrated photonic circuits, and fully
programmable four-mode interferometers with photon-number-resolving
readout have been demonstrated.  Relevant primary sources include:

- Crespi et al., *Suppression law of quantum states in a 3D photonic
  fast Fourier transform chip*, Nature Communications 7, 10469 (2016),
  <https://doi.org/10.1038/ncomms10469>.
- Dittel et al., *Totally destructive many-particle interference*,
  Physical Review Letters 120, 240404 (2018),
  <https://doi.org/10.1103/PhysRevLett.120.240404>.
- Arrazola et al., *Quantum circuits with many photons on a
  programmable nanophotonic chip*, Nature 591, 54--60 (2021),
  <https://doi.org/10.1038/s41586-021-03202-1>.

## 4. Assumptions that remain challenged

1. **An appended mixer is a controlled observation-basis probe, not a
   complete fabrication-error model.** Generic internal unitary errors
   should next be decomposed into the twelve \(X/Y\) tangent axes plus
   diagonal gauge directions, and then propagated through the actual
   circuit layout.
2. **Perfect indistinguishability is assumed.** Partial
   distinguishability turns a single permanent amplitude into a
   weighted sum over permutations and generally produces a nonzero
   probability floor.  The directional curvature remains measurable
   only if that floor is independently characterized.
3. **Postselected loss is not modeled.** Uniform loss mainly reduces
   counts, but mode-dependent loss changes relative paths and can
   imitate leakage.
4. **Exact protection is axis-dependent.** The parity family is exact
   on \(Y_{13}\) and linearly sensitive on \(X_{13}\).  Calling the
   entire zero “protected” without naming a perturbation class is
   misleading.
5. **Novelty is not yet established.** Suppressed-event leakage is
   already used for device validation.  The potentially new claim is
   the mechanism-resolving directional fingerprint and the all-odd-\(a\)
   exact axis, which require a dedicated literature audit.

The result is therefore strong enough for a thesis section and a
concrete experiment proposal, but not yet a standalone physics paper.
The next necessary calculation is to add partial distinguishability
and reconstructed-unitary uncertainty and determine whether the
quadratic-versus-quartic fingerprints survive realistic backgrounds.
