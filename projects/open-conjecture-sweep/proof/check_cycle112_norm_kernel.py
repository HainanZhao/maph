#!/usr/bin/env python3
import json
def ch(a,p):a%=p;return 0 if a==0 else(1 if pow(a,(p-1)//2,p)==1 else-1)
def main():
 p=7;ns=[a for a in range(p)if ch(a,p)<0];hits=[];profiles={}
 for a in ns:
  for b in ns:
   for d in ns:
    for sig in(-1,1):
     N=2*p;A=[[0]*N for _ in range(N)]
     for u in range(N):
      x,l=u%p,u//p
      for v in range(u+1,N):
       y,m=v%p,v//p
       val=ch((x-y)**2-(a if l==0 else b),p) if l==m else ch(x*x-d*y*y,p)
       if l!=m and x==0 and y==0:val=sig
       A[u][v]=A[v][u]=int(val==1)
     r=bl=0
     for u in range(N):
      for v in range(u+1,N):
       k=sum(A[u][w]==A[u][v] and A[v][w]==A[u][v]for w in range(N)if w not in(u,v))
       if A[u][v]:r=max(r,k)
       else:bl=max(bl,k)
     profiles[(r,bl)]=profiles.get((r,bl),0)+1
     if r<=2 and bl<=3:hits.append((a,b,d,sig))
 print(json.dumps({'status':'PASS','states':54,'hits':hits,'profiles':sorted(([list(k),v]for k,v in profiles.items()))},sort_keys=True))
if __name__=='__main__':main()
