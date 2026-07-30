# Verification environment

Pinned principal environment:

- Linux/x86-64
- Python 3.12.3
- python-flint 0.9.0
- PARI/GP 2.15.4
- pdfTeX from TeX Live 2023

Unconditional PARI class/unit computations use `bnfinit(P,1)` followed
by the full `bnfcertify(bnf)` call returning `1`. The quotient-only
certification flag is not used.

On the recorded AMD EPYC 9354P virtual CPU, the compact
`verify_results_companion.py all` run is expected to finish in under
one minute and below 1 GiB of memory. Full regeneration of every cone
and Arb certificate is case-dependent and may take minutes per case;
it is intentionally separate from the compact consistency verifier.
