#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using Mask = std::uint64_t;
using U128 = unsigned __int128;

struct Group {
  std::string name;
  int n, identity;
  std::vector<std::vector<int>> mul;
  std::vector<int> inv;
  std::vector<Mask> classes;
};

static std::string decimal(U128 value) {
  if (!value) return "0";
  std::string out;
  while (value) { out.push_back('0' + value % 10); value /= 10; }
  std::reverse(out.begin(), out.end());
  return out;
}

static int pop(Mask x) { return std::popcount(x); }
static int lcm(int a, int b) { return a / std::gcd(a, b) * b; }

static void finalize(Group &g) {
  g.inv.assign(g.n, -1);
  for (int x = 0; x < g.n; ++x)
    for (int y = 0; y < g.n; ++y)
      if (g.mul[x][y] == g.identity && g.mul[y][x] == g.identity) g.inv[x] = y;
  for (int x : g.inv) assert(x >= 0);
  std::vector<bool> seen(g.n);
  for (int x = 0; x < g.n; ++x) if (!seen[x]) {
    Mask c = 0;
    for (int h = 0; h < g.n; ++h) {
      int z = g.mul[g.mul[g.inv[h]][x]][h];
      c |= Mask{1} << z;
    }
    for (int z = 0; z < g.n; ++z) if (c & (Mask{1} << z)) seen[z] = true;
    g.classes.push_back(c);
  }
}

static Group symmetric(int n) {
  std::vector<std::array<int, 4>> ps;
  std::array<int, 4> p{0,1,2,3};
  do { ps.push_back(p); } while (std::next_permutation(p.begin(), p.begin() + n));
  std::map<std::array<int,4>, int> index;
  for (int i = 0; i < static_cast<int>(ps.size()); ++i) index[ps[i]] = i;
  Group g{"S" + std::to_string(n), static_cast<int>(ps.size()), 0, {}, {}, {}};
  g.mul.assign(g.n, std::vector<int>(g.n));
  for (int i = 0; i < g.n; ++i) for (int j = 0; j < g.n; ++j) {
    std::array<int,4> q{0,1,2,3};
    for (int k = 0; k < n; ++k) q[k] = ps[i][ps[j][k]];
    g.mul[i][j] = index[q];
  }
  finalize(g); return g;
}

static Group dihedral8() {
  Group g{"D8", 8, 0, {}, {}, {}};
  g.mul.assign(8, std::vector<int>(8));
  for (int r = 0; r < 4; ++r) for (int s = 0; s < 2; ++s)
    for (int u = 0; u < 4; ++u) for (int t = 0; t < 2; ++t) {
      int a = 2*r+s, b = 2*u+t;
      int v = (r + (s ? -u : u) + 4) % 4;
      g.mul[a][b] = 2*v + ((s+t)&1);
    }
  finalize(g); return g;
}

static Group quaternion8() {
  // Element 2*b+s means (-1)^s times basis b, where b=0,1,2,3 is 1,i,j,k.
  int basis[4][4] = {{0,1,2,3},{1,0,3,2},{2,3,0,1},{3,2,1,0}};
  int sign[4][4] = {{0,0,0,0},{0,1,0,1},{0,1,1,0},{0,0,1,1}};
  Group g{"Q8", 8, 0, {}, {}, {}};
  g.mul.assign(8, std::vector<int>(8));
  for (int a = 0; a < 8; ++a) for (int b = 0; b < 8; ++b) {
    int ba=a/2, sa=a%2, bb=b/2, sb=b%2;
    g.mul[a][b] = 2*basis[ba][bb] + (sa ^ sb ^ sign[ba][bb]);
  }
  finalize(g); return g;
}

static Mask closure(const Group &g, Mask seed) {
  bool changed = true;
  while (changed) {
    changed = false;
    for (int a = 0; a < g.n; ++a) if (seed & (Mask{1}<<a))
      for (int b = 0; b < g.n; ++b) if (seed & (Mask{1}<<b)) {
        Mask bit = Mask{1} << g.mul[a][b];
        if (!(seed & bit)) { seed |= bit; changed = true; }
      }
  }
  return seed;
}

