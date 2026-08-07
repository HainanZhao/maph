# Oracle post-result packet: C104 four-bit dihedral Cayley gate

**`PROVED` recommendation:** seal a finite-method-family boundary for the
four-bit (D_{14}) Cayley class. The exhaustive q=7 result has no hit and its
group-ring and adjacency routes agree exactly. This is not a q-uniform no-hit:
q=23 was correctly skipped because the preregistration permits it only after
a q=7 hit.

The exact state is

\[
C=\epsilon_R\{r^a:a\ne0\}\cup\epsilon_0\{s\}
\cup\epsilon_+\{r^as:\chi(a)=1\}\cup\epsilon_-\{r^as:\chi(a)=-1\}.
\]

All 16 masks fail. Only masks 3 and 14 have the required degree 7/Seidel row
sum; their off-diagonal (S^2) distributions are respectively
\({-12:7,-8:42,8:42}\) and \({-12:49,12:42}\), so both fail the
frozen condition. Falsifier: a replayed mask passing q=7 row and square
conditions, or a disagreement between convolution and adjacency counts.

Questioning the framing: this is a finite four-bit class, not evidence that
dihedral constructions broadly fail. C101 closes fixed six-block signs and
C103 closes its prescribed one-inversion extension; C104 changes to a global
group-convolution state, but rules out neither arbitrary dihedral connection
sets nor the book-Ramsey conjecture. A future distinct engine must first study
the compressed group-ring/autocorrelation state
\(C=A\sqcup Bs\), (A=-A\subseteq\mathbb Z_q\), (|A|+|B|=q\), through
Fourier/Parseval constraints and a direct Seidel equivalence—not another orbit
bit or arbitrary subset census.
