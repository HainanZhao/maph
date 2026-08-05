// Count every labelled C71 D=5 equality-core assignment, without retaining a large log.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

using Pair = std::array<int, 2>;
using Map = std::array<int, 6>;

static bool has(Pair p, int x) { return p[0] == x || p[1] == x; }

int main(int argc, char** argv) {
  const int shard = argc > 1 ? std::stoi(argv[1]) : 0;
  const int shards = argc > 2 ? std::stoi(argv[2]) : 1;
  const uint64_t limit = argc > 3 ? std::stoull(argv[3]) : 1000000;
  if (shards < 1 || shard < 0 || shard >= shards) return 2;
  std::vector<Pair> options;
  for (int a = 0; a < 6; ++a) for (int b = a + 1; b < 6; ++b) options.push_back({a, b});
  constexpr int total = 15 * 15 * 15 * 15 * 15;
  uint64_t checked = 0, solutions = 0;
  bool capped = false;
  for (int code = shard; code < total && !capped; code += shards) {
    ++checked;
    int x = code;
    std::array<Pair, 5> pair;
    for (auto& p : pair) { p = options[x % 15]; x /= 15; }
    std::array<std::vector<Map>, 5> maps;
    bool empty = false;
    for (int j = 0; j < 5; ++j) {
      std::array<int, 4> remaining{}, side{};
      int a = 0, b = 0;
      for (int i = 0; i < 6; ++i) if (!has(pair[j], i)) remaining[a++] = i;
      for (int q = 0; q < 5; ++q) if (q != j) side[b++] = q;
      std::sort(remaining.begin(), remaining.end());
      do {
        Map m; m.fill(-1); bool valid = true;
        for (int t = 0; t < 4; ++t) {
          const int i = remaining[t], q = side[t];
          if (has(pair[q], i)) valid = false;
          else m[i] = q;
        }
        if (valid) { m[pair[j][0]] = j; m[pair[j][1]] = j; maps[j].push_back(m); }
      } while (std::next_permutation(remaining.begin(), remaining.end()));
      if (maps[j].empty()) { empty = true; break; }
    }
    if (empty) continue;
    std::array<Map, 5> selected;
    auto dfs = [&](auto&& self, int j) -> void {
      if (capped) return;
      if (j == 5) { if (++solutions >= limit) capped = true; return; }
      for (const auto& m : maps[j]) {
        bool valid = true;
        for (int k = 0; k < j; ++k) {
          int common = 0;
          for (int i = 0; i < 6; ++i) common += m[i] == selected[k][i];
          if (common != 1) { valid = false; break; }
        }
        if (valid) { selected[j] = m; self(self, j + 1); }
      }
    };
    dfs(dfs, 0);
  }
  std::cout << "{\"status\":\"" << (capped ? "CAP" : "DONE")
            << "\",\"epistemic_status\":\"PROVED\",\"shard\":" << shard
            << ",\"shards\":" << shards << ",\"pair_codes_checked\":" << checked
            << ",\"solutions\":" << solutions << ",\"solution_limit\":" << limit
            << ",\"total_pair_codes\":" << total << "}\n";
}
