# Discrete mathematics and quantum-interference exploration

The current research direction is the exact classification of dark events
in Fourier multiport interferometers.  See
[`docs/physics-pivot.md`](docs/physics-pivot.md) for the research question,
the proposed cyclotomic-balance explanation, the first exact scan, and the
claim ledger.

The repository began as a reproducible exploration of [Erdős Problem
700](https://www.erdosproblems.com/700). That work remains archived and
tested here. For an integer \(n\), define

\[
f(n)=\min_{1<k\leq n/2}\gcd\left(n,\binom{n}{k}\right).
\]

The long-term questions are:

1. Characterize the composite \(n\) for which
   \(f(n)=n/P(n)\), where \(P(n)\) is the largest prime factor of \(n\).
2. Determine whether \(f(n)>\sqrt n\) for infinitely many composite \(n\).
3. Prove strong general upper bounds for \(f(n)\).

Our initial scope is deliberately narrower: compute trustworthy data and
understand \(f(n)\) for prime powers and integers with two distinct prime
factors.

## Repository map

- [`docs/physics-pivot.md`](docs/physics-pivot.md): current quantum-optics
  direction and first computational observations.
- [`docs/thesis-stage1.md`](docs/thesis-stage1.md): assumption audit,
  mechanism classification, the reflection-plane Bessel generating
  function, rigorous zero-free region, and current conjectures.
- [`docs/thesis-outline.md`](docs/thesis-outline.md): proposed thesis
  claim, chapter structure, success criteria, and research sprints.
- [`docs/thesis-stage2-reciprocity.md`](docs/thesis-stage2-reciprocity.md):
  current checkpoint, theorem inventory, rejected assumptions, and next
  thesis work.
- [`docs/agent-n11-findings.md`](docs/agent-n11-findings.md): exact
  affine-quasipolynomial analysis of the eleven-particle residue.
- [`docs/agent-n11-direct-proof.md`](docs/agent-n11-direct-proof.md):
  symbolic Krawtchouk-duality proof of the hidden affine-line histogram
  identity.
- [`docs/agent-unitary-leakage.md`](docs/agent-unitary-leakage.md):
  exact directional leakage fingerprints and the all-odd protected-axis
  theorem.
- [`docs/agent-irred-extension.md`](docs/agent-irred-extension.md):
  extended irreducibility certificates and failed elementary
  Newton/Eisenstein proof routes.
- [`scripts/audit_reflection_irreducibility.py`](scripts/audit_reflection_irreducibility.py):
  standard-library finite-field certificates for the stronger polynomial
  irreducibility conjecture.
- [`src/fourier_suppression.py`](src/fourier_suppression.py): exact
  phase-histogram computation for Fourier multiports.
- [`scripts/scan_fourier_suppression.py`](scripts/scan_fourier_suppression.py):
  enumerate dark events and separate the elementary symmetry-predicted
  cases.
- [`tests/test_fourier_suppression.py`](tests/test_fourier_suppression.py):
  exact tests, including the Hong--Ou--Mandel event.
- [`docs/roadmap.md`](docs/roadmap.md): phased research plan.
- [`docs/brainstorm-stage2.md`](docs/brainstorm-stage2.md): current proof avenues.
- [`docs/brainstorm-stage3.md`](docs/brainstorm-stage3.md): near-multiple reduction
  and high-leverage conjectures.
- [`docs/brainstorm-stage4.md`](docs/brainstorm-stage4.md): iterative experiments,
  the reciprocal-threshold conjecture, and the prefix-packing proof target.
- [`docs/brainstorm-stage5.md`](docs/brainstorm-stage5.md): Lucas failure depth,
  a falsified two-digit conjecture, and the inherited-family theorem.
- [`docs/brainstorm-stage6.md`](docs/brainstorm-stage6.md): unbounded hidden
  carry depth and the exact third-prefix formulas.
- [`docs/brainstorm-stage7.md`](docs/brainstorm-stage7.md): adversarial
  near-witness searches and the finite CRT-box formulation.
- [`docs/brainstorm-stage8.md`](docs/brainstorm-stage8.md): sparse-box
  counterexample searches and the character-sum reformulation.
- [`docs/brainstorm-stage9.md`](docs/brainstorm-stage9.md): complement
  symmetry, genuine three-base obstructions, and the full Fourier formula.
- [`docs/brainstorm-stage10.md`](docs/brainstorm-stage10.md): adaptive
  three-base covers, degree-four searches, and a falsified fixed-triple rule.
- [`docs/brainstorm-stage11.md`](docs/brainstorm-stage11.md): unrestricted
  degree-four examples, defect-sensitive behavior, and pair isolation.
- [`docs/brainstorm-stage12.md`](docs/brainstorm-stage12.md): defect ports,
  fixed-radical depth obstructions, adversarial certificates, and current
  literature.
- [`docs/progress.md`](docs/progress.md): dated research log and claim ledger.
- [`docs/mathematics.md`](docs/mathematics.md): definitions and proved lemmas.
- [`docs/status-and-next-problem.md`](docs/status-and-next-problem.md):
  current status, remaining-effort estimates, and the Problem 699 follow-on.
- [`src/erdos700.py`](src/erdos700.py): exact computation using valuations.
- [`scripts/explore.py`](scripts/explore.py): data exploration CLI.
- [`tests/test_erdos700.py`](tests/test_erdos700.py): independent cross-checks.

## Quick start

The project uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/scan_fourier_suppression.py --modes 4 --particles 4
python3 scripts/analyze_four_mode_thesis.py
python3 scripts/certify_reflection_conjecture.py --a-limit 1000
python3 scripts/audit_reflection_irreducibility.py
python3 scripts/analyze_n11_affine.py
python3 scripts/analyze_unitary_leakage.py
python3 scripts/analyze_reciprocity_census.py
python3 scripts/explore.py --limit 500
python3 scripts/explore.py --limit 5000 --csv data/f_values_5000.csv
python3 scripts/scan_squarefree_triples.py --prime-limit 200
python3 scripts/analyze_2qr.py --q-limit 1000
cc -O3 -std=c11 -o /tmp/falsify_near30 scripts/falsify_near30.c
/tmp/falsify_near30 10000
cc -O3 -std=c11 -o /tmp/falsify_reciprocal scripts/falsify_reciprocal.c
/tmp/falsify_reciprocal 100000 all
python3 scripts/carry_signatures.py 2088
python3 scripts/analyze_primary_pseudoperfect.py 52495396602
python3 scripts/search_power5_near_witnesses.py --max-exponent 100
python3 scripts/search_supercritical_boxes.py --max-exponent 12
python3 scripts/analyze_box_bias.py 2952450
python3 scripts/scan_lucas_helly.py --limit 10000
python3 scripts/search_high_cover_degree.py --primes 2 3 5 7
python3 scripts/search_prime_extensions.py --base 300 --prime-limit 2000
cc -O3 -std=c11 -o /tmp/falsify_three_base_cover scripts/falsify_three_base_cover.c
/tmp/falsify_three_base_cover 100000
cc -O3 -std=c11 -o /tmp/falsify_three_base_cover_fast scripts/falsify_three_base_cover_fast.c
/tmp/falsify_three_base_cover_fast 300000
cc -O3 -std=c11 -o /tmp/scan_cover_degree_all scripts/scan_cover_degree_all.c
/tmp/scan_cover_degree_all 100000 supercritical
python3 scripts/search_pair_isolation.py --primes 2 3 5 --max-exponent 10
python3 scripts/adversarial_certificate_search.py --kernel 2 3 5 --exhaustive --max-exponent 3
```

## Standards for claims

Every mathematical statement in the notes is marked as one of:

- **Proved:** accompanied by a proof in the notes or a precise citation.
- **Computational observation:** checked only in a stated finite range.
- **Conjecture:** suggested by data but not proved.
- **Question:** a possible direction with no asserted truth value.

Finite computation is evidence, not proof of an unbounded statement.