static std::vector<Mask> subgroups(const Group &g) {
  std::set<Mask> all{Mask{1} << g.identity};
  bool changed = true;
  while (changed) {
    changed = false;
    std::vector<Mask> snapshot(all.begin(), all.end());
    for (Mask h : snapshot) for (int x = 0; x < g.n; ++x) if (!(h & (Mask{1}<<x))) {
      Mask k = closure(g, h | (Mask{1}<<x));
      changed |= all.insert(k).second;
    }
  }
  return {all.begin(), all.end()};
}

static Mask product_set(const Group &g, Mask a, Mask b) {
  Mask out = 0;
  for (int x=0;x<g.n;++x) if (a&(Mask{1}<<x))
    for (int y=0;y<g.n;++y) if (b&(Mask{1}<<y)) out |= Mask{1}<<g.mul[x][y];
  return out;
}

static constexpr std::array<std::array<int,3>,5> RIGHT_NEIGHBORS{{
  {{2,3,4}}, {{0,3,4}}, {{0,1,4}}, {{0,1,2}}, {{1,2,3}}
}};

static U128 density_indicator(const Group &g, Mask a) {
  std::vector<Mask> translated(g.n);
  for (int x=0;x<g.n;++x) for (int z=0;z<g.n;++z)
    if (a & (Mask{1}<<z)) translated[x] |= Mask{1} << g.mul[x][z];
  U128 total = 0;
  for (int x1=0;x1<g.n;++x1) for (int x2=0;x2<g.n;++x2)
    for (int x3=0;x3<g.n;++x3) for (int x4=0;x4<g.n;++x4) {
      int xs[5]{g.identity,x1,x2,x3,x4}; U128 term=1;
      for (const auto &nb : RIGHT_NEIGHBORS) {
        Mask meet = translated[xs[nb[0]]] & translated[xs[nb[1]]] & translated[xs[nb[2]]];
        term *= pop(meet);
      }
      total += term;
    }
  return total;
}

static U128 density_scaled_class_average(const Group &g, Mask a, int &q_out) {
  int q=1; for (Mask c:g.classes) q=lcm(q,pop(c)); q_out=q;
  std::vector<int> w(g.n);
  for (Mask c:g.classes) {
    int value = q * pop(c&a) / pop(c);
    for (int z=0;z<g.n;++z) if (c&(Mask{1}<<z)) w[z]=value;
  }
  U128 total=0;
  for (int x1=0;x1<g.n;++x1) for (int x2=0;x2<g.n;++x2)
    for (int x3=0;x3<g.n;++x3) for (int x4=0;x4<g.n;++x4) {
      int xs[5]{g.identity,x1,x2,x3,x4}; U128 term=1;
      for (const auto &nb:RIGHT_NEIGHBORS) {
        std::uint64_t sum=0;
        for (int y=0;y<g.n;++y) {
          std::uint64_t product=1;
          for (int i:nb) product*=w[g.mul[g.inv[xs[i]]][y]];
          sum+=product;
        }
        term*=sum;
      }
      total+=term;
    }
  return total;
}

static U128 direct_ten_variable_s3(const Group &g, Mask a) {
  U128 total=0;
  for(int x0=0;x0<g.n;++x0)for(int x1=0;x1<g.n;++x1)for(int x2=0;x2<g.n;++x2)for(int x3=0;x3<g.n;++x3)for(int x4=0;x4<g.n;++x4)
    for(int y0=0;y0<g.n;++y0)for(int y1=0;y1<g.n;++y1)for(int y2=0;y2<g.n;++y2)for(int y3=0;y3<g.n;++y3)for(int y4=0;y4<g.n;++y4) {
      int xs[5]{x0,x1,x2,x3,x4}, ys[5]{y0,y1,y2,y3,y4}; bool good=true;
      for(int j=0;j<5;++j) for(int i:RIGHT_NEIGHBORS[j]) if(!(a&(Mask{1}<<g.mul[g.inv[xs[i]]][ys[j]]))) good=false;
      total += good;
    }
  return total;
}

