# Paper II reproducibility package

This package accompanies:

> *Twisted-Convolution Identities in Dimensions Seven and Eight:
> Shintani Height Rigidity and CM Descent*

## Main theorem

For every admissible dimension-seven tuple of discriminant \(32\), and
for every admissible dimension-eight tuple, both \(0\) and \(1\) are
formal TCC shifts. Shift sets agree for forms of the same discriminant.
The admissible dimension-seven discriminant-\(8\) stratum is explicitly
outside the theorem and remains open.

Dimension eight has two separately certified form discriminants:

- discriminant \(45\), closed by linear CM reinduction and an oriented
  imaginary-quadratic Stark-unit calculation;
- discriminant \(5\), closed by quadratic ray units and exact symbolic
  reduction of all 63 cocycle phases.

## Required software

- Python 3.12 or compatible;
- NumPy;
- PARI/GP 2.15.4 or compatible;
- python-flint 0.9.0 for the rigorous Arb orientation and
  dimension-seven height certificates.

## Principal commands

```bash
python3 -m unittest tests.test_dimension_seven_closure
gp -q scripts/dimension_seven_admissible_strata.gp
gp -q scripts/dimension_seven_exact_tcc.gp
gp -q scripts/dimension_eight_linear_cm_reinduction.gp
gp -q scripts/dimension_eight_cm_unit_lattice.gp
PYTHONPATH=scripts python3 scripts/certify_dimension_eight_cm_orientation.py
gp -q scripts/dimension_eight_cm_real_unit_bridge.gp
gp -q scripts/dimension_eight_exact_tcc.gp
gp -q scripts/dimension_eight_maximal_tuple_audit.gp
gp -q scripts/dimension_eight_maximal_quadratic_units.gp
python3 scripts/dimension_eight_maximal_sign_audit.py
python3 scripts/dimension_eight_maximal_exact_tcc.py
python3 -m unittest tests.test_dimension_eight_unconditional_closure
```

Every archived file is covered by `ARCHIVE_CONTENTS.sha256`.

The manuscripts and documentation use CC BY 4.0; executable code uses
the MIT license. See `LICENSE` and `LICENSE-CODE`.
