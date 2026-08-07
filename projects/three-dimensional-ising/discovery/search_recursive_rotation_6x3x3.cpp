// Discovery search for a high-face-count 6x3x3 rotation whose deletion of
// the final x-slice recovers the pinned recursive 5x3x3 rotation.
#include <algorithm>
#include <array>
#include <bitset>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

constexpr int N = 54;
constexpr int E = 117;
using Rotation = std::vector<std::vector<int>>;
using EdgeMask = std::bitset<E>;

static const std::array<std::vector<int>, 45> base = {{
  {3,9,1},{10,4,2,0},{11,1,5},{0,6,4,12},{7,5,1,13,3},{8,14,2,4},
  {15,7,3},{6,16,8,4},{5,7,17},{12,18,10,0},{9,19,11,13,1},{20,2,14,10},
  {21,9,3,13,15},{14,22,16,12,4,10},{23,13,11,5,17},{6,24,12,16},
  {7,15,13,25,17},{8,16,26,14},{9,21,27,19},{22,20,10,18,28},
  {11,19,23,29},{18,12,24,22,30},{25,13,23,19,31,21},
  {32,20,22,14,26},{25,21,15,33},{16,22,24,34,26},{35,23,17,25},
  {18,30,36,28},{31,19,27,37,29},{32,28,38,20},{39,27,21,31,33},
  {28,32,40,34,30,22},{35,41,31,29,23},{42,30,34,24},
  {31,43,35,25,33},{34,44,32,26},{27,39,37},{36,40,38,28},
  {41,29,37},{42,40,36,30},{41,37,39,43,31},{38,40,32,44},
  {43,39,33},{34,40,42,44},{43,41,35}
}};

static int vertex(int x, int y, int z) { return (x * 3 + y) * 3 + z; }

static Rotation adjacency() {
  Rotation result(N);
  for (int x=0; x<6; ++x) for (int y=0; y<3; ++y) for (int z=0; z<3; ++z) {
    int u=vertex(x,y,z);
    auto add=[&](int xx,int yy,int zz) { result[u].push_back(vertex(xx,yy,zz)); };
    if (x) add(x-1,y,z);
    if (x+1<6) add(x+1,y,z);
    if (y) add(x,y-1,z);
    if (y+1<3) add(x,y+1,z);
    if (z) add(x,y,z-1);
    if (z+1<3) add(x,y,z+1);
  }
  return result;
}

