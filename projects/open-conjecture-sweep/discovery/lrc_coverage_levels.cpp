#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <thread>
#include <unordered_set>
#include <vector>

namespace {

constexpr int MAX_K = 16;
constexpr int MAX_WORDS = 2;

struct State {
  std::array<std::uint8_t, MAX_K> value{};
  bool operator==(State const&) const = default;
  bool operator<(State const& other) const { return value < other.value; }
};

struct StateHash {
  std::size_t operator()(State const& state) const noexcept {
    std::uint64_t hash = 1469598103934665603ULL;
    for (std::uint8_t value : state.value) {
      hash ^= value;
      hash *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(hash);
  }
};

using Mask = std::array<std::uint64_t, MAX_WORDS>;

bool is_prime(int value) {
  if (value < 2) return false;
  for (int d = 2; static_cast<long long>(d) * d <= value; ++d) {
    if (value % d == 0) return false;
  }
  return true;
}

int power_mod(int base, int exponent, int modulus) {
  long long result = 1;
  long long factor = base;
  while (exponent > 0) {
    if (exponent & 1) result = result * factor % modulus;
    factor = factor * factor % modulus;
    exponent >>= 1;
  }
  return static_cast<int>(result);
}

std::vector<int> prime_factors(int value) {
  std::vector<int> factors;
  for (int d = 2; d * d <= value; ++d) {
    if (value % d != 0) continue;
    factors.push_back(d);
    while (value % d == 0) value /= d;
  }
  if (value > 1) factors.push_back(value);
  return factors;
}

int least_primitive_root(int prime) {
  auto factors = prime_factors(prime - 1);
  for (int candidate = 2; candidate < prime; ++candidate) {
    bool primitive = true;
    for (int factor : factors) {
      if (power_mod(candidate, (prime - 1) / factor, prime) == 1) {
        primitive = false;
        break;
      }
    }
    if (primitive) return candidate;
  }
  std::abort();
}

int popcount(Mask const& mask, int words) {
  int result = 0;
  for (int i = 0; i < words; ++i) result += __builtin_popcountll(mask[static_cast<std::size_t>(i)]);
  return result;
}

struct Engine {
  int k;
  int p;
  int h;
  int words;
  int primitive_root;
  Mask full{};
  std::vector<Mask> covers;
  std::vector<std::vector<int>> covering_centers;
  std::vector<int> exponent_to_speed;

  Engine(int dimension, int prime)
      : k(dimension), p(prime), h((prime - 1) / 2), words((h + 63) / 64),
        primitive_root(least_primitive_root(prime)), covers(static_cast<std::size_t>(h)),
        covering_centers(static_cast<std::size_t>(h)), exponent_to_speed(static_cast<std::size_t>(h)) {
    for (int word = 0; word < words; ++word) full[static_cast<std::size_t>(word)] = ~0ULL;
    if (h % 64 != 0) full[static_cast<std::size_t>(words - 1)] = (1ULL << (h % 64)) - 1ULL;
    std::vector<char> bad(static_cast<std::size_t>(h), 0);
    int residue = 1;
    for (int exponent = 0; exponent < h; ++exponent) {
      int signed_residue = std::min(residue, p - residue);
      exponent_to_speed[static_cast<std::size_t>(exponent)] = signed_residue;
      bad[static_cast<std::size_t>(exponent)] = static_cast<char>((k + 1) * signed_residue < p);
      residue = static_cast<int>(static_cast<long long>(residue) * primitive_root % p);
    }
    for (int center = 0; center < h; ++center) {
      for (int time = 0; time < h; ++time) {
        if (!bad[static_cast<std::size_t>((center + time) % h)]) continue;
        covers[static_cast<std::size_t>(center)][static_cast<std::size_t>(time / 64)] |=
            1ULL << (time % 64);
        covering_centers[static_cast<std::size_t>(time)].push_back(center);
      }
    }
  }

