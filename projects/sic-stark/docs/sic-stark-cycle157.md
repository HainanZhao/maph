# SIC--Stark research cycle 157: Fourier-normalization audit and stop decision

Date: 2026-07-29

## Question

Cycle 156 found well-conditioned growth in the raw helical packets
\[
 \mathscr S_{a,b,r}(s)
 =\sum_{k\in\mathbb Z}K_{a,b}(r+3k;\gamma(s)).
\]
Before abandoning the componentwise boundary estimate, cycle 157 asked
whether the omitted Fourier normalization cancels that growth and
whether the normalized coefficient has an explicit map to the three
ray-class logarithms \(\mathscr P_j\).

## Exact Fourier ledger

Equation (66) extracts the \(y\)-independent phase
\[
 \exp\!\left(
  -\frac{\pi i\alpha Q}{24\omega_1}
 \right)
\]
before writing the continuous Fourier character. The corresponding
ordinary Fourier coefficient must therefore restore
\[
 g(\alpha)=
 \exp\!\left(
  +\frac{\pi i\alpha Q}{24\omega_1}
 \right).
\]
Cycle 156 intentionally inserted no such gauge, so its raw packets
were not ordinary Fourier coefficients.

At the fused boundary, one \(z\mapsto z+3\) step contributes \(-q\)
from the normalized Gamma product and \(-q\) from \(g\). The
Fourier-normalized boundary scalar is consequently \(q^2\), times the
rational term ratio. At finite \(s\), the two lens bases remain
distinct, so the \(-q\) and \(q^2\) descriptions are boundary
identities rather than interior identities.

The direct weighted quotient
\[
 \frac{g(\alpha_{z+3})K_{a,b}(z+3)}
      {g(\alpha_z)K_{a,b}(z)}
\]
agrees with the independently telescoped quotient to \(53.50\) digits
for \((a,b)=(0,2)\) and \(53.08\) digits for \((0,1)\).

## Exact finite-frequency descent

For every integer alias \(z\),
\[
 N_z=a+2-6z,\qquad \ell_z=b-6z.
\]
The helical Zak descent gives
\[
 (p_a,p_b)=(-5(N_z-2),\ell_z)\pmod6=(a,b).
\]
This was checked for all 36 finite frequencies and \(25\) consecutive
aliases each, for \(900\) exact integer records.

Thus all aliases belong to one finite coefficient. The standard
restriction gives them unit weights after the ordinary Fourier gauge
has been included in each ambient coefficient. The three former
\(r\bmod3\) packets merely partition the same complete \(z\)-sum; they
are not the three ray classes.

## Corrected numerical packet

Define the complete additive Fourier coefficient
\[
 C_{a,b}(\tau)=
 \sum_{z\in\mathbb Z}g(\alpha_z)K_{a,b}(z;\tau),
\]
and the ordinary transformed value
\[
 \widehat K_{a,b}(\tau)
 =24\,\Gamma_M(Q,0;\tau)\,C_{a,b}(\tau).
\]
The conductor-3 control \((0,2)\) and primitive mode \((0,1)\) were
evaluated at 20 and 40 digits, each with 15 guard digits:
\[
\begin{array}{c|r|r}
1/s&|\widehat K_{0,2}|&|\widehat K_{0,1}|\\
\hline
64   &8.5083387096&66.1239056514\\
256  &110.7415988298&209.7958785509\\
1024 &640.4477899766&774.5149644044\\
4096 &2053.3133149338&1248.3648168160
\end{array}
\]
The endpoint growth factors are \(241.33\) and \(18.88\),
respectively. Every transformed value agrees between the two
precisions by at least \(31.34\) digits. The common scalar
\(\Gamma_M(Q,0)\) stays bounded and approaches about \(-0.452\), so it
does not cause the growth.

The finite-\(s\) Fourier-gauge step approaches its fused value \(-q\):
its relative discrepancy falls from \(2.52\times10^{-1}\) at \(1/s=64\)
to \(3.52\times10^{-3}\) at \(1/s=4096\).

Finite growth is not a proof of nonexistence. It is nevertheless
strong, well-conditioned evidence against using either the raw or the
ordinary Fourier-normalized additive coefficient as a bounded
componentwise proof target.

## Missing arithmetic map

The audit traced the repository's definitions from the ambient
Fourier transform through the helical quotient. It found no equation
that maps the 36 additive coefficients \(C_{a,b}\) to the three
primitive norm-37 ray-class logarithms \(\mathscr P_j\). In
particular, the following data are absent:

1. selection or combination of finite characteristics into the three
   Frobenius classes;
2. the nonlinear operation turning an additive coefficient into a
   logarithmic ray value;
3. logarithm branches and any boundary subtraction or finite part;
4. an identification of that object with the AFK cocycle values.

The characteristic-to-ray certificate begins with an already supplied
boundary/cocycle value. It does not derive that value from the
continuous spectral coefficient.

The dimension-four and dimension-five calibration scripts also do not
close this gate: in both controls, the interior alias sum and the
proved boundary overlap are computed independently, without an
asserted equality between them.

The AFK twisted convolution equation (1.49) is a finite algebraic sum
of Shintani--Faddeev cocycle values. It does not itself define a map
from the continuous additive Fourier coefficient above to those
values.

## Verdict

The normalization audit is complete, and the current route should stop.

- BF\(_6\), as written, is retired: it concerns raw ungauged packets,
  and its asserted implication to MFC\(_6\) lacks the necessary map.
- Restoring the correct Fourier gauge does not reveal bounded
  componentwise behavior on the tested ladder.
- MFC\(_6\) may remain a conceptual conjecture about the intended
  cocycle/ray values, but it is not operationally testable from the
  present definition of “spectral periodization.”
- No further boundary-packet numerics are justified until an explicit
  coefficient-to-cocycle/ray-logarithm formula is supplied from an
  independent derivation.

This is a stop/divert decision, not a claim that the dimension-six SIC
statement is false. The exact downstream algebra remains useful if a
valid analytic input is later found.

## Artifacts

- `scripts/dimension_six_cycle157_fourier_normalization_audit.py`
- `certificates/dimension-six-cycle157-fourier-normalization-audit.json`

Reproduction:

```bash
cd projects/sic-stark/scripts
python3 dimension_six_cycle157_fourier_normalization_audit.py \
  --dps-low 20 --dps-high 40 \
  > ../certificates/dimension-six-cycle157-fourier-normalization-audit.json
```
