# C105 complement-translate obstruction

**`PROVED` claim.** Let (q\equiv7\pmod8), (A=-A\subseteq\mathbb Z_q)
with (0\notin A), and (B=\mathbb Z_q\setminus A). In
(D_{2q}=\langle r,s\mid r^q=s^2=1,srs=r^{-1}\rangle), the Cayley
connection set

\[
C=\{r^a:a\in A\}\sqcup\{r^bs:b\in B\}
\]

cannot yield a Seidel matrix whose off-diagonal square entries belong to
\(\{0,-4\}\).

Put (k=|A|) and (P(t)=|\{x\in A:x-t\in A\}|). Since (C=C^{-1})
and (|C|=q), the associated graph is q-regular on (2q) vertices, so
(S\mathbf1=-\mathbf1). For (g\ne e), direct expansion of
(S=J-I-2M) gives

\[
(S^2)_{e,g}=-2q-2+4(1_C(g)+(1_C*1_C)(g)). \tag{1}
\]

For (g=r^t), (t\ne0), the two rotation--rotation and
reflection--reflection products give

\[
1_C(r^t)+(1_C*1_C)(r^t)=1_A(t)+2P(t)+q-2k. \tag{2}
\]

Equation (1) would force (2) into
\(\{(q-1)/2,(q+1)/2\}\). Its parity is (1_A(t)+1\), while the lower
and upper values have parity odd and even, respectively. Thus both cases
give

\[
P(t)=k-(q+1)/4\quad(t\ne0). \tag{3}
\]

Summing (3) over nonzero (t) counts ordered distinct pairs of (A):

\[
k(k-1)=(q-1)(k-(q+1)/4),
\]

whose roots are ((q-1)/2,(q+1)/2). Symmetry with zero excluded makes
(k) even; because (q\equiv7\pmod8), only (k=(q+1)/2) remains. Hence
(P(t)=(q+1)/4), which is even.

Finally, in the fiber defining (P(t)), the involution
((x,y)\mapsto(-y,-x)) has a fixed point precisely when
(x=t/2\in A). Therefore (P(t)\equiv1_A(t/2)\pmod2). Its even constant
value forces (A) empty, contradicting (k=(q+1)/2). This proves the
claim. The proof makes no assertion about non-complement (B), nonsymmetric
(A), arbitrary dihedral sets, or book-Ramsey generally.
