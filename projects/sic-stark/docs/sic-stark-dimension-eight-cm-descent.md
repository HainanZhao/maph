# Dimension-eight projective CM-descent gate

## Result

The literal test
\[
\chi^\sigma=\chi^{-1}
\]
fails for both quartic characters because \(\sigma\) interchanges the
two labeled infinite places.  The projective test nevertheless passes:
\[
\theta_\chi:=\chi(\chi^\sigma)^{-1}
\]
is the same order-two character for \(\chi=[1,0,0]\) and
\(\chi=[1,1,0]\).

On the full ray group
\[
\operatorname{Cl}_{(24)\infty_1\infty_2}(\mathbb Q(\sqrt5))
\cong C_4\times C_2^3,
\]
base conjugation has matrix
\[
\begin{pmatrix}
3&2&0&2\\
0&1&0&0\\
0&1&1&0\\
0&0&0&1
\end{pmatrix}.
\]
The exact dual-coordinate calculation is:

| one-place character | full pullback | conjugate | inverse | projective quotient |
|---|---|---|---|---|
| \([1,0,0]\) | \([3,0,0,0]\) | \([1,1,0,1]\) | \([1,0,0,0]\) | \([2,1,0,1]\) |
| \([1,1,0]\) | \([3,0,0,1]\) | \([1,1,0,0]\) | \([1,0,0,1]\) | \([2,1,0,1]\) |

The class field of the kernel of \([2,1,0,1]\) is
\[
\mathbb Q(\sqrt5,\sqrt{-6}).
\]
Its three quadratic subfields are
\[
\mathbb Q(\sqrt5),\qquad
\mathbb Q(\sqrt{-6}),\qquad
\mathbb Q(\sqrt{-30}).
\]
Thus the induced representations have projective image \(V_4\).
The two imaginary quadratic fields provide the promised CM-descent
candidates.

The exact computation is in
`scripts/dimension_eight_cm_descent.gp`, with transcript
`certificates/dimension-eight-cm-descent.txt`.

## What remains

This does not yet prove the two oriented identities in the paper.
The remaining tasks are:

1. Construct the actual Hecke characters over
   \(\mathbb Q(\sqrt{-6})\) or \(\mathbb Q(\sqrt{-30})\) whose
   inductions equal the two linear Artin representations, including
   any scalar twist invisible projectively.
2. Determine their exact finite conductors and infinity types.
3. Match the Euler factors removed in the paper's \(L_S\)-functions.
4. Translate the imaginary-quadratic Kronecker-limit formula, including
   roots of unity and reciprocity conventions, into the oriented
   resolvents \(R_0,R_1\).
5. Use the existing separated \(10^{-114}\) enclosures only after that
   exact algebraic candidate set has been established.

This makes dimension eight materially closer than dimension six.
For the dimension-six order-six character, the corresponding
projective quotient has order three, so the \(V_4\) re-induction
mechanism is unavailable.
