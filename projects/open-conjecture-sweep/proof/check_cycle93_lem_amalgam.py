"""Exact C93 canonical C81 free-amalgam replay."""
from __future__ import annotations
import json
PRE=(0,0,2,0,1,8,25,7,42); N=16

def build():
    # Copy A: 0..8; copy B maps 0->0, 3->3, and other v->v+7.
    mp=lambda v: v if v in (0,3) else v+7
    pre=[0]*N
    for copy,fn in ((0,lambda v:v),(1,mp)):
        for v,m in enumerate(PRE):
            target=fn(v)
            for u in range(9):
                if m>>u&1: pre[target]|=1<<fn(u)
    pre[mp(1)]|=1<<1 # x<y
    for k in range(N):
        for v in range(N):
            if pre[v]>>k&1: pre[v]|=pre[k]
    assert all(not(pre[v]>>v&1) for v in range(N))
    return tuple(pre),1,mp(1),0,3

def count(pre, extra=None, reverse=False):
    p=list(pre)
    if extra: p[extra[1]]|=1<<extra[0]
    for k in range(N):
        for v in range(N):
            if p[v]>>k&1:p[v]|=p[k]
    dp=[0]*(1<<N); dp[0]=1
    for s in range(1<<N):
        if not dp[s]:continue
        if reverse:
            for v in range(N):
                if not(s>>v&1) and not any((p[u]>>v&1) and not(s>>u&1) for u in range(N)): dp[s|1<<v]+=dp[s]
        else:
            for v in range(N):
                if not(s>>v&1) and p[v]&~s==0:dp[s|1<<v]+=dp[s]
    return dp[-1]

def payload():
    pre,x,y,z,w=build(); total=count(pre); pairs=[[0]*N for _ in range(N)]
    for a in range(N):
      for b in range(N):
       if a!=b:pairs[a][b]=count(pre,(a,b))
    assert total==count(pre,reverse=True)
    assert all(pairs[a][b]+pairs[b][a]==total for a in range(N) for b in range(a))
    edge=lambda a,b:pairs[a][b]>pairs[b][a]
    inc=lambda a,b:not(pre[a]>>b&1 or pre[b]>>a&1)
    tri=[(x,z),(z,w),(w,x),(y,z),(z,w),(w,y)]
    reverse_marked=[count(pre,pair,reverse=True) for pair in tri]
    assert reverse_marked==[pairs[a][b] for a,b in tri]
    marked=all(edge(a,b) for a,b in tri)
    restricted=any(edge(a,b)and edge(b,c)and edge(c,d)and edge(d,a) and all(inc(u,v) for u,v in ((a,b),(b,c),(c,d),(d,a))) for a in range(N)for b in range(N)for c in range(N)for d in range(N)if len({a,b,c,d})==4)
    return {"status":"PASS","epistemic_status":"PROVED","vertices":N,"extensions":total,"x":x,"y":y,"z":z,"w":w,"marked_pairs":[[a,b,pairs[a][b],pairs[b][a]] for a,b in tri],"marked_pair_route_agreement":True,"marked_arrows_hold":marked,"full_cycle":edge(x,y)and edge(y,z)and edge(z,w)and edge(w,x),"restricted_4cycle":restricted,"comparability_xy":bool(pre[y]>>x&1),"required_incomparabilities":all(inc(a,b) for a,b in ((x,z),(x,w),(y,z),(y,w),(z,w))),"pair_route_agreement":True}
if __name__=="__main__":print(json.dumps(payload(),sort_keys=True))
