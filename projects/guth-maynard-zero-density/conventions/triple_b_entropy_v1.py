"""Exact Cycle 94 triple-B entropy phase ledger."""

import sympy as sp


h, delta, m, n, n_prime, c0 = sp.symbols(
    "h delta m n n_prime c0", positive=True
)
h_prime = h - delta

F = (
    delta * sp.log(c0 * delta / m)
    - h * sp.log(h / n)
    + h_prime * sp.log(h_prime / n_prime)
)


def verify_all() -> dict[str, object]:
    f_h = sp.simplify(sp.diff(F, h))
    f_delta = sp.diff(F, delta)
    hessian = sp.hessian(F, (h, delta))
    determinant = sp.simplify(hessian.det())
    assert f_h == sp.log(n * h_prime / (h * n_prime))
    expected_delta = sp.log(c0 * delta * n_prime / (m * h_prime))
    assert sp.simplify(
        sp.expand_log(f_delta, force=True) - sp.expand_log(expected_delta, force=True)
    ) == 0
    assert determinant == 0
    # Central F_h=0 gives h'/h=n'/n. Substitution into F_delta=0 gives
    # c0*delta*n/(m*h)=1, hence m=c0*n*delta/h=c0*(n-n').
    central_m = sp.simplify(c0 * n * delta / h)
    anchor_difference = sp.simplify(
        central_m.subs(delta, h * (n - n_prime) / n)
    )
    assert anchor_difference == c0 * (n - n_prime)
    return {
        "combined_phase": (
            "F=Delta*log(c0*Delta/m)-h*log(h/n)"
            "+(h-Delta)*log((h-Delta)/n')"
        ),
        "F_h": "log((h-Delta)*n/(h*n'))",
        "F_Delta": "log(c0*Delta*n'/(m*(h-Delta)))",
        "central_ratio": "(h-Delta)/h=n'/n",
        "central_anchor_difference": "m=c0*(n-n')",
        "hessian": [
            ["1/(h-Delta)-1/h", "-1/(h-Delta)"],
            ["-1/(h-Delta)", "1/Delta+1/(h-Delta)"],
        ],
        "hessian_determinant": "0 identically",
        "homogeneity": "F(lambda*h,lambda*Delta)=lambda*F(h,Delta)",
        "open_modes": (
            "nonzero Poisson modes in h and Delta create projective entropy "
            "aliases and are not covered by the central relation"
        ),
        "gate": "central anchor-difference web banked; projective entropy aliases open",
    }


if __name__ == "__main__":
    print(verify_all())
