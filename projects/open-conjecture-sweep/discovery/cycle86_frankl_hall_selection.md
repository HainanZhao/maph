# C86 selection: all-inclusion Hall transport for height-four Frankl

## Creative comparison

`CONJECTURED` candidates were a rank-layer Hall transport for finite
union-closed families of dimension three, an inverse global-dual construction
for intersecting Ryser at \(r=6\), and a degree-normalized entropy route for
the Möbius-ladder Sidorenko problem.  The Ryser cone is not yet a defined
certificate state space after C69--C72.  The Sidorenko route lacks a new
small exact verifier and would risk reopening C85's step-kernel behavior.

## Question the target

The target is not another small family census: it is whether the source's
immediate-cover injection can be replaced by a genuine inclusion matching.
For a family \(\mathcal F\) and element \(x\), let \(G_x\) have left
\(\mathcal F_x^c\), right \(\mathcal F_x\), and an edge \(A\!\to B\)
exactly when \(A\subseteq B\).  A matching saturating the left side proves
that \(x\) is abundant.  The selected `CONJECTURED` mechanism is that a
finite separating union-closed family of dimension three has an optimal
\(x\) with this property.

## Question the critique

All-inclusion Hall transport can be strictly stronger than abundance, so a
failure may be immediate even where Frankl is true.  A pass on four points is
not evidence for dimension three in general.  The point of the gate is to
decide whether the proposed repair survives the source's precise
immediate-cover obstruction before theory work, not to infer a theorem from a
finite census.

## Oracle selection

Oracle selected the all-inclusion Hall mechanism over the rejected Ryser and
Sidorenko routes.  The exact gate enumerates all \(2^{16}=65,536\) labelled
subfamilies of \(\mathcal P([4])\), retaining only nontrivial, union-closed,
full-universe, separating, dimension-three families.  For each retained
family it tests every optimal element by maximum matching and independently
by Hall subsets.  The published dimension-three Examples 3.19 and 3.20 are
mandatory controls.

The falsifier is one retained family in which every optimal element has a
Hall-deficient left subset.  A failure rejects only this all-inclusion
transport mechanism.  A full pass authorizes only an attempted rank-layer
Hall lemma; it does not authorize an \([5]\) census.