  State canonical(State const& input, int size) const {
    if (size == 0) return {};
    State best;
    bool have_best = false;
    int previous = -1;
    for (int index = 0; index < size; ++index) {
      int pivot = input.value[static_cast<std::size_t>(index)];
      if (pivot == previous) continue;
      previous = pivot;
      State candidate;
      for (int j = 0; j < size; ++j) {
        int value = input.value[static_cast<std::size_t>(j)];
        candidate.value[static_cast<std::size_t>(j)] =
            static_cast<std::uint8_t>(value >= pivot ? value - pivot : value + h - pivot);
      }
      std::sort(candidate.value.begin(), candidate.value.begin() + size);
      if (!have_best || candidate < best) {
        best = candidate;
        have_best = true;
      }
    }
    return best;
  }

  State add(State const& state, int size, int center) const {
    State raw = state;
    auto begin = raw.value.begin();
    auto position = std::upper_bound(begin, begin + size, static_cast<std::uint8_t>(center));
    std::move_backward(position, begin + size, begin + size + 1);
    *position = static_cast<std::uint8_t>(center);
    return canonical(raw, size + 1);
  }

  Mask covered_by(State const& state, int size) const {
    Mask covered{};
    for (int i = 0; i < size; ++i) {
      Mask const& cover = covers[state.value[static_cast<std::size_t>(i)]];
      for (int word = 0; word < words; ++word) covered[static_cast<std::size_t>(word)] |= cover[static_cast<std::size_t>(word)];
    }
    return covered;
  }

  bool cannot_complete(Mask const& covered, int size) const {
    int remaining = k - size;
    int uncovered = h - popcount(covered, words);
    int best = 0;
    for (Mask const& cover : covers) {
      int extra = 0;
      for (int word = 0; word < words; ++word) {
        extra += __builtin_popcountll(cover[static_cast<std::size_t>(word)] &
                                     ~covered[static_cast<std::size_t>(word)]);
      }
      best = std::max(best, extra);
    }
    return uncovered > remaining * best;
  }

  int first_uncovered(Mask const& covered) const {
    for (int time = 0; time < h; ++time) {
      if ((covered[static_cast<std::size_t>(time / 64)] & (1ULL << (time % 64))) == 0) return time;
    }
    return -1;
  }

  State residue_representative(State const& exponents) const {
    State values;
    for (int i = 0; i < k; ++i) values.value[static_cast<std::size_t>(i)] =
        static_cast<std::uint8_t>(exponent_to_speed[exponents.value[static_cast<std::size_t>(i)]]);
    State best;
    bool have_best = false;
    for (int i = 0; i < k; ++i) {
      int pivot = values.value[static_cast<std::size_t>(i)];
      int inverse = power_mod(pivot, p - 2, p);
      State candidate;
      for (int j = 0; j < k; ++j) {
        int normalized = static_cast<int>(static_cast<long long>(values.value[static_cast<std::size_t>(j)]) * inverse % p);
        candidate.value[static_cast<std::size_t>(j)] = static_cast<std::uint8_t>(std::min(normalized, p - normalized));
      }
      std::sort(candidate.value.begin(), candidate.value.begin() + k);
      if (!have_best || candidate < best) {
        best = candidate;
        have_best = true;
      }
    }
    return best;
  }
};

}  // namespace

int main(int argc, char** argv) {
  int k = 0;
  int p = 0;
  int threads = 3;
  int max_seconds = 300;
  std::uint64_t state_cap = std::numeric_limits<std::uint64_t>::max();
  std::uint64_t edge_cap = std::numeric_limits<std::uint64_t>::max();
  std::uint64_t leaf_cap = std::numeric_limits<std::uint64_t>::max();
  std::string output_path;
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    auto value = [&]() {
      if (++i >= argc) std::exit(2);
      return std::string(argv[i]);
    };
    if (arg == "--k") k = std::stoi(value());
    else if (arg == "--p") p = std::stoi(value());
    else if (arg == "--threads") threads = std::stoi(value());
    else if (arg == "--max-seconds") max_seconds = std::stoi(value());
    else if (arg == "--state-cap") state_cap = std::stoull(value());
    else if (arg == "--edge-cap") edge_cap = std::stoull(value());
    else if (arg == "--leaf-cap") leaf_cap = std::stoull(value());
    else if (arg == "--output") output_path = value();
    else {
      std::cerr << "unknown argument: " << arg << '\n';
      return 2;
    }
  }
  if (k < 2 || k > MAX_K || !is_prime(p) || (p - 1) / 2 > 127 || threads < 1 ||
      max_seconds < 1 || state_cap < 1 || edge_cap < 1 || leaf_cap < 1) {
    std::cerr << "invalid arguments\n";
    return 2;
  }

