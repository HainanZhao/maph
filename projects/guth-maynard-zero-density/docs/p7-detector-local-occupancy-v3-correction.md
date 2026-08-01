# P7 detector local occupancy v3 — final regression-harness correction

**PROVED:** This is a narrow versioned correction to the v2 correction
artifact. The v2 corrected companion document remains the readable
mathematical statement. The v1 and v2 artifacts remain immutable and
byte-replayable.

The v2 test made one remaining prose-only assertion: it expected the literal
phrase zero extension in a field that instead says that the local phase
changes neither the support nor this extension. The semantic convention is
unchanged: every selected exact primitive character satisfies
\(\chi(\mathfrak a)=0\) when \((\mathfrak a,\mathfrak f)\ne1\).

The v3 harness checks that actual invariant rather than an incidental wording.
No theorem, source pin, conductor convention, zero extension, occupancy
obstruction, conditional detector route, or P7 gate assessment changes.

The corrected replay sequence is:

    python3 proof/build_p7_detector_local_occupancy_v1.py --check
    python3 proof/build_p7_detector_local_occupancy_v2.py --check
    python3 proof/build_p7_detector_local_occupancy_v3.py --check
    python3 -m unittest tests/test_p7_detector_local_occupancy_v3.py -v
