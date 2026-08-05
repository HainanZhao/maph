# C80 balance-and-zero-shift compressed profile census

For \(d\in\{6,7\}\), a compressed coordinate is a Gaussian integer \(x+iy\)
which is the sum of \(d\) fourth roots of unity. Exactly when
\[
 |x|+|y|\le d,\qquad x+y\equiv d\pmod 2,
\]
it has such a representation. The coordinate domains have 49 and 64 elements
for \(d=6\) and \(d=7\), respectively.

The executable dynamic-programs ordered strings of \(m=42/d\) coordinates by
their Gaussian sum and squared norm. It joins strings for \(A\) and \(B\)
only at the frozen balances \(\sum A^{(d)}=0\),
\(\sum B^{(d)}=1+i\), and the required combined zero-shift norms \(74\)
and \(72\).

The reported count is an exact **upper bound** before every nonzero
compressed-PAF constraint. It is useful only to decide whether balance and
zero-shift constraints alone give a tractable interface; it is not a candidate
census and does not support an existence, nonexistence, or lift claim.
