# Cycle 098 — W4 genuine Shintani-index distribution

This first W4 slice reads only the completed genuine v3 normal-closure
ledger.  Before inspecting its output, freeze the calculations:

1. tabulate every `derived_subgroup_order` over all 8,200 records;
2. separately count records with odd order greater than two;
3. require agreement with the ledger's embedded histogram and with the
   registered 446-row odd-index parity replay.

The resulting values are exact finite-range descriptive statistics
(`OBSERVED`), not an asymptotic density, a new index theorem, or a
packet identity.  Any disagreement blocks W4 rather than being rounded
or silently reconciled.
