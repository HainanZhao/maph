# C92 Frankl temperature-continuation source audit

`PROVED` source convention: Zargar, *The union-closed sets conjecture for
non-uniform distributions*, Corollary 1.4, works in the intersection-closed
dual.  For \(k\ge5\) and \(1\le m\le\sqrt{k}\), it gives an element \(i\)
with
\[
 f_i(m/k)=
 \frac{\sum_{A\in\mathcal I:i\notin A}(m/k)^{|A|}}
      {\sum_{A\in\mathcal I}(m/k)^{|A|}}\ge\frac12.
\]
Thus \((k,m)=(9,3)\) legally fixes \(t=1/3\).  At \(t=1\), the same
inequality is exactly the intersection-closed dual of uniform Frankl.

`OBSERVED` bounded proof-language audit: the accessible primary text states
the conclusion as “there is an \(i\)” at each fixed weight and explicitly
poses which other temperatures work.  Its theorem/corollary statements do
not supply a common element across two temperatures, a witness-set
intersection theorem, or monotonicity of the identity of a witness.  This is
not a claim that no such lemma exists elsewhere; it clears only the direct
statement-overlap check required for the finite falsifier.

The C92 property is therefore `CONJECTURED`: for every finite
intersection-closed \(\mathcal I\), do the two witness sets
\(W_{1/3}=\{i:f_i(1/3)\ge1/2\}\) and
\(W_1=\{i:f_i(1)\ge1/2\}\) intersect?  It is stronger than both endpoint
statements and is not claimed to imply a pathwise monotonicity theorem.

The source's assumptions do not require a minimal or separating convention.
C92 nevertheless freezes the nontrivial full-labelled-universe subdomain
\(\bigcup\mathcal I=[4]\), \(\varnothing\in\mathcal I\), and
\(|\mathcal I|\ge2\), so its witness labels have a fixed four-coordinate
meaning.  This is a deliberately scoped finite control, not a replacement for
the source theorem's full domain.
