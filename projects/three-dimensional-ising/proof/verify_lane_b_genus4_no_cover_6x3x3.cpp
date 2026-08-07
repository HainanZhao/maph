// Proof-side exact finite face-incidence obstruction for a genus-four 6x3x3 embedding.
// A genus-four rotation would have one of the excess-length patterns
// (10), (8,6), or (6,6,6), with every other face an elementary square.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>

constexpr int X=6,Y=3,Z=3,N=X*Y*Z,E=117,S=84;
using Walk=std::vector<int>;
using SquareMask=unsigned __int128;

static int vertex(int x,int y,int z) { return (x*Y+y)*Z+z; }

struct Graph {
  std::array<std::vector<int>,N> adjacency;
  std::array<std::array<int,N>,N> edge_index;
  std::vector<std::array<int,4>> squares;
  std::array<SquareMask,E> incident{};

  Graph() {
    for (auto& row:edge_index) row.fill(-1);
    int edge_count=0;
    auto join=[&](int u,int v) {
      adjacency[u].push_back(v);
      adjacency[v].push_back(u);
      edge_index[u][v]=edge_index[v][u]=edge_count++;
    };
    for (int x=0;x<X;++x) for (int y=0;y<Y;++y) for (int z=0;z<Z;++z) {
      int u=vertex(x,y,z);
      if (x+1<X) join(u,vertex(x+1,y,z));
      if (y+1<Y) join(u,vertex(x,y+1,z));
      if (z+1<Z) join(u,vertex(x,y,z+1));
    }
    if (edge_count!=E) throw std::runtime_error("edge-count regression");
    for (int x=0;x<X;++x) for (int y=0;y<Y;++y) for (int z=0;z<Z;++z) {
      std::array<int,3> coordinate{x,y,z};
      for (int first=0;first<3;++first) for (int second=first+1;second<3;++second) {
        auto a=coordinate,b=coordinate,opposite=coordinate;
        ++a[first]; ++b[second]; ++opposite[first]; ++opposite[second];
        if (opposite[0]>=X || opposite[1]>=Y || opposite[2]>=Z) continue;
        squares.push_back({
          vertex(x,y,z),vertex(a[0],a[1],a[2]),
          vertex(opposite[0],opposite[1],opposite[2]),vertex(b[0],b[1],b[2])
        });
      }
    }
    if ((int)squares.size()!=S) throw std::runtime_error("square-count regression");
    for (int square=0;square<S;++square) {
      for (int side=0;side<4;++side) {
        int edge=edge_index[squares[square][side]][squares[square][(side+1)%4]];
        incident[edge]|=(SquareMask{1}<<square);
      }
    }
  }
};

static Walk canonical(Walk walk) {
  Walk best;
  bool initialized=false;
  for (int reverse=0;reverse<2;++reverse) {
    if (reverse) std::reverse(walk.begin(),walk.end());
    for (int offset=0;offset<(int)walk.size();++offset) {
      Walk candidate;
      for (int index=0;index<(int)walk.size();++index)
        candidate.push_back(walk[(offset+index)%walk.size()]);
      if (!initialized || candidate<best) { best=candidate; initialized=true; }
    }
    if (reverse) std::reverse(walk.begin(),walk.end());
  }
  return best;
}

static std::vector<Walk> reduced_walks(const Graph& graph,int length,bool simple) {
  std::set<Walk> result;
  std::vector<int> path;
  std::array<std::array<bool,N>,N> used{};
  auto extend=[&](auto&& self,int start)->void {
    if ((int)path.size()==length) {
      int end=path.back();
      if (graph.edge_index[end][start]<0 || used[end][start]) return;
      if (path[path.size()-2]==start || path[1]==end) return;
      if (simple && std::set<int>(path.begin(),path.end()).size()!=path.size()) return;
      result.insert(canonical(path));
      return;
    }
    int current=path.back();
    for (int next:graph.adjacency[current]) {
      if (path.size()>1 && next==path[path.size()-2]) continue;
      if (used[current][next]) continue;
      path.push_back(next); used[current][next]=true;
      self(self,start);
      used[current][next]=false; path.pop_back();
    }
  };
  for (int start=0;start<N;++start) {
    path={start};
    extend(extend,start);
  }
  return {result.begin(),result.end()};
}

