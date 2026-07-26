# A direct proof of the hidden \(N=11\) histogram identity

This note proves, for every integer \(n\geq0\),

\[
\operatorname{hist}\!\left(
(0,1,3,n+2),(1,3,2,n)\right)
=
\operatorname{hist}\!\left(
(0,3,3,n),(1,1,2,n+2)\right).
\tag{1}
\]

The proof is symbolic.  It does not use interpolation or a bounded
computer check.  Its main ingredient is the self-duality of binary
Krawtchouk polynomials.

## 1. From a histogram to four evaluations

Let \(q^4=1\), and put

\[
L_j(q)=\sum_{k=0}^3q^{jk}z_k.
\]

For input occupation \(r\) and output occupation \(s\), define

\[
\mathcal A_q(r,s)
=
\left(\prod_{k=0}^3r_k!\right)
[z^r]\prod_{j=0}^3L_j(q)^{s_j}.
\tag{2}
\]

If \(h_e(r,s)\) is the labelled path-count histogram, then

\[
\mathcal A_q(r,s)=\sum_{e=0}^3h_e(r,s)q^e.
\tag{3}
\]

Consequently two histograms are equal if and only if their quantities
\(\mathcal A_q\) agree at the four fourth roots
\(q=1,i,-1,-i\).  This is just invertibility of the four-point discrete
Fourier transform.

Both inputs in (1) have \(z_0\)-occupation zero.  Write

\[
X=z_1,\qquad Y=z_2,\qquad Z=z_3,\qquad
S=X+Z,\qquad D=X-Z,
\]

and set

\[
N=n+3.
\]

The coefficient sought on the left of (1) is that of
\(X^1Y^3Z^{N-1}\); the coefficient on the right is that of
\(X^3Y^3Z^{N-3}\).  The input-factorial multipliers in (2) are,
respectively,

\[
6(n+2)!\quad\text{and}\quad36n!.
\tag{4}
\]

It will therefore suffice at every fourth root to prove the
unlabelled-coefficient relation

\[
(n+1)(n+2)\,C_L=6C_R.
\tag{5}
\]

## 2. The evaluations at \(q=i\)

At \(q=i\), the four linear forms are

\[
L_0=Y+S,\quad L_1=-Y+iD,\quad
L_2=Y-S,\quad L_3=-Y-iD.
\]

The common part involving \(L_0\) and \(L_2\) is

\[
A(Y,S)=(Y+S)(Y-S)^2
=\sum_{m=0}^3a_mY^{3-m}S^m,
\qquad (a_0,a_1,a_2,a_3)=(1,-1,-1,1).
\tag{6}
\]

More generally, for \(0\leq p\leq N\), put

\[
B_p(Y,D)=(-Y+iD)^p(-Y-iD)^{N-p}.
\]

The left transition uses \(p=3\), while the right transition uses
\(p=1\).  Define the binary Krawtchouk coefficients

\[
K_m(p;N)=
\sum_r(-1)^r\binom pr\binom{N-p}{m-r}.
\tag{7}
\]

Direct binomial expansion gives

\[
[Y^m]B_p(Y,D)
=(-1)^{N-p}i^{N-m}K_m(p;N)D^{N-m}.
\tag{8}
\]

The phase in (8) is identical for \(p=3\) and \(p=1\), since those
indices differ by two.  A second binomial expansion gives

\[
[X^kZ^{N-k}]S^mD^{N-m}
=(-1)^{N-m-k}K_k(m;N).
\tag{9}
\]

Combining (6)--(9), each summand contributing to \(C_L\), corresponding
to \((p,k)=(3,1)\), differs from the matching summand contributing to
\(C_R\), corresponding to \((p,k)=(1,3)\), only through

\[
K_m(3;N)K_1(m;N)
\quad\text{versus}\quad
K_m(1;N)K_3(m;N).
\]

Krawtchouk self-duality in the unnormalised convention (7) says

