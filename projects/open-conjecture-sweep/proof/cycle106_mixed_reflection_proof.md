# C106 mixed-reflection prime-power obstruction

**`PROVED` claim.** Let (q\equiv7\pmod8) be a prime power. If
(C=A\sqcup Bs\subset D_{2q}), (A=-A), (0\notin A), and
(|A|+|B|=q), then its degree-q Cayley Seidel matrix cannot have all
off-diagonal square entries in ({0,-4}).

For (S=J-I-2M), direct expansion gives, for (g\ne e),

\[
(S^2)_{e,g}=-2q-2+4(1_C(g)+(1_C*1_C)(g)).
\]

For a reflection (g=r^ts), (1_C(g)=1_B(t)) and the two mixed products
give ((1_C*1_C)(g)=2Q(t)), where (Q=1_A*1_B). The required square values
therefore force (1_B(t)+2Q(t)in{(q-1)/2,(q+1)/2}). Parity selects the
lower value when (t\in B) and the upper value otherwise, giving

\[
Q(t)+1_B(t)=(q+1)/4. \tag{1}
\]

Summing (1) gives ((|A|+1)|B|=q(q+1)/4). With (b=|B|) and
(|A|=q-b),

\[
b^2-(q+1)b+q(q+1)/4=0,
\]

so (q+1=(2b-(q+1))^2) is square. Write (q+1=m^2). Since q is odd,
m is even and (q=(m-1)(m+1)), with the two positive odd factors coprime.
If q is a prime power, one factor must be 1, hence (m=2) and q=3,
contrary to (q\equiv7\pmod8). This contradicts the Seidel condition.

The result is confined to the displayed inverse-closed degree-q dihedral
Cayley state; it says nothing about non-Cayley constructions or book-Ramsey.
