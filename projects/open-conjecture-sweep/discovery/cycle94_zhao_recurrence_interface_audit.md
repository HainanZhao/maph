# C94 Zhao recurrence-interface audit

## Question

C94 proposed a uniform-in-\(n\), fixed-diagram recurrence for
\[
 t_{\rm Cay}(K_{5,5}\setminus C_{10};S_n,\mathbf 1_{T_1T_2})
\]
over Zhao's full family of arbitrary subgroup pairs \(T_1,T_2\leq S_n\).
Before treating an \(S_4\) or \(S_5\) calculation as a recurrence test, the
state that a putative recurrence would transfer must be specified.

## Source-fixed interface

`PROVED` from Zhao, *Conjugacy Class Averages and Sidorenko's Conjecture*,
arXiv:2606.15368v1, Proposition 1.1 / the Cayley-form Szegedy reduction and
the proof of Theorem 1.3: the quantified inputs are, independently for every
\(n\), all pairs \(T_1,T_2\leq S_n\), with connection set \(T_1T_2\).
The source supplies no inclusion-compatible tower
\((T_{1,n},T_{2,n})\subseteq S_n\) and no transition map from a pair at
\(n\) to a pair at \(n+1\).

For the frozen labelled Möbius graph, the translation-fixed contraction in
`proof/cycle_51_conjugacy_averaging_soundness.md` has denominator
\(|\Gamma|^9\): it fixes one left vertex, sums the other four left variables,
and then the five independent right variables.

## State-only recurrence obstruction

Consider the precise proposed schema in which a fixed finite diagram state
and its transition coefficients depend on \(n\) only—not on fresh,
unbounded data describing \(T_1,T_2\).  Such a recurrence cannot represent
Zhao's full input family.

`PROVED`: at \(n=1\) there is only one subgroup pair.  At \(n=2\), the two
valid pairs
\[
(T_1,T_2)=(\{e\},\{e\})\quad\hbox{and}\quad(T_1,T_2)=(S_2,S_2)
\]
have connection sets \(\{e\}\) and \(S_2\), respectively.  For a connected
bipartite graph with ten vertices, the identity connection set forces every
vertex label to equal the first fixed left label, so its normalized density is
\(|S_2|^{-(10-1)}=2^{-9}\).  The full connection set has density \(1\).
Both cases have the identical unique \(S_1\) predecessor.  Thus an
\(n\)-only transition from a subgroup-free \(S_1\) state has one output, but
the required \(S_2\) outputs differ.

This is deliberately narrow: it refutes only the stated state-only transfer
schema.  A recurrence carrying new subgroup-specific data is not refuted, but
its state is not a fixed finite diagram basis unless a further compression
theorem is proved.

## Consequence for C94

`PROVED`: an \(S_4\) or \(S_5\) contraction cannot falsify or validate the
unqualified C94 recurrence idea, because the idea lacked a transition on
Zhao's quantified inputs.  It would again be a finite census.

`CONJECTURED` next viable bridge: restrict first to a source-justified,
inclusion-compatible family of subgroup towers (for example a fixed Young or
wreath-product construction), and derive a diagram recurrence whose state
explicitly records the induced stabilizer/intersection data.  Its falsifier
must be a named tower and a direct contraction whose exact value disagrees
with the symbolic transition.  Such a restricted theorem would not by itself
cover Zhao's all-subgroup condition; that containment must be proved rather
than assumed.

## Stop/pivot criterion

Do not preregister a symmetric-group computation until a concrete tower,
state map, symbolic transition, and direct disagreement criterion are all
specified.  If no source-defined tower covers the arbitrary-subgroup
quantifier, return to wide portfolio discovery instead of enlarging the
finite-group ladder.
