#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <string>
#include <thread>
#include <unordered_set>
#include <vector>

namespace {

using Tuple = std::vector<int>;
using Mask = std::vector<std::uint64_t>;

struct TupleHash {
  std::size_t operator()(Tuple const& values) const noexcept {
    std::size_t h = 0;
    for (int value : values) {
      h ^= std::hash<int>{}(value) + 0x9e3779b97f4a7c15ULL + (h << 6U) + (h >> 2U);
    }
    return h;
  }
};

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

Tuple canonical(Tuple const& values, int modulus) {
  if (values.empty()) return {};
  Tuple best;
  int previous = -1;
  for (int pivot : values) {
    if (pivot == previous) continue;
    previous = pivot;
    int shift = (modulus - pivot) % modulus;
    Tuple candidate;
    candidate.reserve(values.size());
    for (int value : values) candidate.push_back((value + shift) % modulus);
    std::sort(candidate.begin(), candidate.end());
    if (best.empty() || candidate < best) best = std::move(candidate);
  }
  return best;
}

Tuple canonical_parent(Tuple const& canonical_child, int modulus) {
  if (canonical_child.empty()) return {};
  Tuple parent = canonical_child;
  parent.pop_back();
  return canonical(parent, modulus);
}

void set_bit(Mask& mask, int position) {
  mask[static_cast<std::size_t>(position) / 64U] |= 1ULL << (position % 64);
}

int popcount(Mask const& mask) {
  int result = 0;
  for (std::uint64_t word : mask) result += __builtin_popcountll(word);
  return result;
}

int extra_count(Mask const& cover, Mask const& used) {
  int result = 0;
  for (std::size_t i = 0; i < cover.size(); ++i) result += __builtin_popcountll(cover[i] & ~used[i]);
  return result;
}

void union_into(Mask& destination, Mask const& source) {
  for (std::size_t i = 0; i < destination.size(); ++i) destination[i] |= source[i];
}

struct Search {
  int k;
  int p;
  int h;
  int words;
  int primitive_root;
  std::vector<int> exponent_to_speed;
  std::vector<Mask> covers;
  Mask full;
  std::uint64_t node_cap;
  std::chrono::steady_clock::time_point deadline;
  bool stopped = false;
  std::string stop_reason;
  std::uint64_t nodes = 0;
  std::uint64_t leaves = 0;
  std::unordered_set<Tuple, TupleHash> solutions;
  std::atomic<std::uint64_t>* shared_nodes;
  std::atomic<bool>* shared_stop;

  Search(int dimension, int prime, std::uint64_t maximum_nodes, int max_seconds,
         std::atomic<std::uint64_t>* global_nodes = nullptr,
         std::atomic<bool>* global_stop = nullptr)
      : k(dimension), p(prime), h((prime - 1) / 2), words((h + 63) / 64),
        primitive_root(least_primitive_root(prime)), exponent_to_speed(static_cast<std::size_t>(h)),
        covers(static_cast<std::size_t>(h), Mask(static_cast<std::size_t>(words), 0)),
        full(static_cast<std::size_t>(words), ~0ULL), node_cap(maximum_nodes),
        deadline(std::chrono::steady_clock::now() + std::chrono::seconds(max_seconds)),
        shared_nodes(global_nodes), shared_stop(global_stop) {
    if (h % 64 != 0) full.back() = (1ULL << (h % 64)) - 1ULL;
    std::vector<char> base_bad(static_cast<std::size_t>(h), 0);
    int residue = 1;
    for (int exponent = 0; exponent < h; ++exponent) {
      int signed_residue = std::min(residue, p - residue);
      exponent_to_speed[static_cast<std::size_t>(exponent)] = signed_residue;
      base_bad[static_cast<std::size_t>(exponent)] =
          static_cast<char>((k + 1) * signed_residue < p);
      residue = static_cast<int>((static_cast<long long>(residue) * primitive_root) % p);
    }
    for (int center = 0; center < h; ++center) {
      for (int time = 0; time < h; ++time) {
        if (base_bad[static_cast<std::size_t>((center + time) % h)]) {
          set_bit(covers[static_cast<std::size_t>(center)], time);
        }
      }
    }
  }

