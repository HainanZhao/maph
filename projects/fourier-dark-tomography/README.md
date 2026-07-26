# Fourier dark-event tomography

This project studies local coherent-error identification from multiphoton
dark events in Fourier multiports.

The central theorem gives, for every \(m\ge2\) and every \(n>2\) divisible
by \(m\), an explicit Fourier-cat input, \(m(m-1)/2\) dark outcomes, and two
fixed signed probes whose limiting contrast Jacobian identifies all
\(m(m-1)\) off-diagonal Hermitian error coordinates.  The construction is
dimension-minimal within the weak-probe regular-local protocol.

## Layout

- `paper/`: self-contained Physical Review A manuscript and submission
  materials.
- `docs/general-fourier-cat-tomography.md`: arbitrary-mode theorem and
  proof.
- `docs/agent-su4-tomography.md`: exact \(F_4\) Fock and cat certificates.
- `docs/finite-angle-statistics.md`: finite-probe bias and Fisher analysis.
- `docs/prior-art-general-m-identifiability.md`: targeted novelty audit.
- `src/fourier_suppression.py`: exact Fourier phase-histogram machinery.
- `scripts/`: exact certificates and finite-angle analyses.
- `tests/`: theorem regression tests and independent polynomial checks.

## Quick start

Run commands from this directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/certify_general_fourier_cat_tomography.py --max-modes 9
python3 scripts/search_su4_dark_tomography.py
python3 scripts/analyze_cat_finite_statistics.py
```

Compile the paper from `paper/`:

```bash
cd paper
/tmp/tectonic -X compile manuscript.tex --outdir build --keep-logs
```

## Scope

The theorem is local, assumes calibrated cat and probe phases, and targets
off-diagonal coherent lossless errors.  It is not full \(U(m)\) process
tomography, a global uniqueness theorem, or a hardware-independent
sample-complexity claim.
