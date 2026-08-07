#!/usr/bin/env python3
from itertools import combinations,permutations
import json
q=7
def chi(x):
 x%=q
 return 0 if x==0 else (1 if pow(x,3,q)==1 else -1)
Q=[[int(i==j)-chi(j-i) for j in range(q)]for i in range(q)]
Qt=list(map(list,zip(*Q)));J=[[1]*q for _ in range(q)]
def mm(a,b):return [[sum(a[i][k]*b[k][j]for k in range(q))for j in range(q)]for i in range(q)]
def goodP(a):return all(a[i][i]==0 and all(a[i][j]in(-1,1)for j in range(q)if i!=j)and sum(a[i])==-2 for i in range(q))and a==list(map(list,zip(*a)))
edges=list(combinations(range(q),2)); Ps=[]
for es in combinations(edges,7):
 deg=[0]*q
 for i,j in es:deg[i]+=1;deg[j]+=1
 if deg==[2]*q:
  P=[[-1]*q for _ in range(q)]
  for i in range(q):P[i][i]=0
  for i,j in es:P[i][j]=P[j][i]=1
  Ps.append(P)
assert len(Ps)==465
hits=0;pol=0
for p in permutations(range(q)):
 R=[[int(j==p[i])for j in range(q)]for i in range(q)]
 if mm(Qt,R)!=mm(list(map(list,zip(*R))),Q):continue
 pol+=1
 for P0 in Ps:
  A=mm(Qt,R);B=mm(Qt,P0);P1=[[-(4*(A[i][j]+1)+B[i][j])//8 for j in range(q)]for i in range(q)]
  if goodP(P1) and mm(P0,Q)==[[ -4*R[i][j]-mm(Q,P1)[i][j] for j in range(q)]for i in range(q)]:hits+=1
print(json.dumps({'status':'PASS','p0_states':len(Ps),'polarities':pol,'hits':hits},sort_keys=True))
