#!/usr/bin/env python3
"""Independent exact-modular check of the Lane B character-transfer identity."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _frontier_sector_polynomials,
    _rotation_faces,
)
from src.conventions import Edge,cubic_box  # noqa: E402
from src.lane_b_recursive_family import recursive_rotation  # noqa: E402


PRIME=1_000_000_007


def _polynomial_value(polynomial:tuple[int,...],value:int)->int:
    result=0
    power=1
    for coefficient in polynomial:
        result=(result+coefficient*power)%PRIME
        power=power*value%PRIME
    return result


def _edge_boundary(edge:Edge)->int:
    left=3*edge.u[1]+edge.u[2]
    right=3*edge.v[1]+edge.v[2]
    return (1<<left)|(1<<right)


def _slice_kernel(edges:list[tuple[Edge,int]],character:int,value:int)->list[int]:
    kernel=[0]*512
    kernel[0]=1
    for edge,label in edges:
        flip=_edge_boundary(edge)
        signed_weight=-value if (character&label).bit_count()&1 else value
        updated=kernel[:]
        for boundary,coefficient in enumerate(kernel):
            if coefficient:
                updated[boundary^flip]=(updated[boundary^flip]+coefficient*signed_weight)%PRIME
        kernel=updated
    return kernel


def _connector_weights(edges:list[tuple[Edge,int]],character:int,value:int)->list[int]:
    weights=[0]*512
    weights[0]=1
    for edge,label in edges:
        position=3*edge.u[1]+edge.u[2]
        signed_weight=-value if (character&label).bit_count()&1 else value
        current=weights[:]
        for mask,coefficient in enumerate(current):
            if coefficient and not ((mask>>position)&1):
                weights[mask|(1<<position)]=coefficient*signed_weight%PRIME
    return weights


def _character_transfer(length:int,labels:list[int],character:int,value:int)->int:
    _,edges=cubic_box((length,3,3))
    transverse=[[] for _ in range(length)]
    connectors=[[] for _ in range(length-1)]
    for edge,label in zip(edges,labels):
        if edge.u[0]==edge.v[0]:
            transverse[edge.u[0]].append((edge,label))
        else:
            connectors[edge.u[0]].append((edge,label))
    even_masks=[mask for mask in range(512) if mask.bit_count()%2==0]
    state={0:1}
    for layer in range(length):
        kernel=_slice_kernel(transverse[layer],character,value)
        if layer==length-1:
            return sum(coefficient*kernel[mask] for mask,coefficient in state.items())%PRIME
        connector=_connector_weights(connectors[layer],character,value)
        updated={mask:0 for mask in even_masks}
        for incoming,coefficient in state.items():
            for outgoing in even_masks:
                updated[outgoing]=(
                    updated[outgoing]
                    +coefficient*kernel[incoming^outgoing]*connector[outgoing]
                )%PRIME
        state=updated
    raise AssertionError("unreachable transfer exit")


def _characters(dimension:int,exhaustive:bool)->list[int]:
    if exhaustive:
        return list(range(1<<dimension))
    selected={0,(1<<dimension)-1}
    selected.update(1<<index for index in range(dimension))
    selected.update((1<<left)|(1<<right) for left in range(dimension) for right in range(left+1,dimension))
    return sorted(selected)


def _case(length:int,exhaustive:bool)->dict[str,object]:
    vertices,edges=cubic_box((length,3,3))
    rotation=recursive_rotation(length)
    faces,_=_rotation_faces(vertices,edges,rotation)
    genus=length-1
    labels,face_rank=_edge_homology_labels(len(edges),faces,_cycle_basis(vertices,edges),genus)
    sectors,maximum_states=_frontier_sector_polynomials(vertices,edges,labels)
    characters=_characters(2*genus,exhaustive)
    evaluations=[]
    for value in (2,3):
        sector_values={homology:_polynomial_value(polynomial,value) for homology,polynomial in sectors.items()}
        for character in characters:
            walsh=sum(
                (-coefficient if (character&homology).bit_count()&1 else coefficient)
                for homology,coefficient in sector_values.items()
            )%PRIME
            transfer=_character_transfer(length,labels,character,value)
            if walsh!=transfer:
                raise AssertionError(
                    f"character transfer mismatch L={length}, mu={character}, t={value}"
                )
        evaluations.append({"t":value,"characters":len(characters),"all_agree":True})
    return {
        "length":length,"genus":genus,"face_rank":face_rank,
        "sector_count":len(sectors),"maximum_frontier_states":maximum_states,
        "character_selection":"exhaustive" if exhaustive else "zero, all-ones, units, and pairs",
        "evaluations":evaluations,
    }


def verify()->dict[str,object]:
    return {
        "claim_status":"COMPUTATIONALLY VERIFIED",
        "arithmetic":{"field":f"GF({PRIME})","evaluation_points":[2,3]},
        "independence":(
            "Route 1 evaluates exact homology-sector polynomials from the edge frontier. "
            "Route 2 contracts the independently ordered 256-state slice-parity matrices."
        ),
        "cases":[_case(4,True),_case(5,False)],
        "claim_boundary":(
            "These modular controls test the implementation. The multivariate all-size identity "
            "is established algebraically in lane_b_bounded_theta_transfer_proof.md."
        ),
    }


if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
