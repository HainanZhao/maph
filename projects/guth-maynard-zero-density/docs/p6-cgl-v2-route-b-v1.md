# P6 CGL-v2 Route B reconstruction v1

## Outcome

`OBSERVED`: the independent exponent-polytope/conductor Route B reconstructs
all 46 canonical registry rows, including `L12.odd_prime` and
`L12.two_power`, as a source-bound audit with overall disposition
`OPEN_ANALYTIC_INPUT`. It proves no theorem in Chen--Gupta--Li,
arXiv:2507.08296v2; it neither repairs nor validates the claimed `7/3`
estimate, selects no P7 family, and yields no new zero-density or
short-interval result.

The machine-readable route record is
[p6-cgl-v2-route-b-v1.json](../artifacts/p6-cgl-v2-route-b-v1.json). It
pins the CGL TeX (`0b9ebb6b...`), the sealed 46-row preregistration, and the
reachable Guth--Maynard source/AAM inputs, and records every row's source
region, formula/check, hypotheses, disposition, and blockers.

## Route-B algebra

With
\(\alpha=\log q/\log(qT)\),
\(\tau=1-\alpha\),
\(\lambda=\log q_1/\log(qT)\), and
\(\beta=\lambda+\tau\), the middle coefficient functions are compared
directly with \(3/(2-\sigma)\). The resulting crossings are:

| Term | Route-B crossing / coefficient |
|---|---|
| \(C_1\) | \(\sigma=(3+2\lambda)/(6+\lambda)\), base \(q_1^{1/3}q^2T^2\) |
| \(C_2\) | \(\sigma=(4-2\beta)/(4-\beta)\), base \(q^3T^{9/4}q_1^{-3/4}\) |
| \(C_3\) | \(20\sigma^2-(43-3\beta)\sigma+24-6\beta=0\), coefficient \((37+3\beta-\sqrt{9\beta^2+222\beta-71})/12\) |
| \(C_4\) | \(\sigma=7/10\), coefficient \(30/13\) |

For \(q_1=q\), hence \(\beta=1\), this gives
\(q^{7/3}T^2\), \(9/4\), \((10-\sqrt{10})/3\), and \(30/13\).
The exact margins against `7/3` are retained, including `1/12`, `1/39`, and
\((\sqrt{10}-3)/3>0\). This is exact conditional algebra, not a proof of the
preprint's zero-density theorem.

## Explicitly unresolved inputs

- `S06_EXTERNAL_INPUTS`: the route maps, but does not close, the hypotheses
  of the cited mean-value, Huxley, Heath--Brown, Montgomery, Davenport, and
  Guth--Maynard inputs.
- `Z03_TAIL_X_RANGE`: the CGL tail argument takes \(T\to\infty\) with \(X\)
  polynomially bounded in \(T\), while later setting \(X=(qT)^\epsilon\)
  under uniform \((q,T)\) language. Route B adds no \(q\leq T^C\) restriction,
  no tail replacement, and no \(T=1\) repair.
- `Z05_PRIMITIVE_EULER_FACTORS` and `Z06_CONDUCTOR_SUM_Q1`: no source-backed
  primitive-to-all-character zero-set/conductor-sum transfer is supplied.
- `F08_T_SMOOTH_UNDEFINED`: the source uses `T`-smooth without defining it;
  Route B does not invent a divisor-chain convention.
- `S03_MULTIPLICITY_NOT_STATED`: the displayed zero-count definition does not
  explicitly fix multiplicity.

Replay:

```sh
python3 proof/p6_cgl_v2_route_b_v1.py --check
python3 -m unittest tests/test_p6_cgl_v2_route_b_v1.py -v
```
