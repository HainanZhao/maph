// Independent replay of the generalized C72 equality-core blocker search.
//
// Independence from cycle72_bad_core_search.cpp is structural: a core is a
// list of 11-bit vertex-incidence signatures in each part (not 64-bit edge
// sets), compatible extension traces are exact signature partitions, and the
// blocker test is memo-free iterative-deepening branch-and-bound.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <set>
#include <string>
#include <string_view>
#include <vector>

using Pair = std::array<uint8_t, 2>;
using Map = std::array<uint8_t, 6>;
using RGS = std::array<uint8_t, 5>;
using Trace = std::array<uint16_t, 6>;
constexpr uint16_t ALL_LINES = (uint16_t{1} << 11) - 1;

struct SideDomain {
  std::string_view name;
  RGS representative;
};

// These are the three possible multiplicity shapes.  If three repeated
// vertices occupied one noncentral part, their required disjoint star pairs
// would cover all six star positions.  A witness based outside that part
// could then make its required contact there only through a two-star repeated
// vertex, contradicting exact one-point contact with every star line.  Four
// or more repeats already cannot have pairwise-disjoint two-subsets of six.
// Thus every multiplicity is <=2; the integer partitions of five satisfying
// that condition are exactly 1+1+1+1+1, 2+1+1+1, and 2+2+1.
constexpr std::array<SideDomain, 3> SIDE_DOMAIN{{
    {"distinct", {0, 1, 2, 3, 4}},
    {"double", {0, 0, 1, 2, 3}},
    {"double-double", {0, 0, 1, 1, 2}},
}};

static void generate_rgs(int at, uint8_t maximum, RGS &x,
                         std::vector<RGS> &out) {
  if (at == 5) {
    out.push_back(x);
    return;
  }
  for (uint8_t value = 0; value <= std::min<uint8_t>(4, maximum + 1);
       ++value) {
    x[at] = value;
    generate_rgs(at + 1, std::max(maximum, value), x, out);
  }
}

static std::array<uint8_t, 5> multiplicity_shape(const RGS &x) {
  std::array<uint8_t, 5> count{};
  for (uint8_t value : x) ++count[value];
  std::sort(count.begin(), count.end(), std::greater<>());
  return count;
}

static bool audit_side_domain(const std::vector<RGS> &all_rgs) {
  if (all_rgs.size() != 52) return false;
  std::set<std::array<uint8_t, 5>> derived;
  for (const RGS &x : all_rgs) {
    auto shape = multiplicity_shape(x);
    if (shape[0] <= 2) derived.insert(shape);
  }
  std::set<std::array<uint8_t, 5>> declared;
  for (const auto &entry : SIDE_DOMAIN) {
    if (entry.representative[0] != 0) return false;
    for (int i = 1; i < 5; ++i) {
      uint8_t prior_max = *std::max_element(entry.representative.begin(),
                                            entry.representative.begin() + i);
      if (entry.representative[i] > prior_max + 1) return false;
    }
    declared.insert(multiplicity_shape(entry.representative));
  }
  return derived == declared && declared.size() == 3;
}

static bool contains(const Pair &p, int value) {
  return p[0] == value || p[1] == value;
}

struct SignatureCore {
  // A nonzero signature is the set of core lines incident with one vertex.
  // Part identity plus signature uniquely identifies every core vertex here.
  std::array<std::vector<uint16_t>, 6> part;
};

