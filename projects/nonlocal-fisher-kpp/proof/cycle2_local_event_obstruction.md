# Cycle 2 frozen result — local event closure obstruction

## Claim boundary

`CONJECTURED` under the repository promotion policy, pending independent
proof audit: no exact hump-event law whose state is only the complete local
germ of a positive profile at a regular level can reproduce the level
velocity of every solution of the radius-one top-hat Fisher--KPP equation.

This does not rule out an asymptotic event map carrying a nonlocal competition
trace, and it makes no claim about P1/P2 or a selected wavelength.

## Exact identity

For $W=\log u$, $C=K*u$, and a regular level
$W(X(t),t)=\log\theta$,

\[
X'(t)=-\frac{D(W_{xx}+W_x^2)+1-C}{W_x}.
\]

The right side depends on the window trace $C$, which is not determined by
the local germ of $u$ at $X$.

## Frozen counterexample

At $X=0$, take

\[
u_0(x)=2-\frac{x}{1+x^2}
\]

and, for sufficiently small $\varepsilon>0$,

\[
u_\varepsilon=u_0+\varepsilon h,\qquad
h(x)=\begin{cases}
((x-\tfrac14)(\tfrac34-x))^3,&x\in[\tfrac14,\tfrac34],\\
0,&\text{otherwise}.
\end{cases}
\]

Both profiles are positive and identical on a neighborhood of zero, so their
complete local germs and the regular level $u(0)=2$ agree. The bump is $C^2$
and has exact mass $1/17920$. Consequently,

\[
(K*u_\varepsilon)(0)-(K*u_0)(0)=\frac{\varepsilon}{35840}.
\]

Since the common values are $u(0)=2$ and $u_x(0)=-1$, the two instantaneous
level velocities differ by

\[
X_\varepsilon'(0)-X_0'(0)=-\frac{\varepsilon}{17920}\ne0.
\]

Thus equal local-event states have unequal exact transitions. The killed
state class is local-germ-only closure; the missing observable is at least
the window competition trace $K*u$.
