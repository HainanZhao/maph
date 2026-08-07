#!/usr/bin/env python3
"""Difference-set route for all degree-7 two-block circulant states."""
import itertools,json

Q=7
SYMMETRIC=[frozenset(v for i,p in enumerate(((1,6),(2,5),(3,4))) if (m>>i)&1 for v in p) for m in range(8)]

def common(A,B,d,colour):
    return sum(((z in A)==colour) and (((z-d)%Q in B)==colour) for z in range(Q))

def check(d11,d12,d22):
    red=blue=0
    # Within layer 0 and 1: a nonzero difference d labels the edge colour.
    for D,E in ((d11,d12),(d22,{-x%Q for x in d12})):
        for d in range(1,Q):
            colour=d in D
            # For a blue within-layer edge, z=0 and z=d are counted by the
            # complement indicator but are the two endpoints, not neighbours.
            k=common(D,D,d,colour)+common(E,E,d,colour)-(2 if not colour else 0)
            if colour:red=max(red,k)
            else:blue=max(blue,k)
    # Across layers, x=0 and y=d; the two same-layer common-neighbour terms.
    for d in range(Q):
        colour=d in d12
        # For a blue cross edge, the two endpoints occur once each in these
        # complement intersections and must be removed.
        k=common(d11,{-x%Q for x in d12},d,colour)+common(d12,d22,d,colour)-(2 if not colour else 0)
        if colour:red=max(red,k)
        else:blue=max(blue,k)
    return red,blue

def main():
    states=[]; profiles={};hits=[]
    for d11,d22 in itertools.product(SYMMETRIC,repeat=2):
        if len(d11)!=len(d22):continue
        for d12 in itertools.combinations(range(Q),Q-len(d11)):
            d12=frozenset(d12); states.append((d11,d12,d22))
            p=check(d11,d12,d22);profiles[p]=profiles.get(p,0)+1
            if p[0]<=2 and p[1]<=3:hits.append([sorted(d11),sorted(d12),sorted(d22)])
    assert len(states)==512
    print(json.dumps({'status':'PASS','states':len(states),'hits':hits,'profiles':[[list(k),v] for k,v in sorted(profiles.items())]},sort_keys=True))
if __name__=='__main__':main()
