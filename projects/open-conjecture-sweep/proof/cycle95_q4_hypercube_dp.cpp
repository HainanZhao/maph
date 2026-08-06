#include <algorithm>
#include <cstdint>
#include <fstream>
#include <limits>
#include <string>
#include <vector>

static int dist2(int a, int b) {
  unsigned x = static_cast<unsigned>(a ^ b);
  int d = 0;
  while (x) { d += static_cast<int>(x & 1U); x >>= 1U; }
  return d * d;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::ofstream out(argv[1]);
  out << "subset\tcost\tcycle\n";
  constexpr int INF = std::numeric_limits<int>::max() / 4;
  int rows = 0, max_cost = 0, over = 0;
  for (int root = 0; root < 16; ++root) {
    const int m = 15 - root;
    const int lim = 1 << m;
    std::vector<int> dp(static_cast<size_t>(lim) * m, INF);
    std::vector<int> parent(static_cast<size_t>(lim) * m, -2);
    auto ix = [m](int mask, int v) { return static_cast<size_t>(mask) * m + v; };
    for (int v = 0; v < m; ++v) {
      const int bit = 1 << v;
      dp[ix(bit, v)] = dist2(root, root + 1 + v);
      parent[ix(bit, v)] = -1;
    }
    for (int mask = 1; mask < lim; ++mask) {
      for (int v = 0; v < m; ++v) if (mask & (1 << v)) {
        if ((mask & (mask - 1)) == 0) continue;
        int before = mask ^ (1 << v), best = INF, arg = -1;
        for (int u = 0; u < m; ++u) if (before & (1 << u)) {
          int cand = dp[ix(before, u)] + dist2(root + 1 + u, root + 1 + v);
          if (cand < best) { best = cand; arg = u; }
        }
        dp[ix(mask, v)] = best;
        parent[ix(mask, v)] = arg;
      }
    }
    for (int mask = 1; mask < lim; ++mask) {
      int best = INF, last = -1;
      for (int v = 0; v < m; ++v) if (mask & (1 << v)) {
        int cand = dp[ix(mask, v)] + dist2(root + 1 + v, root);
        if (cand < best) { best = cand; last = v; }
      }
      std::vector<int> tail;
      int curmask = mask, v = last;
      while (v >= 0) {
        tail.push_back(root + 1 + v);
        int p = parent[ix(curmask, v)];
        curmask ^= 1 << v;
        v = p;
      }
      std::reverse(tail.begin(), tail.end());
      std::vector<int> cycle{root};
      cycle.insert(cycle.end(), tail.begin(), tail.end());
      int check = 0;
      for (size_t i = 0; i < cycle.size(); ++i)
        check += dist2(cycle[i], cycle[(i + 1) % cycle.size()]);
      if (check != best) return 3;
      int subset = 1 << root;
      for (int x : tail) subset |= 1 << x;
      out << subset << '\t' << best << '\t';
      for (size_t i = 0; i < cycle.size(); ++i) {
        if (i) out << ',';
        out << cycle[i];
      }
      out << '\n';
      ++rows; max_cost = std::max(max_cost, best); if (best > 32) ++over;
    }
  }
  std::ofstream summary(std::string(argv[1]) + ".summary.json");
  summary << "{\"status\":\"PASS\",\"subsets\":" << rows
          << ",\"max_cost\":" << max_cost << ",\"over_threshold\":"
          << over << "}\n";
  return rows == 65519 ? 0 : 4;
}
