"""Exact symbolic Cycle 60 coordinate-ANOVA ledger."""
from __future__ import annotations

from math import comb


def component_types(s: int) -> list[dict[str, object]]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive ordinary-coordinate count")
    rows: list[dict[str, object]] = []
    for powered_centered in (False, True):
        for ordinary_centered in range(s + 1):
            multiplicity = comb(s, ordinary_centered)
            rows.append({
                "powered_centered": powered_centered,
                "ordinary_centered": ordinary_centered,
                "subset_multiplicity": multiplicity,
                "powered_edge_factor": "w_(mh)(q)" if powered_centered else "k(mh)",
                "ordinary_centered_factor": "w_h(p)",
                "ordinary_mean_factor": "k(h)",
                "is_constant_component": (not powered_centered and ordinary_centered == 0),
                "is_full_interaction": (powered_centered and ordinary_centered == s),
            })
    return rows


def anova_ledger(s: int) -> dict[str, object]:
    rows = component_types(s)
    coordinate_count = s + 1
    return {
        "s": s,
        "coordinate_count": coordinate_count,
        "subset_component_count": 2 ** coordinate_count,
        "nonconstant_component_count": 2 ** coordinate_count - 1,
        "symmetry_type_count": len(rows),
        "type_multiplicity_sum": sum(int(row["subset_multiplicity"]) for row in rows),
        "constant_component": "sum_(t,u)z_t conj(z_u) k(m(t-u)) k(t-u)^s",
        "full_interaction": "sum_(t,u)z_t conj(z_u) w_(m(t-u))(q) product_j w_(t-u)(p_j)",
        "full_interaction_quadratic_norm": "sum_(e,f)omega_e conj(omega_f) C_m(h_e,h_f) C(h_e,h_f)^s",
        "parseval": "||E||_2^2=sum_J||E_J||_2^2",
        "variance_parseval": "||E-E_empty||_2^2=sum_(J nonempty)||E_J||_2^2",
        "types": rows,
    }


def verify_all() -> dict[str, object]:
    s3 = anova_ledger(3)
    s4 = anova_ledger(4)
    if s3["subset_component_count"] != 16 or s3["symmetry_type_count"] != 8:
        raise RuntimeError("s3 ANOVA count")
    if s4["subset_component_count"] != 32 or s4["symmetry_type_count"] != 10:
        raise RuntimeError("s4 ANOVA count")
    if s3["type_multiplicity_sum"] != 16 or s4["type_multiplicity_sum"] != 32:
        raise RuntimeError("type multiplicity reconciliation")
    for data in (s3, s4):
        full = [row for row in data["types"] if row["is_full_interaction"]]
        constant = [row for row in data["types"] if row["is_constant_component"]]
        if len(full) != 1 or len(constant) != 1:
            raise RuntimeError("distinguished ANOVA components")
    return {
        "s3": s3,
        "s4": s4,
        "routing": "large_variance_routes_to_one_nonconstant_component_at_constant_cost; small_variance_is_flat_energy_inverse_branch",
    }


if __name__ == "__main__":
    print(verify_all())