  auto start = std::chrono::steady_clock::now();
  auto deadline = start + std::chrono::seconds(max_seconds);
  Engine engine(k, p);
  std::vector<State> current(1);
  std::unordered_set<State, StateHash> solutions;
  std::atomic<std::uint64_t> expanded(0);
  std::atomic<std::uint64_t> edges(0);
  std::atomic<std::uint64_t> leaves(0);
  std::atomic<bool> stopped(false);
  std::atomic<int> stop_code(0);
  auto request_stop = [&](int code) {
    int expected = 0;
    stop_code.compare_exchange_strong(expected, code, std::memory_order_relaxed);
    stopped.store(true, std::memory_order_relaxed);
  };
  int completed_depth = -1;

  for (int depth = 0; depth <= k && !stopped.load(std::memory_order_relaxed); ++depth) {
    std::sort(current.begin(), current.end());
    std::atomic<std::size_t> next_index(0);
    std::vector<std::vector<State>> local_next(static_cast<std::size_t>(threads));
    std::vector<std::unordered_set<State, StateHash>> local_solutions(static_cast<std::size_t>(threads));
    std::size_t max_children = static_cast<std::size_t>(engine.h);
    if (depth < k) {
      max_children = 0;
      for (auto const& centers : engine.covering_centers) max_children = std::max(max_children, centers.size());
    }
    std::size_t reserve_each = current.size() * max_children / static_cast<std::size_t>(threads) + max_children;
    reserve_each = std::min<std::size_t>(reserve_each, 4'000'000U);
    for (auto& next : local_next) next.reserve(reserve_each);
    std::vector<std::thread> workers;
    for (int worker = 0; worker < threads; ++worker) {
      workers.emplace_back([&, worker]() {
        auto& next = local_next[static_cast<std::size_t>(worker)];
        auto& found = local_solutions[static_cast<std::size_t>(worker)];
        while (!stopped.load(std::memory_order_relaxed)) {
          std::size_t index = next_index.fetch_add(1, std::memory_order_relaxed);
          if (index >= current.size()) break;
          std::uint64_t seen = expanded.fetch_add(1, std::memory_order_relaxed) + 1;
          if (seen > state_cap) {
            request_stop(1);
            break;
          }
          if ((seen & ((1ULL << 18U) - 1ULL)) == 0 && std::chrono::steady_clock::now() >= deadline) {
            request_stop(2);
            break;
          }
          State const& state = current[index];
          Mask covered = engine.covered_by(state, depth);
          if (depth == k) {
            std::uint64_t leaf = leaves.fetch_add(1, std::memory_order_relaxed) + 1;
            if (leaf > leaf_cap) {
              request_stop(3);
              break;
            }
            if (covered == engine.full) found.insert(engine.residue_representative(state));
            continue;
          }
          if (engine.cannot_complete(covered, depth)) continue;
          int uncovered = engine.first_uncovered(covered);
          auto emit = [&](int center) {
            std::uint64_t generated = edges.fetch_add(1, std::memory_order_relaxed) + 1;
            if (generated > edge_cap) {
              request_stop(4);
              return;
            }
            next.push_back(engine.add(state, depth, center));
          };
          if (uncovered < 0) {
            for (int center = 0; center < engine.h && !stopped.load(std::memory_order_relaxed); ++center) emit(center);
          } else {
            for (int center : engine.covering_centers[static_cast<std::size_t>(uncovered)]) {
              if (stopped.load(std::memory_order_relaxed)) break;
              emit(center);
            }
          }
        }
      });
    }
    for (auto& worker : workers) worker.join();
    if (stopped.load(std::memory_order_relaxed)) break;
    for (auto& found : local_solutions) solutions.insert(found.begin(), found.end());
    completed_depth = depth;
    std::cerr << "level=" << depth << " states=" << current.size()
              << " expanded=" << expanded.load() << " edges=" << edges.load()
              << " leaves=" << leaves.load() << " solutions=" << solutions.size() << '\n';
    if (depth == k) break;
    std::vector<std::thread> sorters;
    for (int worker = 0; worker < threads; ++worker) {
      sorters.emplace_back([&, worker]() {
        auto& part = local_next[static_cast<std::size_t>(worker)];
        std::sort(part.begin(), part.end());
        part.erase(std::unique(part.begin(), part.end()), part.end());
      });
    }
    for (auto& sorter : sorters) sorter.join();
    std::size_t upper_size = 0;
    for (auto const& part : local_next) upper_size += part.size();
    std::vector<State> merged;
    merged.reserve(upper_size);
    std::vector<std::size_t> position(static_cast<std::size_t>(threads), 0);
    while (true) {
      State const* least = nullptr;
      for (int worker = 0; worker < threads; ++worker) {
        auto const& part = local_next[static_cast<std::size_t>(worker)];
        std::size_t index = position[static_cast<std::size_t>(worker)];
        if (index < part.size() && (least == nullptr || part[index] < *least)) least = &part[index];
      }
      if (least == nullptr) break;
      State value = *least;
      merged.push_back(value);
      for (int worker = 0; worker < threads; ++worker) {
        auto const& part = local_next[static_cast<std::size_t>(worker)];
        auto& index = position[static_cast<std::size_t>(worker)];
        if (index < part.size() && part[index] == value) ++index;
      }
    }
    current = std::move(merged);
  }

