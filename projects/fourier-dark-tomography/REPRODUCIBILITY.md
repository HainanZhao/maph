# Reproducing the Fourier dark-event results

Use the release tag `fourier-dark-tomography-v1`. From this project
directory, all Python calculations use only the standard library.

## Complete test suite

```sh
python3 -m unittest discover -s tests -v
```

## Claim-to-command map

| Manuscript result | Command |
|---|---|
| Arbitrary-mode ranks and fixed-probe references | `python3 scripts/certify_general_fourier_cat_tomography.py --max-modes 9` |
| \(F_4\) Fock and cat Jacobians and determinants | `python3 scripts/search_su4_dark_tomography.py` |
| Finite-angle bias and count-information table | `python3 scripts/analyze_cat_finite_statistics.py` |
| All-mode probability, allocation, and CR scaling | `python3 scripts/analyze_general_resource_scaling.py` |
| Weighted \(F_4\) reconstruction Monte Carlo | `python3 scripts/simulate_f4_reconstruction.py --repetitions 5000` |

The coefficient-SPAM ranks are tested exactly over Gaussian integers by
`tests/test_general_fourier_cat_tomography.py`. The arbitrary-mode
identifiability matrices use exact rational elimination. The finite-angle
and Monte Carlo programs evaluate the defining normalized cat polynomial
directly.

## Paper

```sh
cd paper
/tmp/tectonic -X compile manuscript.tex --outdir build --keep-logs
```

The code is available under the [MIT license](LICENSE-CODE). The manuscript
and bibliography are not relicensed by that file.