static std::vector<int> edge_walk(const Graph& graph,const Walk& walk) {
  std::vector<int> result;
  for (int index=0;index<(int)walk.size();++index)
    result.push_back(graph.edge_index[walk[index]][walk[(index+1)%walk.size()]]);
  return result;
}

static int popcount(SquareMask value) {
  return __builtin_popcountll(static_cast<std::uint64_t>(value))
       + __builtin_popcountll(static_cast<std::uint64_t>(value>>64));
}

static int trailing(SquareMask value) {
  std::uint64_t low=static_cast<std::uint64_t>(value);
  if (low) return __builtin_ctzll(low);
  return 64+__builtin_ctzll(static_cast<std::uint64_t>(value>>64));
}

static bool square_cover_search(
    const Graph& graph,std::array<std::int8_t,E> capacities,SquareMask undecided) {
  while (true) {
    SquareMask forced_in=0,forced_out=0;
    for (int edge=0;edge<E;++edge) {
      SquareMask candidates=graph.incident[edge]&undecided;
      int available=popcount(candidates);
      if (capacities[edge]<0 || capacities[edge]>available) return false;
      if (capacities[edge]==0) forced_out|=candidates;
      else if (capacities[edge]==available) forced_in|=candidates;
    }
    if (forced_in&forced_out) return false;
    forced_in&=~forced_out;
    if (!(forced_in|forced_out)) break;
    SquareMask scan=forced_in;
    while (scan) {
      int square=trailing(scan);
      scan&=scan-1;
      for (int side=0;side<4;++side) {
        int edge=graph.edge_index[graph.squares[square][side]][graph.squares[square][(side+1)%4]];
        --capacities[edge];
      }
    }
    undecided&=~(forced_in|forced_out);
  }
  bool done=true;
  SquareMask choices=0;
  int choice_count=S+1;
  for (int edge=0;edge<E;++edge) if (capacities[edge]) {
    done=false;
    SquareMask candidates=graph.incident[edge]&undecided;
    int count=popcount(candidates);
    if (count<choice_count) { choice_count=count; choices=candidates; }
  }
  if (done) return true;
  if (!choices) return false;
  int square=trailing(choices);
  SquareMask bit=SquareMask{1}<<square;
  auto included=capacities;
  for (int side=0;side<4;++side) {
    int edge=graph.edge_index[graph.squares[square][side]][graph.squares[square][(side+1)%4]];
    --included[edge];
  }
  if (square_cover_search(graph,included,undecided^bit)) return true;
  return square_cover_search(graph,capacities,undecided^bit);
}

static bool has_cover(const Graph& graph,const std::vector<const std::vector<int>*>& fixed) {
  std::array<std::int8_t,E> capacities;
  capacities.fill(2);
  for (const auto* walk:fixed) for (int edge:*walk) {
    if (--capacities[edge]<0) return false;
  }
  SquareMask all=(SquareMask{1}<<S)-1;
  return square_cover_search(graph,capacities,all);
}

int main() {
  Graph graph;
  auto six_walks=reduced_walks(graph,6,true);
  auto eight_walks=reduced_walks(graph,8,false);
  auto ten_walks=reduced_walks(graph,10,false);
  std::vector<std::vector<int>> six,eight,ten;
  for (const auto& walk:six_walks) six.push_back(edge_walk(graph,walk));
  for (const auto& walk:eight_walks) eight.push_back(edge_walk(graph,walk));
  for (const auto& walk:ten_walks) ten.push_back(edge_walk(graph,walk));
  std::cout<<"six="<<six.size()<<" eight="<<eight.size()<<" ten="<<ten.size()<<'\n';

  std::uint64_t ten_survivors=0,pair_survivors=0,triple_survivors=0;
  for (const auto& candidate:ten)
    if (has_cover(graph,{&candidate})) ++ten_survivors;
  std::cout<<"ten_survivors="<<ten_survivors<<'\n';
  for (const auto& left:eight) for (const auto& right:six)
    if (has_cover(graph,{&left,&right})) ++pair_survivors;
  std::cout<<"eight_six_survivors="<<pair_survivors<<'\n';
  for (std::size_t first=0;first<six.size();++first)
    for (std::size_t second=first;second<six.size();++second)
      for (std::size_t third=second;third<six.size();++third)
        if (has_cover(graph,{&six[first],&six[second],&six[third]})) ++triple_survivors;
  std::cout<<"three_six_survivors="<<triple_survivors<<'\n';
  return (ten_survivors||pair_survivors||triple_survivors)?1:0;
}