  Tuple residue_representative(Tuple const& exponents) const {
    Tuple values;
    values.reserve(exponents.size());
    for (int exponent : exponents) values.push_back(exponent_to_speed[static_cast<std::size_t>(exponent)]);
    Tuple best;
    for (int pivot : values) {
      int inverse = power_mod(pivot, p - 2, p);
      Tuple candidate;
      candidate.reserve(values.size());
      for (int value : values) {
        int normalized = static_cast<int>((static_cast<long long>(value) * inverse) % p);
        candidate.push_back(std::min(normalized, p - normalized));
      }
      std::sort(candidate.begin(), candidate.end());
      if (best.empty() || candidate < best) best = std::move(candidate);
    }
    return best;
  }

  Mask covered_by(Tuple const& centers) const {
    Mask result(static_cast<std::size_t>(words), 0);
    for (int center : centers) union_into(result, covers[static_cast<std::size_t>(center)]);
    return result;
  }

  bool cannot_complete(Tuple const& centers, Mask const& covered) const {
    int remaining_slots = k - static_cast<int>(centers.size());
    int uncovered = h - popcount(covered);
    int best_extra = 0;
    for (Mask const& candidate : covers) best_extra = std::max(best_extra, extra_count(candidate, covered));
    return uncovered > remaining_slots * best_extra;
  }

  std::vector<Tuple> accepted_children(Tuple const& current) const {
    std::unordered_set<Tuple, TupleHash> seen;
    std::vector<Tuple> accepted;
    seen.reserve(static_cast<std::size_t>(h));
    accepted.reserve(static_cast<std::size_t>(h));
    for (int added = 0; added < h; ++added) {
      Tuple raw;
      raw.reserve(current.size() + 1U);
      auto position = std::upper_bound(current.begin(), current.end(), added);
      raw.insert(raw.end(), current.begin(), position);
      raw.push_back(added);
      raw.insert(raw.end(), position, current.end());
      Tuple child = canonical(raw, h);
      if (!seen.insert(child).second) continue;
      if (canonical_parent(child, h) != current) continue;
      accepted.push_back(std::move(child));
    }
    std::sort(accepted.begin(), accepted.end());
    return accepted;
  }

  void run(Tuple const& current) {
    if (stopped || (shared_stop != nullptr && shared_stop->load(std::memory_order_relaxed))) return;
    ++nodes;
    std::uint64_t budget_nodes = nodes;
    if (shared_nodes != nullptr) {
      budget_nodes = shared_nodes->fetch_add(1, std::memory_order_relaxed) + 1;
    }
    if (budget_nodes > node_cap) {
      stopped = true;
      stop_reason = "NODE_CAP";
      if (shared_stop != nullptr) shared_stop->store(true, std::memory_order_relaxed);
      return;
    }
    if ((budget_nodes & ((1ULL << 18U) - 1ULL)) == 0 &&
        std::chrono::steady_clock::now() >= deadline) {
      stopped = true;
      stop_reason = "TIMEOUT";
      if (shared_stop != nullptr) shared_stop->store(true, std::memory_order_relaxed);
      return;
    }
    if (budget_nodes % 10000000ULL == 0) {
      std::cerr << "progress aggregate_nodes=" << budget_nodes << " worker_nodes=" << nodes
                << " worker_leaves=" << leaves << " worker_solutions=" << solutions.size()
                << " depth=" << current.size() << '\n';
    }

    Mask covered = covered_by(current);
    if (static_cast<int>(current.size()) == k) {
      ++leaves;
      if (covered == full) solutions.insert(residue_representative(current));
      return;
    }
    if (cannot_complete(current, covered)) return;

    for (Tuple const& child : accepted_children(current)) {
      run(child);
      if (stopped) return;
    }
  }
};

}  // namespace

