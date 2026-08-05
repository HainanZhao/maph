#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <string>
#include <thread>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using Mask = std::vector<std::uint64_t>;
using Tuple = std::vector<int>;

struct TupleHash {
  std::size_t operator()(Tuple const& values) const noexcept {
    std::size_t h = 0;
    for (int value : values) {
      h ^= std::hash<int>{}(value) + 0x9e3779b97f4a7c15ULL + (h << 6U) + (h >> 2U);
    }
    return h;
  }
};

int inverse_mod(int value, int prime) {
  int old_r = value;
  int r = prime;
  int old_s = 1;
  int s = 0;
  while (r != 0) {
    int q = old_r / r;
    int next_r = old_r - q * r;
    old_r = r;
    r = next_r;
    int next_s = old_s - q * s;
    old_s = s;
    s = next_s;
  }
  int result = old_s % prime;
  return result < 0 ? result + prime : result;
}

Tuple canonicalize(Tuple const& tuple, int prime) {
  Tuple best;
  for (int pivot : tuple) {
    int inv = inverse_mod(pivot, prime);
    Tuple candidate;
    candidate.reserve(tuple.size());
    for (int value : tuple) {
      int residue = static_cast<int>((static_cast<long long>(value) * inv) % prime);
      candidate.push_back(std::min(residue, prime - residue));
    }
    std::sort(candidate.begin(), candidate.end());
    if (best.empty() || candidate < best) best = std::move(candidate);
  }
  return best;
}

bool bit(Mask const& mask, int position) {
  return (mask[static_cast<std::size_t>(position) / 64U] >> (position % 64)) & 1ULL;
}

void set_bit(Mask& mask, int position) {
  mask[static_cast<std::size_t>(position) / 64U] |= 1ULL << (position % 64);
}

void union_into(Mask& destination, Mask const& source) {
  for (std::size_t i = 0; i < destination.size(); ++i) destination[i] |= source[i];
}

int popcount(Mask const& mask) {
  int result = 0;
  for (std::uint64_t word : mask) result += __builtin_popcountll(word);
  return result;
}

int intersection_popcount(Mask const& left, Mask const& right) {
  int result = 0;
  for (std::size_t i = 0; i < left.size(); ++i) result += __builtin_popcountll(left[i] & right[i]);
  return result;
}

struct Context {
  int k;
  int p;
  int half;
  int words;
  Mask full;
  std::vector<Mask> covers;

  Context(int dimension, int prime)
      : k(dimension), p(prime), half((prime - 1) / 2), words((half + 63) / 64),
        full(static_cast<std::size_t>(words), ~0ULL),
        covers(static_cast<std::size_t>(half), Mask(static_cast<std::size_t>(words), 0)) {
    if (half % 64 != 0) full.back() = (1ULL << (half % 64)) - 1ULL;
    for (int speed = 1; speed <= half; ++speed) {
      for (int time = 1; time <= half; ++time) {
        int residue = static_cast<int>((static_cast<long long>(speed) * time) % p);
        if (residue * (k + 1) < p || (p - residue) * (k + 1) < p) {
          set_bit(covers[static_cast<std::size_t>(speed - 1)], time - 1);
        }
      }
    }
  }
};

struct Shared {
  Context const& context;
  std::chrono::steady_clock::time_point deadline;
  std::atomic<bool> stopped{false};
  std::atomic<std::uint64_t> nodes{0};
  std::atomic<std::uint64_t> leaves{0};
  std::atomic<std::uint64_t> next_progress{10000000};
};

struct Search {
  Shared& shared;
  std::vector<char> eliminated;
  std::vector<int> remaining;
  Mask covered;
  Tuple chosen;
  std::unordered_set<Tuple, TupleHash> solutions;

  explicit Search(Shared& state)
      : shared(state), eliminated(static_cast<std::size_t>(state.context.half), 0),
        remaining(static_cast<std::size_t>(state.context.half), 0),
        covered(static_cast<std::size_t>(state.context.words), 0) {
    for (int position = 0; position < shared.context.half; ++position) {
      for (int speed = 0; speed < shared.context.half; ++speed) {
        if (bit(shared.context.covers[static_cast<std::size_t>(speed)], position)) {
          ++remaining[static_cast<std::size_t>(position)];
        }
      }
    }
  }

