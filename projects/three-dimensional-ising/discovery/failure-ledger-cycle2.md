# Cycle 2 failure ledger

This supplements, and does not modify, the Stage 1 ledger frozen by the Cycle
1 artifact.

| ID | Lane and ansatz | Status | Exact result | Remaining opening |
|---|---|---|---|---|
| F201 | A: direct binary parity `R` in the standard vertex tetrahedron equation | `RESTRICTED NO-GO` | `PROVED`: the `(out,in)=(0,3)` residual restricts on `x=y=z=t` to `-(t-1)^3(t+1)^2`, nonzero for `0<t<1` | IRF/cube relations or non-invariant auxiliary mixing |
| F202 | A: naive three-parameter physical layer family | `RESTRICTED NO-GO` | `PROVED`: an exact `3x3` periodic commutator entry is `25050585732481024/54045009375` | A different spectral locus and intertwiner |
| F203 | B: factorization over genus-one handle bits | `RESTRICTED NO-GO` | `PROVED`: both the toroidal `3x3` calibration and a minimum-genus embedding of the free cubic `3x3x2` slab have `F` matrix rank two, not one | Submaximal growing-genus TT rank |
| F204 | B: bounded Boolean Fourier degree | `KILLED` | `PROVED`: for a cellular embedding every homology class has a graph cycle and a nonzero positive-weight sector polynomial, so all `4^g` Fourier characters occur | A collective transform not based on Fourier sparsity |
| F205 | B: polynomially many sectors from cubic symmetry | `KILLED` | `PROVED`: `|Aut(G_L)|=48` for `L>=3`, hence at least `ceil(4^g/48)` spin-structure orbits | Algebraic equivalences larger than geometric symmetry |
| F206 | C: substitute the known free-fermion bosonization for the Ising-dual gauge model | `KILLED` | `PROVED`: standard and modified Gauss projectors disagree already on `G_v=+1, W_NE=-1` | A new interacting higher-form equivalence with the physical constraint |
| F207 | C: leave gauge flux unrestricted and evaluate sectors independently | `KILLED` | `PROVED`: an `LxL` torus has `2^(L^2+1)` gauge-inequivalent link fields | A proved collective flux summation |
| F208 | D: local cubic parity tensor is not Gaussian | `KILLED` as an objection | `PROVED`: all 32 even principal minors agree with one antisymmetric `6x6` matrix | The obstruction is global crossings, not the site tensor |
| F209 | D: ordinary crossings remain matchgates after diagonal bond gauges | `RESTRICTED NO-GO` | `PROVED`: the four-leg Grassmann--Pluecker residual is `2` and scales nontrivially under invertible diagonal gauges | General holographic bases or correlated crossover selectors |
| F210 | D: independent bounded crossing selectors reduce complexity | `RESTRICTED NO-GO` | `PROVED`: `C_b=C_f+2E_1111` uses `D=2`, but `c` independent crossings give `2^c` exact sectors | Exact recursive closure of the selector network |
| F211 | E: nearest-neighbour or pairwise closure after checkerboard `2x2x2` blocking | `RESTRICTED NO-GO` | `PROVED`: exact four- and six-body Walsh ratios are not one | A larger finite algebra, critical-locus closure, or nonlocal coordinates |
