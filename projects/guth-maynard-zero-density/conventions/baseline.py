"""Frozen Cycle-1 conventions for the Guth--Maynard baseline replay.

This module is a conventions source of truth, not a proof of the cited
analytic number theory.  Proof routes must derive their results independently
and compare their outputs with these frozen labels and expected values.
"""

from fractions import Fraction


# Zero-counting convention: multiplicities included and both ordinate signs.
ZERO_REAL_PART_COMPARISON = ">="
ZERO_ORDINATE_INTERVAL = "absolute_value_at_most_T"
ZERO_MULTIPLICITY = "included"

# Parameter orientation and closed audit domain.
SIGMA_LOWER = Fraction(1, 2)
SIGMA_UPPER = Fraction(1, 1)
INGHAM_SWITCH_UPPER = Fraction(7, 10)

# Published baseline outputs to be reconstructed, not assumed by proof routes.
EXPECTED_CROSSOVER_SIGMA = Fraction(7, 10)
EXPECTED_DENSITY_CONSTANT = Fraction(30, 13)
EXPECTED_UNIFORM_THETA = Fraction(17, 30)
EXPECTED_ALMOST_ALL_THETA = Fraction(2, 15)

# Display conventions.
DENSITY_FORM = "N(sigma,T) <= T^(A(sigma)*(1-sigma)+o(1))"
UNIFORM_INTERVAL_ORIENTATION = "[x,x+y]"
ALMOST_ALL_BASE_INTERVAL = "x in [X,2X] intersect Z"

