# SIC--Stark research cycle 101: the archimedean parity-twist gate

Date: 2026-07-28

## Question

Can a Dirichlet twist move the mixed-signature character into the scope
of a proved totally-odd strong Stark theorem?

## Exact parity calculation

Write archimedean parity at the two real places of
\(K=\mathbf Q(\sqrt{21})\) as a vector in \((\mathbf Z/2)^2\).  Up to
place labeling, the target has parity

\[
 (0,1).
\]

A Dirichlet character of \(\mathbf Q\), restricted to \(K\), has the
same parity at both real places.  Its parity is therefore either

\[
 (0,0)\quad\text{or}\quad(1,1).
\]

Scalar twisting can consequently produce only

\[
 (0,1)+(0,0)=(0,1),\qquad
 (0,1)+(1,1)=(1,0).
\]

It can swap which real place is odd, but it cannot make the character
totally odd or totally even.  The certificate is

```text
scripts/dimension_six_parity_twist_gate.py
```

## Theorem coverage

Nickel's proved strong Stark result applies to totally odd characters in
the CM setting, not to this mixed parity
([arXiv:2106.05619](https://arxiv.org/abs/2106.05619)).
Ferrara explicitly develops a \(p\)-adic \(L\)-function for mixed
signature real-quadratic characters, but the corresponding statement is
posed as a conjecture; the proved comparison in that paper is for the
imaginary-quadratic split-\(p\) case
([arXiv:1904.10561](https://arxiv.org/abs/1904.10561)).

Thus neither theorem can be imported after a harmless scalar twist.

## Result

\[
\boxed{\text{mixed archimedean parity is stable under scalar twisting.}}
\]

Together with cycle 99, this rules out both conductor descent and parity
descent.  A proof must treat the original mixed-signature representation
or establish the finite cyclic-limit identity directly.