int main(int argc, char** argv) {
  int k = 0;
  int p = 0;
  int max_seconds = 300;
  std::uint64_t node_cap = std::numeric_limits<std::uint64_t>::max();
  int shard_index = 0;
  int shard_count = 1;
  int threads = 1;
  int task_depth = 4;
  std::string output_path;
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    auto value = [&]() {
      if (++i >= argc) std::exit(2);
      return std::string(argv[i]);
    };
    if (arg == "--k") k = std::stoi(value());
    else if (arg == "--p") p = std::stoi(value());
    else if (arg == "--max-seconds") max_seconds = std::stoi(value());
    else if (arg == "--node-cap") node_cap = std::stoull(value());
    else if (arg == "--shard-index") shard_index = std::stoi(value());
    else if (arg == "--shard-count") shard_count = std::stoi(value());
    else if (arg == "--threads") threads = std::stoi(value());
    else if (arg == "--task-depth") task_depth = std::stoi(value());
    else if (arg == "--output") output_path = value();
    else {
      std::cerr << "unknown argument: " << arg << '\n';
      return 2;
    }
  }
  if (k < 2 || !is_prime(p) || max_seconds < 1 || node_cap < 1 ||
      shard_count < 1 || shard_index < 0 || shard_index >= shard_count) {
    std::cerr << "usage: lrc_orbit_quotient --k K --p PRIME --node-cap N --max-seconds N "
                 "[--shard-index I --shard-count N] [--output PATH]\n";
    return 2;
  }
  if (threads < 1 || task_depth < 1 || task_depth >= k ||
      (threads > 1 && (shard_count != 1 || shard_index != 0))) {
    std::cerr << "parallel mode requires --threads N, 1 <= --task-depth < K, and no static sharding\n";
    return 2;
  }

  auto start = std::chrono::steady_clock::now();
  if (threads > 1) {
    Search coordinator(k, p, node_cap, max_seconds);
    std::vector<Tuple> frontier(1);
    std::uint64_t prefix_nodes = 0;
    for (int depth = 0; depth < task_depth; ++depth) {
      std::vector<Tuple> next;
      for (Tuple const& current : frontier) {
        ++prefix_nodes;
        Mask covered = coordinator.covered_by(current);
        if (coordinator.cannot_complete(current, covered)) continue;
        auto children = coordinator.accepted_children(current);
        next.insert(next.end(), std::make_move_iterator(children.begin()),
                    std::make_move_iterator(children.end()));
      }
      frontier = std::move(next);
    }
    std::atomic<std::uint64_t> global_nodes(prefix_nodes);
    std::atomic<std::size_t> next_task(0);
    std::atomic<bool> global_stop(prefix_nodes > node_cap);
    std::vector<std::unique_ptr<Search>> workers;
    std::vector<std::size_t> worker_tasks(static_cast<std::size_t>(threads), 0);
    workers.reserve(static_cast<std::size_t>(threads));
    for (int worker = 0; worker < threads; ++worker) {
      workers.push_back(std::make_unique<Search>(k, p, node_cap, max_seconds,
                                                 &global_nodes, &global_stop));
    }
    std::vector<std::thread> pool;
    pool.reserve(static_cast<std::size_t>(threads));
    for (int worker = 0; worker < threads; ++worker) {
      pool.emplace_back([&, worker]() {
        Search& search = *workers[static_cast<std::size_t>(worker)];
        while (!global_stop.load(std::memory_order_relaxed)) {
          std::size_t task = next_task.fetch_add(1, std::memory_order_relaxed);
          if (task >= frontier.size()) break;
          ++worker_tasks[static_cast<std::size_t>(worker)];
          search.run(frontier[task]);
        }
      });
    }
    for (auto& worker : pool) worker.join();

    std::unordered_set<Tuple, TupleHash> merged;
    std::uint64_t leaves = 0;
    std::size_t assigned_tasks = 0;
    std::string stop_reason;
    for (std::size_t worker = 0; worker < workers.size(); ++worker) {
      leaves += workers[worker]->leaves;
      assigned_tasks += worker_tasks[worker];
      merged.insert(workers[worker]->solutions.begin(), workers[worker]->solutions.end());
      if (!workers[worker]->stop_reason.empty()) stop_reason = workers[worker]->stop_reason;
    }
    std::vector<Tuple> ordered(merged.begin(), merged.end());
    std::sort(ordered.begin(), ordered.end());
    bool complete = !global_stop.load(std::memory_order_relaxed) && assigned_tasks == frontier.size();
    double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
    std::cout << "status=" << (complete ? "COMPLETE" : "INCOMPLETE") << '\n';
    if (!complete) std::cout << "stop_reason=" << (stop_reason.empty() ? "NODE_CAP" : stop_reason) << '\n';
    std::cout << "k=" << k << '\n';
    std::cout << "p=" << p << '\n';
    std::cout << "primitive_root=" << coordinator.primitive_root << '\n';
    std::cout << "threads=" << threads << '\n';
    std::cout << "task_depth=" << task_depth << '\n';
    std::cout << "frontier_tasks=" << frontier.size() << '\n';
    std::cout << "assigned_tasks=" << assigned_tasks << '\n';
    std::cout << "canonical_solutions=" << ordered.size() << '\n';
    std::cout << "nodes=" << global_nodes.load(std::memory_order_relaxed) << '\n';
    std::cout << "leaves=" << leaves << '\n';
    std::cout << "wall_seconds=" << elapsed << '\n';
    if (complete && !output_path.empty()) {
      std::ofstream output(output_path);
      for (Tuple const& tuple : ordered) {
        for (std::size_t i = 0; i < tuple.size(); ++i) output << (i == 0 ? "" : " ") << tuple[i];
        output << '\n';
      }
    }
    return complete ? 0 : 3;
  }

  Search search(k, p, node_cap, max_seconds);
  std::size_t assigned_tasks = 0;
  if (shard_count == 1) {
    search.run({});
  } else {
    auto root_children = search.accepted_children({});
    if (root_children.size() != 1U || root_children.front() != Tuple{0}) {
      std::cerr << "unexpected canonical root children\n";
      return 3;
    }
    auto tasks = search.accepted_children(root_children.front());
    for (std::size_t task = static_cast<std::size_t>(shard_index); task < tasks.size();
         task += static_cast<std::size_t>(shard_count)) {
      ++assigned_tasks;
      search.run(tasks[task]);
      if (search.stopped) break;
    }
  }
  std::vector<Tuple> ordered(search.solutions.begin(), search.solutions.end());
  std::sort(ordered.begin(), ordered.end());
  double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  bool complete = !search.stopped;
  std::cout << "status=" << (complete ? "COMPLETE" : "INCOMPLETE") << '\n';
  if (!complete) std::cout << "stop_reason=" << search.stop_reason << '\n';
  std::cout << "k=" << k << '\n';
  std::cout << "p=" << p << '\n';
  std::cout << "primitive_root=" << search.primitive_root << '\n';
  std::cout << "shard_index=" << shard_index << '\n';
  std::cout << "shard_count=" << shard_count << '\n';
  std::cout << "assigned_tasks=" << assigned_tasks << '\n';
  std::cout << "canonical_solutions=" << ordered.size() << '\n';
  std::cout << "nodes=" << search.nodes << '\n';
  std::cout << "leaves=" << search.leaves << '\n';
  std::cout << "wall_seconds=" << elapsed << '\n';
  if (complete && !output_path.empty()) {
    std::ofstream output(output_path);
    for (Tuple const& tuple : ordered) {
      for (std::size_t i = 0; i < tuple.size(); ++i) output << (i == 0 ? "" : " ") << tuple[i];
      output << '\n';
    }
  }
  return complete ? 0 : 3;
}
