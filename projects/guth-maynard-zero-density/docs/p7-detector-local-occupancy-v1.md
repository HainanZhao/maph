# P7-3C — detector-side local occupancy and the uncoloured difference gate

## Outcome and claim boundary

`PROVED`: for a selected primitive Hecke character of exact finite conductor
(mathfrak f) over (mathbb Q(i)), the pinned circle-zero estimate gives an
explicit logarithmic bound for the zero multiset in a unit height window:


\[
 Z_\chi(u)\leq L_0(N\mathfrak f,u)
 :=3\log N\mathfrak f+6\log(|u|+3)+6\log4+34.
 \tag{1}
\]

`PROVED`: this does **not** remove the cross-character loss in the P7
uncoloured time projection.  Once a detector has made every fixed-character
fibre (1)-separated, a radius-(Delta<1/2) interval already has at most
one selected time from each character; (1) supplies no improvement.  At a
fixed modulus this leaves up to (2Q) simultaneous colours, and across the
dyadic shell it leaves fewer than (12Q^2) colours.

`PROVED`: the bound

\[
 \mathcal D_\Delta(\mathcal T)\leq
 |\mathcal T|\,\mathcal M_\Delta(\mathcal T),\qquad
 \mathcal M_\Delta(\mathcal T):=
 \sup_u\#\bigl(\mathcal T\cap[u-\Delta,u+\Delta]\bigr),
 \tag{2}
\]

is sharp even when every colour fibre is (1)-separated and has at most one
point in every unit height interval.  Thus local zero counts and the primitive
family cardinality alone cannot deliver an (o(|mathcal T|P)) difference
bound, where (P) is the number of occurring colours.

`PROVED` conditional on a displayed detector hypothesis: the existing joint
Hecke large sieve can bound (mathcal M_Delta) at source scale only if one
common ideal polynomial is uniformly large at every detector row.  P7 has not
yet supplied that detector or threshold.  The P7 cubic gate therefore remains
open, and its separate averaged-block input remains open as well.

This is research-stage source/algebra/replay work only.  No hostile audit is
initiated, and no zero-density, detector, large-value, or prime-ideal theorem
is claimed.

## 1. Exact conductor, zero extension, and the statistic

Let

\[
 W\subset\{(\mathfrak f,\chi,t):Q<N\mathfrak f\leq2Q,
 \ \chi\text{ primitive of exact finite conductor }\mathfrak f,
 \ 0\leq t\leq T\},
 \qquad \mathcal T=\pi_tW,
 \tag{3}
\]

where (mathcal T) is a set of distinct times and (m=|mathcal T|).  Every
row retains the frozen convention

\[
 \chi(\mathfrak a)=0\quad\text{if }(\mathfrak a,\mathfrak f)\ne1.
 \tag{4}
\]

No character is completed or inflated in this note.  In particular, a local
zero count for a row in (3) is a count for the (L)-function at its **exact**
primitive conductor.

For (0<Delta<1/2), the preceding fixed-ray transfer uses

\[
 \mathcal D_\Delta(\mathcal T)=\sup_v
 \#\{(t,s)\in\mathcal T^2: |(t-s)-v|\leq\Delta\}.
 \tag{5}
\]

For fixed (t,v), the admissible (s)'s lie in one interval of radius
(Delta).  This proves (2).  Conversely, the diagonal pairs give

\[
 \mathcal D_\Delta(\mathcal T)\geq m.
 \tag{6}
\]

Thus a proposed source-scale target below (m) is impossible for this
L2-to-discrete route, independently of detector arithmetic.

## 2. A source-checked individual local zero count

Thorner--Zaman's pinned manuscript gives, for a Hecke character (chi),
(s=\sigma+iu) with (\sigma>1), and (0<r\leq1),

\[
 N_\chi(r;s)\leq
 \{4\log D_K+2\log N\mathfrak f_\chi
 +2n_K\log(|u|+3)+2n_K+4+4\delta(\chi)\}r+4+4\delta(\chi).
 \tag{7}
\]

Here (N_chi(r;s)) counts nontrivial zeros in the indicated circle.  Its
proof uses the zero multiset in the explicit formula, so (7) is also valid
for a detector that preserves zero multiplicity; it is a fortiori valid for
distinct zero ordinates.

For (K=\mathbb Q(i)), take the circle center
(21/20+iu), radius (3/4).  If
(eta\geq1/2) and (|\gamma-u|\leq1/2), then

\[
 \left(\frac{21}{20}-\beta\right)^2+(\gamma-u)^2
 \leq\left(\frac{11}{20}\right)^2+\left(\frac12\right)^2
 =\frac{221}{400}<\frac{225}{400}=\left(\frac34\right)^2.
 \tag{8}
\]

For (eta<1/2), the pinned functional equation maps
(eta+i\gamma) to a zero (1-\beta-i\gamma) of
(L(s,\overline\chi)), in the reflected window centered at (-u).  Apply
(7) to both halves, use (D_K=4), (n_K=2), and
(delta(\chi)\leq1).  This proves (1).

This is a useful detector hygiene fact, but it is not a family local-density
bound: it has no cancellation across characters.

## 3. What a zero detector can obtain from (1)

Suppose, only for this paragraph, that a detector row (t) is assigned to a
zero of the same exact primitive (L(s,\chi)) at ordinate within
(alpha), and no zero receives more than (b) selected rows.  If
(alpha+\Delta\leq1/2), then (1) gives

\[
 \#\{t\in\mathcal T_\chi:|t-u|\leq\Delta\}
 \leq bL_0(N\mathfrak f,u).
 \tag{9}
\]

This is the correct local-zero consequence without a spacing extraction.
If the standard detector thinning makes every (mathcal T_\chi)
(1)-separated, the left side of (9) is instead at most (1), which is
stronger.

