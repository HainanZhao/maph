#!/usr/bin/env python3
from fractions import Fraction
from itertools import combinations,permutations
import json
q=7
def ch(a):a%=q;return 0 if a==0 else (1 if pow(a,3,q)==1 else -1)
Q=[[int(i==j)-ch(j-i)for j in range(q)]for i in range(q)]
T=[list(x)for x in zip(*Q)]
def mul(a,b):return [[sum(a[i][k]*b[k][j]for k in range(q))for j in range(q)]for i in range(q)]
Ps=[]
for E in combinations(list(combinations(range(q),2)),7):
 d=[0]*q
 for i,j in E:d[i]+=1;d[j]+=1
 if d==[2]*q:
  A=[[-1]*q for _ in range(q)]
  for i in range(q):A[i][i]=0
  for i,j in E:A[i][j]=A[j][i]=1
  Ps.append(A)
hit=pol=0
for p in permutations(range(q)):
 R=[[int(j==p[i])for j in range(q)]for i in range(q)]
 if mul(T,R)!=mul([list(x)for x in zip(*R)],Q):continue
 pol+=1
 for A in Ps:
  u=mul(T,R);v=mul(T,mul(A,Q));B=[[Fraction(-4*(u[i][j]+1)-v[i][j],8)for j in range(q)]for i in range(q)]
  if all(x.denominator==1 for r in B for x in r):
   C=[[int(x)for x in r]for r in B]
   if C==[list(x)for x in zip(*C)]and all(C[i][i]==0 and sum(C[i])==-2 and all(C[i][j]in(-1,1)for j in range(q)if i!=j)for i in range(q))and mul(A,Q)==[[-4*R[i][j]-mul(Q,C)[i][j]for j in range(q)]for i in range(q)]:hit+=1
print(json.dumps({'status':'PASS','polarities':pol,'p0_states':len(Ps),'hits':hit},sort_keys=True))
