#!/usr/bin/env python3
"""Independent full-adjacency bitset replay for C114."""
import itertools,json
Q=7; N=14
SYMMETRIC=[frozenset(v for i,p in enumerate(((1,6),(2,5),(3,4))) if (m>>i)&1 for v in p) for m in range(8)]
def main():
 hits=[];profiles={};states=0
 for a,c in itertools.product(SYMMETRIC,repeat=2):
  if len(a)!=len(c):continue
  for b0 in itertools.combinations(range(Q),Q-len(a)):
   b=frozenset(b0);rows=[0]*N;states+=1
   for x in range(Q):
    for y in range(Q):
     if x!=y and (y-x)%Q in a:rows[x]|=1<<y
     if x!=y and (y-x)%Q in c:rows[Q+x]|=1<<(Q+y)
     if (y-x)%Q in b:rows[x]|=1<<(Q+y);rows[Q+y]|=1<<x
   assert all(r.bit_count()==Q for r in rows)
   red=blue=0
   for u in range(N):
    for v in range(u+1,N):
     if (rows[u]>>v)&1:k=(rows[u]&rows[v]).bit_count();red=max(red,k)
     else:k=((~rows[u])&(~rows[v])&((1<<N)-1)).bit_count()-2;blue=max(blue,k)
   profiles[(red,blue)]=profiles.get((red,blue),0)+1
   if red<=2 and blue<=3:hits.append([sorted(a),sorted(b),sorted(c)])
 assert states==512
 print(json.dumps({'status':'PASS','states':states,'hits':hits,'profiles':[[list(k),v] for k,v in sorted(profiles.items())]},sort_keys=True))
if __name__=='__main__':main()
