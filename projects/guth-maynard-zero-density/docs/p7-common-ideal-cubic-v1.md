# P7-3 — common ideal-indexed cubic/energy bridge over \(\mathbb Q(i)\)

## Outcome and claim boundary

`PROVED`: for a common ideal coefficient function, the joint primitive
ray-class/time family has the exact labelled Gram kernel, norm-fibre formula,
and cubic-trace expansion displayed below. `PROVED`: for one fixed modulus,
a coloured additive energy has an exact complete-ray-class Parseval identity.
These facts retain distinct ideals of equal norm, character labels, and the
zero-extension convention.

`PROVED`: the pinned Guth--Maynard integer cubic argument cannot be invoked
*verbatim* for the joint \((\chi,t)\) family. Its one common integer
coefficient sequence and globally separated uncoloured time set are absent;
primitive labels are not a character group; and varying exact conductors do
not have a common ray-class group without changing zero-extended values.

This is a type/source-hypothesis boundary, not a saturation theorem or a
negative theorem about a character-aware method. No ideal cubic large-value
inequality, Hecke zero-density estimate, detector, or prime-ideal
short-interval theorem is proved.

## Exact common-ideal formulation

Let \(c(\mathfrak a)\) be one fixed coefficient function, supported on
\(N< N\mathfrak a\leq2N\), with \(|c(\mathfrak a)|\leq1\), and let \(w\)
be a fixed real weight. A sample point is

\[
x=(\mathfrak f_x,\chi_x,t_x),
\]

where \(\chi_x\) is primitive of exact finite conductor \(\mathfrak f_x\)
in the selected shell. Values are zero on ideals not coprime to
\(\mathfrak f_x\). For a finite labelled sample \(W\), put

\[
 M_{x,\mathfrak a}=c(\mathfrak a)w(N\mathfrak a/N)
 \chi_x(\mathfrak a)(N\mathfrak a)^{it_x},\qquad K=MM^*.
\]

Then \(K\) is positive semidefinite and exactly

\[
 K_{xy}=\sum_{\mathfrak a}|c(\mathfrak a)|^2w(N\mathfrak a/N)^2
 \chi_x(\mathfrak a)\overline{\chi_y(\mathfrak a)}
 (N\mathfrak a)^{i(t_x-t_y)}.
\]

Grouping by norms gives

\[
 K_{xy}=\sum_n n^{i(t_x-t_y)}B_{xy}(n),\qquad
 B_{xy}(n)=\sum_{N\mathfrak a=n}|c(\mathfrak a)|^2w(n/N)^2
 \chi_x(\mathfrak a)\overline{\chi_y(\mathfrak a)}.
\]

Thus \(B_{xy}(n)\), not one common \(b_n\), is the exact collapsed
coefficient. Distinct ideals of the same norm remain distinct terms even
when their time phase agrees. The repeated norms themselves have a controlled
single-character L2 cost: for
\(b_\chi(n)=\sum_{N\mathfrak a=n}c(\mathfrak a)\chi(\mathfrak a)\),
Cauchy gives

\[
 |b_\chi(n)|^2\leq a_{\mathbb Q(i)}(n)
 \sum_{N\mathfrak a=n}|c(\mathfrak a)|^2\mathbf1_{(\mathfrak a,\mathfrak f_\chi)=1}
 \leq \tau(n)\sum_{N\mathfrak a=n}|c(\mathfrak a)|^2.
\]

On \(n\asymp N\), this is an \(N^{o(1)}\) loss, and it is a
\(T^{o(1)}\) loss in P7-1's already pinned \(N\leq T^C\) regime. Hence
repeated norms are retained exactly but are not, by themselves, the
common-coefficient barrier. The unresolved issue is the pair-label dependence
of \(B_{xy}\) and the coloured sample geometry.

Expanding the trace gives the exact labelled cubic identity

