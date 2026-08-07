#!/usr/bin/env python3
"""Independent 14-bit adjacency replay of the full C117 orbit."""
import json
N=14
def main():
 profiles={};hits=[];states=0
 for deleted0 in range(16):
  for deleted1 in range(deleted0+1,16):
   verts=[x for x in range(16) if x not in (deleted0,deleted1)]
   base=[[0 if i==j else (-1 if ((verts[i]&verts[j]).bit_count()%2) else 1) for j in range(N)] for i in range(N)]
   for mask in range(1<<13):
    signs=[1]+[1 if (mask>>(i-1))&1 else -1 for i in range(1,N)]
    rows=[0]*N
    for i in range(N):
     for j in range(i+1,N):
      if signs[i]*base[i][j]*signs[j]<0:rows[i]|=1<<j;rows[j]|=1<<i
    red=blue=0
    for i in range(N):
     for j in range(i+1,N):
      if (rows[i]>>j)&1:red=max(red,(rows[i]&rows[j]).bit_count())
      else:blue=max(blue,((~rows[i])&(~rows[j])&((1<<N)-1)).bit_count()-2)
    profiles[(red,blue)]=profiles.get((red,blue),0)+1;states+=1
    if red<=2 and blue<=3:hits.append([deleted0,deleted1,mask])
 assert states==983040
 print(json.dumps({'status':'PASS','states':states,'hits':hits,'profiles':[[list(k),v] for k,v in sorted(profiles.items())]},sort_keys=True))
if __name__=='__main__':main()
