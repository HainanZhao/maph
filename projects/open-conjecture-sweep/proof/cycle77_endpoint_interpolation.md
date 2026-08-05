# Endpoint interpolation for the compatible three-qubit gate

## Theorem — PROVED

Let \(\rho_{ABC}\) be any three-qubit state, let \(a,b,c\ge0\) with
\(a+b+c=1\), and let \(Q_q=\operatorname{diag}(q,1-q)\) with
\(1/2\le q\le1\).  Then

\[
\begin{aligned}
H_q={}&a\rho_{AB}\otimes Q_q+b\rho_{AC}\otimes Q_q
       +cQ_q\otimes\rho_{BC}\\
\preceq{}&a|00\rangle\!\langle00|_{AB}\otimes Q_q+
 b|00\rangle\!\langle00|_{AC}\otimes Q_q+
 cQ_q\otimes|00\rangle\!\langle00|_{BC}=:T_q.
\end{aligned}
\]

Consequently Song--Chen Conjecture 2 holds for every compatible three-qubit
state when \(\mu\) is supported on \(AB,AC,BC\), with arbitrary weights and
an arbitrary qubit state \(Q\).

This is narrower than the full compatible-marginal conjecture: it does not
cover other subset supports, more parties, or local dimension above two.

## Proof

After a local unitary, write \(Q_q=\operatorname{diag}(q,1-q)\), and put
\(t=2q-1\).  Then

\[
Q_q=(1-t)\frac{I}{2}+t|0\rangle\langle0|,
\qquad H_q=(1-t)H_{1/2}+tH_1,
\qquad T_q=(1-t)T_{1/2}+tT_1.
\]

Song--Chen, Proposition 3, states \(H_{1/2}\preceq T_{1/2}\) for exactly
these compatible marginals and arbitrary nonnegative \(a,b,c\).  At the
other endpoint \(H_1\) is a density matrix, while \(T_1=|000\rangle
\langle000|\); hence \(H_1\preceq T_1\).

Permute systems so that \(a\ge b\ge c\).  The diagonal entries of \(T_q\)
in decreasing order are

\[
q,\quad (1-q)a,\quad(1-q)b,\quad(1-q)c,\quad0,0,0,0.
\]

Indeed \(q\ge1-q\ge(1-q)a\), so their order never changes.  Thus every
Ky Fan sum of \(T_q\) is affine in \(t\):

\[
K_k(T_q)=(1-t)K_k(T_{1/2})+tK_k(T_1).
\]

Ky Fan convexity now gives, for every \(k\),

\[
\begin{aligned}
K_k(H_q)&\le(1-t)K_k(H_{1/2})+tK_k(H_1)\\
&\le(1-t)K_k(T_{1/2})+tK_k(T_1)=K_k(T_q).
\end{aligned}
\]

The traces are equal, proving the claimed majorization. \(\square\)

## Exact replay

```sh
python3 proof/check_cycle77_endpoint_interpolation.py
```