\[
\begin{aligned}
 \operatorname{tr}(K^3)=\sum_{x,y,z\in W}\sum_{\mathfrak a,\mathfrak b,\mathfrak c}
 &u(\mathfrak a)u(\mathfrak b)u(\mathfrak c)
 \chi_x(\mathfrak a)\overline{\chi_y(\mathfrak a)}
 \chi_y(\mathfrak b)\overline{\chi_z(\mathfrak b)}
 \chi_z(\mathfrak c)\overline{\chi_x(\mathfrak c)}\\
 &\times (N\mathfrak a)^{i(t_x-t_y)}(N\mathfrak b)^{i(t_y-t_z)}
 (N\mathfrak c)^{i(t_z-t_x)},
\end{aligned}
\]

where \(u(\mathfrak a)=|c(\mathfrak a)|^2w(N\mathfrak a/N)^2\).
The quotient notation in the sealed artifact is only shorthand for this
zero-extended product; no fractional ideal on a non-coprime modulus is being
evaluated.

## Fixed-modulus coloured energy

For a fixed modulus \(\mathfrak f\), set
\(G_{\mathfrak f}=\operatorname{Cl}(\mathfrak f)\). Embed a selected set
of primitive labels in the *complete* dual group \(\widehat G_{\mathfrak f}\).
For integral, discretized times define

\[
 E_{\rm col}^{=}(W)=\#\{(x_1,x_2,x_3,x_4)\in W^4:
 t_1+t_2=t_3+t_4,\ \chi_1\chi_2=\chi_3\chi_4\}.
\]

Complete character orthogonality gives

\[
 E_{\rm col}^{=}(W)=\frac1{|G_{\mathfrak f}|}
 \sum_{g\in G_{\mathfrak f}}\int_0^1
 \left|\sum_{(\chi,t)\in W}\chi(g)e(t\theta)\right|^4d\theta.
\]

Consequently it is at most the exact additive energy of the *time multiset*.
It is not generally the energy of a de-duplicated time set: different
characters can have the same height. A smooth real-height analogue replaces
the exact time condition by the Fourier weight of the chosen smoothing.

The complete ambient group is necessary. At \(\mathfrak f=(3)\), the unique
nontrivial primitive character has order two and its square has conductor
one, so exact-conductor primitive characters are not closed under
multiplication.

## Why the cited cubic proof does not import verbatim

Guth--Maynard's pinned cubic trace is an integer Poisson calculation for one
coefficient sequence and a globally separated \(W\subset\mathbb R\).
Here the exact norm collapse produces \(B_{xy}(n)\), while detector-selected
heights naturally have separation only within a fixed \(\chi\)-fibre.
Two distinct characters at the same height are different family points but
coincide after forgetting colours, invalidating the cited diagonal step.

Nor can varying conductor groups be silently unified. Pulling every character
to a common multiple \(\mathfrak F\) changes its zero-extended value on
ideals coprime to its own conductor but not to \(\mathfrak F\). Restricting
the coefficients to \((\mathfrak a,\mathfrak F)=1\) is a new loss that has
not been bounded. Finally, positivity of \(K\) does not make its displayed
labelled cubic summands, or the primitive Möbius projector, termwise positive.

The required next input is therefore a uniform *coloured primitive* cubic
trace/large-value bound that controls fibre-local separation, same-height
colour collisions, repeated-norm \(B_{xy}\) terms, cross-conductor triples,
and the signed primitive projector. Neither the checked Guth--Maynard cubic
argument nor Thorner's L2 large sieve supplies it. This leaves
character-aware and conductor-by-conductor routes open.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_common_ideal_cubic_v1.py --check
python3 -m unittest tests/test_p7_common_ideal_cubic_v1.py -v
```

The replay pins the P7-1/P7-2 artifacts and the cited Guth--Maynard source,
performs exact finite labelled-Gram and coloured-Parseval checks, and has a
strict 60-second / 256 MiB resource contract.