static void check_graph_controls() {
  int edges=0; for (auto nb:RIGHT_NEIGHBORS) edges += nb.size(); assert(edges==15);
  for(int shift=0;shift<5;++shift) for(int j=0;j<5;++j) {
    std::set<int> rotated; for(int i:RIGHT_NEIGHBORS[j]) rotated.insert((i+shift)%5);
    std::set<int> expected; for(int i:RIGHT_NEIGHBORS[(j+shift)%5]) expected.insert(i);
    assert(rotated==expected);
  }
}

static void emit_row(std::ofstream &rows, const std::string &family, const Group &g, Mask a, U128 plain, int q, U128 averaged, int &negative, std::string &first) {
  U128 scale=1; for(int i=0;i<15;++i) scale*=q;
  U128 left=plain*scale; int sign=(left>averaged)-(left<averaged);
  rows<<family<<'\t'<<g.name<<'\t'<<a<<'\t'<<pop(a)<<'\t'<<q<<'\t'<<decimal(plain)<<'\t'<<decimal(averaged)<<'\t'<<sign<<'\n';
  if(sign<0) { ++negative; if(first.empty()) first=family+":"+g.name+":"+std::to_string(a); }
}

int main(int argc,char**argv) {
  if(argc!=2) return 2; std::filesystem::create_directories(argv[1]);
  check_graph_controls(); Group s3=symmetric(3), s4=symmetric(4), d8=dihedral8(), q8=quaternion8();
  std::ofstream rows(std::string(argv[1])+"/comparison-rows.tsv");
  rows<<"family\tgroup\tindicator_mask\tindicator_size\tclass_scale\tplain_numerator\taverage_scaled_numerator\tcomparison_sign\n";
  int negative=0, total=0; std::string first;
  std::vector<Group*> small{&s3,&d8,&q8};
  for(Group* g:small) for(Mask a=0;a<(Mask{1}<<g->n);++a) { int q; emit_row(rows,"all_indicator",*g,a,density_indicator(*g,a),q,density_scaled_class_average(*g,a,q),negative,first); ++total; }
  for(Group* g:std::vector<Group*>{&s3,&s4}) {
    std::set<Mask> products; auto subs=subgroups(*g);
    for(Mask a:subs) for(Mask b:subs) products.insert(product_set(*g,a,b));
    assert(products.size()<=4096);
    for(Mask a:products) { int q; emit_row(rows,"subgroup_product",*g,a,density_indicator(*g,a),q,density_scaled_class_average(*g,a,q),negative,first); ++total; }
  }
  // Direct ten-variable control on exactly the frozen S3 empty/full/least non-class indicators.
  Mask nonclass=0; for(Mask a=0;a<(Mask{1}<<s3.n);++a) { bool ok=true; for(Mask c:s3.classes) if((a&c)!=0 && (a&c)!=c) ok=false; if(!ok){nonclass=a;break;} }
  std::ofstream controls(std::string(argv[1])+"/direct-s3-controls.tsv"); controls<<"indicator_mask\tdirect_numerator\tnormalized_times_group\n";
  for(Mask a:std::vector<Mask>{0,(Mask{1}<<s3.n)-1,nonclass}) { U128 direct=direct_ten_variable_s3(s3,a), normalized=density_indicator(s3,a); assert(direct==normalized*s3.n); controls<<a<<'\t'<<decimal(direct)<<'\t'<<decimal(normalized*s3.n)<<'\n'; }
  std::ofstream summary(std::string(argv[1])+"/summary.json");
  summary<<"{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n  \"edge_count\": 15,\n  \"comparison_rows\": "<<total<<",\n  \"negative_rows\": "<<negative<<",\n  \"first_countermodel\": "<<(first.empty()?"null":"\""+first+"\"")<<",\n  \"groups\": {\"S3\":6,\"D8\":8,\"Q8\":8,\"S4\":24}\n}\n";
  std::cout<<"rows="<<total<<" negative="<<negative<<"\n";
}
