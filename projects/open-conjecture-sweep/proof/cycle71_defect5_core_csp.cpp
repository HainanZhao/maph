// Exact exhaustive equality-core CSP for the D=5 high-star boundary.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using Pair=std::array<int,2>; using Map=std::array<int,6>;
static bool endpoint(Pair p,int x){return p[0]==x||p[1]==x;}
int main(int argc,char**argv){
  int shard=argc>1?std::stoi(argv[1]):0, shards=argc>2?std::stoi(argv[2]):1;
  std::vector<Pair> P; for(int a=0;a<6;a++)for(int b=a+1;b<6;b++)P.push_back({a,b});
  const int total=15*15*15*15*15; uint64_t tried=0;
  for(int code=shard;code<total;code+=shards){
    int x=code; std::array<Pair,5> e; for(int j=0;j<5;j++){e[j]=P[x%15];x/=15;}
    std::array<std::vector<Map>,5> opts;
    for(int j=0;j<5;j++){
      std::array<int,4> rem{}, sides{}; int a=0,b=0;
      for(int i=0;i<6;i++)if(!endpoint(e[j],i))rem[a++]=i;
      for(int q=0;q<5;q++)if(q!=j)sides[b++]=q;
      std::sort(rem.begin(),rem.end());
      do {Map m; m.fill(-1); bool ok=true;
        for(int t=0;t<4;t++){int i=rem[t],q=sides[t]; if(endpoint(e[q],i))ok=false; else m[i]=q;}
        if(ok){m[e[j][0]]=j;m[e[j][1]]=j;opts[j].push_back(m);}
      } while(std::next_permutation(rem.begin(),rem.end()));
      if(opts[j].empty())goto next;
    }
    {std::array<Map,5> chosen; bool found=false;
      auto dfs=[&](auto&&self,int j)->void{if(found)return; if(j==5){found=true;return;}
        for(const auto&m:opts[j]){bool ok=true;for(int k=0;k<j;k++){int common=0;for(int i=0;i<6;i++)common+=m[i]==chosen[k][i];if(common!=1){ok=false;break;}}
          if(ok){chosen[j]=m;self(self,j+1);if(found)return;}}
      }; dfs(dfs,0); if(found){
        std::cout<<"{\"status\":\"SAT\",\"epistemic_status\":\"PROVED\",\"pairs\":[";
        for(int j=0;j<5;j++){if(j)std::cout<<',';std::cout<<'['<<e[j][0]<<','<<e[j][1]<<']';} std::cout<<"],\"maps\":[";
        for(int j=0;j<5;j++){if(j)std::cout<<',';std::cout<<'[';for(int i=0;i<6;i++){if(i)std::cout<<',';std::cout<<chosen[j][i];}std::cout<<']';} std::cout<<"],\"claim_boundary\":\"Exact D=5 equality-core realization only; it does not certify tau=6.\"}\n";return 0;}
    } next: ++tried;
  }
  std::cout<<"{\"status\":\"UNSAT_SHARD\",\"epistemic_status\":\"PROVED\",\"shard\":"<<shard<<",\"shards\":"<<shards<<",\"codes_checked\":"<<tried<<"}\n";
}