static SignatureCore build_signature_core(
    const RGS &side, const RGS &central, const std::array<Pair, 5> &pairs,
    const std::array<Map, 5> &maps) {
  SignatureCore core;

  uint16_t v = 0;
  for (int i = 0; i < 6; ++i) v |= uint16_t{1} << i;
  core.part[0].push_back(v);
  for (int block = 0; block < 5; ++block) {
    uint16_t signature = 0;
    for (int j = 0; j < 5; ++j)
      if (central[j] == block) signature |= uint16_t{1} << (6 + j);
    if (signature) core.part[0].push_back(signature);
  }

  for (int q = 0; q < 5; ++q) {
    std::array<int8_t, 6> repeated;
    repeated.fill(-1);
    for (int j = 0; j < 5; ++j) {
      if (side[j] != q) continue;
      for (uint8_t i : pairs[j]) {
        if (repeated[i] != -1) std::abort();
        repeated[i] = static_cast<int8_t>(j);
      }
    }
    std::array<bool, 5> emitted{};
    for (int i = 0; i < 6; ++i) {
      if (repeated[i] >= 0) {
        int j = repeated[i];
        if (emitted[j]) continue;
        emitted[j] = true;
        uint16_t signature = (uint16_t{1} << pairs[j][0]) |
                             (uint16_t{1} << pairs[j][1]) |
                             (uint16_t{1} << (6 + j));
        core.part[q + 1].push_back(signature);
      } else {
        uint16_t signature = uint16_t{1} << i;
        for (int j = 0; j < 5; ++j)
          if (maps[j][i] == q) signature |= uint16_t{1} << (6 + j);
        core.part[q + 1].push_back(signature);
      }
    }
  }
  for (auto &vertices : core.part) {
    std::sort(vertices.begin(), vertices.end());
    if (std::adjacent_find(vertices.begin(), vertices.end()) != vertices.end())
      std::abort();
  }
  return core;
}

static std::vector<Trace> exact_signature_traces(const SignatureCore &core) {
  std::vector<Trace> traces;
  Trace selected{};
  auto visit = [&](auto &&self, int part, uint16_t covered) -> void {
    if (part == 6) {
      if (covered == ALL_LINES) traces.push_back(selected);
      return;
    }
    // Signature zero means that this part contributes a fresh vertex.
    selected[part] = 0;
    self(self, part + 1, covered);
    for (uint16_t signature : core.part[part]) {
      if (covered & signature) continue;
      selected[part] = signature;
      self(self, part + 1, covered | signature);
    }
  };
  visit(visit, 0, 0);
  std::sort(traces.begin(), traces.end());
  if (std::adjacent_find(traces.begin(), traces.end()) != traces.end())
    std::abort();
  return traces;
}

struct BlockerInstance {
  std::vector<uint64_t> vertex_coverage;
  std::vector<std::vector<int>> member_vertices;
  uint64_t full = 0;
};

static BlockerInstance make_blocker_instance(const SignatureCore &core,
                                             const std::vector<Trace> &traces) {
  BlockerInstance instance;
  std::array<std::vector<int>, 6> vertex_id;
  for (int q = 0; q < 6; ++q) {
    for (size_t z = 0; z < core.part[q].size(); ++z) {
      vertex_id[q].push_back(static_cast<int>(instance.vertex_coverage.size()));
      instance.vertex_coverage.push_back(0);
    }
  }
  const size_t members = 11 + traces.size();
  if (members > 63) std::abort();
  instance.member_vertices.resize(members);
  instance.full = (uint64_t{1} << members) - 1;

  for (int line = 0; line < 11; ++line) {
    for (int q = 0; q < 6; ++q) {
      for (size_t z = 0; z < core.part[q].size(); ++z) {
        if (core.part[q][z] & (uint16_t{1} << line))
          instance.member_vertices[line].push_back(vertex_id[q][z]);
      }
    }
  }
  for (size_t t = 0; t < traces.size(); ++t) {
    const int member = 11 + static_cast<int>(t);
    for (int q = 0; q < 6; ++q) {
      if (!traces[t][q]) continue;
      auto it = std::lower_bound(core.part[q].begin(), core.part[q].end(),
                                 traces[t][q]);
      if (it == core.part[q].end() || *it != traces[t][q]) std::abort();
      size_t z = static_cast<size_t>(it - core.part[q].begin());
      instance.member_vertices[member].push_back(vertex_id[q][z]);
    }
  }
  for (size_t member = 0; member < members; ++member) {
    if (instance.member_vertices[member].empty()) std::abort();
    for (int vertex : instance.member_vertices[member])
      instance.vertex_coverage[vertex] |= uint64_t{1} << member;
  }
  return instance;
}

