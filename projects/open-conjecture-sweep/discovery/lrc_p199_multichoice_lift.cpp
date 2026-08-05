#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <atomic>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace {

constexpr int K = 13;
constexpr int P = 199;
constexpr int C = 14;
constexpr int Q = P * C;
constexpr int WORDS = (Q + 63) / 64;
constexpr std::uint64_t NODE_CAP = 1'000'000;
constexpr int WALL_SECONDS = 30;

struct Mask {
  std::array<std::uint64_t, WORDS> word{};
};

bool is_full(Mask const& mask, Mask const& full) {
  return mask.word == full.word;
}

int popcount(Mask const& mask) {
  int result = 0;
  for (auto value : mask.word) result += __builtin_popcountll(value);
  return result;
}

Mask unite(Mask left, Mask const& right) {
  for (int index = 0; index < WORDS; ++index) left.word[static_cast<std::size_t>(index)] |= right.word[static_cast<std::size_t>(index)];
  return left;
}

Mask difference(Mask const& full, Mask const& covered) {
  Mask result;
  for (int index = 0; index < WORDS; ++index) result.word[static_cast<std::size_t>(index)] =
      full.word[static_cast<std::size_t>(index)] & ~covered.word[static_cast<std::size_t>(index)];
  return result;
}

bool contains(Mask const& mask, int point) {
  return (mask.word[static_cast<std::size_t>(point / 64)] >> (point % 64)) & 1ULL;
}

struct Search {
  Mask full{};
  std::array<std::array<Mask, C>, K> bad{};
  std::array<std::vector<std::pair<int, int>>, Q> options;
  std::array<int, K> base{};
  std::array<int, K> digit{};
  std::uint64_t nodes = 0;
  bool capped = false;
  std::chrono::steady_clock::time_point deadline;

  explicit Search(std::array<int, K> const& base_in) : base(base_in) {
    for (int word = 0; word < WORDS; ++word) full.word[static_cast<std::size_t>(word)] = ~0ULL;
    if (Q % 64) full.word.back() = (1ULL << (Q % 64)) - 1ULL;
    digit.fill(-1);
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      for (int choice = 0; choice < C; ++choice) {
        int speed = base[static_cast<std::size_t>(coordinate)] + P * choice;
        for (int time = 0; time < Q; ++time) {
          int residue = static_cast<int>((static_cast<long long>(time) * speed) % Q);
          if (14 * std::min(residue, Q - residue) < Q) {
            bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)]
                .word[static_cast<std::size_t>(time / 64)] |= 1ULL << (time % 64);
          }
        }
      }
    }
    for (int time = 0; time < Q; ++time) {
      for (int coordinate = 0; coordinate < K; ++coordinate) {
        for (int choice = 0; choice < C; ++choice) {
          if (contains(bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)], time)) {
            options[static_cast<std::size_t>(time)].emplace_back(coordinate, choice);
          }
        }
      }
    }
    deadline = std::chrono::steady_clock::now() + std::chrono::seconds(WALL_SECONDS);
  }

  bool direct_improper(std::array<int, K> const& candidate) const {
    for (int omitted = 0; omitted < K; ++omitted) {
      int divisor = C;
      for (int coordinate = 0; coordinate < K; ++coordinate) {
        if (coordinate != omitted) divisor = std::gcd(divisor, candidate[static_cast<std::size_t>(coordinate)]);
      }
      if (divisor > 1) return false;
    }
    Mask covered;
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      covered = unite(covered, bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(candidate[static_cast<std::size_t>(coordinate)] / P)]);
    }
    return is_full(covered, full);
  }

  bool finish_if_covered(Mask const& covered, int div2, int div7) {
    if (!is_full(covered, full)) return false;
    if (div2 >= 12 || div7 >= 12) return false;
    std::array<int, K> candidate{};
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      int choice = digit[static_cast<std::size_t>(coordinate)];
      if (choice < 0) {
        for (choice = 0; choice < C; ++choice) {
          if (std::gcd(base[static_cast<std::size_t>(coordinate)] + P * choice, C) == 1) break;
        }
        if (choice == C) throw std::runtime_error("missing coprime completion digit");
        digit[static_cast<std::size_t>(coordinate)] = choice;
      }
      candidate[static_cast<std::size_t>(coordinate)] = base[static_cast<std::size_t>(coordinate)] + P * choice;
    }
    if (!direct_improper(candidate)) throw std::runtime_error("covered completion failed direct improper check");
    return true;
  }

  bool impossible_by_gain_bound(Mask const& covered) const {
    Mask uncovered = difference(full, covered);
    int needed = popcount(uncovered);
    int available = 0;
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      if (digit[static_cast<std::size_t>(coordinate)] >= 0) continue;
      int best = 0;
      for (int choice = 0; choice < C; ++choice) {
        Mask gained = bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)];
        for (int word = 0; word < WORDS; ++word) gained.word[static_cast<std::size_t>(word)] &= uncovered.word[static_cast<std::size_t>(word)];
        best = std::max(best, popcount(gained));
      }
      available += best;
    }
    return available < needed;
  }

  bool greedy() {
    for (int rotation = 0; rotation < K; ++rotation) {
      std::array<int, K> trial{};
      trial.fill(-1);
      Mask covered{};
      int div2 = 0;
      int div7 = 0;
      for (int step = 0; step < K; ++step) {
        int coordinate = (rotation + step) % K;
        Mask uncovered = difference(full, covered);
        int selected = -1;
        int best_gain = -1;
        for (int choice = 0; choice < C; ++choice) {
          Mask gained = bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)];
          for (int word = 0; word < WORDS; ++word) gained.word[static_cast<std::size_t>(word)] &= uncovered.word[static_cast<std::size_t>(word)];
          int gain = popcount(gained);
          if (gain > best_gain) {
            best_gain = gain;
            selected = choice;
          }
        }
        trial[static_cast<std::size_t>(coordinate)] = selected;
        int speed = base[static_cast<std::size_t>(coordinate)] + P * selected;
        div2 += speed % 2 == 0;
        div7 += speed % 7 == 0;
        covered = unite(covered, bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(selected)]);
      }
      if (div2 >= 12 || div7 >= 12 || !is_full(covered, full)) continue;
      std::array<int, K> candidate{};
      for (int coordinate = 0; coordinate < K; ++coordinate) {
        candidate[static_cast<std::size_t>(coordinate)] = base[static_cast<std::size_t>(coordinate)] + P * trial[static_cast<std::size_t>(coordinate)];
      }
      if (direct_improper(candidate)) {
        digit = trial;
        return true;
      }
    }
    digit.fill(-1);
    return false;
  }

  bool search(Mask const& covered, int div2, int div7) {
    if (++nodes > NODE_CAP || std::chrono::steady_clock::now() > deadline) {
      capped = true;
      return false;
    }
    if (div2 >= 12 || div7 >= 12) return false;
    if (is_full(covered, full)) return finish_if_covered(covered, div2, div7);
    if (impossible_by_gain_bound(covered)) return false;

    int target = -1;
    int best_choices = 1'000'000;
    int inspected = 0;
    for (int point = 0; point < Q && inspected < 128; ++point) {
      if (contains(covered, point)) continue;
      ++inspected;
      int count = 0;
      for (auto [coordinate, choice] : options[static_cast<std::size_t>(point)]) {
        (void)choice;
        if (digit[static_cast<std::size_t>(coordinate)] < 0) ++count;
      }
      if (count == 0) return false;
      if (count < best_choices) {
        best_choices = count;
        target = point;
      }
    }
    if (target < 0) throw std::runtime_error("uncovered point selection failed");

    Mask uncovered = difference(full, covered);
    struct Choice { int coordinate; int digit; int gain; };
    std::vector<Choice> choices;
    for (auto [coordinate, choice] : options[static_cast<std::size_t>(target)]) {
      if (digit[static_cast<std::size_t>(coordinate)] >= 0) continue;
      Mask gained = bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)];
      for (int word = 0; word < WORDS; ++word) gained.word[static_cast<std::size_t>(word)] &= uncovered.word[static_cast<std::size_t>(word)];
      choices.push_back({coordinate, choice, popcount(gained)});
    }
    std::sort(choices.begin(), choices.end(), [](Choice const& left, Choice const& right) {
      if (left.gain != right.gain) return left.gain > right.gain;
      if (left.coordinate != right.coordinate) return left.coordinate < right.coordinate;
      return left.digit < right.digit;
    });
    for (Choice const& choice : choices) {
      digit[static_cast<std::size_t>(choice.coordinate)] = choice.digit;
      int speed = base[static_cast<std::size_t>(choice.coordinate)] + P * choice.digit;
      if (search(unite(covered, bad[static_cast<std::size_t>(choice.coordinate)][static_cast<std::size_t>(choice.digit)]),
                 div2 + (speed % 2 == 0), div7 + (speed % 7 == 0))) return true;
      digit[static_cast<std::size_t>(choice.coordinate)] = -1;
      if (capped) return false;
    }
    return false;
  }
};

}  // namespace

