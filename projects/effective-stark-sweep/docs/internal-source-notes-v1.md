# Internal SIC source notes for the sweep

Date: 2026-07-29

The workspace contains `projects/sic-stark`; no distinct
`projects/sic-start` directory was found.  The former was therefore
used as the unpublished/internal research source intended by the
instruction.

The W1 implementation specifically borrows:

- the exact formula
  \[
  [H:H\cap\mathbb Q^{\rm ab}]
  =|C|/|B\cap C|
  =|\langle B,C\rangle|/|B|
  \]
  and the conductor-lowering warning from `sic-stark-cycle45.md`;
- the place-swap lesson and two-place character pullback from
  `dimension_eight_cm_descent.gp`;
- the operational unit-congruence tests from
  `dimension_five_shintani_audit.gp`,
  `dimension_seven_shintani_audit.gp`, and
  `dimension_eight_lower_shintani_audit.gp`;
- the separation between a theorem-coverage screen and a completed
  proof from `screen_higher_dimension_theorem_coverage.py`;
- the explicit warning that dimension 16 fails condition (0-9) from
  the current SIC program-status note.

These sources are treated as frozen internal reproduction inputs.  A
screen result is consequently labeled `ROUTE_CANDIDATE`, not
`PROVED`, until the downstream proof obligations close.