static int face_count(const Rotation& rotation, std::vector<int>* lengths=nullptr) {
  std::array<std::array<bool,N>,N> seen{};
  int faces=0;
  if (lengths) lengths->clear();
  for (int u=0; u<N; ++u) for (int v:rotation[u]) if (!seen[u][v]) {
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

static std::vector<EdgeMask> face_masks(const Rotation& rotation) {
  std::array<std::array<int,N>,N> edge_index{};
  for (auto& row:edge_index) row.fill(-1);
  Rotation adj=adjacency();
  int edge_count=0;
  for (int u=0; u<N; ++u) for (int v:adj[u]) if (u<v) {
    edge_index[u][v]=edge_index[v][u]=edge_count++;
  }
  if (edge_count!=E) throw std::runtime_error("edge-count regression");
  std::array<std::array<bool,N>,N> seen{};
  std::vector<EdgeMask> result;
  for (int u=0; u<N; ++u) for (int v:rotation[u]) if (!seen[u][v]) {
    EdgeMask mask;
    int a=u,b=v;
    while (!seen[a][b]) {
      seen[a][b]=true;
      mask.flip(edge_index[a][b]);
      const auto& cyclic=rotation[b];
      auto position=std::find(cyclic.begin(),cyclic.end(),a);
      int next=cyclic[(position-cyclic.begin()+1)%cyclic.size()];
      a=b;
      b=next;
    }
    result.push_back(mask);
  }
  return result;
}

static int gf2_rank(std::vector<EdgeMask> vectors) {
  int rank=0;
  for (int column=E-1; column>=0; --column) {
    int pivot=-1;
    for (int row=rank; row<(int)vectors.size(); ++row) {
      if (vectors[row][column]) { pivot=row; break; }
    }
    if (pivot<0) continue;
    std::swap(vectors[rank],vectors[pivot]);
    for (int row=0; row<(int)vectors.size(); ++row) {
      if (row!=rank && vectors[row][column]) vectors[row]^=vectors[rank];
    }
    ++rank;
  }
  return rank;
}

static int boundary_defect(const Rotation& rotation) {
  auto current=face_masks(rotation);
  int current_rank=gf2_rank(current);
  Rotation old_rotation(N);
  for (int u=0; u<45; ++u) old_rotation[u]=base[u];
  auto old=face_masks(old_rotation);
  current.insert(current.end(),old.begin(),old.end());
  return gf2_rank(current)-current_rank;
}

static void randomize(Rotation& rotation, std::mt19937_64& random) {
  for (int u=0; u<45; ++u) rotation[u]=base[u];
  for (int u=36; u<45; ++u) {
    int special=u+9;
    int position=random()%(rotation[u].size()+1);
    rotation[u].insert(rotation[u].begin()+position,special);
  }
  Rotation adj=adjacency();
  for (int u=45; u<54; ++u) {
    rotation[u]=adj[u];
    std::shuffle(rotation[u].begin(),rotation[u].end(),random);
  }
}

int main(int argc,char** argv) {
  std::uint64_t seed=argc>1?std::stoull(argv[1]):20260812ULL;
  long long iterations=argc>2?std::stoll(argv[2]):200000000LL;
  int target_faces=argc>3?std::stoi(argv[3]):57;
  std::mt19937_64 random(seed);
  int best=-1,best_defect=999;
  Rotation best_rotation;
  std::vector<int> best_lengths;
  long long completed=0;
  while (completed<iterations) {
    Rotation rotation(N);
    randomize(rotation,random);
    int score=face_count(rotation);
    constexpr int tranche=300000;
    for (int local=0; local<tranche && completed<iterations; ++local,++completed) {
      int u=36+random()%18;
      auto old=rotation[u];
      if (u<45) {
        int special=u+9;
        auto position=std::find(rotation[u].begin(),rotation[u].end(),special);
        rotation[u].erase(position);
        int insertion=random()%(rotation[u].size()+1);
        rotation[u].insert(rotation[u].begin()+insertion,special);
      } else {
        int left=random()%rotation[u].size();
        int right=random()%rotation[u].size();
        if (left==right) continue;
        std::swap(rotation[u][left],rotation[u][right]);
      }
      int candidate=face_count(rotation);
      double fraction=static_cast<double>(local)/tranche;
      double temperature=std::max(0.025,1.4*std::exp(-9.0*fraction));
      bool accept=candidate>=score;
      if (!accept) {
        double uniform=(random()+0.5)/(static_cast<double>(random.max())+1.0);
        accept=uniform<std::exp((candidate-score)/temperature);
      }
      if (accept) score=candidate;
      else rotation[u]=old;
      int defect=score>=55?boundary_defect(rotation):999;
      if (score>best || (score==best && defect<best_defect)) {
        best=score;
        best_defect=defect;
        best_rotation=rotation;
        face_count(rotation,&best_lengths);
        std::sort(best_lengths.begin(),best_lengths.end());
        std::cerr<<"best="<<best<<" defect="<<best_defect
                 <<" iteration="<<completed<<" lengths=";
        for (int length:best_lengths) std::cerr<<length<<',';
        std::cerr<<'\n';
        if (best>=target_faces) { completed=iterations; break; }
      }
    }
  }
  std::cout<<"ROTATION\n";
  for (int u=0; u<N; ++u) {
    std::cout<<u<<':';
    for (int v:best_rotation[u]) std::cout<<' '<<v;
    std::cout<<'\n';
  }
  return best>=target_faces?0:1;
}