int main(int argc, char** argv) try {
  if (argc != 3) {
    std::cerr << "usage: lrc_p199_multichoice_lift INPUT OUTPUT\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  std::ofstream output(argv[2]);
  if (!input || !output) throw std::runtime_error("cannot open input or output");
  std::vector<std::array<int, K>> bases;
  for (std::string line; std::getline(input, line);) {
    std::istringstream stream(line);
    std::array<int, K> base{};
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      if (!(stream >> base[static_cast<std::size_t>(coordinate)])) throw std::runtime_error("malformed input row");
    }
    int extra = 0;
    if (stream >> extra) throw std::runtime_error("overlong input row");
    bases.push_back(base);
  }
  if (bases.size() != 100) throw std::runtime_error("sample must contain exactly 100 rows");
  struct Result { bool sat = false; bool capped = false; std::uint64_t nodes = 0; long long micros = 0; std::array<int, K> digit{}; };
  std::vector<Result> results(bases.size());
  std::atomic<std::size_t> next(0);
  std::vector<std::thread> workers;
  for (int worker = 0; worker < 3; ++worker) {
    workers.emplace_back([&] {
      while (true) {
        std::size_t row = next.fetch_add(1);
        if (row >= bases.size()) return;
        auto start = std::chrono::steady_clock::now();
        Search search(bases[row]);
        bool sat = search.greedy() || search.search(Mask{}, 0, 0);
        Result& result = results[row];
        result.sat = sat;
        result.capped = search.capped;
        result.nodes = search.nodes;
        result.micros = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now() - start).count();
        result.digit = search.digit;
      }
    });
  }
  for (auto& worker : workers) worker.join();
  for (std::size_t row = 0; row < results.size(); ++row) {
    Result const& result = results[row];
    output << row << ' ' << (result.sat ? "SAT" : result.capped ? "CAP" : "UNSAT") << ' '
           << result.nodes << ' ' << result.micros;
    if (result.sat) for (int value : result.digit) output << ' ' << value;
    output << '\n';
  }
  return 0;
} catch (std::exception const& error) {
  std::cerr << "error: " << error.what() << '\n';
  return 1;
}
