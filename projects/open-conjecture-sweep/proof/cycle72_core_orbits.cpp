// Enumerate and quotient generalized C71 equality cores for one fixed side pattern.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>

using Pair = std::array<int, 2>;
using Map = std::array<int, 6>;
using Sides = std::array<int, 5>;

static bool has(Pair p, int x) { return p[0] == x || p[1] == x; }

static std::string pack(const std::array<Pair,5>& pair, const std::array<Map,5>& maps) {
  std::string key; key.reserve(40);
  for (const auto& p : pair) { key.push_back(char(p[0])); key.push_back(char(p[1])); }
  for (const auto& m : maps) for (int q : m) key.push_back(char(q));
  return key;
}

static void unpack(const std::string& key, std::array<Pair,5>& pair, std::array<Map,5>& maps) {
  int at = 0;
  for (auto& p : pair) { p[0] = uint8_t(key[at++]); p[1] = uint8_t(key[at++]); }
  for (auto& m : maps) for (int& q : m) q = uint8_t(key[at++]);
}

struct Generator { std::array<int,6> star; std::array<int,5> r, side; };

static std::string act(const std::string& key, const Generator& g) {
  std::array<Pair,5> pair, out_pair; std::array<Map,5> maps, out_maps;
  unpack(key, pair, maps);
  for (int j = 0; j < 5; ++j) {
    const int jj = g.r[j];
    out_pair[jj] = {g.star[pair[j][0]], g.star[pair[j][1]]};
    if (out_pair[jj][0] > out_pair[jj][1]) std::swap(out_pair[jj][0], out_pair[jj][1]);
    for (int i = 0; i < 6; ++i) out_maps[jj][g.star[i]] = g.side[maps[j][i]];
  }
  return pack(out_pair, out_maps);
}

struct DSU {
  std::vector<int> p, sz;
  explicit DSU(int n): p(n), sz(n,1) { std::iota(p.begin(),p.end(),0); }
  int find(int x) { while (x != p[x]) { p[x] = p[p[x]]; x = p[x]; } return x; }
  void join(int a,int b) { a=find(a);b=find(b);if(a==b)return;if(sz[a]<sz[b])std::swap(a,b);p[b]=a;sz[a]+=sz[b]; }
};

static std::vector<std::string> enumerate(const Sides& side_of) {
  std::vector<Pair> pair_options;
  for (int a=0;a<6;++a) for(int b=a+1;b<6;++b) pair_options.push_back({a,b});
  constexpr int total=15*15*15*15*15;
  std::vector<std::string> solutions;
  for(int code0=0;code0<total;++code0){
    int code=code0;std::array<Pair,5> pair;
    for(auto&p:pair){p=pair_options[code%15];code/=15;}
    bool impossible=false;
    for(int j=0;j<5;++j)for(int k=0;k<j;++k)
      if(side_of[j]==side_of[k]&&(has(pair[j],pair[k][0])||has(pair[j],pair[k][1])))impossible=true;
    if(impossible)continue;
    std::array<std::vector<Map>,5> maps;
    for(int j=0;j<5&&!impossible;++j){
      std::array<int,4> rem{},avail{};int a=0,b=0;
      for(int i=0;i<6;++i)if(!has(pair[j],i))rem[a++]=i;
      for(int q=0;q<5;++q)if(q!=side_of[j])avail[b++]=q;
      std::sort(rem.begin(),rem.end());
      do{Map m;m.fill(-1);bool valid=true;
        for(int t=0;t<4;++t){int i=rem[t],q=avail[t];
          for(int ell=0;ell<5;++ell)if(side_of[ell]==q&&has(pair[ell],i))valid=false;
          m[i]=q;
        }
        if(valid){m[pair[j][0]]=side_of[j];m[pair[j][1]]=side_of[j];maps[j].push_back(m);}
      }while(std::next_permutation(rem.begin(),rem.end()));
      if(maps[j].empty())impossible=true;
    }
    if(impossible)continue;
    std::array<Map,5> selected;
    auto dfs=[&](auto&&self,int j)->void{
      if(j==5){solutions.push_back(pack(pair,selected));return;}
      for(const auto&m:maps[j]){bool valid=true;
        for(int k=0;k<j;++k){int common=0;for(int i=0;i<6;++i)common+=m[i]==selected[k][i];if(common!=1){valid=false;break;}}
        if(valid){selected[j]=m;self(self,j+1);}
      }
    };dfs(dfs,0);
  }
  std::sort(solutions.begin(),solutions.end());
  if(std::adjacent_find(solutions.begin(),solutions.end())!=solutions.end())throw std::runtime_error("duplicate solution");
  return solutions;
}