// Exact memo-free IDDFS.  The lower bound uses the maximum number of still
// uncovered family members coverable by one vertex; branching uses the
// uncovered family member with the fewest non-dominated candidate vertices.
static bool blocker_dfs(const BlockerInstance &x, uint64_t covered,
                        int remaining) {
  if (covered == x.full) return true;
  if (remaining == 0) return false;
  uint64_t uncovered = x.full & ~covered;
  int maximum_gain = 0;
  for (uint64_t coverage : x.vertex_coverage)
    maximum_gain = std::max(maximum_gain, std::popcount(coverage & uncovered));
  if (maximum_gain == 0 ||
      (std::popcount(uncovered) + maximum_gain - 1) / maximum_gain > remaining)
    return false;

  const std::vector<int> *branch = nullptr;
  std::vector<int> reduced;
  size_t best_size = std::numeric_limits<size_t>::max();
  while (uncovered) {
    int member = std::countr_zero(uncovered);
    uncovered &= uncovered - 1;
    const auto &candidates = x.member_vertices[member];
    if (candidates.size() < best_size) {
      branch = &candidates;
      best_size = candidates.size();
    }
  }
  reduced = *branch;
  // For this node, a candidate whose new coverage is contained in another's
  // is never needed.  This is local dominance, not memoization.
  reduced.erase(std::remove_if(reduced.begin(), reduced.end(), [&](int a) {
                  uint64_t ca = x.vertex_coverage[a] & ~covered;
                  for (int b : *branch) {
                    if (a == b) continue;
                    uint64_t cb = x.vertex_coverage[b] & ~covered;
                    if (ca != cb && (ca | cb) == cb) return true;
                    if (ca == cb && b < a) return true;
                  }
                  return false;
                }),
                reduced.end());
  std::sort(reduced.begin(), reduced.end(), [&](int a, int b) {
    return std::popcount(x.vertex_coverage[a] & ~covered) >
           std::popcount(x.vertex_coverage[b] & ~covered);
  });
  for (int vertex : reduced)
    if (blocker_dfs(x, covered | x.vertex_coverage[vertex], remaining - 1))
      return true;
  return false;
}

static bool has_five_blocker(const SignatureCore &core,
                             const std::vector<Trace> &traces) {
  BlockerInstance instance = make_blocker_instance(core, traces);
  for (int depth = 0; depth <= 5; ++depth)
    if (blocker_dfs(instance, 0, depth)) return true;
  return false;
}

static uint64_t fnv_byte(uint64_t hash, uint8_t byte) {
  return (hash ^ byte) * UINT64_C(1099511628211);
}

static uint64_t hash_core(const RGS &side, const RGS &central,
                          const std::array<Pair, 5> &pairs,
                          const std::array<Map, 5> &maps,
                          const std::vector<Trace> &traces) {
  uint64_t hash = UINT64_C(14695981039346656037);
  for (uint8_t x : side) hash = fnv_byte(hash, x);
  for (uint8_t x : central) hash = fnv_byte(hash, x);
  for (const Pair &pair : pairs)
    for (uint8_t x : pair) hash = fnv_byte(hash, x);
  for (const Map &map : maps)
    for (uint8_t x : map) hash = fnv_byte(hash, x);
  const uint16_t count = static_cast<uint16_t>(traces.size());
  hash = fnv_byte(hash, count & 0xff);
  hash = fnv_byte(hash, count >> 8);
  for (const Trace &trace : traces) {
    for (uint16_t signature : trace) {
      hash = fnv_byte(hash, signature & 0xff);
      hash = fnv_byte(hash, signature >> 8);
    }
  }
  return hash;
}

static uint64_t strong_mix(uint64_t x) {
  // SplitMix64 finalizer.
  x ^= x >> 30;
  x *= UINT64_C(0xbf58476d1ce4e5b9);
  x ^= x >> 27;
  x *= UINT64_C(0x94d049bb133111eb);
  return x ^ (x >> 31);
}

static void print_rgs(const RGS &x) {
  std::cout << '[';
  for (int i = 0; i < 5; ++i) {
    if (i) std::cout << ',';
    std::cout << int(x[i]);
  }
  std::cout << ']';
}

