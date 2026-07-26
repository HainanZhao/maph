# Vendored PGLib-OPF cases

Source release: PGLib-OPF `v23.07`, published 2023-07-24.

Upstream repository:
<https://github.com/power-grid-lib/pglib-opf/tree/v23.07>

Only the four small cases needed for initial validation are vendored:

| File | SHA-256 |
|---|---|
| `pglib_opf_case5_pjm.m` | `cadf7501a15c2d508820493cef6acc85757274197e74c40bcec4fc4ecf619e6f` |
| `pglib_opf_case14_ieee.m` | `bd5c568621de65e4b0922317010868bc7fa94173807faa10ea8fdbbe77c28106` |
| `pglib_opf_case5_pjm__api.m` | `f672aa36ff5645bb569fb0866967c66690ce0dd37c830ee55a3fe5b2dd0cb7d6` |
| `pglib_opf_case14_ieee__api.m` | `6e007be95df3f7171d0c9494c8cc3db1aca1a3a0f2073c3ffbfa43e7b0cd49a2` |

The upstream files identify their original sources and are licensed under
Creative Commons Attribution 4.0.  They are included without modification.

The parser in `src/matpower.py` accepts only the numeric subset needed here;
it does not execute MATLAB code.