\[
\binom NpK_m(p;N)=\binom NmK_p(m;N).
\tag{10}
\]

Applying (10) twice yields, term by term,

\[
K_m(3;N)K_1(m;N)
=
\frac{\binom N1}{\binom N3}
K_m(1;N)K_3(m;N)
=
\frac{6}{(N-1)(N-2)}
K_m(1;N)K_3(m;N).
\tag{11}
\]

All signs, phases, and the coefficients \(a_m\) are common to the two
sides.  Since \(N-1=n+2\) and \(N-2=n+1\), summing (11) proves (5) at
\(q=i\).

## 3. The other three evaluations

At \(q=-1\), both output products reduce to the same polynomial:

\[
(Y+S)^3(Y-S)^{n+3}.
\tag{12}
\]

After taking the coefficient of \(Y^3\), the ratio between the
\(X^1Z^{N-1}\) and \(X^3Z^{N-3}\) coefficients is

\[
\frac{\binom N1}{\binom N3}
=\frac{6}{(n+1)(n+2)}.
\]

Thus (5) also holds at \(q=-1\).

At \(q=1\), every single-particle phase is one.  Each labelled
permanent contains \((n+6)!\) terms, so the two labelled evaluations
are equal.  Equivalently, the multinomial coefficient ratio cancels
the input-factorial ratio (4).

Finally, the evaluations at \(q=-i\) are the complex conjugates of
those at \(q=i\), because all histogram entries are real integers.
They are therefore equal as well.

The labelled evaluations agree at all four fourth roots.  Invertibility
of the four-point discrete Fourier transform now proves (1).

## 4. What the proof explains

The equality is genuinely an equality of all four phase counts, not
merely equality of the physical Fourier amplitudes at \(q=i\).
However, its cleanest proof does proceed through the four
root-of-unity evaluations.

At \(q=-1\), the identity is a parity-aggregation symmetry.  At
\(q=i\), the nontrivial equality is the \(1\leftrightarrow3\) instance
of Krawtchouk self-duality.  The factorial weights required to pass
from generating-polynomial coefficients to labelled permanent terms
cancel exactly the binomial ratio in that duality.

Thus the identity is not an accidental agreement of affine
quasipolynomials.  It comes from a discrete Fourier/Krawtchouk duality
hidden by the occupation-vector notation.

## 5. The identity is one instance of a general reciprocity

The argument above does not depend on \(p=3\), \(k=1\), or on the
particular split \(1+2=3\) between output modes zero and two.  It proves
the following stronger statement.

**Odd-split reciprocity theorem.**  Let \(N,d\geq0\), let
\(s_0+s_2=d\), let \(0\leq a\leq d\), and let
\(0\leq p,k\leq N\).  Then the full four-phase histograms for the
\(F_4\) transitions

\[
\begin{aligned}
(a,k,d-a,N-k)&\longrightarrow(s_0,p,s_2,N-p),\\
(a,p,d-a,N-p)&\longrightarrow(s_0,k,s_2,N-k)
\end{aligned}
\tag{13}
\]

are identical.

For the proof with arbitrary \(a\), restore \(W=z_0\) and set

\[
E=W+Y,\qquad T=W-Y,\qquad S=X+Z,\qquad D=X-Z.
\]

At \(q=i\), write

\[
\begin{aligned}
A(E,S)&=(E+S)^{s_0}(E-S)^{s_2}
       =\sum_{m=0}^d\alpha_mE^{d-m}S^m,\\
B_p(T,D)&=(T+iD)^p(T-iD)^{N-p}.
\end{aligned}
\]

The required elementary coefficient formulas are

\[
\begin{aligned}
[T^m]B_p
  &=(-1)^{N-p-m}i^{N-m}K_m(p;N)D^{N-m},\\
[W^aY^{d-a}]E^{d-m}T^m
  &=(-1)^mK_a(m;d),\\
[X^kZ^{N-k}]S^mD^{N-m}
  &=(-1)^{N-m-k}K_k(m;N).
\end{aligned}
\tag{14}
\]