  std::vector<State> ordered(solutions.begin(), solutions.end());
  std::sort(ordered.begin(), ordered.end());
  double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  bool complete = !stopped.load(std::memory_order_relaxed) && completed_depth == k;
  std::cout << "status=" << (complete ? "COMPLETE" : "INCOMPLETE") << '\n';
  if (!complete) {
    static constexpr std::array<char const*, 5> reasons = {
        "UNKNOWN", "STATE_CAP", "TIMEOUT", "LEAF_CAP", "EDGE_CAP"};
    int code = stop_code.load(std::memory_order_relaxed);
    std::cout << "stop_reason=" << reasons[static_cast<std::size_t>(code)] << '\n';
  }
  std::cout << "k=" << k << '\n';
  std::cout << "p=" << p << '\n';
  std::cout << "primitive_root=" << engine.primitive_root << '\n';
  std::cout << "threads=" << threads << '\n';
  std::cout << "completed_depth=" << completed_depth << '\n';
  std::cout << "canonical_solutions=" << ordered.size() << '\n';
  std::cout << "expanded_states=" << expanded.load() << '\n';
  std::cout << "generated_edges=" << edges.load() << '\n';
  std::cout << "leaf_states=" << leaves.load() << '\n';
  std::cout << "wall_seconds=" << elapsed << '\n';
  if (complete && !output_path.empty()) {
    std::ofstream output(output_path);
    for (State const& tuple : ordered) {
      for (int i = 0; i < k; ++i) output << (i == 0 ? "" : " ") << static_cast<int>(tuple.value[static_cast<std::size_t>(i)]);
      output << '\n';
    }
  }
  return complete ? 0 : 3;
}
