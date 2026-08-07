#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <unordered_set>
#include <vector>

using Block = std::array<int, 6>;
constexpr int V = 23, NB = 20, NP = 253;

static const std::array<Block, NB> START = {{
    {3,12,13,17,21,22}, {5,6,8,11,16,21}, {4,5,13,14,16,19},
    {0,1,10,13,14,21}, {0,5,15,16,20,22}, {3,8,10,14,15,17},
    {0,4,11,12,13,15}, {0,3,4,6,7,17}, {1,6,9,15,16,18},
    {2,7,15,16,19,21}, {2,6,10,11,19,22}, {1,5,7,10,12,16},
    {0,1,2,4,8,22}, {4,9,10,18,20,21}, {2,3,5,9,17,18},
    {2,6,12,13,14,20}, {7,9,11,14,18,22}, {0,8,9,12,18,19},
    {7,8,9,13,18,20}, {1,3,11,17,19,20}
}};

int pair_index(int a, int b) {
  if (a > b) std::swap(a, b);
  return a * (2 * V - a - 1) / 2 + (b - a - 1);
}

std::bitset<NP> pair_mask(const Block& block) {
  std::bitset<NP> result;
  for (int i = 0; i < 6; ++i)
    for (int j = i + 1; j < 6; ++j)
      result.set(pair_index(block[i], block[j]));
  return result;
}

std::pair<int, int> pair_endpoints(int index) {
  for (int u = 0; u < V; ++u) for (int v = u + 1; v < V; ++v)
    if (pair_index(u, v) == index) return {u, v};
  std::abort();
}

template <std::size_t K> struct GroupKey {
  std::array<std::uint32_t, K> values{};
  bool operator==(const GroupKey&) const = default;
};

template <std::size_t K> struct GroupKeyHash {
  std::size_t operator()(const GroupKey<K>& key) const {
    std::size_t hash = 0xcbf29ce484222325ULL;
    for (auto value : key.values)
      hash = (hash ^ value) * 0x100000001b3ULL;
    return hash;
  }
};

template <std::size_t K>
bool cover_with_groups(const std::vector<std::pair<int, int>>& edges,
                       std::array<std::bitset<V>, K>& groups,
                       std::unordered_set<GroupKey<K>, GroupKeyHash<K>>& failed) {
  GroupKey<K> key;
  for (std::size_t i = 0; i < K; ++i)
    key.values[i] = static_cast<std::uint32_t>(groups[i].to_ulong());
  std::sort(key.values.begin(), key.values.end());
  if (!failed.insert(key).second) return false;

  int chosen = -1;
  int fewest = static_cast<int>(K) + 1;
  for (int e = 0; e < static_cast<int>(edges.size()); ++e) {
    auto [u, v] = edges[e];
    bool covered = false;
    int feasible = 0;
    for (const auto& group : groups) {
      if (group.test(u) && group.test(v)) { covered = true; break; }
      auto expanded = group;
      expanded.set(u); expanded.set(v);
      feasible += expanded.count() <= 6;
    }
    if (covered) continue;
    if (feasible == 0) return false;
    if (feasible < fewest) { fewest = feasible; chosen = e; }
  }
  if (chosen < 0) return true;

  auto [u, v] = edges[chosen];
  std::array<int, K> order{};
  for (std::size_t i = 0; i < K; ++i) order[i] = static_cast<int>(i);
  std::sort(order.begin(), order.end(), [&](int left, int right) {
    auto l = groups[left]; l.set(u); l.set(v);
    auto r = groups[right]; r.set(u); r.set(v);
    return l.count() < r.count();
  });
  std::array<unsigned long, K> tried{};
  int tried_count = 0;
  for (int which : order) {
    unsigned long signature = groups[which].to_ulong();
    if (std::find(tried.begin(), tried.begin() + tried_count, signature)
        != tried.begin() + tried_count) continue;
    tried[tried_count++] = signature;
    auto prior = groups[which];
    groups[which].set(u); groups[which].set(v);
    if (groups[which].count() <= 6 && cover_with_groups(edges, groups, failed)) return true;
    groups[which] = prior;
  }
  return false;
}

Block fill_block(std::bitset<V> vertices) {
  Block block{};
  int used = 0;
  for (int v = 0; v < V; ++v) if (vertices.test(v)) block[used++] = v;
  for (int v = 0; used < 6 && v < V; ++v)
    if (!vertices.test(v)) block[used++] = v;
  return block;
}

void order_edges(std::vector<std::pair<int, int>>& edges) {
  std::array<int, V> degree{};
  for (auto [u, v] : edges) { ++degree[u]; ++degree[v]; }
  std::sort(edges.begin(), edges.end(), [&](auto left, auto right) {
    return degree[left.first] + degree[left.second]
         > degree[right.first] + degree[right.second];
  });
}

void print_answer(std::array<Block, NB> answer) {
  std::cout << "VERIFIED_20_BLOCK_COVER\n";
  for (auto block : answer) {
    std::sort(block.begin(), block.end());
    for (int v : block) std::cout << v + 1 << ' ';
    std::cout << '\n';
  }
}

