// Exploratory unrestricted rotation search for the free 6x3x3 box.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

constexpr int X=6,Y=3,Z=3,N=X*Y*Z;
using Rotation=std::vector<std::vector<int>>;

static int vertex(int x,int y,int z) { return (x*Y+y)*Z+z; }

static int face_count(const Rotation& rotation,std::vector<int>* lengths=nullptr) {
  std::array<std::array<bool,N>,N> seen{};
  int faces=0;
  if (lengths) lengths->clear();
  for (int u=0;u<N;++u) for (int v:rotation[u]) if (!seen[u][v]) {
    ++faces;
    int a=u,b=v,length=0;
    while (!seen[a][b]) {
      seen[a][b]=true;
      ++length;
      const auto& cyclic=rotation[b];
      auto position=std::find(cyclic.begin(),cyclic.end(),a);
      int next=cyclic[(position-cyclic.begin()+1)%cyclic.size()];
      a=b;
      b=next;
    }
    if (lengths) lengths->push_back(length);
  }
  return faces;
}

int main(int argc,char** argv) {
  std::uint64_t seed=argc>1?std::stoull(argv[1]):20260816ULL;
  long long iterations=argc>2?std::stoll(argv[2]):100000000LL;
  int target=argc>3?std::stoi(argv[3]):57;
  std::mt19937_64 random(seed);
  Rotation adjacency(N);
  for (int x=0;x<X;++x) for (int y=0;y<Y;++y) for (int z=0;z<Z;++z) {
    int u=vertex(x,y,z);
    auto join=[&](int xx,int yy,int zz) {
      int v=vertex(xx,yy,zz);
      adjacency[u].push_back(v);
      adjacency[v].push_back(u);
    };
    if (x+1<X) join(x+1,y,z);
    if (y+1<Y) join(x,y+1,z);
    if (z+1<Z) join(x,y,z+1);
  }
  int best=-1;
  Rotation best_rotation;
  std::vector<int> best_lengths;
  long long completed=0;
  while (completed<iterations) {
    Rotation rotation=adjacency;
    for (auto& cyclic:rotation) std::shuffle(cyclic.begin(),cyclic.end(),random);
    int score=face_count(rotation);
    constexpr int tranche=300000;
    for (int local=0;local<tranche && completed<iterations;++local,++completed) {
      int u=random()%N;
      auto& cyclic=rotation[u];
      int left=random()%cyclic.size();
      int right=random()%cyclic.size();
      if (left==right) continue;
      std::swap(cyclic[left],cyclic[right]);
      int candidate=face_count(rotation);
      double fraction=static_cast<double>(local)/tranche;
      double temperature=std::max(0.03,1.5*std::exp(-9.0*fraction));
      bool accept=candidate>=score;
      if (!accept) {
        double uniform=(random()+0.5)/(static_cast<double>(random.max())+1.0);
        accept=uniform<std::exp((candidate-score)/temperature);
      }
      if (accept) score=candidate;
      else std::swap(cyclic[left],cyclic[right]);
      if (score>best) {
        best=score;
        best_rotation=rotation;
        face_count(rotation,&best_lengths);
        std::sort(best_lengths.begin(),best_lengths.end());
        std::cerr<<"best="<<best<<" iteration="<<completed<<" lengths=";
        for (int length:best_lengths) std::cerr<<length<<',';
        std::cerr<<'\n';
        if (best>=target) { completed=iterations; break; }
      }
    }
  }
  std::cout<<"ROTATION\n";
  for (int u=0;u<N;++u) {
    std::cout<<u<<':';
    for (int v:best_rotation[u]) std::cout<<' '<<v;
    std::cout<<'\n';
  }
  return best>=target?0:1;
}
