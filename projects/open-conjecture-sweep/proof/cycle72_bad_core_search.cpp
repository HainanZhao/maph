// Counterexample-directed search for a generalized D=5 core lacking a five-blocker.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <functional>
#include <iostream>
#include <unordered_set>
#include <vector>

using Pair=std::array<int,2>; using Map=std::array<int,6>; using RGS=std::array<int,5>;
static bool has(Pair p,int x){return p[0]==x||p[1]==x;}
static void rgs(int at,int mx,RGS&a,std::vector<RGS>&out){if(at==5){out.push_back(a);return;}for(int x=0;x<=std::min(4,mx+1);++x){a[at]=x;rgs(at+1,std::max(mx,x),a,out);}}
struct Core { std::array<uint64_t,11> edge{}; std::array<std::vector<int>,6> side; int vertices=0; };
static void hbyte(uint64_t&h,uint8_t x){h^=x;h*=1099511628211ULL;}
static void hu16(uint64_t&h,uint16_t x){hbyte(h,x&255);hbyte(h,x>>8);}
static uint64_t mix64(uint64_t x){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return x^(x>>31);}
static Core build(const RGS&s,const RGS&c,const std::array<Pair,5>&p,const std::array<Map,5>&m){
 Core x;int next=5;int star[5][6];for(auto&row:star)for(int&i:row)i=-1;
 // Repeated star vertex r_j has canonical id j in both of its star lines.
 for(int j=0;j<5;++j)for(int i:p[j]){int&q=star[s[j]][i];if(q<0)q=j;else if(q!=j)throw 1;}
 for(int q=0;q<5;++q)for(int i=0;i<6;++i)if(star[q][i]<0)star[q][i]=next++;
 int v=next++;std::array<int,5> cen;cen.fill(-1);for(int j=0;j<5;++j){int&z=cen[c[j]];if(z<0)z=next++;}
 for(int q=0;q<5;++q){for(int i=0;i<6;++i)if(std::find(x.side[q+1].begin(),x.side[q+1].end(),star[q][i])==x.side[q+1].end())x.side[q+1].push_back(star[q][i]);}
 x.side[0].push_back(v);for(int z:cen)if(z>=0)x.side[0].push_back(z);
 for(int i=0;i<6;++i){uint64_t e=1ULL<<v;for(int q=0;q<5;++q)e|=1ULL<<star[q][i];x.edge[i]=e;}
 for(int j=0;j<5;++j){uint64_t e=1ULL<<cen[c[j]];for(int q=0;q<5;++q){if(q==s[j])e|=1ULL<<j;else{int found=-1;for(int i=0;i<6;++i)if(m[j][i]==q)found=i;if(found<0)throw 2;e|=1ULL<<star[q][found];}}x.edge[6+j]=e;}
 x.vertices=next;return x;
}
static bool blocker(const Core&core,int cap,int&type_count,bool&overflow,uint64_t&canonical_hash){
 std::vector<uint64_t> types;overflow=false;std::array<uint16_t,64> incidence{};
 for(int i=0;i<11;++i){uint64_t bits=core.edge[i];while(bits){uint64_t bit=bits&-bits;bits-=bit;incidence[std::countr_zero(bit)]|=uint16_t(1u<<i);}}
 constexpr uint16_t all_core_lines=(1u<<11)-1;
 std::function<void(int,uint64_t,uint16_t)> gen=[&](int q,uint64_t mask,uint16_t covered){if(overflow)return;if(q==6){if(covered!=all_core_lines)return;if(types.size()==size_t(cap)){overflow=true;return;}types.push_back(mask);return;}gen(q+1,mask,covered);for(int z:core.side[q])if(!(covered&incidence[z]))gen(q+1,mask|(1ULL<<z),covered|incidence[z]);};
 gen(0,0,0);type_count=types.size();if(overflow)return false;
 std::vector<std::array<uint16_t,6>> trace_signatures;trace_signatures.reserve(types.size());
 for(uint64_t type:types){std::array<uint16_t,6> sig{};for(int q=0;q<6;++q)for(int z:core.side[q])if(type&(1ULL<<z)){sig[q]=incidence[z];break;}trace_signatures.push_back(sig);}
 std::sort(trace_signatures.begin(),trace_signatures.end());hu16(canonical_hash,trace_signatures.size());for(const auto&sig:trace_signatures)for(uint16_t x:sig)hu16(canonical_hash,x);
 std::vector<uint64_t> family(core.edge.begin(),core.edge.end());family.insert(family.end(),types.begin(),types.end());
 std::array<std::unordered_set<uint64_t>,6> seen;
 std::function<bool(int,uint64_t)> dfs=[&](int depth,uint64_t chosen){if(!seen[depth].insert(chosen).second)return false;int best=-1,bestn=99;for(int i=0;i<int(family.size());++i)if(!(family[i]&chosen)){int n=std::popcount(family[i]);if(n<bestn){best=i;bestn=n;}}if(best<0)return true;if(depth==5||bestn==0)return false;uint64_t choices=family[best];while(choices){uint64_t bit=choices&-choices;choices-=bit;if(dfs(depth+1,chosen|bit))return true;}return false;};
 return dfs(0,0);
}
static void out_rgs(const RGS&a){std::cout<<'[';for(int i=0;i<5;++i){if(i)std::cout<<',';std::cout<<a[i];}std::cout<<']';}
static void out_assignment(const RGS&s,const RGS&c,const std::array<Pair,5>&p,const std::array<Map,5>&m,int types,bool has_blocker){std::cout<<"{\"sides\":";out_rgs(s);std::cout<<",\"central\":";out_rgs(c);std::cout<<",\"pairs\":[";for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'['<<p[j][0]<<','<<p[j][1]<<']';}std::cout<<"],\"maps\":[";for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'[';for(int i=0;i<6;++i){if(i)std::cout<<',';std::cout<<m[j][i];}std::cout<<']';}std::cout<<"],\"extension_types\":"<<types<<",\"has_blocker\":"<<(has_blocker?"true":"false")<<'}';}
int main(int argc,char**argv){int shard=argc>1?std::stoi(argv[1]):0,shards=argc>2?std::stoi(argv[2]):1;uint64_t limit=argc>3?std::stoull(argv[3]):1000000;int side_filter=argc>4?std::stoi(argv[4]):-1;if(shards<1||shard<0||shard>=shards)return 2;std::vector<RGS>R;RGS z{};z[0]=0;rgs(1,0,z,R);if(side_filter>=int(R.size()))return 3;std::vector<Pair>P;for(int a=0;a<6;++a)for(int b=a+1;b<6;++b)P.push_back({a,b});constexpr uint64_t pt=15*15*15*15*15;uint64_t assignments=0,cases=0,hash_sum=0,hash_xor=0;int max_types=0;bool capped=false,bad=false,typecap=false,have_first=false,first_blocker=false;RGS bads{},badc{},firsts{},firstc{};std::array<Pair,5>badp{},firstp{};std::array<Map,5>badm{},firstm{};int first_types=0,bad_types=0;const uint64_t local_total=(side_filter<0?R.size():1)*R.size()*pt;const uint64_t base=side_filter<0?0:uint64_t(side_filter)*R.size()*pt;
 for(uint64_t local=shard;local<local_total&&!capped&&!bad&&!typecap;local+=shards){uint64_t g=base+local;++cases;int si=g/(R.size()*pt),ci=(g/pt)%R.size(),code=g%pt;auto&s=R[si];auto&c=R[ci];std::array<Pair,5>p;for(auto&x:p){x=P[code%15];code/=15;}bool impossible=false;for(int j=0;j<5;++j)for(int k=0;k<j;++k)if(s[j]==s[k]&&(has(p[j],p[k][0])||has(p[j],p[k][1])))impossible=true;if(impossible)continue;std::array<std::vector<Map>,5>opts;
  for(int j=0;j<5&&!impossible;++j){std::array<int,4>rem{},avail{};int a=0,b=0;for(int i=0;i<6;++i)if(!has(p[j],i))rem[a++]=i;for(int q=0;q<5;++q)if(q!=s[j])avail[b++]=q;std::sort(rem.begin(),rem.end());do{Map m;m.fill(-1);bool ok=true;for(int t=0;t<4;++t){int i=rem[t],q=avail[t];for(int ell=0;ell<5;++ell)if(s[ell]==q&&has(p[ell],i))ok=false;m[i]=q;}if(ok){m[p[j][0]]=s[j];m[p[j][1]]=s[j];opts[j].push_back(m);}}while(std::next_permutation(rem.begin(),rem.end()));if(opts[j].empty())impossible=true;}
  if(impossible)continue;
  std::array<Map,5>chosen;auto dfs=[&](auto&&self,int j)->void{if(capped||bad||typecap)return;if(j==5){++assignments;Core core=build(s,c,p,chosen);uint64_t h=14695981039346656037ULL;for(int x:s)hbyte(h,x);for(int x:c)hbyte(h,x);for(const auto&x:p){hbyte(h,x[0]);hbyte(h,x[1]);}for(const auto&m:chosen)for(int x:m)hbyte(h,x);int types=0;bool overflow=false;bool yes=blocker(core,2048,types,overflow,h);max_types=std::max(max_types,types);if(overflow){typecap=true;return;}uint64_t mixed=mix64(h);hash_sum+=mixed;hash_xor^=mixed;if(!have_first){have_first=true;firsts=s;firstc=c;firstp=p;firstm=chosen;first_types=types;first_blocker=yes;}if(!yes){bad=true;bads=s;badc=c;badp=p;badm=chosen;bad_types=types;}if(assignments>=limit)capped=true;return;}for(const auto&m:opts[j]){bool ok=true;for(int k=0;k<j;++k){int common=0;for(int i=0;i<6;++i)common+=m[i]==chosen[k][i];if(common!=(c[j]==c[k]?0:1)){ok=false;break;}}if(ok){chosen[j]=m;self(self,j+1);if(capped||bad||typecap)return;}}};dfs(dfs,0);
 }
 std::cout<<"{\"status\":\""<<(bad?"BAD_CORE":typecap?"TYPE_CAP":capped?"ASSIGNMENT_CAP":"DONE")<<"\",\"epistemic_status\":\"PROVED\",\"shard\":"<<shard<<",\"shards\":"<<shards<<",\"side_filter\":"<<side_filter<<",\"assignments\":"<<assignments<<",\"cases\":"<<cases<<",\"max_extension_types\":"<<max_types<<",\"canonical_hash_sum\":"<<hash_sum<<",\"canonical_hash_xor\":"<<hash_xor;
 if(have_first){std::cout<<",\"first\":";out_assignment(firsts,firstc,firstp,firstm,first_types,first_blocker);}if(bad){std::cout<<",\"bad\":";out_assignment(bads,badc,badp,badm,bad_types,false);}std::cout<<"}\n";
}
