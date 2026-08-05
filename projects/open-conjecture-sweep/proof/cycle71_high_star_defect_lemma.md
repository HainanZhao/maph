# High-star defect lemma

**Theorem (`PROVED`).** Let \(H\) be an intersecting 6-partite 6-uniform
hypergraph with \(\tau(H)=6\).  Define its excess pair-intersection count by

\[
D(H)=\sum_{\{E,F\}\subseteq E(H)}(|E\cap F|-1).
\]

Then \(D(H)\ge5\).

**Proof.** The general degree inequality of
[Francetić--Herke--McKay--Wanless, Theorem 2.3](https://arxiv.org/abs/1508.00951),
with \(r=6\), excludes maximum degree \(4\) and \(5\): its left minus right
side is \(-284\) and \(-719/4\), respectively. Choose
a vertex \(v\) of degree \(d\ge6\).  Let \(\mathcal L_v\) be its star and
let \(R\) be the noncentral vertices lying on at least two members of
\(\mathcal L_v\).

Any line \(L\not\ni v\) intersects all \(d\) star lines. Its vertex in the
side of \(v\) is not \(v\), leaving only five positions where those
intersections can occur. Since \(d\ge6\), two star lines meet \(L\) at one
of those positions, a vertex in \(R\). Thus \(R\) covers every line outside
the star, and \(v\) covers every star line. Therefore \(\{v\}\cup R\) is a
cover. Since \(\tau(H)=6\), \(|R|\ge5\).

If \(k_r\) is the number of star lines through \(r\in R\), restrict the
excess count to pairs of star lines:

\[
D(H)\ge \sum_{\{E,F\}\subseteq\mathcal L_v}(|E\cap F|-1)
=\sum_{r\ne v}\binom{k_r}{2}\ge |R|\ge5.
\]

Thus \(D(H)\ge5\). \(\square\)

**Boundary.** This is a necessary nonlinearity condition for a hypothetical
counterexample. It does not produce a five-cover, classify equality, or prove
the conjecture.