void generate_blocks(int next, int used, Block& block,
                     std::vector<Block>& blocks,
                     std::vector<std::bitset<NP>>& masks) {
  if (used == 6) {
    blocks.push_back(block);
    masks.push_back(pair_mask(block));
    return;
  }
  for (int v = next; v <= V - (6 - used); ++v) {
    block[used] = v;
    generate_blocks(v + 1, used + 1, block, blocks, masks);
  }
}

int main() {
  std::array<std::bitset<NP>, NB> start_masks;
  std::array<int, NP> counts{};
  for (int b = 0; b < NB; ++b) {
    start_masks[b] = pair_mask(START[b]);
    for (int p = 0; p < NP; ++p) counts[p] += start_masks[b].test(p);
  }
  int initially_missing = std::count(counts.begin(), counts.end(), 0);
  if (initially_missing != 2) {
    std::cerr << "invalid near cover: " << initially_missing << " missing\n";
    return 2;
  }

  std::vector<Block> candidates;
  std::vector<std::bitset<NP>> candidate_masks;
  Block scratch{};
  generate_blocks(0, 0, scratch, candidates, candidate_masks);

  for (int r1 = 0; r1 < NB; ++r1) for (int r2 = r1 + 1; r2 < NB; ++r2) {
    std::bitset<NP> need;
    for (int p = 0; p < NP; ++p)
      if (counts[p] - start_masks[r1].test(p) - start_masks[r2].test(p) == 0)
        need.set(p);
    for (std::size_t ci = 0; ci < candidates.size(); ++ci) {
      std::bitset<NP> remaining = need & ~candidate_masks[ci];
      std::bitset<V> vertices;
      for (int u = 0; u < V; ++u) for (int v = u + 1; v < V; ++v)
        if (remaining.test(pair_index(u, v))) { vertices.set(u); vertices.set(v); }
      if (vertices.count() > 6) continue;
      Block second = fill_block(vertices);

      auto second_mask = pair_mask(second);
      std::bitset<NP> covered;
      for (int b = 0; b < NB; ++b)
        if (b != r1 && b != r2) covered |= start_masks[b];
      covered |= candidate_masks[ci] | second_mask;
      if (covered.count() != NP) continue;

      auto answer = START;
      answer[r1] = candidates[ci];
      answer[r2] = second;
      print_answer(answer);
      return 0;
    }
  }
  std::cout << "NO_TWO_BLOCK_REPAIR\n";

  for (int r1 = 0; r1 < NB; ++r1)
    for (int r2 = r1 + 1; r2 < NB; ++r2)
      for (int r3 = r2 + 1; r3 < NB; ++r3) {
        std::vector<std::pair<int, int>> edges;
        for (int p = 0; p < NP; ++p)
          if (counts[p] - start_masks[r1].test(p) - start_masks[r2].test(p)
                        - start_masks[r3].test(p) == 0)
            edges.push_back(pair_endpoints(p));
        order_edges(edges);
        std::array<std::bitset<V>, 3> groups{};
        std::unordered_set<GroupKey<3>, GroupKeyHash<3>> failed;
        if (!cover_with_groups(edges, groups, failed)) continue;
        auto answer = START;
        answer[r1] = fill_block(groups[0]);
        answer[r2] = fill_block(groups[1]);
        answer[r3] = fill_block(groups[2]);
        std::bitset<NP> covered;
        for (const auto& block : answer) covered |= pair_mask(block);
        if (covered.count() != NP) {
          std::cerr << "internal three-block verification failure\n";
          return 3;
        }
        print_answer(answer);
        return 0;
      }
  std::cout << "NO_THREE_BLOCK_REPAIR\n";

  for (int r1 = 0; r1 < NB; ++r1)
    for (int r2 = r1 + 1; r2 < NB; ++r2)
      for (int r3 = r2 + 1; r3 < NB; ++r3)
        for (int r4 = r3 + 1; r4 < NB; ++r4) {
          std::vector<std::pair<int, int>> edges;
          for (int p = 0; p < NP; ++p)
            if (counts[p] - start_masks[r1].test(p) - start_masks[r2].test(p)
                          - start_masks[r3].test(p) - start_masks[r4].test(p) == 0)
              edges.push_back(pair_endpoints(p));
          order_edges(edges);
          std::array<std::bitset<V>, 4> groups{};
          std::unordered_set<GroupKey<4>, GroupKeyHash<4>> failed;
          if (!cover_with_groups(edges, groups, failed)) continue;
          auto answer = START;
          answer[r1] = fill_block(groups[0]);
          answer[r2] = fill_block(groups[1]);
          answer[r3] = fill_block(groups[2]);
          answer[r4] = fill_block(groups[3]);
          std::bitset<NP> covered;
          for (const auto& block : answer) covered |= pair_mask(block);
          if (covered.count() != NP) {
            std::cerr << "internal four-block verification failure\n";
            return 4;
          }
          print_answer(answer);
          return 0;
        }
  std::cout << "NO_FOUR_BLOCK_REPAIR\n";
  return 1;
}
