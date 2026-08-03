#!/usr/bin/env python3
"""Exact section-free uniform ray-measure operation and action solve."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from fractions import Fraction
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1||K.no!=1,error("base field certification or class number failed"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];m6=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);ggen=nfbasistoalg(K,bnfisprincipal(K,gideal)[2]);
T(a,b)={return([(5*a+b)%6,(-a)%6]);};
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
sgnsel(x)={my(p=lift(x),a=polcoeff(p,0),b=polcoeff(p,1),t=2*a+5*b);if(b==0,return(if(t>0,1,-1)));if(b>0,return(if(t>0&&t^2>21*b^2,1,-1)));return(if(t>0||t^2<21*b^2,1,-1));};
cong0(x,rm)={my(n2=idealval(K,rm,p2),n3=idealval(K,rm,p3));if(x==0,return(1));return(idealval(K,idealhnf(K,x),p2)>=n2&&idealval(K,idealhnf(K,x),p3)>=n3);};
unitperiod(rm)={for(k=1,36,if(cong0(beta^k-1,rm)&&sgnsel(beta^k)==1,return(k)));error("unit image period exceeds cap");};
equiv(x,y,rm,ord)={for(k=0,ord-1,forstep(s=-1,1,2,if(cong0(s*beta^k*x-y,rm)&&sgnsel(s*beta^k*x)==sgnsel(y),return(1))));return(0);};
data(a,b)={my(q=positive(a,b),gamma=b*beta-q,gi=idealhnf(K,gamma),c=idealadd(K,m6,gi),rm=idealdiv(K,m6,c),ra=idealdiv(K,gi,c),alpha=nfbasistoalg(K,bnfisprincipal(K,ra)[2]));return([rm,ra,alpha]);};
mpair(rm)={return([idealval(K,rm,p2),idealval(K,rm,p3)]);};
assembled(alpha,rm)={my(ord=unitperiod(rm),M=List());for(e=0,5,if(equiv(alpha,ggen^e,rm,ord),listput(M,e)));return(Set(Vec(M)));};
rayset(ra,rm)={my(R=bnrinit(K,[rm,one],1),M=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));return(Set(Vec(M)));};
audit(a,b)={my(y=T(a,b),d=data(a,b),A=assembled(d[3],d[1]),B=rayset(d[2],d[1]),R=bnrinit(K,[d[1],one],1),target=raylog(R,d[2]),ok=1);if(A!=B,error([a,b,A,B]));for(i=1,#A,if(raylog(R,idealpow(K,gideal,A[i]))!=target,ok=0));if(!ok,error(["conductor",a,b,A,target]));print("ROW=",[a,b,y,mpair(d[1]),A]);};
print("BASE=",[K.no,Vec(nfalgtobasis(K,beta)),Vec(nfalgtobasis(K,ggen)),sgnsel(ggen)]);for(a=0,5,for(b=0,5,audit(a,b)));quit();
'''

DIM = 6


def rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    work = [row[:] for row in rows]
    pivots: list[int] = []
    pivot_row = 0
    for col in range(len(work[0]) - 1):
        found = next((r for r in range(pivot_row, len(work)) if work[r][col]), None)
        if found is None:
            continue
        work[pivot_row], work[found] = work[found], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for r in range(len(work)):
            if r != pivot_row and work[r][col]:
                factor = work[r][col]
                work[r] = [entry - factor * base for entry, base in zip(work[r], work[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivots


def source_rows() -> list[dict[str, object]]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=120)
    rows: list[dict[str, object]] = []
    base: list[object] | None = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, successor, modulus, assembled = ast.literal_eval(line.removeprefix("ROW="))
            rows.append({"characteristic": [a, b], "successor": successor, "modulus": modulus, "assembled_exponents": assembled})
        elif line.startswith("BASE="):
            base = ast.literal_eval(line.removeprefix("BASE="))
    if run.stderr or len(rows) != 36 or base != [1, [2, 1], [-7, 1], -1]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "base": base})
    if {tuple(row["modulus"]) for row in rows} != {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}:
        raise AssertionError("lowered-modulus support drift")
    return rows


def measure(exponents: list[int]) -> list[Fraction]:
    if not exponents:
        raise AssertionError("empty assembled exponent set")
    weight = Fraction(1, len(exponents))
    return [weight if e in exponents else Fraction(0) for e in range(DIM)]


def solve_action(rows: list[dict[str, object]]) -> dict[str, object]:
    by_point = {tuple(row["characteristic"]): row for row in rows}
    vectors = {point: measure(row["assembled_exponents"]) for point, row in by_point.items()}
    equivariance: list[list[Fraction]] = []
    for point, row in by_point.items():
        source = vectors[point]
        target = vectors[tuple(row["successor"])]
        for out in range(DIM):
            equivariance.append([Fraction(int(out == i)) * source[j] for i in range(DIM) for j in range(DIM)] + [target[out]])
    equivariance_rref, equivariance_pivots = rref(equivariance)
    equivariance_inconsistent = [row for row in equivariance_rref if all(value == 0 for value in row[:-1]) and row[-1] != 0]
    equations = equivariance[:]
    for col in range(DIM):
        equations.append([Fraction(int(j == col)) for _i in range(DIM) for j in range(DIM)] + [Fraction(1)])
    reduced, pivots = rref(equations)
    inconsistent = [row for row in reduced if all(value == 0 for value in row[:-1]) and row[-1] != 0]
    measure_rank = len(rref([vectors[point] + [Fraction(0)] for point in sorted(vectors)])[1])
    result: dict[str, object] = {
        "equations": len(equations), "unknowns": DIM * DIM, "equivariance_equations": len(by_point) * DIM,
        "augmentation_equations": DIM, "rref_rank": len(pivots), "measure_span_rank": measure_rank,
        "consistent": not inconsistent,
        "equivariance_consistent_without_augmentation": not equivariance_inconsistent,
        "equivariance_rref_rank": len(equivariance_pivots),
    }
    measure_groups: dict[tuple[Fraction, ...], list[tuple[int, int]]] = {}
    for point, vector in vectors.items():
        measure_groups.setdefault(tuple(vector), []).append(point)
    collisions = []
    for vector, points in sorted(measure_groups.items()):
        successor_vectors = {tuple(vectors[tuple(by_point[point]["successor"])]) for point in points}
        if len(successor_vectors) > 1:
            collisions.append({"source_measure": [str(value) for value in vector], "points": [list(point) for point in points], "successor_measures": [[str(value) for value in successor] for successor in sorted(successor_vectors)]})
    result["identical_source_measure_conflicts"] = collisions
    if inconsistent:
        row = inconsistent[0]
        result["inconsistency_certificate"] = [str(value) for value in row]
        return result
    if len(pivots) != DIM * DIM or measure_rank != DIM:
        result["status"] = "UNDERDETERMINED_LINEAR_CLASS_REQUIRES_SEPARATE_PREREGISTERED_ANALYSIS"
        return result
    solution = [Fraction(0) for _ in range(DIM * DIM)]
    for r, col in enumerate(pivots):
        solution[col] = reduced[r][-1]
    matrix = [[solution[i * DIM + j] for j in range(DIM)] for i in range(DIM)]
    cube = [[sum(matrix[i][k] * matrix[k][l] * matrix[l][j] for k in range(DIM) for l in range(DIM)) for j in range(DIM)] for i in range(DIM)]
    if cube != [[Fraction(int(i == j)) for j in range(DIM)] for i in range(DIM)]:
        result["status"] = "UNIQUE_EQUIVARIANT_AUGMENTATION_ACTION_FAILS_THIRD_RETURN"
        result["matrix"] = [[str(value) for value in row] for row in matrix]
        return result
    result["status"] = "UNIQUE_SECTION_FREE_LINEAR_ACTION_EXISTS"
    result["matrix"] = [[str(value) for value in row] for row in matrix]
    return result


def build_payload() -> dict[str, object]:
    rows = source_rows()
    solved = solve_action(rows)
    anchors = {tuple(row["characteristic"]): row["assembled_exponents"] for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if anchors != {(3, 5): [1], (3, 4): [2]}:
        raise AssertionError(anchors)
    return {
        "schema": "sic-stark-cycle-182-section-free-linear-operation-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result tests the preregistered canonical uniform-fibre map and the complete rational augmentation-preserving linear target-action class only. It defines no AFK coefficient identification, Stark regulator equality, fusion theorem, or TCC identity.",
        "conventions": {"source": "Q[(Z/6Z)^2] with T(a,b)=(5a+b,-a)", "target": "Q[C6]", "canonical_map": "basis point maps to uniform measure on its source-built assembled exponent set", "target_action": "all rational augmentation-preserving 6x6 actions constrained by equivariance and A^3=I"},
        "summary": {"rows_checked": len(rows), "conductor_pushforwards_checked": len(rows), "orientation_anchors": {"3,5": anchors[(3, 5)], "3,4": anchors[(3, 4)]}, "action_solve": solved},
        "rows": rows,
        "gate_outcome": {"section_free_linear_operation": solved.get("status", "LINEAR_CLASS_INCONSISTENT"), "scope": "finite section-free operation class only"},
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
