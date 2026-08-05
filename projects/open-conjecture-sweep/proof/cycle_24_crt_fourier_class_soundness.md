# Cycle 24: CRT/Ramanujan class capacity dual

For (p=199,c=14), identify a time with its CRT coordinates
((\alpha,\beta)\in\mathbb Z_{199}\times\mathbb Z_{14}).  Partition times
into the eight classes

\[
 (\mathbf1_{\alpha\ne0},\gcd(\beta,14))
 \in\{0,1\}\times\{1,2,7,14\}.
\]

`PROVED`: these are the common level sets of the tensor product of the
Ramanujan class algebras.  The (199)-factor has basis
(1,R_{199}\), with (R_{199}(0)=198) and (R_{199}(x)=-1) otherwise;
the (14)-factor has the four divisor-Ramanujan functions.  Their evaluation
matrix has nonzero integer determinant, so every class-constant weight has a
unique representation in this low-degree Fourier basis.

Let (z_r\ge0) be a class-constant weight and let (n_r) be the size of
class (r).  For a fixed coordinate block and allowed option (o), write
(v_{B,o,r}) for the number of covered times in class (r).  Then

\[
 W=\sum_r n_rz_r,\qquad
 U=\sum_B\max_o\sum_rv_{B,o,r}z_r.
\]

The standard capacity argument gives (W\le U) for every global selection
which covers every time.  Therefore an integer (z) with (U<W) excludes
the named leaf after direct-CNF replay.  `PROVED`: exhaustive cutting-plane
separation is equivalent to the finite all-option class LP when no omitted
option is violated, by the same feasible-set inclusion argument as Cycle 23.

The class score and floating LP are `OBSERVED` discovery tools.  Failure of
this eight-class family says nothing about other characters, other weights,
partitions, a semantic primal model, or (LRC(13)).