static Generator identity(){Generator g;std::iota(g.star.begin(),g.star.end(),0);std::iota(g.r.begin(),g.r.end(),0);std::iota(g.side.begin(),g.side.end(),0);return g;}

static std::vector<Generator> generators(const Sides& s){
  std::vector<Generator> out;
  for(int a=0;a<5;++a){auto g=identity();std::swap(g.star[a],g.star[a+1]);out.push_back(g);}
  std::array<std::vector<int>,5> blocks;std::array<bool,5> used{};
  for(int j=0;j<5;++j){blocks[s[j]].push_back(j);used[s[j]]=true;}
  for(int q=0;q<5;++q)for(size_t t=1;t<blocks[q].size();++t){auto g=identity();std::swap(g.r[blocks[q][t-1]],g.r[blocks[q][t]]);out.push_back(g);}
  for(int size=1;size<=5;++size){std::vector<int> qs;for(int q=0;q<5;++q)if(int(blocks[q].size())==size)qs.push_back(q);
    for(size_t z=1;z<qs.size();++z){int a=qs[z-1],b=qs[z];auto g=identity();std::swap(g.side[a],g.side[b]);
      for(int t=0;t<size;++t)std::swap(g.r[blocks[a][t]],g.r[blocks[b][t]]);out.push_back(g);}
  }
  std::vector<int> unused;for(int q=0;q<5;++q)if(!used[q])unused.push_back(q);
  for(size_t z=1;z<unused.size();++z){auto g=identity();std::swap(g.side[unused[z-1]],g.side[unused[z]]);out.push_back(g);}
  return out;
}

int main(int argc,char**argv){
  if(argc!=2)return 2;std::string shape=argv[1];Sides sides;
  if(shape=="221")sides={0,0,1,1,2};else if(shape=="2111")sides={0,0,1,2,3};else if(shape=="11111")sides={0,1,2,3,4};else return 3;
  auto solutions=enumerate(sides);std::unordered_map<std::string,int> index;index.reserve(solutions.size()*2);
  for(int i=0;i<int(solutions.size());++i)index.emplace(solutions[i],i);
  auto gens=generators(sides);DSU dsu(solutions.size());
  for(int i=0;i<int(solutions.size());++i)for(const auto&g:gens){auto target=act(solutions[i],g);auto it=index.find(target);if(it==index.end())throw std::runtime_error("symmetry left solution set");dsu.join(i,it->second);}
  std::vector<int> roots;for(int i=0;i<int(solutions.size());++i)if(dsu.find(i)==i)roots.push_back(i);
  std::cout<<"{\"status\":\"PASS\",\"epistemic_status\":\"PROVED\",\"shape\":\""<<shape<<"\",\"solutions\":"<<solutions.size()<<",\"generators\":"<<gens.size()<<",\"orbits\":"<<roots.size()<<",\"representatives\":[";
  for(size_t z=0;z<roots.size();++z){if(z)std::cout<<',';std::array<Pair,5> pair;std::array<Map,5> maps;unpack(solutions[roots[z]],pair,maps);std::cout<<"{\"pairs\":[";
    for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'['<<pair[j][0]<<','<<pair[j][1]<<']';}std::cout<<"],\"maps\":[";
    for(int j=0;j<5;++j){if(j)std::cout<<',';std::cout<<'[';for(int i=0;i<6;++i){if(i)std::cout<<',';std::cout<<maps[j][i];}std::cout<<']';}std::cout<<"]}";
  }
  std::cout<<"]}\n";
}
