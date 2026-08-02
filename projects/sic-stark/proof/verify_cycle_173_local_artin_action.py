#!/usr/bin/env python3
"""Derive the first local Artin action for the oriented d=6 ray field.

The exact PARI check fixes the ray class field data and its oriented global
generator.  The remaining calculation is the local inertia action on
``P_L/P_L^2``: wild inertia acts trivially and the order-two tame quotient
acts through the unique order-two element of ``F_3^*``.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);
L=bnfinit(x^12+3*x^11-6*x^10-16*x^9+3*x^8+27*x^6+3*x^4-16*x^3-6*x^2+3*x+1,1);
R=bnrinit(K,[6,[1,0]],1);
pK=idealprimedec(K,3);pL=idealprimedec(L,3);
beta=Mod(y,y^2-5*y+1);p37=idealhnf(K,4*beta+1);
log37=lift(bnrisprincipal(R,p37,0)[1]);
relative=bnrclassfield(R,,1);ray_absolute=rnfequation(K,relative);
ray_isomorphisms=nfisisom(x^12+3*x^11-6*x^10-16*x^9+3*x^8+27*x^6+3*x^4-16*x^3-6*x^2+3*x+1,ray_absolute);
print("K_CERTIFIED=",bnfcertify(K));
print("RAY_ORDER=",R.no);
print("RAY_CYC=",R.cyc);
print("K_PRIME_COUNT=",#pK);
print("K_E=",pK[1][3]);
print("K_F=",pK[1][4]);
print("L_PRIME_COUNT=",#pL);
print("L_E=",pL[1][3]);
print("L_F=",pL[1][4]);
print("P37_NORM=",idealnorm(K,p37));
print("P37_RAY_LOG=",log37);
print("RAY_FIELD_ISOMORPHISM_COUNT=",#ray_isomorphisms);
quit();
'''


def exact_local_data() -> dict[str, str]:
    completed = subprocess.run(
        ["gp", "-q"], input=GP, text=True, capture_output=True, check=True
    )
    rows = [line.split("=", 1) for line in completed.stdout.splitlines() if "=" in line]
    return {key.strip(): value.strip() for key, value in rows}


def build_payload() -> dict[str, object]:
    data = exact_local_data()
    expected = {
        "K_CERTIFIED": "1", "RAY_ORDER": "6", "RAY_CYC": "[6]", "K_PRIME_COUNT": "1",
        "K_E": "2", "K_F": "1", "L_PRIME_COUNT": "1", "L_E": "12",
        "L_F": "1", "P37_NORM": "37", "P37_RAY_LOG": "1",
        "RAY_FIELD_ISOMORPHISM_COUNT": "6",
    }
    if data != expected:
        raise AssertionError({"actual": data, "expected": expected})

    # Exact local-inertia calculation.  Since L/K is cyclic of degree 6 and
    # totally ramified at 3, its wild inertia is the unique order-three
    # subgroup W=<g^2>.  W fixes P_L/P_L^2.  The quotient C6/W=C2 acts by
    # its tame character in F_3^*, whose only nonidentity element is 2=-1.
    rho_g = 2
    action = [pow(rho_g, exponent, 3) for exponent in range(6)]
    if action != [1, 2, 1, 2, 1, 2]:
        raise AssertionError(action)
    if action[1] != action[5] or action[2] != 1:
        raise AssertionError("orientation or wild-action derivation drift")
    return {
        "schema": "sic-stark-cycle-173-local-artin-action-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact local-inertia result determines only the action on "
            "the first quotient U_L^1/U_L^2. It proves no deeper-filtration "
            "action, wild-local regulator equality, coefficient map, AFK "
            "interface, fusion theorem, or TCC identity."
        ),
        "exact_inputs": {
            "ray_group": "C6", "oriented_generator": "g=Frob_(4 beta+1), ray log 1",
            "local_prime": "unique P above 3", "base_e_f": [2, 1],
            "ray_e_f": [12, 1], "relative_e": 6, "residue_field": "F3",
        },
        "local_inertia_derivation": {
            "wild_inertia": "W=<g^2>=C3", "wild_action_on_gr1": 1,
            "tame_quotient": "C2", "tame_character_image": "F3^*={1,2}",
            "rho_g": "multiplication by 2 = -1", "rho_g_squared": "identity",
            "all_artin_powers": action,
        },
        "orientation_test": {
            "rho_g_equals_rho_g_inverse": True,
            "conclusion": "The first local graded quotient loses the oriented Artin label.",
        },
        "gate_outcome": {
            "first_graded_action": "DERIVED_ORIENTATION_BLIND",
            "next_engine": "derive the first deeper graded quotient or a non-graded oriented local invariant",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
