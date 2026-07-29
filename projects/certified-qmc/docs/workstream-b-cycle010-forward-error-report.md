# Workstream B Cycle 010 — producer-error report

Completed at: **2026-07-29T04:51:31Z**

Status: **PARTIAL PASS; EXTERNAL-COMPARISON GATE REMAINS CLOSED**

## Outcome

Two prerequisite layers are now replayable.

1. `VERIFIED_PLAN_METADATA`: the pinned FFTW 3.3.10
   `FFTW_ESTIMATE` plans for every radix-two length from \(1\) through
   \(2^{18}\) replayed identically twice.  The certificate records the
   forward and inverse plan trees, `fftw_flops` counts, costs, compiler,
   binary/source hashes, P2 constants, and `FE_TONEAREST`.
2. `ENCLOSED_DIRECT_PRODUCER_ERROR`: the non-FFT LatNet Builder
   `CoordUniformCBC` evaluation graph for symmetric unilevel `CU:P2`
   and product weights now has an executable binary64 forward-error
   enclosure.  Each local error is the exact dyadic difference between
   the rounded operation and its real operation; Arb propagates the
   input, \(2\pi^2\), and accumulated error at 256 bits.

Three small adversarial cases—including mixed-scale weights and the
\(\gamma_j=j^{-2}\) denominator pattern—were enclosed.  An independently
evaluated Arb sum-product merit lies inside every propagated result
ball.

The audited LatNet source and its pinned LatticeTester submodule were
then compiled against the recorded dependencies.  At 17 displayed
digits, all three synthetic direct-evaluation results decode to the
same binary64 words as the midpoint replay.  This is a bit-identical
midpoint check, not a decimal-tolerance comparison.

Three synthetic fast-CBC searches at \(N=16,32,64\) were also banked.
Their final printed merits were independently enclosed, and direct
exact-polynomial/Arb enumeration proves that every selected component
is a mathematical CBC minimizer.  Three stages have exact polynomial
ties; those are recorded as exact ties rather than falsely promoted to
strict separations.  This is an after-the-fact certificate for the
frozen small searches, not a general error theorem for FFTW.

## Source-level producer map

At LatNet Builder commit
`39dd60fceb0c86a6124b701072d91f8e3aed73df`:

- `ConcreteCoordUniformState-P.cc` performs the pointwise product-state
  update;
- `CoordUniformInnerProd.h` and `CompressedSum.h` implement the direct
  symmetric inner product and its summation order;
- `CoordUniformCBC.h` normalizes by \(N\), adds the prior base merit,
  and updates the selected state; and
- `CoordUniformInnerProdFast.h` replaces the candidate inner product
  with real FFT, complex multiplication, normalized inverse FFT, and
  lower-level accumulation.

Thus the direct and fast paths share kernel construction, state update,
normalization, and base-merit logic.  This map remains useful for A3
and for numerical validation, but Cycle 011 removes CBC selection from
the Workstream B comparison entirely.

## Why the gate is still closed

`fftw_flops` is an exact plan-operation count, not a stability theorem.
The certificate deliberately does not promote those counts into a
Higham-style \(\gamma_k\) bound.  Cycle 011 further corrects the trusted
base: historical producer builds are generally unrecoverable, so a
plan-specific FFTW proof would address the wrong object.

Consequently:

- the direct-evaluation component of \(B_{\rm alg}\) is enclosed;
- the FFTW transcript is re-tagged `NUMERICAL_MODEL_VALIDATION`;
- future merit-bearing tables use a model-class evaluation envelope
  plus an exact lexical formatting bound;
- historical files without producer build metadata remain admissible
  when the explicit model-class assumptions apply; and
- no new external merit was selected, read, or compared in this cycle.

## Protocol incident disposition

The example merit field exposed before preregistration remains
`EXPLORATORY_PROTOCOL_CONTAMINATED`.  No exact/enclosed subtraction was
performed, and no numerical value from that field appears in a
certificate or this report.  It cannot be the first confirmatory target.

## Next gate

Cycle 011 disposition:

1. ~~bank a bit-identical transcript between the compiled LatNet direct
   evaluator and the binary64 midpoint replay;~~
2. instrument the pinned fast-CBC FFT block on synthetic, nonexternal
   inputs and bank final decisions; **complete at \(N\le64\)**;
3. ~~prove a plan-specific FFTW error bound~~; **retired as the wrong
   historical trusted base**;
4. remove selection from Workstream B and survey merit-column presence;
5. compute \(T_{\rm format}\) first and build
   \(T_{\rm eval}(\mathcal M)\) only for merit-bearing targets; and
6. only after those pass, timestamp and fetch a previously unseen
   merit value.

Artifacts:

- `certificates/workstream-b-fftw-plan-audit.json`
- `certificates/workstream-b-direct-producer-bound.json`
- `certificates/workstream-b-latnet-direct-replay.json`
- `certificates/workstream-b-fastcbc-synthetic-transcript.json`
- `src/producer_error.py`
- `native/fftw_plan_audit.c`
