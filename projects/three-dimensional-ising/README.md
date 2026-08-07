# Structural representations for the 3D Ising model

This project investigates exact finite-lattice structure for the
nearest-neighbour, zero-field, ferromagnetic Ising model on the simple cubic
lattice. It does **not** claim an exact solution.

The sealed baseline is the Stage 1 obstruction reconstruction in
[`docs/stage1-obstruction.md`](docs/stage1-obstruction.md), frozen by
[`artifacts/cycle-1-b1-stage1-obstruction-v1.json`](artifacts/cycle-1-b1-stage1-obstruction-v1.json).
The current result is the
[`Stage 2 five-lane candidate report`](docs/cycle2-candidate-report.md), frozen
by [`artifacts/cycle-2-b2-five-lane-boundary-v1.json`](artifacts/cycle-2-b2-five-lane-boundary-v1.json).
Replay with:

```bash
python3 -m pip install -r requirements.txt
python3 proof/verify_stage1_baseline.py
python3 proof/verify_cycle2_five_lanes.py
python3 -m unittest discover -s tests -v
```

Strategic state is in [`PROGRAM.md`](PROGRAM.md); the user-owned research
directive is in [`GOAL.md`](GOAL.md); failed or overbroad routes are retained
in the frozen [`Stage 1 failure ledger`](discovery/failure-ledger.md) and its
[`Cycle 2 supplement`](discovery/failure-ledger-cycle2.md).
