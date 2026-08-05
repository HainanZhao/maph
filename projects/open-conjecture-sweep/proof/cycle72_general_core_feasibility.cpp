// Find one fully generalized D=5 equality core for each pair of RGS partitions.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

using Pair=std::array<int,2>; using Map=std::array<int,6>; using RGS=std::array<int,5>;
static bool has(Pair p,int x){return p[0]==x||p[1]==x;}
static void rgs(int at,int mx,RGS& a,std::vector<RGS>& out){if(at==5){out.push_back(a);return;}for(int x=0;x<=std::min(4,mx+1);++x){a[at]=x;rgs(at+1,std::max(mx,x),a,out);}}

static bool find_one(const RGS& side,const RGS& central,std::array<Pair,5>& answer_pair,std::array<Map,5>& answer_map,uint64_t& checked){
 std::vector<Pair>P;for(int a=0;a<6;++a)for(int b=a+1;b<6;++b)P.push_back({a,b});
 constexpr int total=15*15*15*15*15;
 for(int code0=0;code0<total;++code0){++checked;int code=code0;std::array<Pair,5> pair;for(auto&p:pair){p=P[code%15];code/=15;}
  bool bad=false;for(int j=0;j<5;++j)for(int k=0;k<j;++k)if(side[j]==side[k]&&(has(pair[j],pair[k][0])||has(pair[j],pair[k][1])))bad=true;
  if(bad)continue;
  std::array<std::vector<Map>,5> opts;
  for(int j=0;j<5&&!bad;++j){std::array<int,4> rem{},avail{};int a=0,b=0;for(int i=0;i<6;++i)if(!has(pair[j],i))rem[a++]=i;for(int q=0;q<5;++q)if(q!=side[j])avail[b++]=q;std::sort(rem.begin(),rem.end());
   do{Map m;m.fill(-1);bool ok=true;for(int t=0;t<4;++t){int i=rem[t],q=avail[t];for(int ell=0;ell<5;++ell)if(side[ell]==q&&has(pair[ell],i))ok=false;m[i]=q;}if(ok){m[pair[j][0]]=side[j];m[pair[j][1]]=side[j];opts[j].push_back(m);}}while(std::next_permutation(rem.begin(),rem.end()));
   if(opts[j].empty())bad=true;
  }
  if(bad)continue;
  std::array<Map,5> selected;bool found=false;
  auto dfs=[&](auto&&self,int j)->void{if(found)return;if(j==5){found=true;return;}for(const auto&m:opts[j]){bool ok=true;for(int k=0;k<j;++k){int common=0;for(int i=0;i<6;++i)common+=m[i]==selected[k][i];if(common!=(central[j]==central[k]?0:1)){ok=false;break;}}if(ok){selected[j]=m;self(self,j+1);if(found)return;}}};
  dfs(dfs,0);if(found){answer_pair=pair;answer_map=selected;return true;}
 }
 return false;
}
static void put_rgs(const RGS& x){std::cout<<'[';for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<x[i];}std::cout<<']';}
int main(int argc,char**argv){int shard=argc>1?std::stoi(argv[1]):0,shards=argc>2?std::stoi(argv[2]):1;if(shards<1||shard<0||shard>=shards)return 2;std::vector<RGS>R;RGS z{};z[0]=0;rgs(1,0,z,R);if(R.size()!=52)return 3;
 uint64_t codes=0;int cases=0,sat=0;std::cout<<"{\"status\":\"DONE\",\"epistemic_status\":\"PROVED\",\"shard\":"<<shard<<",\"shards\":"<<shards<<",\"rows\":[";bool first=true;
 for(int ix=shard;ix<52*52;ix+=shards){++cases;int a=ix/52,b=ix%52;std::array<Pair,5>pair;std::array<Map,5>maps;bool yes=find_one(R[a],R[b],pair,maps,codes);if(yes)++sat;if(!first)std::cout<<',';first=false;std::cout<<"{\"sides\":";put_rgs(R[a]);std::cout<<",\"central\":";put_rgs(R[b]);std::cout<<",\"status\":\""<<(yes?"SAT":"UNSAT")<<'\"';if(yes){std::cout<<",\"pairs\":[";for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'['<<pair[j][0]<<','<<pair[j][1]<<']';}std::cout<<"],\"maps\":[";for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'[';for(int i=0;i<6;++i){if(i)std::cout<<',';std::cout<<maps[j][i];}std::cout<<']';}std::cout<<']';}std::cout<<'}';}
 std::cout<<"],\"partition_pairs_checked\":"<<cases<<",\"pair_codes_checked\":"<<codes<<",\"sat_partition_pairs\":"<<sat<<"}\n";
}
