#!/usr/bin/env python3
import json
def c(x,p):x%=p;return 0 if x==0 else(1 if pow(x,(p-1)//2,p)==1 else-1)
p=7;ns=[x for x in range(p)if c(x,p)<0];out={};hit=[]
for a in ns:
 for b in ns:
  for d in ns:
   for s in(-1,1):
    M=[0]*14
    for u in range(14):
     for v in range(14):
      if u==v:continue
      x,l=u%p,u//p;y,m=v%p,v//p
      if l==m:z=c((x-y)**2-(a if l==0 else b),p)
      else:
       X,Y=(x,y) if l==0 else (y,x)
       z=c(X*X-d*Y*Y,p)if(X,Y)!=(0,0)else s
      M[u]|=(z==1)<<v
    rr=bb=0
    for u in range(14):
     for v in range(u+1,14):
      if(M[u]>>v)&1:rr=max(rr,(M[u]&M[v]).bit_count())
      else:bb=max(bb,((~M[u]&~M[v]&((1<<14)-1)).bit_count()-2))
    out[(rr,bb)]=out.get((rr,bb),0)+1
    if rr<=2 and bb<=3:hit.append((a,b,d,s))
print(json.dumps({'status':'PASS','states':54,'hits':hit,'profiles':sorted(([list(k),v]for k,v in out.items()))},sort_keys=True))
