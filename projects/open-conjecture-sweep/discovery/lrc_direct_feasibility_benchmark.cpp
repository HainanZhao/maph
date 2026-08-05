#define main cycle3_in_memory_main
#include "lrc_coverage_levels.cpp"
#undef main

#include <fstream>
#include <unordered_map>

namespace {

bool empty(Mask const& mask) { return mask == Mask{}; }

Mask minus(Mask mask, Mask const& cover, int words) {
  for (int word = 0; word < words; ++word) mask[static_cast<std::size_t>(word)] &= ~cover[static_cast<std::size_t>(word)];
  return mask;
}

int first(Mask const& mask, int words) {
  for (int word = 0; word < words; ++word) {
    std::uint64_t bits = mask[static_cast<std::size_t>(word)];
    if (bits) return word * 64 + __builtin_ctzll(bits);
  }
  return -1;
}

struct Key {
  Mask mask{};
  std::uint8_t remaining{};
  bool operator==(Key const&) const = default;
};

struct KeyHash {
  std::size_t operator()(Key const& key) const noexcept {
    std::uint64_t hash = key.mask[0] * 0x9e3779b97f4a7c15ULL;
    hash ^= key.mask[1] + 0x517cc1b727220a95ULL + (hash << 6U) + (hash >> 2U);
    hash ^= key.remaining;
    return static_cast<std::size_t>(hash);
  }
};

class DirectSolver {
 public:
  DirectSolver(Engine const& engine, std::uint64_t node_cap)
      : engine_(engine), node_cap_(node_cap) {}

  enum class Result { FEASIBLE, INFEASIBLE, CAP };

  Result solve(Mask uncovered, int remaining) {
    nodes_ = 0;
    return search(uncovered, remaining);
  }

  std::uint64_t nodes() const { return nodes_; }

 private:
  Engine const& engine_;
  std::uint64_t node_cap_;
  std::uint64_t nodes_ = 0;
  std::unordered_map<Key, Result, KeyHash> memo_;

  Result search(Mask uncovered, int remaining) {
    if (empty(uncovered)) return Result::FEASIBLE;
    if (remaining == 0) return Result::INFEASIBLE;
    if (nodes_++ >= node_cap_) return Result::CAP;
    Key key{uncovered, static_cast<std::uint8_t>(remaining)};
    if (auto found = memo_.find(key); found != memo_.end()) return found->second;
    int target = first(uncovered, engine_.words);
    std::vector<std::pair<int, int>> choices;
    for (int center : engine_.covering_centers[static_cast<std::size_t>(target)]) {
      Mask next = minus(uncovered, engine_.covers[static_cast<std::size_t>(center)], engine_.words);
      int gain = popcount(uncovered, engine_.words) - popcount(next, engine_.words);
      choices.emplace_back(-gain, center);
    }
    std::sort(choices.begin(), choices.end());
    bool saw_cap = false;
    for (auto [ignored, center] : choices) {
      (void)ignored;
      Result result = search(minus(uncovered, engine_.covers[static_cast<std::size_t>(center)], engine_.words), remaining - 1);
      if (result == Result::FEASIBLE) {
        memo_.emplace(key, result);
        return result;
      }
      if (result == Result::CAP) saw_cap = true;
    }
    Result result = saw_cap ? Result::CAP : Result::INFEASIBLE;
    memo_.emplace(key, result);
    return result;
  }
};

}  // namespace

int main(int argc, char** argv) try {
  if (argc != 3) {
    std::cerr << "usage: lrc_direct_feasibility_benchmark INPUT OUTPUT\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  std::ofstream output(argv[2]);
  Engine engine(13, 199);
  DirectSolver solver(engine, 1'000'000);
  std::uint64_t rows = 0, feasible = 0, infeasible = 0, capped = 0;
  std::vector<std::uint64_t> nanoseconds;
  State state;
  while (true) {
    state = {};
    for (int index = 0; index < 8; ++index) {
      int value;
      if (!(input >> value)) goto done;
      state.value[static_cast<std::size_t>(index)] = static_cast<std::uint8_t>(value);
    }
    Mask uncovered = engine.full;
    for (int index = 0; index < 8; ++index) {
      uncovered = minus(uncovered, engine.covers[state.value[static_cast<std::size_t>(index)]], engine.words);
    }
    auto start = std::chrono::steady_clock::now();
    auto result = solver.solve(uncovered, 5);
    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - start).count();
    nanoseconds.push_back(static_cast<std::uint64_t>(elapsed));
    char const* label = result == DirectSolver::Result::FEASIBLE ? "FEASIBLE" :
                        result == DirectSolver::Result::INFEASIBLE ? "INFEASIBLE" : "CAP";
    if (result == DirectSolver::Result::FEASIBLE) ++feasible;
    else if (result == DirectSolver::Result::INFEASIBLE) ++infeasible;
    else ++capped;
    output << label << ' ' << popcount(uncovered, engine.words) << ' ' << solver.nodes()
           << ' ' << elapsed << '\n';
    ++rows;
  }
done:
  if (!input.eof()) throw std::runtime_error("malformed input");
  std::sort(nanoseconds.begin(), nanoseconds.end());
  std::uint64_t p99 = nanoseconds.empty() ? 0 : nanoseconds[(nanoseconds.size() * 99 + 99) / 100 - 1];
  output << "summary rows=" << rows << " feasible=" << feasible << " infeasible=" << infeasible
         << " cap=" << capped << " p99_nanoseconds=" << p99 << '\n';
  if (!output) throw std::runtime_error("output failure");
  return capped == 0 ? 0 : 3;
} catch (std::exception const& error) {
  std::cerr << "fatal=" << error.what() << '\n';
  return 4;
}
