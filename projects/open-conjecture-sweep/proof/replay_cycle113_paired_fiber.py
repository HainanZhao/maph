#!/usr/bin/env python3
"""Independent bitset C113 replay: direct matrices only, no triangle formula."""
import json

Q=7; N=14
PAIRS=[(x,y) for x in range(Q) for y in range(x+1,Q)]
FREE=[p for p in PAIRS if p[0] != 0]

def main():
    hits=[]; profiles={}
    for mask in range(1 << 15):
        h={(0,y):1 for y in range(1,Q)}
        h.update({(x,y):1 if (mask>>i)&1 else -1 for i,(x,y) in enumerate(FREE)})
        rows=[0]*N
        for x in range(Q): rows[2*x]|=1<<(2*x+1); rows[2*x+1]|=1<<(2*x)
        for x,y in PAIRS:
            s=h[(x,y)]
            for e in (0,1):
                for f in (0,1):
                    if (1 if e==f else -1)==s:
                        u,v=2*x+e,2*y+f; rows[u]|=1<<v; rows[v]|=1<<u
        r=b=0
        for u in range(N):
            for v in range(u+1,N):
                same=(rows[u]&rows[v]).bit_count() if (rows[u]>>v)&1 else ((~rows[u])&(~rows[v])&((1<<N)-1)).bit_count()-2
                if (rows[u]>>v)&1:r=max(r,same)
                else:b=max(b,same)
        profiles[(r,b)]=profiles.get((r,b),0)+1
        if r<=2 and b<=3:hits.append(mask)
    print(json.dumps({'status':'PASS' if not hits else 'FAIL','balanced_states_directly_checked':32768,'hits':hits,'profiles':[[list(k),v] for k,v in sorted(profiles.items())]},sort_keys=True))
if __name__=='__main__':main()
