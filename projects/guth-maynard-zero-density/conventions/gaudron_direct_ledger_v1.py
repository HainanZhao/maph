"""Cycle 98 exponent ledger for direct Gaudron insertion."""

from fractions import Fraction


FIELD_DEGREE_EXPONENT = Fraction(3, 5)
MODE_EXPONENT = Fraction(3, 5)
COEFFICIENT_WEIGHT_EXPONENT = Fraction(1, 3)


def cost_ledger() -> dict[str, object]:
    auxiliary_integer = FIELD_DEGREE_EXPONENT
    coefficient_factor = FIELD_DEGREE_EXPONENT
    squared_height_factor = 2 * FIELD_DEGREE_EXPONENT
    total = auxiliary_integer + coefficient_factor + squared_height_factor
    return {
        "field_degree_exponent": str(FIELD_DEGREE_EXPONENT),
        "mode_exponent": str(MODE_EXPONENT),
        "coefficient_weight_exponent": str(COEFFICIENT_WEIGHT_EXPONENT),
        "gaudron_n": 2,
        "gaudron_t": 1,
        "costs": {
            "auxiliary_integer_a0": str(auxiliary_integer),
            "log_b_plus_a0": str(coefficient_factor),
            "squared_degree_height": str(squared_height_factor),
        },
        "negative_log_exponent": str(total),
        "direct_lower_bound": "exp(-X^(12/5+o(1)))",
        "required_lower_bound": "X^(-C)=exp(-C*log(X))",
        "comparison": "DIRECT_WORST_CASE_GUARANTEE_TOO_WEAK_FOR_POWER_SEPARATION",
        "scope": (
            "Gaudron Theorem 1.1 inserted with d<=4M and M<<D; "
            "no saturation claim for sparse or averaged refinements"
        ),
    }


def support_ledger() -> dict[str, str]:
    return {
        "u_equation": "2*pi*u/D=log((h-Delta)*n/(h*n'))",
        "v_equation": "2*pi*v/D=log(c0*Delta*n'/(m*(h-Delta)))",
        "dyadic_support": "all logarithm arguments lie in fixed compact subsets of (0,infinity)",
        "mode_radius": "max(|u|,|u+v|)<<D=X^(3/5+o(1))",
        "root_degree": "deg(alpha)<=2M",
        "field_degree": "[Q(i,alpha):Q]<=2deg(alpha)<=4M",
    }