  int next_to_cover() const {
    int best_position = -1;
    int best_remaining = std::numeric_limits<int>::max();
    for (int position = 0; position < shared.context.half; ++position) {
      if (!bit(covered, position) && remaining[static_cast<std::size_t>(position)] < best_remaining) {
        best_position = position;
        best_remaining = remaining[static_cast<std::size_t>(position)];
      }
    }
    return best_position;
  }

  void eliminate(int speed_index) {
    eliminated[static_cast<std::size_t>(speed_index)] = 1;
    for (int position = 0; position < shared.context.half; ++position) {
      if (bit(shared.context.covers[static_cast<std::size_t>(speed_index)], position)) {
        --remaining[static_cast<std::size_t>(position)];
      }
    }
  }

  bool early_bound(int next_position) const {
    if (next_position != -1 && remaining[static_cast<std::size_t>(next_position)] == 0) return true;
    if (static_cast<int>(chosen.size()) < shared.context.k - 4 || next_position == -1) return false;

    Mask uncovered = shared.context.full;
    for (std::size_t i = 0; i < uncovered.size(); ++i) uncovered[i] &= ~covered[i];
    int total = popcount(uncovered);
    int best_any = 0;
    int best_next = 0;
    for (int speed = 0; speed < shared.context.half; ++speed) {
      if (eliminated[static_cast<std::size_t>(speed)]) continue;
      int amount = intersection_popcount(uncovered, shared.context.covers[static_cast<std::size_t>(speed)]);
      best_any = std::max(best_any, amount);
      if (bit(shared.context.covers[static_cast<std::size_t>(speed)], next_position)) {
        best_next = std::max(best_next, amount);
      }
    }
    int slots = shared.context.k - static_cast<int>(chosen.size());
    return total > best_next + best_any * (slots - 1);
  }

  void run() {
    if (shared.stopped.load(std::memory_order_relaxed)) return;
    std::uint64_t node = shared.nodes.fetch_add(1, std::memory_order_relaxed) + 1;
    std::uint64_t threshold = shared.next_progress.load(std::memory_order_relaxed);
    if (node >= threshold && shared.next_progress.compare_exchange_strong(threshold, threshold + 10000000)) {
      auto now = std::chrono::steady_clock::now();
      if (now >= shared.deadline) shared.stopped.store(true, std::memory_order_relaxed);
      std::cerr << "progress nodes=" << node << " leaves=" << shared.leaves.load()
                << " local_solutions=" << solutions.size() << '\n';
    }
    if ((node & ((1ULL << 18U) - 1ULL)) == 0 && std::chrono::steady_clock::now() >= shared.deadline) {
      shared.stopped.store(true, std::memory_order_relaxed);
      return;
    }

    if (static_cast<int>(chosen.size()) == shared.context.k) {
      shared.leaves.fetch_add(1, std::memory_order_relaxed);
      if (covered == shared.context.full) solutions.insert(canonicalize(chosen, shared.context.p));
      return;
    }

    int next_position = next_to_cover();
    if (early_bound(next_position)) return;
    auto saved_eliminated = eliminated;
    auto saved_remaining = remaining;
    for (int speed = 0; speed < shared.context.half; ++speed) {
      if (shared.stopped.load(std::memory_order_relaxed)) break;
      if (eliminated[static_cast<std::size_t>(speed)]) continue;
      if (next_position == -1 || bit(shared.context.covers[static_cast<std::size_t>(speed)], next_position)) {
        Mask old_covered = covered;
        chosen.push_back(speed + 1);
        union_into(covered, shared.context.covers[static_cast<std::size_t>(speed)]);
        run();
        chosen.pop_back();
        covered = std::move(old_covered);
        eliminate(speed);
      }
    }
    eliminated = std::move(saved_eliminated);
    remaining = std::move(saved_remaining);
  }
};

