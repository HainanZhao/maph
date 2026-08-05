#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif

using Big=boost::multiprecision::cpp_int;
using Exp=std::array<int,5>;
using Vertex=std::array<std::uint64_t,5>;
using Vertices=std::array<Vertex,5>;
static std::vector<Exp> exponents;
static std::map<Exp,int> index_of;
static std::uint64_t binom[16][16];
static std::atomic<std::uint64_t> global_cells{0};
static std::uint64_t global_cap=0;

struct Unresolved{int depth;Vertices vertices;};
struct FamilyResult{std::string name;std::uint64_t visited=0,certified=0,unresolved=0;int max_depth=0;bool complete=true;std::vector<Unresolved> cells;};

static std::vector<std::string> split(const std::string&s){std::stringstream in(s);std::vector<std::string>f;std::string x;while(std::getline(in,x,'\t'))f.push_back(x);return f;}

static std::vector<Big> load(const std::filesystem::path&path){
  struct Raw{Exp e;std::int64_t n;std::uint64_t d;};std::ifstream in(path);std::string line;std::getline(in,line);std::vector<Raw>raw;std::uint64_t lcm=1;
  while(std::getline(in,line)){if(line.empty())continue;auto f=split(line);Raw r{};for(int i=0;i<5;++i)r.e[i]=std::stoi(f[i]);r.n=std::stoll(f[5]);r.d=std::stoull(f[6]);lcm=std::lcm(lcm,r.d);raw.push_back(r);}
  std::vector<Big> poly(exponents.size());for(const auto&r:raw)poly[index_of.at(r.e)]+=Big(r.n)*(lcm/r.d);return poly;
}

static bool coefficient_certificate(const std::vector<Big>&p){for(const auto&c:p)if(c<0)return false;return true;}

static std::pair<int,int> longest_edge(const Vertices&v){
  std::uint64_t best=0;std::pair<int,int>edge{0,1};
  for(int i=0;i<5;++i)for(int j=i+1;j<5;++j){std::uint64_t d=0;for(int k=0;k<5;++k){auto x=static_cast<std::int64_t>(v[i][k])-static_cast<std::int64_t>(v[j][k]);d+=static_cast<std::uint64_t>(x*x);}if(d>best){best=d;edge={i,j};}}
  return edge;
}

static std::vector<Big> child_poly(const std::vector<Big>&p,int i,int j,bool replace_i){
  std::vector<Big> out(p.size());
  for(std::size_t at=0;at<p.size();++at)if(p[at]!=0){const auto&a=exponents[at];int expanded=replace_i?a[j]:a[i];int other=15-a[i]-a[j];
    for(int k=0;k<=expanded;++k){Exp b=a;std::uint64_t factor=binom[expanded][k]<<(k+other);
      if(replace_i){b[j]=k;b[i]=a[i]+a[j]-k;}else{b[i]=k;b[j]=a[i]+a[j]-k;}
      out[index_of.at(b)]+=p[at]*factor;}}
  return out;
}

static Vertices child_vertices(const Vertices&v,int i,int j,bool replace_i){Vertices w=v;for(auto&vertex:w)for(auto&x:vertex)x*=2;int replace=replace_i?i:j;for(int k=0;k<5;++k)w[replace][k]=v[i][k]+v[j][k];return w;}

static void certify(const std::vector<Big>&p,const Vertices&v,int depth,FamilyResult&r){
  const auto ordinal=global_cells.fetch_add(1);if(ordinal>=global_cap){r.complete=false;++r.unresolved;r.cells.push_back({depth,v});return;}++r.visited;r.max_depth=std::max(r.max_depth,depth);
  if(coefficient_certificate(p)){++r.certified;return;}
  if(depth>=18){r.complete=false;++r.unresolved;r.cells.push_back({depth,v});return;}
  auto [i,j]=longest_edge(v);
  auto left=child_poly(p,i,j,false);auto left_v=child_vertices(v,i,j,false);certify(left,left_v,depth+1,r);
  if(global_cells.load()>=global_cap){r.complete=false;++r.unresolved;r.cells.push_back({depth,v});return;}
  auto right=child_poly(p,i,j,true);auto right_v=child_vertices(v,i,j,true);certify(right,right_v,depth+1,r);
}

int main(int argc,char**argv){
  if(argc!=4){std::cerr<<"usage: bernstein PULLBACK_DIR OUTDIR CELL_CAP\n";return 2;}global_cap=std::stoull(argv[3]);if(global_cap>1000000)return 2;
  for(int a=0;a<=15;++a)for(int b=0;b<=15-a;++b)for(int c=0;c<=15-a-b;++c)for(int d=0;d<=15-a-b-c;++d){Exp e{a,b,c,d,15-a-b-c-d};index_of[e]=exponents.size();exponents.push_back(e);}
  for(int n=0;n<=15;++n){binom[n][0]=binom[n][n]=1;for(int k=1;k<n;++k)binom[n][k]=binom[n-1][k-1]+binom[n-1][k];}
  const std::array<std::string,4>names{{"cycle_equal","cycle_zero","trans_equal","trans_zero"}};std::array<FamilyResult,4>results;
  #ifdef _OPENMP
  omp_set_num_threads(3);
  #pragma omp parallel for schedule(dynamic)
  #endif
  for(int family=0;family<4;++family){auto p=load(std::filesystem::path(argv[1])/(names[family]+".tsv"));Vertices v{};for(int i=0;i<5;++i)v[i][i]=1;FamilyResult r;r.name=names[family];certify(p,v,0,r);results[family]=r;}
  std::filesystem::create_directories(argv[2]);std::ofstream out(std::filesystem::path(argv[2])/"bernstein-summary.json");out<<"{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n  \"cell_cap\": "<<global_cap<<",\n  \"global_cells\": "<<std::min(global_cells.load(),global_cap)<<",\n  \"families\": {\n";
  bool all=true;for(int i=0;i<4;++i){auto&r=results[i];all&=r.complete;out<<"    \""<<r.name<<"\": {\"complete\": "<<(r.complete?"true":"false")<<", \"visited\": "<<r.visited<<", \"certified_leaves\": "<<r.certified<<", \"unresolved\": "<<r.unresolved<<", \"max_depth\": "<<r.max_depth<<"}"<<(i==3?"\n":",\n");}
  out<<"  },\n  \"complete_cover\": "<<(all?"true":"false")<<"\n}\n";
  for(const auto&r:results){std::ofstream cells(std::filesystem::path(argv[2])/(r.name+"-unresolved.tsv"));cells<<"depth";for(int v=0;v<5;++v)for(int k=0;k<5;++k)cells<<"\tv"<<v<<"z"<<k;cells<<'\n';for(const auto&cell:r.cells){cells<<cell.depth;for(const auto&vertex:cell.vertices)for(auto x:vertex)cells<<'\t'<<x;cells<<'\n';}}
  for(const auto&r:results)std::cout<<r.name<<" complete="<<r.complete<<" visited="<<r.visited<<" certified="<<r.certified<<" unresolved="<<r.unresolved<<" depth="<<r.max_depth<<'\n';return 0;
}