static void print_assignment(const RGS &side, const RGS &central,
                             const std::array<Pair, 5> &pairs,
                             const std::array<Map, 5> &maps,
                             size_t trace_count) {
  std::cout << "{\"sides\":";
  print_rgs(side);
  std::cout << ",\"central\":";
  print_rgs(central);
  std::cout << ",\"pairs\":[";
  for (int j = 0; j < 5; ++j) {
    if (j) std::cout << ',';
    std::cout << '[' << int(pairs[j][0]) << ',' << int(pairs[j][1]) << ']';
  }
  std::cout << "],\"maps\":[";
  for (int j = 0; j < 5; ++j) {
    if (j) std::cout << ',';
    std::cout << '[';
    for (int i = 0; i < 6; ++i) {
      if (i) std::cout << ',';
      std::cout << int(maps[j][i]);
    }
    std::cout << ']';
  }
  std::cout << "],\"extension_traces\":" << trace_count << '}';
}

static std::vector<Map> map_options(const RGS &side,
                                    const std::array<Pair, 5> &pairs, int j) {
  std::vector<Map> out;
  Map map;
  map.fill(255);
  map[pairs[j][0]] = side[j];
  map[pairs[j][1]] = side[j];
  std::array<uint8_t, 4> other_parts{};
  int count = 0;
  for (uint8_t q = 0; q < 5; ++q)
    if (q != side[j]) other_parts[count++] = q;

  auto assign = [&](auto &&self, int at, uint8_t used) -> void {
    if (at == 4) {
      out.push_back(map);
      return;
    }
    uint8_t q = other_parts[at];
    for (uint8_t i = 0; i < 6; ++i) {
      if (used & (uint8_t{1} << i)) continue;
      bool occupied_by_repeat = false;
      for (int ell = 0; ell < 5; ++ell)
        if (side[ell] == q && contains(pairs[ell], i))
          occupied_by_repeat = true;
      if (occupied_by_repeat) continue;
      map[i] = q;
      self(self, at + 1, used | (uint8_t{1} << i));
      map[i] = 255;
    }
  };
  uint8_t used = (uint8_t{1} << pairs[j][0]) | (uint8_t{1} << pairs[j][1]);
  assign(assign, 0, used);
  return out;
}

struct RunState {
  uint64_t assignment_cap = 0;
  uint64_t realized = 0;
  uint64_t cases = 0;
  uint64_t hash_sum = 0;
  uint64_t hash_xor = 0;
  size_t max_traces = 0;
  bool bad = false;
  bool capped = false;
  RGS bad_central{};
  std::array<Pair, 5> bad_pairs{};
  std::array<Map, 5> bad_maps{};
  size_t bad_traces = 0;
};

