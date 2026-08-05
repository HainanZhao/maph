#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using Point = std::array<long double, 5>;

static constexpr std::array<std::pair<int, int>, 15> EDGES{{
    {0,2},{0,3},{0,4}, {1,0},{1,3},{1,4}, {2,0},{2,1},{2,4},
    {3,0},{3,1},{3,2}, {4,1},{4,2},{4,3}
}};

struct RNG {
  std::array<std::uint64_t, 4> s{};
  static std::uint64_t rotl(std::uint64_t x, int k) { return (x << k) | (x >> (64-k)); }
  static std::uint64_t splitmix(std::uint64_t& x) {
    std::uint64_t z = (x += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
  }
  explicit RNG(std::uint64_t seed) { for (auto& x : s) x = splitmix(seed); }
  std::uint64_t next() {
    const std::uint64_t result = rotl(s[1] * 5, 7) * 9;
    const std::uint64_t t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3];
    s[2] ^= t; s[3] = rotl(s[3], 45);
    return result;
  }
  long double unit() { return std::ldexp(static_cast<long double>(next()), -64); }
  std::uint64_t bounded(std::uint64_t n) {
    const std::uint64_t threshold = -n % n;
    for (;;) { const auto x = next(); if (x >= threshold) return x % n; }
  }
};

struct Eval { long double score, t, m, deficit; };

static Eval evaluate(const Point& x) {
  const long double p=x[0], q=x[1];
  const long double aw[2]{p,1-p}, bw[2]{q,1-q};
  const long double w[2][2]{{1,x[2]},{x[3],x[4]}};
  long double t=0;
  for (unsigned mask=0; mask<32; ++mask) {
    int left[5]; long double term=1;
    for (int i=0;i<5;++i) { left[i]=(mask>>i)&1; term*=aw[left[i]]; }
    for (int j=0;j<5;++j) {
      long double integrated=0;
      for (int b=0;b<2;++b) {
        long double z=bw[b];
        for (int i=0;i<5;++i) {
          const int d=(j-i+5)%5;
          if (d!=0 && d!=4) z*=w[left[i]][b];
        }
        integrated+=z;
      }
      term*=integrated;
    }
    t+=term;
  }
  long double m=0;
  for(int a=0;a<2;++a) for(int b=0;b<2;++b) m+=aw[a]*bw[b]*w[a][b];
  if (!(m>0) || !(t>0)) return {std::numeric_limits<long double>::infinity(),t,m,t};
  const long double score=std::log(t)-15*std::log(m);
  const long double mpow=std::pow(m,15);
  return {score,t,m,t-mpow};
}

static long double reflect(long double x) {
  while (x<0 || x>1) { if(x<0)x=-x; if(x>1)x=2-x; }
  return x;
}

static std::string key(const Point& p) {
  std::ostringstream o; o<<std::setprecision(21);
  for(auto x:p)o<<x<<',';
  return o.str();
}

int main(int argc, char** argv) {
  if(argc!=3) { std::cerr<<"usage: search SEED OUTDIR\n"; return 2; }
  const std::uint64_t seed=std::stoull(argv[1]);
  const std::filesystem::path outdir=argv[2];
  std::filesystem::create_directories(outdir);
  constexpr int N=256, G=4000;
  constexpr long double F=0.75L, CR=0.9L;
  RNG rng(seed);
  std::array<Point,N> pop{};
  std::array<Eval,N> val{};
  for(int i=0;i<32;++i) for(int j=0;j<5;++j) pop[i][j]=(i>>j)&1;
  for(int i=32;i<N;++i) {
    for(auto& z:pop[i]) z=rng.unit();
    if(i<112) { const int face=(i-32)%10; pop[i][face/2]=face%2; }
  }
  for(int i=0;i<N;++i) val[i]=evaluate(pop[i]);
  std::uint64_t trials=0;
  for(int gen=0;gen<G;++gen) {
    for(int i=0;i<N;++i) {
      int a,b,c;
      do a=static_cast<int>(rng.bounded(N)); while(a==i);
      do b=static_cast<int>(rng.bounded(N)); while(b==i||b==a);
      do c=static_cast<int>(rng.bounded(N)); while(c==i||c==a||c==b);
      const int forced=static_cast<int>(rng.bounded(5));
      Point trial=pop[i];
      for(int j=0;j<5;++j) if(j==forced || rng.unit()<CR)
        trial[j]=reflect(pop[a][j]+F*(pop[b][j]-pop[c][j]));
      const Eval ev=evaluate(trial); ++trials;
      if(ev.score<=val[i].score) { pop[i]=trial; val[i]=ev; }
    }
  }
  std::vector<int> order(N); for(int i=0;i<N;++i)order[i]=i;
  std::sort(order.begin(),order.end(),[&](int a,int b){return val[a].score<val[b].score;});
  std::ofstream rows(outdir/("candidates-"+std::to_string(seed)+".tsv"));
  rows<<"seed\trank\tp\tq\tw01\tw10\tw11\tlog_ratio\tt_H\tm\tfloat_deficit\n"<<std::setprecision(21);
  std::set<std::string> seen; int retained=0;
  for(int i:order) if(seen.insert(key(pop[i])).second) {
    rows<<seed<<'\t'<<retained;
    for(auto z:pop[i])rows<<'\t'<<z;
    rows<<'\t'<<val[i].score<<'\t'<<val[i].t<<'\t'<<val[i].m<<'\t'<<val[i].deficit<<'\n';
    if(++retained==32)break;
  }
  const auto best=order.front();
  std::ofstream summary(outdir/("summary-"+std::to_string(seed)+".json"));
  summary<<std::setprecision(21)<<"{\n"
    <<"  \"seed\": "<<seed<<",\n  \"population\": 256,\n  \"generations\": 4000,\n"
    <<"  \"trial_evaluations\": "<<trials<<",\n  \"retained_distinct\": "<<retained<<",\n"
    <<"  \"best_log_ratio\": "<<val[best].score<<",\n  \"best_float_deficit\": "<<val[best].deficit<<"\n}\n";
  std::cout<<seed<<" trials="<<trials<<" retained="<<retained<<" best="<<std::setprecision(21)<<val[best].score<<"\n";
}
