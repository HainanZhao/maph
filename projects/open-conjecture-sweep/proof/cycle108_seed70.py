#!/usr/bin/env python3
"""Exact reproduction of Epoch's public n=70 Seidel construction (2026-07-31)."""
from __future__ import annotations
import json

Q=139; L=69; N=278
def chi(x:int)->int:
 x%=Q
 return 0 if x==0 else (1 if pow(x,(Q-1)//2,Q)==1 else -1)
def seidel():
 a=[]; b=[]; power=1
 for t in range(L):
  a.append(1 if t==0 else chi(power-1)); b.append(-chi(power+1)); power=power*4%Q
 s=[[0]*N for _ in range(N)]
 def put(i,j,v):s[i][j]=s[j][i]=v
 put(0,1,-1)
 for g,v in enumerate((1,1,-1,-1)):
  for t in range(L):put(0,2+g*L+t,v)
 for g,v in enumerate((-1,1,1,-1)):
  for t in range(L):put(1,2+g*L+t,v)
 def x(r,c):return a[(c-r)%L]
 def y(r,c):return b[(c-r)%L]
 def block(g,h,f,m=1):
  for r in range(L):
   for c in range(L):
    if g!=h or r!=c:s[2+g*L+r][2+h*L+c]=m*f(r,c)
 for g,m in ((0,1),(1,-1),(2,1),(3,-1)):block(g,g,y,m)
 for g,h,f,m in ((0,1,y,-1),(0,2,x,-1),(0,3,x,1),(1,2,x,-1),(1,3,x,-1),(2,3,y,1)):
  block(g,h,f,m)
  for r in range(L):
   for c in range(L):s[2+h*L+c][2+g*L+r]=s[2+g*L+r][2+h*L+c]
 return s
def audit(s):
 assert all(s[i][j]==s[j][i] for i in range(N) for j in range(N))
 assert all(s[i][i]==0 and s[i][j] in (-1,1) for i in range(N) for j in range(N) if i!=j)
 assert [sum(row) for row in s]==[-1]*N
 sq=[[sum(s[i][k]*s[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
 assert all(sq[i][i]==277 for i in range(N))
 assert all(sq[i][j] in (0,-4) for i in range(N) for j in range(N) if i!=j)
 rows=[sum((s[i][j]==1)<<j for j in range(N)) for i in range(N)]
 red=blue=0
 for i in range(N):
  for j in range(i+1,N):
   if s[i][j]==1:red=max(red,(rows[i]&rows[j]).bit_count())
   else:blue=max(blue,((~rows[i])&(~rows[j])&((1<<N)-1)).bit_count()-2)
 assert (red,blue)==(68,69)
 return {'status':'PASS','order':N,'row_sum':-1,'square_diagonal':277,'off_diagonal_values':[0,-4],'red_book_max':red,'blue_book_max':blue}
if __name__=='__main__':print(json.dumps(audit(seidel()),sort_keys=True))
