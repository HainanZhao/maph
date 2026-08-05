# C80 periodic compression identity

For a length-\(n=dm\) complex sequence \(C\), define
\[
 C^{(d)}_r=\sum_{t=0}^{d-1}C_{r+tm}\qquad(r\in\mathbb Z/m\mathbb Z)
\]
and use \(\operatorname{PAF}_C(s)=\sum_{j\bmod n}C_j\overline{C_{j+s}}\).
Grouping the double sum by the residue \(u=t'-t\bmod d\) gives
\[
 \operatorname{PAF}_{C^{(d)}}(s)
 =\sum_{u=0}^{d-1}\operatorname{PAF}_C(s+um).
\]
Consequently a quaternary Legendre pair at length \(42\) compresses to a
pair with total PAF \((74,-12,\ldots,-12)\) for \(d=6,m=7\), and
\((72,-14,\ldots,-14)\) for \(d=7,m=6\). The zero row is
\(84-2(d-1)\), because exactly one of the \(d\) folded original PAF rows is
the original shift-zero row.

This source is a frozen C80 convention control. The executable exhausts all
quaternary pairs at lengths 2 and 6 and checks this identity for every
divisor compression of each accepted control pair. It makes no length-42
existence or lift claim.
