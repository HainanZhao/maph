"""A two-angle, lossless three-bus power-flow model.

Bus 0 is the angle reference.  All voltage magnitudes are fixed to one.
Positive line weights are the magnitudes of the line susceptances.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


Vector2 = tuple[float, float]
Matrix2 = tuple[tuple[float, float], tuple[float, float]]


@dataclass(frozen=True)
class KantorovichCertificate:
    """A local Newton--Kantorovich feasibility certificate."""

    certified: bool
    residual_inf: float
    newton_step_inf: float
    inverse_jacobian_inf: float
    jacobian_lipschitz: float
    h: float
    radius: float | None


def injections(
    theta: Sequence[float],
    b01: float = 1.0,
    b12: float = 1.0,
    b02: float = 1.0,
) -> Vector2:
    """Return active injections at buses 1 and 2."""

    theta1, theta2 = theta
    p1 = b01 * math.sin(theta1) + b12 * math.sin(theta1 - theta2)
    p2 = b02 * math.sin(theta2) + b12 * math.sin(theta2 - theta1)
    return p1, p2


def jacobian(
    theta: Sequence[float],
    b01: float = 1.0,
    b12: float = 1.0,
    b02: float = 1.0,
) -> Matrix2:
    """Return the Jacobian of ``injections`` with respect to both angles."""

    theta1, theta2 = theta
    coupling = b12 * math.cos(theta1 - theta2)
    return (
        (b01 * math.cos(theta1) + coupling, -coupling),
        (-coupling, b02 * math.cos(theta2) + coupling),
    )


def solve_2x2(matrix: Matrix2, rhs: Sequence[float]) -> Vector2:
    """Solve a nonsingular real 2x2 system."""

    (a, b), (c, d) = matrix
    determinant = a * d - b * c
    scale = max(abs(a * d), abs(b * c), 1.0)
    if abs(determinant) <= 1e-14 * scale:
        raise ValueError("singular or numerically singular Jacobian")
    x = (d * rhs[0] - b * rhs[1]) / determinant
    y = (-c * rhs[0] + a * rhs[1]) / determinant
    return x, y


def inverse_inf_norm(matrix: Matrix2) -> float:
    """Return the induced infinity norm of a nonsingular 2x2 inverse."""

    (a, b), (c, d) = matrix
    determinant = a * d - b * c
    scale = max(abs(a * d), abs(b * c), 1.0)
    if abs(determinant) <= 1e-14 * scale:
        raise ValueError("singular or numerically singular Jacobian")
    return max(
        (abs(d) + abs(b)) / abs(determinant),
        (abs(c) + abs(a)) / abs(determinant),
    )


def global_jacobian_lipschitz(
    b01: float = 1.0,
    b12: float = 1.0,
    b02: float = 1.0,
) -> float:
    """A global infinity-norm Lipschitz constant for the Jacobian.

    This deliberately simple bound uses |cos(x)-cos(y)| <= |x-y|.  It is
    rigorous but not expected to be sharp.
    """

    return max(abs(b01) + 4.0 * abs(b12), abs(b02) + 4.0 * abs(b12))


def kantorovich_certificate(
    theta: Sequence[float],
    target: Sequence[float],
    b01: float = 1.0,
    b12: float = 1.0,
    b02: float = 1.0,
) -> KantorovichCertificate:
    """Certify a nearby solution of injections(theta)=target when possible."""

    value = injections(theta, b01, b12, b02)
    residual = (value[0] - target[0], value[1] - target[1])
    residual_inf = max(abs(residual[0]), abs(residual[1]))
    matrix = jacobian(theta, b01, b12, b02)
    try:
        step = solve_2x2(matrix, residual)
        beta = inverse_inf_norm(matrix)
    except ValueError:
        return KantorovichCertificate(
            certified=False,
            residual_inf=residual_inf,
            newton_step_inf=math.inf,
            inverse_jacobian_inf=math.inf,
            jacobian_lipschitz=global_jacobian_lipschitz(
                b01, b12, b02
            ),
            h=math.inf,
            radius=None,
        )

    eta = max(abs(step[0]), abs(step[1]))
    lipschitz = global_jacobian_lipschitz(b01, b12, b02)
    k = beta * lipschitz
    h = k * eta
    if h > 0.5:
        radius = None
        certified = False
    elif k == 0.0:
        radius = eta
        certified = True
    else:
        radius = (1.0 - math.sqrt(max(0.0, 1.0 - 2.0 * h))) / k
        certified = True
    return KantorovichCertificate(
        certified=certified,
        residual_inf=residual_inf,
        newton_step_inf=eta,
        inverse_jacobian_inf=beta,
        jacobian_lipschitz=lipschitz,
        h=h,
        radius=radius,
    )


def newton_solve(
    theta: Sequence[float],
    target: Sequence[float],
    b01: float = 1.0,
    b12: float = 1.0,
    b02: float = 1.0,
    tolerance: float = 1e-13,
    max_iterations: int = 30,
) -> Vector2:
    """Solve the two-angle power flow by undamped Newton iteration."""

    current = (float(theta[0]), float(theta[1]))
    for _ in range(max_iterations):
        value = injections(current, b01, b12, b02)
        residual = (value[0] - target[0], value[1] - target[1])
        if max(abs(residual[0]), abs(residual[1])) <= tolerance:
            return current
        step = solve_2x2(jacobian(current, b01, b12, b02), residual)
        current = (current[0] - step[0], current[1] - step[1])
    raise RuntimeError("Newton iteration did not converge")
