# C78 replay archive

The original C78 record and its certification withdrawal remain immutable. The
current canonical certification status is
artifacts/cycle-78-b078-compatible-spin-endpoint-correction-v3.json. It is
PROVED: C79 independently establishes the \(Q=I/2\) endpoint, and the C78
v2/v3 correction chain records the re-audited interpolation.

From this project directory, run:

    source ../../tools/dev-env.sh
    research prereg check docs/cycle-78-b078-compatible-spin-endpoint-preregistration-v1.md --expected-cycle 78
    research prereg check docs/cycle-79-b079-compatible-endpoint-foundation-preregistration-v1.md --expected-cycle 79
    python3 proof/check_cycle79_compatible_endpoint_foundation.py
    python3 proof/check_cycle78_endpoint_interpolation.py
    python3 proof/build_cycle_79_compatible_endpoint_foundation.py --check
    python3 proof/build_cycle_78_endpoint_reinstatement.py --check
    python3 proof/build_cycle_78_reinstatement_timestamp_correction.py --check

The manuscript source is main.tex. It covers compatible three-qubit states
with measure supported on AB, AC, and BC, and every qubit reference state. The
manuscript is a draft pending renewed literature and hostile manuscript audit;
it has not been released.
