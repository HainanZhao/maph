# The Effective-Stark Sweep

This project is a certified census of unconditional archimedean Stark
instances over real quadratic fields.  Its final records have exactly
two possible mathematical outcomes:

- `PROVED`, routed through one frozen proved engine and accompanied by
  a replayable packet certificate; or
- `FRONTIER`, accompanied by the first named obstruction encountered by
  the frozen decision procedure.

No numerical approximation is promoted to a theorem.  The reusable
proof machinery remains in the sibling
[`sic-stark`](../sic-stark/) project; this directory provides the
census definitions, orchestration, records, and certificates.

## Current state

Cycles 001–052 are complete. Publication uploads, identifier recording, and
correspondence are administrative metadata, not research gates.  The
earlier sequencing records are retained only as process history and are
superseded by `data/research-activation-v3.json`.

The exact state can be checked with:

```bash
python3 scripts/audit_activation.py
python3 -m unittest discover -s tests -v
python3 scripts/audit_w1_anchor_screen.py
```

The order-six analytic certificate was replayed with Python 3.12.3 and
python-flint 0.9.0:

```bash
python scripts/certify_q7_p7_packet.py \
  --digits 70 --tolerance 1e-11
```

The seven anchor bundles are frozen in
[`data/anchor-battery-v1.json`](data/anchor-battery-v1.json).  They
cover the two Engine-A calibrations, four Engine-B packets, and the
Engine-C primitive packet.

The seven-bundle end-to-end reproduction passed. The maximal-order
ideal backbone contains 8,200 conjugacy-deduplicated cases over 121
certified fields. A preregistered 66-case structural pilot found one
new Engine-B route candidate, five Engine-C route candidates, and one
clean index-four frontier. See
[`docs/cycles-001-010-summary.md`](docs/cycles-001-010-summary.md).

`ROUTE_CANDIDATE` is not a theorem tag. No new case becomes `PROVED`
until its engine-specific packet and identification certificates pass.

The second campaign proves unconditional powered algebraicity for the
first order-six case, over `Q(sqrt(7))`, with safe exponent 4032. Its
exact candidate packet is ray-field verified and Sturm/Frobenius
labeled. A PARI-independent Yamamoto-cone evaluator encloses all six
logarithms in Arb balls; the powered height upper bound is
\(9.20\times10^{-9}\), giving a Voutier margin above 5,688. The explicit
packet identity is therefore `VERIFIED`.
The full W1 census routes 6,931 cases and records 1,269 frontiers. See
[`docs/cycles-011-020-summary.md`](docs/cycles-011-020-summary.md).

The full Engine-C geometry gate has now processed 1,350 primitive
quartic packets. It leaves 728 C-eligible cases, reroutes 63 to B,
names 22 mathematical frontiers, and quarantines four tool failures.
The enlarged B queue has been screened completely through absolute
normal-closure degree 40: 195 of 372 cases pass both imaginary-base
routes, with zero route disagreements, and collapse to 59 distinct
normal closures. The other 177 cases expose a newly explicit
obstruction, `NO_ABELIAN_IMAGINARY_BASE`.

Two new B divisor tables are banked. The
\(\mathbb Q(\sqrt{14}),\mathfrak p_7\infty_2\) case has safe exponent
4032 and is the next B identification target; the
\(\mathbb Q(\sqrt{111})\), norm-3 case has safe exponent 13,810,176.
The exact algebraic half of the first new C target over
\(\mathbb Q(\sqrt6)\), norm 8, is complete, but its explicit unit
identity remains `NUMERICAL` until the named Arb orientation gate
passes.

Engine A has also been reduced before its deferred bulk: 3,899 cases
are exact trivial identities \(X_A=1\), while 1,560 nontrivial cases
contain 2,232 quadratic packet occurrences in only 912 distinct
quartic fields. See
[`docs/cycles-021-050-summary.md`](docs/cycles-021-050-summary.md).

The next five B closures have now been selected by exact theorem cost,
not conductor proxies. Their safe exponents are 2880, 2016, 2592,
4032, and 15840. The portfolio contains the smallest new closure, the
cheapest exponent, a prime-power conductor, a four-occurrence
order-six transfer, and the first order-ten target. See
[`docs/cycle-051-theorem-value-selection.md`](docs/cycle-051-theorem-value-selection.md).

After discovery of the `NO_ABELIAN_IMAGINARY_BASE` false-pass mode, the
entire affected proof perimeter was rerun before any selected closure:
7/7 anchors passed end to end and structurally, all three currently
B-routed anchors passed the corrected predicate, and all 195/195 prior
B passes agreed exactly in fresh processes. See
[`docs/cycle-052-corrected-battery.md`](docs/cycle-052-corrected-battery.md).

The promoted \(\mathbb Q(\sqrt{57})\), norm-27 case now has a dedicated
W2 certificate. Both derived imaginary bases reconstruct its degree-24
normal closure, and the selected \(\mathbb Q(\sqrt{-19})\) route has
clearing exponents 864, 324, and 108, hence safe exponent 2592. W3
packet identification is next. The \(\mathbb Q(\sqrt6)\) Arb step is
explicitly blocked until the \(e=8\) normalization, eightfold
orientation, and second-base packet check are proved.

## Claim tags

- `VERIFIED`: exact or replay-certified statement.
- `ENCLOSED`: rigorous Arb enclosure.
- `NUMERICAL`: exploratory or cross-check output only.
- `CONJECTURAL`: explicitly conjectural census analysis.