Let (P) be the number of exact primitive characters occurring in (W).
The selected P7 cardinality bounds give

\[
 P\leq|X(\mathfrak f)|\leq N\mathfrak f\leq2Q
 \quad\text{at one fixed }\mathfrak f,
 \tag{10}
\]

and, over the whole shell,

\[
 P\leq\mathcal F_{\rm prim}(Q)
 <12Q^2.
 \tag{11}
\]

Consequently one-separated fibres imply only

\[
 \mathcal D_\Delta(\mathcal T)\leq 2mQ
 \quad\text{at fixed }\mathfrak f,
 \qquad
 \mathcal D_\Delta(\mathcal T)<12mQ^2
 \quad\text{over the shell}.
 \tag{12}
\]

If (Q=T^\vartheta) for fixed (\vartheta>0), these retain respectively
(T^\vartheta) and (T^{2\vartheta}), up to logarithms.  They become
subpower only under the additional condition (Q=T^{o(1)}), which is not
part of frozen P7.

## 4. Sharp detector-side obstruction

The (P)-colour, (J)-block configuration

\[
 t_{j,c}=3j+\frac{c}{8P}
 \qquad(0\leq j<J,\ 0\leq c<P)
 \tag{13}
\]

has (m=JP).  Assign (t_{j,c}) to colour (c).  Every colour fibre is
(3)-separated and has at most one point in a unit height interval.  But at
(Delta=1/4),

\[
 \mathcal M_{1/4}(\mathcal T)=P,
 \qquad
 \mathcal D_{1/4}(\mathcal T)=JP^2=mP.
 \tag{14}
\]

The replay checks (14) exactly for (P=3,J=4).  This is a combinatorial
model, not a claimed configuration of Hecke zeros.  Its force is precise: no
deduction using only fibrewise spacing, an individual unit-window count, and
the number of colours can replace (mP) by a subpower quantity.

## 5. The conditional joint character--height route

There is one route that can genuinely see cross-character clustering.  Assume
there is a **single common** ideal coefficient function (c(\mathfrak a)),
supported on (N<N\mathfrak a\leq2N), such that

\[
 D_\chi(t)=\sum_{N<N\mathfrak a\leq2N}
 c(\mathfrak a)\chi(\mathfrak a)(N\mathfrak a)^{-it},
 \qquad |D_\chi(t)|\geq V
 \tag{15}
\]

for every detector row.  The commonness is material: character-dependent
coefficient functions cannot be inserted into the source large sieve.

Fix a local center (u), choose one labelled detector row above each
distinct time in (mathcal T\cap[u-1/4,u+1/4]), and replace

\[
 c(\mathfrak a)\longmapsto
 c_u(\mathfrak a)=c(\mathfrak a)(N\mathfrak a)^{-iu}.
 \tag{16}
\]

This preserves its (ell^2) norm, support, exact conductor labels, and the
zero extension (4).  Unit-radius Sobolev sampling with radius (1/4), then
Thorner's Theorem 2.1 with source conductor cutoff (2Q), height (2), and
(m=0), gives

\[
 \mathcal M_{1/4}(\mathcal T)V^2
 \ll_K \mathcal L_{\rm loc}(N,Q)\|c\|_2^2,
 \tag{17}
\]

where

\[
 \mathcal L_{\rm loc}(N,Q)=
 \left(4+\frac12\log^2(2N)\right)
 (2N+16Q^2)(\log(4Q))^A.
 \tag{18}
\]

Together with (2), this would give

\[
 \mathcal D_{1/4}(\mathcal T)
 \ll_K m\,\frac{\mathcal L_{\rm loc}(N,Q)\|c\|_2^2}{V^2}.
 \tag{19}
\]

The same source inequality by itself does not produce (V).  Indeed, taking
(c) supported on the unit ideal merely gives the unconditional local count
(mathcal M_{1/4}\ll_K(1+16Q^2)(\log(4Q))^A), a family-cardinality-scale
bound.  It does not improve (11) to a subpower statement.

Thus the exact missing detector input is a common (c), a uniform threshold
(V), and the inequality

\[
 \frac{\mathcal L_{\rm loc}(N,Q)\|c\|_2^2}{V^2}
 \ll_K\frac{\mathcal D_{\rm target}}m.
 \tag{20}
\]

For the fixed-ray cubic budget from the preceding artifact,
(mathcal D_{\rm target}) is the displayed
(H z_{\mathcal B}^2/(\Gamma_{\rm Th}\|u_{\mathfrak f}\|_2^2)) scale.
Equation (20) is not presently established.

## 6. The weakest usable occupancy hypothesis

For this particular L2-to-discrete method, the logically weakest missing
input is directly

\[
 \mathcal D_\Delta(\mathcal T)\leq\mathcal D_{\rm target},
 \tag{21}
\]

or a new localized theorem that bypasses (5).  Among hypotheses stated as a
one-point cross-character height occupancy condition, the weakest natural
one is exactly

\[
 \operatorname{OCC}_\Delta(M):\qquad
 \mathcal M_\Delta(\mathcal T)\leq M.
 \tag{22}
\]

It gives (2), and (14) proves that the multiplier (mM) is sharp.  Therefore
the exact one-point hypothesis needed for a target
(mathcal D_{\rm target}) is

\[
 \operatorname{OCC}_\Delta(\mathcal D_{\rm target}/m).
 \tag{23}
\]

A labelled occupancy bound is sufficient but stronger: multiple labelled
rows at one height do not enlarge the time projection relevant to
(mathcal D_\Delta).

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_detector_local_occupancy_v1.py --check
python3 -m unittest tests/test_p7_detector_local_occupancy_v1.py -v
```
