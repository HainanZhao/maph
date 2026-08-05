# Diagonal three-qubit slice of compatible spin alignment

## Consistency lemma — PROVED, prior result

Let \(Q=\operatorname{diag}(q,1-q)\) with \(1/2\le q\le1\), and put

\[
 H(\rho)=\frac13\bigl(\rho_{AB}\otimes Q_C+\rho_{AC}\otimes Q_B+
 Q_A\otimes\rho_{BC}\bigr).
\]

If the three-qubit state \(\rho\) is diagonal in the computational basis,
then \(H(\rho)\preceq H(|000\rangle\langle000|)\).  Thus Song--Chen
Conjecture 2 holds for diagonal three-qubit states with uniform two-body
weights and diagonal \(Q\).

This is not new: it is a direct special case of M. A. Alhejji and E. Knill,
*Towards a resolution of the spin alignment problem*, Proposition IV.5, which
allows an arbitrary classical state tuple and probability measure.  The exact
calculation below is retained solely as a conventions/replay cross-check for
the compatible-marginal specialization.  It does not address coherent
off-diagonal states, nonuniform weights, higher local dimension, or more
parties.

## Proof

Write \(T=H(|000\rangle\langle000|)\), and for a bit string \(x\) write
\(H_x=H(|x\rangle\langle x|)\).  These matrices are diagonal.  Directly
sorting their eight affine diagonal entries gives the following table of
\(K_k(T)-K_k(H_x)\), where \(K_k\) is the sum of the largest \(k\)
eigenvalues.  Unlisted entries are zero.

| Hamming weight of \(x\) | interval | nonzero differences |
| --- | --- | --- |
| 0 | all | none |
| 1 | all | \(k=1:(2q-1)/3\) |
| 2 | all | \(k=1:(4q-2)/3,\quad k=2:(2q-1)/3\) |
| 3 | \([1/2,3/4]\) | \(k=1:2q-1,\ k=2:(4q-2)/3,\ k=3:(2q-1)/3\) |
| 3 | \([3/4,1]\) | \(k=1:2q/3,\ k=2:1/3,\ k=3:2(1-q)/3\) |

Every displayed quantity is nonnegative on its stated interval.  Hence
\(H_x\preceq T\) for each of the eight basis strings.  The exact affine
entry/chamber enumeration in `cycle77_diagonal_slice.py` independently checks
all 63 basis/chamber/Ky-Fan rows; `check_cycle77_diagonal_table.py` checks the
displayed table separately.

Finally, a diagonal state is \(\rho=\sum_xp_x|x\rangle\langle x|\), so
\(H(\rho)=\sum_xp_xH_x\).  Ky Fan sums are convex, therefore

\[
 K_k(H(\rho))\le\sum_xp_xK_k(H_x)\le K_k(T)
\]

for every \(k\), and the traces agree.  This is exactly
\(H(\rho)\preceq T\). \(\square\)

## Replay

```sh
python3 proof/cycle77_diagonal_slice.py
python3 proof/check_cycle77_diagonal_table.py
```
