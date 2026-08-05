#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>

#ifdef _OPENMP
#include <omp.h>
#endif

using I = std::int64_t;
using Big = boost::multiprecision::cpp_int;
using Poly = std::array<I, 16>;

static constexpr std::array<std::pair<int,int>, 15> EDGES{{
  {0,2},{0,3},{0,4}, {1,0},{1,3},{1,4}, {2,0},{2,1},{2,4},
  {3,0},{3,1},{3,2}, {4,1},{4,2},{4,3}
}};

struct Direction { int q; std::vector<int> b; };
struct Row { Direction d; Poly p{}; int first = -1; int sign = 0; std::string epsilon; };

static bool edge(int i, int j) { int x = (j - i + 5) % 5; return x != 0 && x != 4; }
static void graph_controls() {
  int n=0; for(int i=0;i<5;++i) for(int j=0;j<5;++j) n += edge(i,j); assert(n==15);
  for(int shift=0;shift<5;++shift) for(int i=0;i<5;++i) for(int j=0;j<5;++j)
    assert(edge(i,j)==edge((i+shift)%5,(j+shift)%5));
  // The five reflections preserve the forbidden differences after j -> -j-1.
  for(int shift=0;shift<5;++shift) for(int i=0;i<5;++i) for(int j=0;j<5;++j)
    assert(edge(i,j)==edge((shift-i+5)%5,(shift-j-1+10)%5));
}

static int gcd_nonzero(const std::vector<int>& b) { int g=0; for(int x:b) g=std::gcd(g,std::abs(x)); return g; }
static bool sign_canonical(const std::vector<int>& b) { for(int x:b) if(x) return x<0; return false; }
static std::vector<Direction> directions(int q) {
  std::vector<std::pair<int,int>> pos; for(int i=0;i<q;++i) for(int j=i;j<q;++j) pos.push_back({i,j});
  std::vector<Direction> out; std::vector<int> u(pos.size());
  const int total=1; // retained only to make the exhaustive recursive range explicit below.
  (void)total;
  auto rec = [&](auto&& self, int at) -> void {
    if(at == (int)u.size()) {
      int sum=0; for(int z=0;z<(int)u.size();++z) sum += (pos[z].first==pos[z].second ? 1 : 2)*u[z];
      if(sum || gcd_nonzero(u)!=1 || !sign_canonical(u)) return;
      Direction d{q,std::vector<int>(q*q)};
      for(int z=0;z<(int)u.size();++z) { auto [i,j]=pos[z]; d.b[i*q+j]=d.b[j*q+i]=u[z]; }
      out.push_back(std::move(d)); return;
    }
    for(int x=-2;x<=2;++x) { u[at]=x; self(self,at+1); }
  };
  rec(rec,0); return out;
}
static std::string matrix_text(const Direction& d) {
  std::ostringstream o; for(int i=0;i<d.q;++i) for(int j=0;j<d.q;++j) { if(i||j)o<<','; o<<d.b[i*d.q+j]; } return o.str();
}
static std::string poly_text(const Poly& p) { std::ostringstream o; for(int k=0;k<=15;++k) { if(k)o<<','; o<<p[k]; } return o.str(); }

static Poly polynomial(const Direction& d) {
  Poly total{}; std::array<int,10> a{};
  const int assignments = [&]{int v=1; for(int x=0;x<10;++x)v*=d.q; return v;}();
  for(int code=0;code<assignments;++code) {
    int z=code; for(int x=0;x<10;++x){a[x]=z%d.q;z/=d.q;}
    Poly cur{}; cur[0]=1; int degree=0;
    for(auto [li,rj]:EDGES) {
      const int w=d.b[a[li]*d.q+a[5+rj]];
      for(int k=degree+1;k>=1;--k) cur[k]+=w*cur[k-1];
      ++degree;
    }
    for(int k=0;k<=15;++k) total[k]+=cur[k];
  }
  total[0]-=assignments;
  return total;
}
static int first_sign(const Poly& p, int& first) { for(int k=1;k<=15;++k) if(p[k]) {first=k; return (p[k]>0)-(p[k]<0);} first=-1;return 0; }
static std::string realize_negative(const Poly& p) {
  for(int m=2;m<=512;++m) { Big s=0; for(int k=1;k<=15;++k) if(p[k]) s += Big(p[k]) << (m*(15-k)); if(s<0) return "2^-"+std::to_string(m); }
  return "ERROR";
}
static void hand_control() {
  Direction d{2,{1,-1,-1,1}}; Poly direct=polynomial(d), subset{}; std::array<int,10>a{};
  for(int code=0;code<1024;++code) {int z=code;for(int x=0;x<10;++x){a[x]=z&1;z>>=1;} for(int mask=0;mask<(1<<15);++mask){int k=0,prod=1;for(int e=0;e<15;++e)if(mask&(1<<e)){auto [li,rj]=EDGES[e];prod*=d.b[a[li]*2+a[5+rj]];++k;}subset[k]+=prod;}}
  subset[0]-=1024; assert(direct==subset); assert(direct[0]==0);
}
int main(int argc,char**argv) {
  if(argc!=2) return 2; std::filesystem::create_directories(argv[1]); graph_controls(); hand_control();
  std::vector<Direction> all=directions(2), q3=directions(3); all.insert(all.end(),q3.begin(),q3.end());
  assert(all.size()<=20000); std::vector<Row> rows(all.size());
  #pragma omp parallel for schedule(dynamic)
  for(int i=0;i<(int)all.size();++i) { rows[i].d=all[i]; rows[i].p=polynomial(all[i]); rows[i].sign=first_sign(rows[i].p,rows[i].first); if(rows[i].sign<0) rows[i].epsilon=realize_negative(rows[i].p); }
  std::ofstream out(std::string(argv[1])+"/rows.tsv"); out<<"q\tmatrix\tcoefficients_Q\tfirst_degree\tclassification\trealized_epsilon\n";
  int neg=0,pos=0,zero=0; for(const auto&r:rows){std::string c=r.sign<0?"LOCAL_NEGATIVE":r.sign>0?"LOCAL_POSITIVE":"IDENTICALLY_ZERO";if(r.sign<0){++neg;assert(r.epsilon!="ERROR");}else if(r.sign>0)++pos;else++zero;out<<r.d.q<<'\t'<<matrix_text(r.d)<<'\t'<<poly_text(r.p)<<'\t'<<r.first<<'\t'<<c<<'\t'<<(r.epsilon.empty()?"-":r.epsilon)<<'\n';}
  std::ofstream summary(std::string(argv[1])+"/summary.json"); summary<<"{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n  \"edge_count\": 15,\n  \"direction_count\": "<<rows.size()<<",\n  \"q2_directions\": "<<directions(2).size()<<",\n  \"q3_directions\": "<<q3.size()<<",\n  \"local_negative\": "<<neg<<",\n  \"local_positive\": "<<pos<<",\n  \"identically_zero\": "<<zero<<"\n}\n";
  std::cout<<"directions="<<rows.size()<<" negative="<<neg<<" positive="<<pos<<" zero="<<zero<<"\n";
}
