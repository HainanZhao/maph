# P6 conductor (q_1)-reset lemma v1

## Claim boundary

`PROVED`: the conductor-induction step does not require a source-selected
auxiliary divisor (q_1\mid q) to survive after a character is replaced by
its primitive inducer. At each exact primitive conductor (d\mid q), one may
run a primitive estimate with its own admissible choice (q_1'=d), form the
final monotone envelope in (dT), and only then sum over conductors.

`CONJECTURED`/external for this project: the primitive CGL-style estimate at
modulus (d), with (q_1'=d), and all analytic hypotheses required to prove
it. This lemma does not validate that estimate, CGL-v2, or its (7/3)
theorem.

`OBSERVED`: the pinned CGL-v2 TeX states both that its displayed estimate is
available for any divisor (q_1\mid q) and that nonprimitive characters are
to be included by applying the final estimate to every factor of (q).
Those source statements motivate the reset, but the exact transfer below is
proved independently from the already sealed primitive-to-all lemma.

## Exact transfer

Fix (1/2<\sigma<1), put (a=1-\sigma>0), and suppose that for each
(d\mid q) the multiplicity-weighted primitive zero count obeys

\[
 P_d(\sigma,T)\le (dT)^{o(1)}
 \left(d^{\frac73a}T^{2a}+(dT)^{\frac{30}{13}a}\right).
 \tag{1}
\]

The choice (q_1'=d) is admissible in the primitive modulus-(d) problem
because (d\mid d) and (d\ge\sqrt d). It is a fresh internal choice; no
claim that an earlier (q_1\mid q) divides (d) is needed.

The sealed primitive-to-all transfer gives the exact conductor partition and
preserves zero multiplicities in (Re s>0). Since (d\le q), both terms in
(1) are monotone:

\[
 d^{\frac73a}T^{2a}\le q^{\frac73a}T^{2a},\qquad
 (dT)^{\frac{30}{13}a}\le(qT)^{\frac{30}{13}a}.
\]

Consequently

\[
 \sum_{\chi\bmod q}N(\sigma,T,\chi)
 \le \tau(q)(qT)^{o(1)}
 \left(q^{\frac73a}T^{2a}+(qT)^{\frac{30}{13}a}\right).
 \tag{2}
\]

The divisor factor is (q^{o(1)}). In particular, because (2\le7/3) and
(30/13\le7/3), (2) is bounded by ((qT)^{(7/3)a+o(1)}), conditional on
the primitive input.

## Gate effect

`PROVED`: Z06's demand for “(q_1)-sensitive termwise domination” is not an
independent conductor-transfer requirement when the primitive theorem is
rerun at each (d) with (q_1'=d). The exact conductor partition,
multiplicity preservation, and divisor loss were already proved by the
primitive-to-all artifact.

`OBSERVED`: this does not close the primitive large-value estimate, the S06
source hypotheses, the detector inputs, the corrected smooth branch, or any
intermediate formula that genuinely needs a prescribed (q_1\ne d). No new
zero-density theorem is promoted.

Replay:

```sh
python3 proof/p6_conductor_q1_reset_v1.py --check
python3 -m unittest tests.test_p6_conductor_q1_reset_v1 -v
```
