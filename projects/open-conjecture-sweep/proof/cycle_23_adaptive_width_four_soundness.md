# Cycle 23: adaptive width-four partition selection

For a fixed nonnegative time weight vector, let \(M_i\) be the maximum
covered weight of one option at coordinate \(i\), and let \(M_{ij}\) be the
maximum covered weight of a joint option on coordinates \(i,j\).  The exact
pair-overlap saving is

\[
 s_{ij}=M_i+M_j-M_{ij}\ge0.
\]

Cycle 23 uses sums of these exact savings only to rank partitions into one
four-coordinate block and three three-coordinate blocks.  This score is not a
certificate and need not predict the true block deficit.

For the selected partition, the proof criterion remains the Cycle-22 theorem:
with exact block-union masks and nonnegative integer weights,

\[
 W=\sum_t w_t,
 \qquad
 U=\sum_B\max_o\sum_t w_t b_{B,o,t},
\]

and \(U<W\) `PROVES` that the named canonical leaf has no improper lift.
Floating LP solutions and adaptive reselection affect discovery only.  Every
promoted row must be independently rebuilt from the target's original direct
CNF clauses, canonical allowed digits, named partition, and integer weights.

## Exact LP representation

`PROVED`: the bounded cutting-plane implementation has the same optimum as
the displayed finite all-option LP whenever it terminates without a violated
option.  It starts from a subset of the inequalities

\[
 \sum_t w_t b_{B,o,t}\le q_B
\]

and after each restricted solve exhaustively evaluates every option (o) in
every block (B).  If none exceeds its returned (q_B), that point satisfies
every omitted inequality and hence is feasible for the full LP.  Conversely,
every full-LP feasible point satisfies the restricted inequalities.  The two
feasible sets therefore contain one another at termination, so their minima
are equal.  A wall or 512-round cap is recorded as `CAP`; it is never treated
as an LP conclusion.

## Claim boundary

A strict replay excludes only its named leaf.  Failure of the savings oracle,
either LP wave, integerization, or a resource cap proves nothing about other
partitions, Fourier structure, either base, \(F_1\), \(J\), or LRC(13).
