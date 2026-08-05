# C63 exact S3 orbit space

## Coordinates

Use the fixed S3 order from C55--C62 and write

\[
 a_e=e,\qquad (a_1,a_2,a_5)=(t+x,t+y,t+z),\quad x+y+z=0,
 \qquad (a_3,a_4)=(c+s,c-s).
\]

Set

\[
 r_2=x^2+y^2+z^2,\quad u=xyz,\quad s_2=s^2,
 \quad \delta^2=\tfrac12r_2^3-27u^2.
\]

The deviations are the roots of

\[
 X^3-\frac{r_2}{2}X-u.
\]

Its discriminant is `delta^2`.  Consequently a real tuple in the projected
orbit coordinates `(e,t,c,r2,u,s2)` comes from a normalized nonnegative S3
function if and only if

\[
\begin{aligned}
 &e+3t+2c=1,\\
 &e,t,c,r_2,s_2\geq0,\\
 &\tfrac12r_2^3-27u^2\geq0,\\
 &3t^2-\tfrac12r_2\geq0,\\
 &t^3-\tfrac12tr_2+u\geq0,\\
 &c^2-s_2\geq0.
\end{aligned}
\]

## Proof of equivalence

Necessity follows from the coordinate definitions.  In particular,

\[
\sum_{i<j}(t+x_i)(t+x_j)=3t^2-\frac{r_2}{2},\qquad
\prod_i(t+x_i)=t^3-\frac{tr_2}{2}+u.
\]

Conversely, nonnegative discriminant makes the depressed cubic have three
real roots `x,y,z` with sum zero and the prescribed `r2,u`.  Put
`q_i=t+x_i`.  Their sum, pair sum, and product are respectively

\[
3t,\qquad 3t^2-\frac{r_2}{2},\qquad
t^3-\frac{tr_2}{2}+u.
\]

These are nonnegative under the displayed conditions.  If exactly one real
`q_i` were negative, its product with two positive roots would be negative;
the zero boundary case instead forces the pair sum negative unless all other
nonzero roots have the same nonnegative sign.  If two roots were negative,
write them `-a,-b` with `a,b>0`.  Since the sum is nonnegative, the third root
`d` satisfies `d>=a+b`, while the pair sum is
`ab-d(a+b) <= ab-(a+b)^2 < 0`, a contradiction.  Hence all three are
nonnegative.  Finally `c>=0`, `s2>=0`, and `c^2>=s2` permit a real
`s` with `s^2=s2` and imply `c+s,c-s>=0`.  This constructs the original
nonnegative function.  The normalization equation gives total mass one.

## Enlarged symmetry and dimension drop

The exact source polynomial is invariant under every permutation of the three
transposition variables and, independently, under swapping the two cycle
variables.  The audit compares all twelve coefficient maps.  Therefore its
centralization deficit lies in

\[
 \mathbb Q[e,t,c,r_2,u,s_2],
\]

not merely in the joint conjugation-invariant ring that also permits
`w=s(x-y)(y-z)(z-x)`.  The exact invariant-span reconstruction has zero
`w` terms.  Thus the projected six-coordinate semialgebraic set above loses no
information relevant to the deficit.  This is an exact continuous reduction;
it is not yet a sign proof or a classification of its minima.

## Exact stationary-stratum reduction

Equivalently, put

\[
 T_1=q_1+q_2+q_3,\quad T_2=\sum_{i<j}q_iq_j,
 \quad T_3=q_1q_2q_3,qquad
 C_1=v_1+v_2,\quad C_2=v_1v_2,
\]

for the three transposition values `q_i` and two cycle values `v_i`.  The
exact conversion writes the deficit as

\[
 P(e,T_1,T_2,T_3,C_1,C_2).
\]

For `{i,j,k}={1,2,3}`, direct differentiation gives

\[
 \frac{\partial P}{\partial q_i}-\frac{\partial P}{\partial q_j}
 =(q_j-q_i)(P_{T_2}+q_kP_{T_3}),
\]

and

\[
 \frac{\partial P}{\partial v_1}-\frac{\partial P}{\partial v_2}
 =(v_2-v_1)P_{C_2}.
\]

Hence every full-support stationary point falls into the following exact
multiplicity strata.

- If the three `q_i` are distinct, then `P_T2=P_T3=0`.  If exactly two
  equal `a` and the third differs, then `P_T2+a*P_T3=0`.  If all three
  agree, no transposition-shape equation is imposed.
- If `v_1!=v_2`, then `P_C2=0`.  If they agree, no cycle-shape equation is
  imposed.

On the fully distinct stratum, equality of all six simplex derivatives is
therefore exactly the six-equation system

\[
 P_{T_2}=P_{T_3}=P_{C_2}=0,\qquad
 P_e-P_{T_1}=P_e-P_{C_1}=0,\qquad e+T_1+C_1=1.
\]

The generated packet records this system coefficient by coefficient.  On a
two-equal transposition stratum the common transposition derivative is
`P_T1-a^2*P_T3`; on the all-equal stratum it is
`P_T1+2*a*P_T2+a^2*P_T3`.  On the equal-cycle stratum the common cycle
derivative is `P_C1+v_1*P_C2`.  These formulas give the remaining finite
list of multiplicity systems without division by a discriminant.  Original
simplex boundaries are obtained by setting a support coordinate to zero and
replacing equality by the standard complementary-slackness inequality for
that coordinate.

This classifies the equations any minimum must satisfy, but it does not by
itself prove that the polynomial ideals are zero-dimensional or that their
feasible real roots have nonnegative deficit.
