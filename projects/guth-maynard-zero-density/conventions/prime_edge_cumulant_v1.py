"""Exact symbolic Cycle 56 prime-coordinate edge cumulant."""
from __future__ import annotations

from math import comb


def signed_expansion(s: int) -> list[dict[str, int | str]]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive ordinary-coordinate count")
    terms: list[dict[str, int | str]] = []
    for powered_choice in (0, 1):
        for ordinary_product_choices in range(s + 1):
            coefficient = (-1) ** (powered_choice + ordinary_product_choices) * comb(s, ordinary_product_choices)
            terms.append({
                "powered_factor": "k_m(h-g)" if powered_choice == 0 else "k_m(h)conj(k_m(g))",
                "ordinary_difference_power": s - ordinary_product_choices,
                "ordinary_product_power": ordinary_product_choices,
                "coefficient": coefficient,
            })
    return terms


def kernel_ledger(s: int) -> dict[str, object]:
    terms = signed_expansion(s)
    return {
        "s": s,
        "ordinary_covariance": "C(h,g)=k(h-g)-k(h)conj(k(g))",
        "powered_covariance": "C_m(h,g)=k(m(h-g))-k(mh)conj(k(mg))",
        "tensor_gram": "E_(m,s)(h,g)=C_m(h,g)C(h,g)^s",
        "diagonal": "E_(m,s)(h,h)=(1-|k(mh)|^2)(1-|k(h)|^2)^s",
        "zero_edge": "E_(m,s)(0,g)=E_(m,s)(h,0)=0",
        "positive_semidefinite": True,
        "signed_terms": terms,
        "term_count": len(terms),
        "coefficient_l1": sum(abs(int(term["coefficient"])) for term in terms),
        "coefficient_sum": sum(int(term["coefficient"]) for term in terms),
    }


def verify_all() -> dict[str, object]:
    s3 = kernel_ledger(3)
    s4 = kernel_ledger(4)
    if s3["term_count"] != 8 or s3["coefficient_l1"] != 16:
        raise RuntimeError("s3 signed expansion")
    if s4["term_count"] != 10 or s4["coefficient_l1"] != 32:
        raise RuntimeError("s4 signed expansion")
    if s3["coefficient_sum"] != 0 or s4["coefficient_sum"] != 0:
        raise RuntimeError("centering cancellation")
    return {
        "s3": s3,
        "s4": s4,
        "analytic_gate": "bound_the_edge_cumulant_spectrum_or_extract_approximate_multiplicativity_with_3_50_margin",
    }


if __name__ == "__main__":
    print(verify_all())
