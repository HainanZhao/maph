# Circularity audit of the five Roblot phase controls

Recorded: 2026-07-31 UTC.

## Verdict

`CONTAINED_ORIENTATION_CIRCULARITY`.

The weak-unit construction and the dominant-embedding representative
are independent of the analytic \(L'\)-target. The character
orientation in the archived five-control comparison is not.

## Provenance audit

1. **Weak unit: PASS.** The corrected RQ-000129 constructor and the
   four remaining constructors were sealed before the analytic phase
   records were opened. Their exact unit and lattice computations do
   not read an \(L'\)-value or Engine-C packet.
2. **Dominant gauge: PASS.** The gauge uses only the orbit
   \((a,b,-a,-b)\) of logarithms of the sealed weak unit. It neither
   reads nor minimizes a residual against \(L'\).
3. **Analytic orientation: FAIL.** In
   `scripts/compare_all_phase_gates.py`, the loop explicitly tests both
   `direct` and `inverse`, and retains the orientation whose rotated
   \(L'\)-ball contains the weak-unit coefficient. This is target-based
   selection.
4. **Artin-label source: NOT YET SUFFICIENT.** The archived controls
   contain selected CM-character coordinates, but the phase project
   does not contain a replay that transports those coordinates to the
   real-quartic generator \(\gamma\) without consulting the phase
   match.

## Claim correction

The old five-control record remains valid for the weaker statement:
for each row, exactly one of the two conjugate character orientations
has a quarter-turn match. It is not an independent validation of a
fully oriented ratio.

No exact theorem or certified case-level Stark identification is
withdrawn. The affected statement was tagged numerical. A new
data-independent five-ratio replay is blocked until exact
reinduction/Artin transport fixes the orientation before \(L'\) is
read.

## Required repair

For each control, reconstruct the map from the original real-quartic
generator to the selected analytic character using only:

- exact ray-character coordinates;
- exact linear reinduction;
- frozen Artin labels;
- the convention \(\chi(\gamma)=i\).

Seal that map, then rerun one orientation only. Merely reusing the
orientation strings selected by the old comparison would repeat the
circularity.