int main(int argc, char **argv) {
  if (argc < 2 || argc > 5) {
    std::cerr << "usage: " << argv[0]
              << " SHAPE [SHARD=0] [SHARDS=1] [ASSIGNMENT_CAP=0]\n";
    return 2;
  }
  const std::string shape_name = argv[1];
  const int shard = argc > 2 ? std::stoi(argv[2]) : 0;
  const int shards = argc > 3 ? std::stoi(argv[3]) : 1;
  const uint64_t assignment_cap = argc > 4 ? std::stoull(argv[4]) : 0;
  if (shards < 1 || shard < 0 || shard >= shards) return 2;

  std::vector<RGS> all_rgs;
  RGS seed{};
  generate_rgs(1, 0, seed, all_rgs);
  if (!audit_side_domain(all_rgs)) return 3;
  const SideDomain *domain = nullptr;
  for (const auto &entry : SIDE_DOMAIN)
    if (entry.name == shape_name) domain = &entry;
  if (!domain) return 4;
  const RGS &side = domain->representative;

  std::array<Pair, 15> pair_catalog{};
  int pair_count = 0;
  for (uint8_t a = 0; a < 6; ++a)
    for (uint8_t b = a + 1; b < 6; ++b) pair_catalog[pair_count++] = {a, b};

  constexpr uint64_t PAIR_TUPLES = 15ULL * 15 * 15 * 15 * 15;
  constexpr uint64_t TOTAL_CASES = 52 * PAIR_TUPLES;
  RunState state;
  state.assignment_cap = assignment_cap;
  std::array<Pair, 5> pairs{};
  std::array<Map, 5> selected{};

  for (uint64_t ordinal = shard;
       ordinal < TOTAL_CASES && !state.bad && !state.capped;
       ordinal += shards) {
    ++state.cases;
    const RGS &central = all_rgs[ordinal / PAIR_TUPLES];
    uint64_t code = ordinal % PAIR_TUPLES;
    for (Pair &pair : pairs) {
      pair = pair_catalog[code % 15];
      code /= 15;
    }
    bool disjoint = true;
    for (int j = 0; j < 5; ++j)
      for (int k = 0; k < j; ++k)
        if (side[j] == side[k] &&
            (contains(pairs[j], pairs[k][0]) ||
             contains(pairs[j], pairs[k][1])))
          disjoint = false;
    if (!disjoint) continue;

    std::array<std::vector<Map>, 5> options;
    bool possible = true;
    for (int j = 0; j < 5; ++j) {
      options[j] = map_options(side, pairs, j);
      if (options[j].empty()) possible = false;
    }
    if (!possible) continue;

    auto enumerate_maps = [&](auto &&self, int j) -> void {
      if (state.bad || state.capped) return;
      if (j < 5) {
        for (const Map &candidate : options[j]) {
          bool compatible = true;
          for (int k = 0; k < j; ++k) {
            int common = 0;
            for (int i = 0; i < 6; ++i)
              common += candidate[i] == selected[k][i];
            const int required = central[j] == central[k] ? 0 : 1;
            if (common != required) {
              compatible = false;
              break;
            }
          }
          if (compatible) {
            selected[j] = candidate;
            self(self, j + 1);
            if (state.bad || state.capped) return;
          }
        }
        return;
      }

      SignatureCore core = build_signature_core(side, central, pairs, selected);
      std::vector<Trace> traces = exact_signature_traces(core);
      state.max_traces = std::max(state.max_traces, traces.size());
      ++state.realized;
      uint64_t mixed = strong_mix(hash_core(side, central, pairs, selected, traces));
      state.hash_sum += mixed;
      state.hash_xor ^= mixed;
      if (!has_five_blocker(core, traces)) {
        state.bad = true;
        state.bad_central = central;
        state.bad_pairs = pairs;
        state.bad_maps = selected;
        state.bad_traces = traces.size();
        return;
      }
      if (state.assignment_cap && state.realized >= state.assignment_cap)
        state.capped = true;
    };
    enumerate_maps(enumerate_maps, 0);
  }

  std::cout << "{\"status\":\""
            << (state.bad ? "BAD_CORE" : state.capped ? "ASSIGNMENT_CAP" : "DONE")
            << "\",\"epistemic_status\":\"PROVED\",\"engine\":"
               "\"signature-partition-iddfs-v1\",\"shape\":\""
            << shape_name << "\",\"side_representative\":";
  print_rgs(side);
  std::cout << ",\"side_domain_check\":\"PASS\",\"shard\":" << shard
            << ",\"shards\":" << shards << ",\"assignment_cap\":"
            << assignment_cap << ",\"total_unsharded_cases\":" << TOTAL_CASES
            << ",\"cases\":" << state.cases
            << ",\"realized_cores\":" << state.realized
            << ",\"max_extension_traces\":" << state.max_traces
            << ",\"hash_spec\":\"FNV1a64 over byte-valued s[5], c[5], "
               "p[5][2], m[5][6], then uint16-LE trace count and "
               "lexicographically sorted traces of six uint16-LE incidence "
               "signatures; aggregate SplitMix64-finalized per-core hashes "
               "by uint64 modular sum and xor\",\"hash_sum\":"
            << state.hash_sum << ",\"hash_xor\":" << state.hash_xor;
  if (state.bad) {
    std::cout << ",\"bad\":";
    print_assignment(side, state.bad_central, state.bad_pairs, state.bad_maps,
                     state.bad_traces);
  }
  std::cout << "}\n";
  return state.bad ? 1 : 0;
}
