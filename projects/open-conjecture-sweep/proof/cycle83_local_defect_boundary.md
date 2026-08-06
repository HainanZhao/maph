# C83 exact boundary: local ordered-tip mechanisms

## Outcome

`PROVED`: for any fixed comparable pair \(x<y\) in a finite poset and any
third element \(z\), uniform linear-extension counts satisfy
\[
 E[x<z]-E[y<z]=E[x<z<y]=E[z<y]-E[z<x].
\]
The exact C81 and C82 controls replay this identity for, respectively, 84 and
78 marked triples.

`PROVED`: the two mechanisms selected to strengthen that identity both fail
on the frozen controls.  In 30 of 434 nonempty C81 interval fibers,
conditioning on \(x<z<y\) and \(x<w<y\) reverses the global strict
pair-majority direction between \(z,w\).  A pairing that preserves the word
outside \(z,w\) has a nonzero signed fiber in 216 of the 252 C81 marked
quadruples with a global \(z\to w\) majority arrow.  The C82 named fiber is
empty, so it supplies no pairing evidence.

`PROVED`: Oracle's final global-defect proposal is false on both frozen
controls.  For every marked \(x<y\) it proposed
\[
 \Pr(z<w)+\Pr(w<x)+\Pr(y<z)\le \tfrac32.
\]
Exact scans find 18 violations among 504 C81 marked quadruples, with maximum
\(2196/1431\) at \((x,y,z,w)=(1,2,4,6)\), and 768 violations among 6084 C82
quadruples, with maximum \(1143450/571725=2\) at \((0,1,2,10)\).

## Claim boundary

These results close only C83's local-fiber and global-defect method family.
They neither produce an ordered two-triangle LEM configuration nor refute or
prove Gupta's equal simple-cycle-spectrum question.  In particular, no frozen
control realizes the complete ordered-tip two-triangle hypothesis, so its
failure cannot be read as a counterexample to a still more specific
extension-graph flow.

## Decision and falsification

The cycle's preregistered pivot condition is met: no explicit charge map or
injection emerged, while its last precise defect inequality has exact
counterexamples.  Return to portfolio discovery rather than add another
fiberwise variant.  This boundary would be falsified by an arithmetic error in
the enumerated extension counts or in any stated marked-tuple count; each is
replayed by the frozen checkers.
