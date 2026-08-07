#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <iostream>
#include <mutex>
#include <random>
#include <thread>
#include <vector>

using Block = std::array<int, 6>;
constexpr int V = 23, NB = 20;

static const std::array<Block, 21> KNOWN = {{
    {9,10,12,16,18,19},{0,3,8,10,11,13},{4,6,14,16,19,20},
    {0,4,5,7,12,21},{5,6,10,13,15,20},{5,8,12,14,15,22},
    {3,4,11,12,15,17},{0,2,3,6,11,14},{0,1,9,15,18,22},
    {2,7,15,16,19,21},{6,13,16,17,19,22},{1,7,10,14,17,21},
    {0,8,16,17,19,20},{1,2,4,8,10,22},{4,9,13,18,20,21},
    {2,3,5,9,17,18},{1,2,6,12,13,20},{7,9,11,13,14,18},
    {6,7,8,9,18,21},{3,7,11,20,21,22},{1,3,5,11,16,19}
}};

struct State {
  std::array<Block, NB> blocks{};
  std::array<std::array<int, V>, V> count{};
  int uncovered = 0;
  int concentration = 0;
};

void recount(State& s) {
  for (auto& row : s.count) row.fill(0);
  for (const auto& block : s.blocks)
    for (int i=0;i<6;i++) for (int j=i+1;j<6;j++) {
      int a=block[i], b=block[j]; if(a>b) std::swap(a,b); s.count[a][b]++;
    }
  s.uncovered=0; s.concentration=0;
  for(int a=0;a<V;a++) for(int b=a+1;b<V;b++) {
    s.uncovered += s.count[a][b]==0;
    int excess=std::max(0,s.count[a][b]-2);
    s.concentration += excess*excess;
  }
}

int worker(int id, int seconds, unsigned long long seed_offset,
           std::atomic<bool>& done, std::mutex& output) {
  std::mt19937_64 rng(0x9e3779b97f4a7c15ULL * (id+1) + seed_offset);
  auto deadline=std::chrono::steady_clock::now()+std::chrono::seconds(seconds);
  int best_global=253;
  while(!done && std::chrono::steady_clock::now()<deadline) {
    State s;
    int dropped=rng()%21;
    for(int i=0,j=0;i<21;i++) if(i!=dropped) s.blocks[j++]=KNOWN[i];
    // Diversify the published seed slightly between restarts.
    for(int z=0;z<20;z++) {
      int b=rng()%NB, p=rng()%6, value=rng()%V;
      bool present=std::find(s.blocks[b].begin(),s.blocks[b].end(),value)!=s.blocks[b].end();
      if(!present) s.blocks[b][p]=value;
    }
    recount(s);
    int stagnation=0;
    for(int step=0; step<200000 && !done; step++) {
      if(s.uncovered==0) {
        done=true;
        std::lock_guard<std::mutex> lock(output);
        std::cout << "VERIFIED_CANDIDATE\n";
        for(auto block:s.blocks) { std::sort(block.begin(),block.end()); for(int x:block) std::cout<<x+1<<' '; std::cout<<'\n'; }
        return 0;
      }
      if(s.uncovered<best_global) {
        best_global=s.uncovered; stagnation=0;
        std::lock_guard<std::mutex> lock(output);
        std::cerr << "worker "<<id<<" best "<<best_global<<"\n";
        if(best_global<=2) {
          std::cerr << "NEAR_COVER " << best_global << "\n";
          for(auto block:s.blocks) { std::sort(block.begin(),block.end()); for(int x:block) std::cerr<<x+1<<' '; std::cerr<<'\n'; }
        }
      } else stagnation++;

      // A missing-pair-directed move cannot alter an unrelated block.  Add
      // occasional unrestricted one-point swaps after a stall so the walk
      // can leave concentrated-repeat basins.
      if(stagnation>200 && rng()%7==0) {
        int b=rng()%NB, p=rng()%6, value=rng()%V;
        auto& block=s.blocks[b];
        if(std::find(block.begin(),block.end(),value)==block.end()) {
          State t=s; t.blocks[b][p]=value; recount(t);
          int old_score=1000000*s.uncovered+s.concentration;
          int new_score=1000000*t.uncovered+t.concentration;
          if(new_score<=old_score || rng()%100<15) s=t;
        }
        continue;
      }

      std::vector<std::pair<int,int>> missing;
      for(int a=0;a<V;a++) for(int b=a+1;b<V;b++) if(!s.count[a][b]) missing.push_back({a,b});
      auto [u,v]=missing[rng()%missing.size()];
      struct Move { int block, p1, p2, value1, value2, score; };
      std::vector<Move> moves;
      int best=1000000000;
      for(int b=0;b<NB;b++) {
        auto &block=s.blocks[b];
        bool hu=std::find(block.begin(),block.end(),u)!=block.end();
        bool hv=std::find(block.begin(),block.end(),v)!=block.end();
        if(hu&&hv) continue;
        if(hu||hv) {
          int add=hu?v:u;
          for(int p=0;p<6;p++) if(block[p]!=u && block[p]!=v) {
            State t=s; t.blocks[b][p]=add; recount(t);
            int noise=(int)(rng()%3==0); int score=1000000*t.uncovered+t.concentration+noise;
            if(score<best){best=score;moves.clear();}
            if(score==best)moves.push_back({b,p,-1,add,-1,t.uncovered});
          }
        } else {
          for(int p=0;p<6;p++) for(int q=p+1;q<6;q++) {
            State t=s; t.blocks[b][p]=u; t.blocks[b][q]=v; recount(t);
            int noise=(int)(rng()%3==0); int score=1000000*t.uncovered+t.concentration+noise;
            if(score<best){best=score;moves.clear();}
            if(score==best)moves.push_back({b,p,q,u,v,t.uncovered});
          }
        }
      }
      if(moves.empty()) break;
      Move m=moves[rng()%moves.size()];
      // Allow occasional uphill moves and force diversification after stalls.
      int current_score=1000000*s.uncovered+s.concentration;
      bool accept=m.score<=current_score || (rng()%1000 < (stagnation>1000?80:4));
      if(accept) {
        s.blocks[m.block][m.p1]=m.value1;
        if(m.p2>=0)s.blocks[m.block][m.p2]=m.value2;
        recount(s);
      }
      if(stagnation>10000) break;
    }
  }
  return best_global;
}

int main(int argc,char**argv){
  int seconds=argc>1?std::stoi(argv[1]):300;
  int threads=argc>2?std::stoi(argv[2]):2;
  unsigned long long seed_offset=argc>3?std::stoull(argv[3]):0;
  std::atomic<bool> done=false; std::mutex output;
  std::vector<std::thread> pool;
  for(int i=0;i<threads;i++) pool.emplace_back(worker,i,seconds,seed_offset,std::ref(done),std::ref(output));
  for(auto& t:pool)t.join();
  return done?0:1;
}
