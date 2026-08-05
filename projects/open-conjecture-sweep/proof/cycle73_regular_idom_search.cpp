// Exact deterministic cubic-graph counterexample search for i(G) <= mu*(G).
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <functional>
#include <iostream>
#include <random>
#include <vector>

struct Graph { int n; std::array<uint64_t,32> adj{}; std::vector<std::pair<int,int>> edges; };
static uint64_t splitmix(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
static bool connected(const Graph&g){uint64_t seen=1,front=1;while(front){int v=std::countr_zero(front);front&=front-1;uint64_t add=g.adj[v]&~seen;seen|=add;front|=add;}return seen==((1ULL<<g.n)-1);}
static bool regular(int n,int degree,uint64_t seed,Graph&g,uint64_t&loops,uint64_t&multiple,uint64_t&disc){
 const int low=std::min(degree,n-1-degree); const bool complement=low!=degree;
 std::mt19937_64 rng(seed);std::vector<int>stub;stub.reserve(low*n);for(int v=0;v<n;++v)for(int t=0;t<low;++t)stub.push_back(v);
 for(int attempt=0;attempt<2000;++attempt){std::shuffle(stub.begin(),stub.end(),rng);g=Graph{n};bool bad=false;for(int i=0;i<low*n;i+=2){int a=stub[i],b=stub[i+1];if(a==b){++loops;bad=true;break;}if(g.adj[a]&(1ULL<<b)){++multiple;bad=true;break;}g.adj[a]|=1ULL<<b;g.adj[b]|=1ULL<<a;g.edges.push_back({std::min(a,b),std::max(a,b)});}if(!bad){if(complement){const uint64_t all=(1ULL<<n)-1;for(int v=0;v<n;++v)g.adj[v]=all&~(1ULL<<v)&~g.adj[v];g.edges.clear();for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)if(g.adj[a]&(1ULL<<b))g.edges.push_back({a,b});}if(connected(g))return true;++disc;}}
 return false;
}
static int independent_domination(const Graph&g,uint64_t& witness){
 const uint64_t full=(1ULL<<g.n)-1;int best=g.n+1;witness=0;
 std::function<void(uint64_t,uint64_t,uint64_t)> dfs=[&](uint64_t chosen,uint64_t allowed,uint64_t dominated){
  int used=std::popcount(chosen);if(used>=best)return;if(dominated==full){best=used;witness=chosen;return;}
  int target=-1,choices=99;uint64_t todo=full&~dominated;
  while(todo){int v=std::countr_zero(todo);todo&=todo-1;int c=std::popcount(allowed&(g.adj[v]|(1ULL<<v)));if(c<choices){choices=c;target=v;}}
  uint64_t branch=allowed&(g.adj[target]|(1ULL<<target));while(branch){uint64_t bit=branch&-branch;branch-=bit;int u=std::countr_zero(bit);dfs(chosen|bit,allowed&~bit&~g.adj[u],dominated|bit|g.adj[u]);}
 };
 dfs(0,full,0);return best;
}
static int minimum_maximal_matching(const Graph&g,std::vector<std::pair<int,int>>& witness){
 int best=g.n/2+1;std::vector<std::pair<int,int>>cur;witness.clear();
 std::function<void(uint64_t)> dfs=[&](uint64_t used){
  if(int(cur.size())>=best)return;int bu=-1,bv=-1,bcount=99;
  for(auto [u,v]:g.edges)if(!(used&(1ULL<<u))&&!(used&(1ULL<<v))){int count=0;for(auto [a,b]:g.edges)if((a==u||b==u||a==v||b==v)&&!(used&(1ULL<<a))&&!(used&(1ULL<<b)))++count;if(count<bcount){bcount=count;bu=u;bv=v;}}
  if(bu<0){best=cur.size();witness=cur;return;}for(auto [a,b]:g.edges)if((a==bu||b==bu||a==bv||b==bv)&&!(used&(1ULL<<a))&&!(used&(1ULL<<b))){cur.push_back({a,b});dfs(used|(1ULL<<a)|(1ULL<<b));cur.pop_back();}
 };
 dfs(0);return best;
}
static void pairs(const std::vector<std::pair<int,int>>&x){std::cout<<'[';for(size_t i=0;i<x.size();++i){if(i)std::cout<<',';std::cout<<'['<<x[i].first<<','<<x[i].second<<']';}std::cout<<']';}
int main(int argc,char**argv){int shard=argc>1?std::stoi(argv[1]):0,shards=argc>2?std::stoi(argv[2]):1,per=argc>3?std::stoi(argv[3]):1000;uint64_t offset=argc>4?std::stoull(argv[4]):0;bool high=argc>5&&std::string(argv[5])=="high";if(shards<1||shard<0||shard>=shards)return 2;uint64_t loops=0,multiple=0,disc=0,retries=0;std::array<int,14>orders{};std::array<int,6>degrees{};Graph counter;uint64_t iset=0;std::vector<std::pair<int,int>>matching;int ci=0,cm=0;bool found=false;
 for(int local=0;local<per&&!found;++local){uint64_t sample=offset+uint64_t(shard)+uint64_t(shards)*local;int degree=high?4+(sample%5):3;int n=high?10+2*((sample/5)%12):6+2*(sample%14);Graph g;bool ok=regular(n,degree,splitmix(0xC73A11ULL+sample),g,loops,multiple,disc);if(!ok){++retries;continue;}++orders[(n-6)/2];++degrees[degree-4+1];uint64_t indset;std::vector<std::pair<int,int>>mat;int i=independent_domination(g,indset),m=minimum_maximal_matching(g,mat);if(i>m){found=true;counter=g;iset=indset;matching=mat;ci=i;cm=m;}}
 std::cout<<"{\"status\":\""<<(found?"COUNTEREXAMPLE":"PASS_SAMPLE")<<"\",\"epistemic_status\":\""<<(found?"RECOGNIZED":"OBSERVED")<<"\",\"shard\":"<<shard<<",\"shards\":"<<shards<<",\"accepted\":[";for(int i=0;i<14;++i){if(i)std::cout<<',';std::cout<<orders[i];}std::cout<<"],\"degree_histogram\":[";for(int i=0;i<6;++i){if(i)std::cout<<',';std::cout<<degrees[i];}std::cout<<"],\"loop_rejections\":"<<loops<<",\"multiple_rejections\":"<<multiple<<",\"disconnect_rejections\":"<<disc<<",\"generator_failures\":"<<retries;
 if(found){std::cout<<",\"n\":"<<counter.n<<",\"edges\":";pairs(counter.edges);std::cout<<",\"i\":"<<ci<<",\"independent_dominating_set\":[";bool first=true;for(int v=0;v<counter.n;++v)if(iset&(1ULL<<v)){if(!first)std::cout<<',';first=false;std::cout<<v;}std::cout<<"],\"mu_star\":"<<cm<<",\"maximal_matching\":";pairs(matching);}std::cout<<"}\n";
}