bool is_prime(int value) {
  if (value < 2) return false;
  for (int d = 2; static_cast<long long>(d) * d <= value; ++d) {
    if (value % d == 0) return false;
  }
  return true;
}

}  // namespace

int main(int argc, char** argv) {
  int k = 0;
  int p = 0;
  int thread_count = 1;
  int max_seconds = 300;
  std::string output_path;
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    auto need_value = [&](char const* name) {
      if (++i >= argc) {
        std::cerr << "missing value for " << name << '\n';
        std::exit(2);
      }
      return std::string(argv[i]);
    };
    if (arg == "--k") k = std::stoi(need_value("--k"));
    else if (arg == "--p") p = std::stoi(need_value("--p"));
    else if (arg == "--threads") thread_count = std::stoi(need_value("--threads"));
    else if (arg == "--max-seconds") max_seconds = std::stoi(need_value("--max-seconds"));
    else if (arg == "--output") output_path = need_value("--output");
    else {
      std::cerr << "unknown argument: " << arg << '\n';
      return 2;
    }
  }
  if (k < 2 || !is_prime(p) || thread_count < 1 || max_seconds < 1) {
    std::cerr << "usage: lrc_ansatz_exact --k K --p PRIME [--threads N] [--max-seconds N] [--output PATH]\n";
    return 2;
  }

  Context context(k, p);
  auto start = std::chrono::steady_clock::now();
  Shared shared{context, start + std::chrono::seconds(max_seconds)};

  Search base(shared);
  base.chosen.push_back(1);
  union_into(base.covered, context.covers[0]);
  int first_uncovered = base.next_to_cover();
  std::vector<int> second_choices;
  for (int speed = 0; speed < context.half; ++speed) {
    if (first_uncovered == -1 || bit(context.covers[static_cast<std::size_t>(speed)], first_uncovered)) {
      second_choices.push_back(speed);
    }
  }

  std::atomic<std::size_t> next_job{0};
  std::vector<std::unordered_set<Tuple, TupleHash>> thread_solutions(static_cast<std::size_t>(thread_count));
  std::vector<std::thread> workers;
  for (int worker = 0; worker < thread_count; ++worker) {
    workers.emplace_back([&, worker] {
      while (!shared.stopped.load(std::memory_order_relaxed)) {
        std::size_t job = next_job.fetch_add(1, std::memory_order_relaxed);
        if (job >= second_choices.size()) break;
        Search search(shared);
        search.chosen.push_back(1);
        union_into(search.covered, context.covers[0]);
        for (std::size_t prior = 0; prior < job; ++prior) search.eliminate(second_choices[prior]);
        int speed = second_choices[job];
        search.chosen.push_back(speed + 1);
        union_into(search.covered, context.covers[static_cast<std::size_t>(speed)]);
        search.run();
        thread_solutions[static_cast<std::size_t>(worker)].merge(search.solutions);
      }
    });
  }
  for (auto& worker : workers) worker.join();

  std::unordered_set<Tuple, TupleHash> solutions;
  for (auto& local : thread_solutions) solutions.merge(local);
  std::vector<Tuple> ordered(solutions.begin(), solutions.end());
  std::sort(ordered.begin(), ordered.end());
  auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  bool complete = !shared.stopped.load(std::memory_order_relaxed) && next_job.load() >= second_choices.size();

  std::cout << "status=" << (complete ? "COMPLETE" : "TIMEOUT") << '\n';
  std::cout << "k=" << k << '\n';
  std::cout << "p=" << p << '\n';
  std::cout << "canonical_solutions=" << ordered.size() << '\n';
  std::cout << "nodes=" << shared.nodes.load() << '\n';
  std::cout << "leaves=" << shared.leaves.load() << '\n';
  std::cout << "wall_seconds=" << elapsed << '\n';

  if (!output_path.empty() && complete) {
    std::ofstream output(output_path);
    for (Tuple const& tuple : ordered) {
      for (std::size_t i = 0; i < tuple.size(); ++i) output << (i == 0 ? "" : " ") << tuple[i];
      output << '\n';
    }
  }
  return complete ? 0 : 3;
}