Let \(C^{(a)}_{p,k}\) be the resulting unlabelled coefficient.
Equation (14) gives

\[
C^{(a)}_{p,k}
=\sum_m \alpha_m
(-1)^{N-p-m}i^{N-m}
(-1)^mK_a(m;d)
(-1)^{N-m-k}
K_m(p;N)K_k(m;N).
\tag{15}
\]

Every factor in (15), other than the last two Krawtchouk factors, is
invariant under exchanging
\(p\) and \(k\).  Krawtchouk duality (10), term by term, therefore gives

\[
C^{(a)}_{p,k}
=\frac{\binom Nk}{\binom Np}C^{(a)}_{k,p}.
\tag{16}
\]

The input-factorial multiplier for the first transition in (13) is

\[
a!\,(d-a)!\,k!\,(N-k)!
=\frac{a!\,(d-a)!\,N!}{\binom Nk},
\]

and the multiplier for the second is
\(a!(d-a)!N!/\binom Np\).  Thus (16) proves equality of the labelled
evaluations at \(q=i\).

At \(q=-1\), the generating polynomial is

\[
(E+S)^d(E-S)^N,
\]

independent of \(p\).  Since the requested monomials have total even
degree \(d\), the relevant term has the form \(E^dS^N\).  Its two
odd-variable coefficients have ratio
\(\binom Nk/\binom Np\), which the same factorial multipliers cancel.
The \(q=1\) evaluations count all labelled paths, and the \(q=-i\)
result follows by conjugation.  Fourier inversion proves the full
histogram theorem.

The Fock-state normalization does not spoil the result.  The product
of the input and output occupation factorials for either transition in
(13) is

\[
a!(d-a)!\,s_0!s_2!\,
k!(N-k)!\,p!(N-p)!,
\]

which is symmetric in \(p,k\).  Hence the normalized transition
amplitudes, not only the unnormalised permanents, are equal.

Combining (13) with ordinary input/output reciprocity gives a symmetric
form of the result.  If

\[
\mathcal H_{d,N}(a,k;s,p)
=\operatorname{hist}\!\left(
(a,k,d-a,N-k),(s,p,d-s,N-p)\right),
\]

then

\[
\mathcal H_{d,N}(a,k;s,p)
=\mathcal H_{d,N}(a,p;s,k)
=\mathcal H_{d,N}(s,k;a,p)
=\mathcal H_{d,N}(s,p;a,k).
\tag{17}
\]

Thus input and output splits may be exchanged independently in the
even and odd parity sectors.  Standard reciprocity supplies only the
simultaneous exchange; Krawtchouk self-duality supplies either partial
exchange.

There is also a matrix-family strengthening.  Define

\[
H(z)=
\begin{pmatrix}
1&1&1&1\\
1&z&-1&-z\\
1&-1&1&-1\\
1&-z&-1&z
\end{pmatrix}.
\tag{18}
\]

For every complex \(z\), the two transitions in (13) have equal
unnormalised permanents for \(H(z)\), and hence equal normalized
amplitudes whenever \(H(z)\) is used as a linear-optical matrix.  Its
four generating forms are

\[
E+S,\qquad T+zD,\qquad E-S,\qquad T-zD.
\]

Replacing \(i\) by \(z\) in (14) contributes the common factor
\(z^{N-m}\) and leaves the Krawtchouk argument unchanged.  Equation
(16) follows verbatim as a polynomial identity in \(z\).  For
\(|z|=1\), \(H(z)/2\) is the standard one-parameter family of
dephased \(4\times4\) complex Hadamard matrices; \(F_4\) is the
\(z=i\) member in this ordering convention.

Taking

\[
d=3,\quad (s_0,s_2)=(1,2),\quad
N=n+3,\quad (p,k)=(3,1)
\]

