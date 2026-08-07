# Oracle C107 selection: Paley-cross bi-translation obstruction

**`CONJECTURED` planning decision.**  The human-selected active problem is
F001 (diagonal book Ramsey); Oracle selects this next cycle only, not a new
problem or project.

## Question the target; question the questioning

The preceding C104--C106 boundaries concern inverse-closed degree-\(q\)
dihedral Cayley states.  A two-layer translation matrix with independently
chosen within-layer states is a strictly larger state, while retaining one
rigid cross-layer operator that may force a contradiction without a graph or
subset census.  The familiar conference/PC-graph mechanism is not a suitable
route: Dai--Lin's 2026 construction already treats that sufficient condition.

The critique could overvalue the Paley vocabulary merely because it makes
Fourier diagonalization cheap.  Thus the selected gate has a single direct
test: the cross-block equation must be forced by row sums and the permitted
Seidel-square values.  If it is not, this route is rejected rather than
repaired by extra orbit restrictions.

## Selected cycle

Let \(q\equiv7\pmod8\) be a prime power, \(G=(\mathbb F_q,+)\), and
\(T_{xy}=\chi(y-x)\), where \(\chi\) is the quadratic character extended
by \(\chi(0)=0\).  Put \(Q=I-T\).  Let \(P_0,P_1\) be independent
symmetric translation Seidel blocks with zero diagonal, off-diagonal values
\(\{\pm1\}\), and row sum \(-2\), and form
\[
 S=\begin{pmatrix}P_0&Q\\Q^{\mathsf T}&P_1\end{pmatrix}.
\]
It has row sum \(-1\).  The state is outside C106 when \(P_0\ne P_1\),
and it is not the conference/PC-graph lift audited in
`f001_dai_lin_2026_source_audit.md`.

The proposed invariant is the cross block
\[
 (S^2)_{01}=Q(P_0+P_1).
\]
Translation invariance and the required entries \(\{0,-4\}\) force it to
equal \(-4R_c\) for one translation \(R_c\).  With
\(QJ=J\) and \(QQ^{\mathsf T}=(q+1)I-J\), the inverse identity
\[
 Q^{-1}=\frac{Q^{\mathsf T}+J}{q+1}
\]
would force
\[
 P_0+P_1=-\frac4{q+1}(Q^{\mathsf T}+J)R_c.
\]
The left side is even integral.  The right side has nonzero entries
\(-8/(q+1)\): it is \(-1\) at \(q=7\) and nonintegral for \(q>7\).

## Verifier, falsifier, and stop

- Prove the Paley identities and forced-cross equation symbolically; verify
  the full \(2q\)-by-\(2q\) identities independently at \(q=7,23\) across
  the 30 shifts only.  Do not enumerate \(P_i\) or arbitrary graphs.
- **Falsifier:** a route disagreement, or an admissible \(P_0,P_1,c\)
  satisfying the displayed forced equation.
- **Resource cap:** one CPU, 60 seconds, 256 MiB peak memory, and 1 MiB
  temporary/output data.
- **Stop:** a pass closes only the fixed-Paley-cross two-layer translation
  family.  Do not patch it with restricted \(P_i\) or a subset census; a
  later route must change \(Q\) or leave two-layer translation invariance.

## Exclusion map

| record | former question / outcome | C107 delta |
|---|---|---|
| C103 | fixed six-block signs with inversion bits; q=7 no-hit | no six-block placement or sign enumeration |
| C104--C106 | inverse-closed degree-\(q\) Cayley states on \(D_{2q}\); uniform obstruction | independent \(P_0,P_1\) on two translation layers, not one dihedral connection set |
| Dai--Lin 2026, Thm. 1.1 / Lemma 2.2 | conference/PC-graph sufficient condition and a \(4n\)-vertex clone-pair lift | \(2q=4n-2\) Paley-tournament cross block, not a conference matrix or a rederivation of their construction |

The full primary-source overlap is recorded in
`discovery/f001_dai_lin_2026_source_audit.md`.
