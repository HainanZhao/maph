# SIC--Stark research cycle 74: CM conductors and ray characters

Over \(M_6=\mathbf Q(\sqrt{-6})\), the two quartic character fields have
absolute equations

\[
\begin{aligned}
E_0:\;&X^8-4X^6-12X^5+18X^4+48X^3-16X^2-168X+166,\\
E_1:\;&X^8-4X^7+8X^5+28X^4+96X^3+144X^2+96X+24.
\end{aligned}
\]

Their conductor is represented in PARI by

\[
[[60,36;0,2],[]],
\]

with local exponents \(3,1,1\) at the selected primes above \(2,3,5\).
The ray group is \(C_8\times C_4\).  For the chosen relative factors the
two conjugate dual characters are

\[
[6,1],[2,3]\quad\text{and}\quad[2,1],[6,3].
\]

Both imaginary quadratic base computations satisfy
`bnfcertify=1`.  The corresponding \(M_{30}\) conductors and characters
are also printed by the exact reinduction script, but \(M_6\) gives the
more convenient unit models used below.
