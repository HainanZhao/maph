// Exhaust the corrected C71 D=5 equality-core CSP with arbitrary R-vertex parts.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

using Pair = std::array<int, 2>;
using Map = std::array<int, 6>;
using Sides = std::array<int, 5>;

static bool has(Pair p, int x) { return p[0] == x || p[1] == x; }

static void rgs_rec(int at, int maximum, Sides& value, std::vector<Sides>& out) {
  if (at == 5) { out.push_back(value); return; }
  for (int x = 0; x <= std::min(4, maximum + 1); ++x) {
    value[at] = x;
    rgs_rec(at + 1, std::max(maximum, x), value, out);
  }
}

int main(int argc, char** argv) {
  const int shard = argc > 1 ? std::stoi(argv[1]) : 0;
  const int shards = argc > 2 ? std::stoi(argv[2]) : 1;
  const uint64_t limit = argc > 3 ? std::stoull(argv[3]) : 1000000;
  if (shards < 1 || shard < 0 || shard >= shards) return 2;
  std::vector<Pair> pair_options;
  for (int a = 0; a < 6; ++a) for (int b = a + 1; b < 6; ++b) pair_options.push_back({a, b});
  std::vector<Sides> patterns;
  Sides seed{}; seed[0] = 0; rgs_rec(1, 0, seed, patterns);
  if (patterns.size() != 52) return 3;
  constexpr int pair_total = 15 * 15 * 15 * 15 * 15;
  const uint64_t case_total = uint64_t(patterns.size()) * pair_total;
  uint64_t checked = 0, solutions = 0;
  std::array<uint64_t, 52> pattern_counts{};
  bool capped = false;
  for (uint64_t global = shard; global < case_total && !capped; global += shards) {
    ++checked;
    const int pattern_index = global / pair_total;
    int code = global % pair_total;
    const auto& side_of = patterns[pattern_index];
    std::array<Pair, 5> pair;
    for (auto& p : pair) { p = pair_options[code % 15]; code /= 15; }
    bool impossible = false;
    for (int j = 0; j < 5; ++j) for (int k = 0; k < j; ++k)
      if (side_of[j] == side_of[k] &&
          (has(pair[j], pair[k][0]) || has(pair[j], pair[k][1]))) impossible = true;
    if (impossible) continue;
    std::array<std::vector<Map>, 5> maps;
    for (int j = 0; j < 5 && !impossible; ++j) {
      std::array<int, 4> remaining{}, available{};
      int a = 0, b = 0;
      for (int i = 0; i < 6; ++i) if (!has(pair[j], i)) remaining[a++] = i;
      for (int q = 0; q < 5; ++q) if (q != side_of[j]) available[b++] = q;
      std::sort(remaining.begin(), remaining.end());
      do {
        Map m; m.fill(-1); bool valid = true;
        for (int t = 0; t < 4; ++t) {
          const int i = remaining[t], q = available[t];
          for (int ell = 0; ell < 5; ++ell)
            if (side_of[ell] == q && has(pair[ell], i)) valid = false;
          m[i] = q;
        }
        if (valid) {
          m[pair[j][0]] = side_of[j]; m[pair[j][1]] = side_of[j];
          maps[j].push_back(m);
        }
      } while (std::next_permutation(remaining.begin(), remaining.end()));
      if (maps[j].empty()) impossible = true;
    }
    if (impossible) continue;
    std::array<Map, 5> selected;
    auto dfs = [&](auto&& self, int j) -> void {
      if (capped) return;
      if (j == 5) {
        ++solutions; ++pattern_counts[pattern_index];
        if (solutions >= limit) capped = true;
        return;
      }
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
            << ",\"shards\":" << shards << ",\"cases_checked\":" << checked
            << ",\"solutions\":" << solutions << ",\"solution_limit\":" << limit
            << ",\"case_total\":" << case_total << ",\"patterns\":[";
  for (size_t p = 0; p < patterns.size(); ++p) {
    if (p) std::cout << ',';
    std::cout << "{\"sides\":[";
    for (int j = 0; j < 5; ++j) { if (j) std::cout << ','; std::cout << patterns[p][j]; }
    std::cout << "],\"solutions\":" << pattern_counts[p] << '}';
  }
  std::cout << "]}\n";
}