in (13) recovers (1).  Hence the observed \(L_A/L_C\) coincidence is
part of an infinite exact family of phase-histogram identities, not an
isolated relation between two affine lines.

## 6. Symmetry and novelty audit

The reciprocity is not generated, in general, by the elementary
symmetries of a Fourier multiport.

Rotations, reflections, and all other monomial mode relabellings can
only permute the four entries of each occupation vector.  Input/output
exchange may additionally exchange the two occupation vectors.
Row and column phase multiplications do not change occupations at all.
For generic parameters in (13), neither possibility maps the first
transition to the second.

For example, take

\[
d=5,\quad a=1,\quad N=11,\quad (s_0,s_2)=(0,5),
\quad (p,k)=(3,2).
\]

The input multisets on the two sides are

\[
\{1,2,4,9\}\quad\text{and}\quad\{1,3,4,8\},
\]

and the output multisets are

\[
\{0,3,5,8\}\quad\text{and}\quad\{0,2,5,9\}.
\]

They remain unequal even after input/output exchange.  Thus not even
arbitrary mode permutations, a much larger class than the Fourier
matrix's dihedral relabellings, explain this instance.  The original
\(N=11\) pair likewise has unequal multisets both before and after
exchange.

The algebraic engine, on the other hand, is classical rather than new:
equation (10) is the standard self-duality of binary Krawtchouk
polynomials.  Krawtchouk matrices are known to arise by condensing
symmetric tensor powers of the two-dimensional Hadamard matrix; see
[Feinsilver and Kocik](https://arxiv.org/abs/quant-ph/0702073).
That is exactly the structure exposed here by the parity variables
\((E,T,S,D)\).  Work on multiparticle suppression in Sylvester
interferometers also exploits the binary/Hadamard structure, although
the paper does not formulate the reciprocity (13); see
[Crespi](https://arxiv.org/abs/1502.06372).

In circuit language, this is best viewed as a **partial reciprocity**,
not a new mode permutation.  Reordering \(F_4\) by parity and applying
the two Hadamard changes of variables exposes

\[
(E+S,\ E-S,\ T+iD,\ T-iD).
\]

The normalized symmetric-power matrix for the last binary split is
symmetric by Krawtchouk self-duality.  This allows the odd occupation
split to be exchanged between the input and output while the two even
splits remain fixed.  Ordinary reciprocity of a symmetric
interferometer would exchange the entire input and output occupations;
(13) exchanges only one sector.

The fourth-root quotient is essential.  If paths are instead
classified by the unreduced integer exponent \(\sum jk\), the two
distributions are already unequal for the \(n=0\) instance of (1).
Equality appears after exponents are reduced modulo four, exactly the
phase information seen by \(F_4\).  Thus the result does not yet
provide a bijection preserving unreduced path weights.

Nor does the naive parity-sector statement extend automatically to
\(F_8\).  For example, the \(F_8\) histograms for

\[
\begin{aligned}
(0,0,1,0,0,1,0,0)&\longrightarrow(1,0,0,1,0,0,0,0),\\
(0,0,1,1,0,0,0,0)&\longrightarrow(1,0,0,0,0,1,0,0)
\end{aligned}
\]

are different, although the second pair is obtained from the first by
swapping its odd-mode occupation subvectors.  The two-mode binary
sectors of \(H(z)\), rather than parity alone, are essential.

The defensible novelty claim is therefore narrow:

- not a new Krawtchouk identity;
- not a new elementary symmetry of \(F_4\);
- apparently a new phase-resolved application of Krawtchouk
  self-duality, yielding an explicit infinite family of equal
  four-mode Fourier path histograms and paired dark events.

The last point is a literature-audit status, not yet a priority claim.
Targeted searches found the standard Krawtchouk/symmetric-tensor
theory and Fourier/Sylvester suppression laws, but no statement
equivalent to (13).  A paper should present the result as a derived
reciprocity theorem and explicitly credit the classical self-duality,
pending a broader citation and expert audit.
