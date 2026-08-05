#define main cycle3_in_memory_main
#include "lrc_coverage_levels.cpp"
#undef main

#include <filesystem>
#include <memory>
#include <mutex>

namespace fs = std::filesystem;

namespace {

constexpr int PARTITIONS = 64;
constexpr std::uint64_t RECORD_BYTES = sizeof(State);

std::uint64_t partition_hash(State const& state) {
  std::uint64_t hash = 1469598103934665603ULL;
  for (std::uint8_t value : state.value) {
    hash ^= value;
    hash *= 1099511628211ULL;
  }
  return hash;
}

int partition_of(State const& state) { return static_cast<int>(partition_hash(state) & 63ULL); }

fs::path level_path(fs::path const& root, int depth, int partition) {
  return root / ("level-" + std::to_string(depth) + "-p" + std::to_string(partition) + ".bin");
}

fs::path shard_path(fs::path const& root, int depth, int partition, int worker) {
  return root / ("raw-" + std::to_string(depth) + "-p" + std::to_string(partition) +
                 "-w" + std::to_string(worker) + ".bin");
}

void require_aligned(fs::path const& path) {
  if (fs::exists(path) && fs::file_size(path) % RECORD_BYTES != 0) {
    throw std::runtime_error("unaligned record file: " + path.string());
  }
}

std::uint64_t remove_counted(fs::path const& path) {
  if (!fs::exists(path)) return 0;
  std::uint64_t bytes = fs::file_size(path);
  if (!fs::remove(path)) throw std::runtime_error("failed to remove " + path.string());
  return bytes;
}

}  // namespace

int main(int argc, char** argv) try {
  int k = 0;
  int p = 0;
  int threads = 3;
  int max_seconds = 300;
  std::uint64_t state_cap = std::numeric_limits<std::uint64_t>::max();
  std::uint64_t edge_cap = std::numeric_limits<std::uint64_t>::max();
  std::uint64_t leaf_cap = std::numeric_limits<std::uint64_t>::max();
  std::uint64_t disk_cap = 64ULL * 1024ULL * 1024ULL * 1024ULL;
  std::string output_path;
  fs::path work_root = "discovery/out/cycle4-work";
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
    else if (arg == "--disk-cap-bytes") disk_cap = std::stoull(value());
    else if (arg == "--output") output_path = value();
    else {
      std::cerr << "unknown argument: " << arg << '\n';
      return 2;
    }
  }
  if (k < 2 || k > MAX_K || !is_prime(p) || (p - 1) / 2 > 127 || threads != 3 ||
      max_seconds < 1 || state_cap < 1 || edge_cap < 1 || leaf_cap < 1 ||
      output_path.empty()) {
    std::cerr << "invalid arguments\n";
    return 2;
  }
  if (fs::exists(work_root)) {
    std::cerr << "refusing existing work root: " << work_root << '\n';
    return 2;
  }
  fs::create_directories(work_root);

  auto start = std::chrono::steady_clock::now();
  auto deadline = start + std::chrono::seconds(max_seconds);
  Engine engine(k, p);
  std::atomic<std::uint64_t> expanded(0), edges(0), leaves(0), live_disk(0), peak_disk(0);
  std::atomic<bool> stopped(false);
  std::atomic<int> stop_code(0);
  auto request_stop = [&](int code) {
    int expected = 0;
    stop_code.compare_exchange_strong(expected, code, std::memory_order_relaxed);
    stopped.store(true, std::memory_order_relaxed);
  };
  auto add_disk = [&](std::uint64_t bytes) {
    std::uint64_t live = live_disk.fetch_add(bytes, std::memory_order_relaxed) + bytes;
    std::uint64_t peak = peak_disk.load(std::memory_order_relaxed);
    while (live > peak && !peak_disk.compare_exchange_weak(peak, live, std::memory_order_relaxed)) {}
    if (live > disk_cap) request_stop(5);
  };
  auto subtract_disk = [&](std::uint64_t bytes) { live_disk.fetch_sub(bytes, std::memory_order_relaxed); };

  State empty;
  {
    fs::path initial = level_path(work_root, 0, partition_of(empty));
    std::ofstream output(initial, std::ios::binary);
    output.write(reinterpret_cast<char const*>(&empty), sizeof(empty));
  }
  add_disk(RECORD_BYTES);
  std::unordered_set<State, StateHash> solutions;
  int completed_depth = -1;

  for (int depth = 0; depth <= k && !stopped.load(std::memory_order_relaxed); ++depth) {
    std::uint64_t edge_start = edges.load(std::memory_order_relaxed);
    std::uint64_t disk_before_expansion = live_disk.load(std::memory_order_relaxed);
    std::atomic<int> next_partition(0);
    std::vector<std::unordered_set<State, StateHash>> local_solutions(static_cast<std::size_t>(threads));
    std::vector<std::uint64_t> worker_states(static_cast<std::size_t>(threads), 0);
    std::vector<std::uint64_t> worker_written(static_cast<std::size_t>(threads), 0);
    std::vector<std::thread> workers;
    for (int worker = 0; worker < threads; ++worker) {
      workers.emplace_back([&, worker]() {
        try {
        std::vector<std::unique_ptr<std::ofstream>> shard(PARTITIONS);
        auto emit = [&](State const& child, int next_depth) {
          std::uint64_t generated = edges.fetch_add(1, std::memory_order_relaxed) + 1;
          if (generated > edge_cap) {
            request_stop(4);
            return;
          }
          if (disk_before_expansion + (generated - edge_start) * RECORD_BYTES > disk_cap) {
            request_stop(5);
            return;
          }
          int target = partition_of(child);
          if (!shard[static_cast<std::size_t>(target)]) {
            shard[static_cast<std::size_t>(target)] = std::make_unique<std::ofstream>(
                shard_path(work_root, next_depth, target, worker), std::ios::binary);
          }
          shard[static_cast<std::size_t>(target)]->write(
              reinterpret_cast<char const*>(&child), sizeof(child));
          if (!*shard[static_cast<std::size_t>(target)]) {
            request_stop(6);
            return;
          }
          ++worker_written[static_cast<std::size_t>(worker)];
        };
        while (!stopped.load(std::memory_order_relaxed)) {
          int partition = next_partition.fetch_add(1, std::memory_order_relaxed);
          if (partition >= PARTITIONS) break;
          fs::path input_path = level_path(work_root, depth, partition);
          if (!fs::exists(input_path)) continue;
          require_aligned(input_path);
          std::ifstream input(input_path, std::ios::binary);
          State state;
          while (!stopped.load(std::memory_order_relaxed) &&
                 input.read(reinterpret_cast<char*>(&state), sizeof(state))) {
            if (partition_of(state) != partition) {
              request_stop(7);
              break;
            }
            ++worker_states[static_cast<std::size_t>(worker)];
            std::uint64_t seen = expanded.fetch_add(1, std::memory_order_relaxed) + 1;
            if (seen > state_cap) {
              request_stop(1);
              break;
            }
            if ((seen & ((1ULL << 18U) - 1ULL)) == 0 &&
                std::chrono::steady_clock::now() >= deadline) {
              request_stop(2);
              break;
            }
            Mask covered = engine.covered_by(state, depth);
            if (depth == k) {
              std::uint64_t leaf = leaves.fetch_add(1, std::memory_order_relaxed) + 1;
              if (leaf > leaf_cap) {
                request_stop(3);
                break;
              }
              if (covered == engine.full) {
                local_solutions[static_cast<std::size_t>(worker)].insert(
                    engine.residue_representative(state));
              }
              continue;
            }
            if (engine.cannot_complete(covered, depth)) continue;
            int uncovered = engine.first_uncovered(covered);
            if (uncovered < 0) {
              for (int center = 0; center < engine.h && !stopped.load(); ++center) {
                emit(engine.add(state, depth, center), depth + 1);
              }
            } else {
              for (int center : engine.covering_centers[static_cast<std::size_t>(uncovered)]) {
                if (stopped.load(std::memory_order_relaxed)) break;
                emit(engine.add(state, depth, center), depth + 1);
              }
            }
          }
        }
        } catch (std::bad_alloc const&) {
          request_stop(8);
        } catch (std::exception const&) {
          request_stop(6);
        }
      });
    }
    for (auto& worker : workers) worker.join();
    std::uint64_t raw_records = 0;
    for (std::uint64_t count : worker_written) raw_records += count;
    add_disk(raw_records * RECORD_BYTES);
    if (stopped.load(std::memory_order_relaxed)) break;
    for (auto& found : local_solutions) solutions.insert(found.begin(), found.end());
    std::uint64_t level_states = 0;
    for (std::uint64_t count : worker_states) level_states += count;
    completed_depth = depth;
    std::cerr << "level=" << depth << " states=" << level_states
              << " expanded=" << expanded.load() << " edges=" << edges.load()
              << " leaves=" << leaves.load() << " solutions=" << solutions.size()
              << " live_disk_bytes=" << live_disk.load() << '\n';
    if (depth == k) break;

    std::atomic<int> dedup_partition(0);
    std::vector<std::thread> dedupers;
    for (int worker = 0; worker < threads; ++worker) {
      dedupers.emplace_back([&]() {
        try {
        while (!stopped.load(std::memory_order_relaxed)) {
          if (std::chrono::steady_clock::now() >= deadline) {
            request_stop(2);
            break;
          }
          int partition = dedup_partition.fetch_add(1, std::memory_order_relaxed);
          if (partition >= PARTITIONS) break;
          std::uint64_t total_bytes = 0;
          for (int source = 0; source < threads; ++source) {
            fs::path path = shard_path(work_root, depth + 1, partition, source);
            require_aligned(path);
            if (fs::exists(path)) total_bytes += fs::file_size(path);
          }
          std::vector<State> records(static_cast<std::size_t>(total_bytes / RECORD_BYTES));
          std::size_t offset = 0;
          for (int source = 0; source < threads; ++source) {
            fs::path path = shard_path(work_root, depth + 1, partition, source);
            if (!fs::exists(path)) continue;
            std::uint64_t bytes = fs::file_size(path);
            std::ifstream input(path, std::ios::binary);
            input.read(reinterpret_cast<char*>(records.data() + offset), static_cast<std::streamsize>(bytes));
            if (!input) throw std::runtime_error("short shard read");
            offset += static_cast<std::size_t>(bytes / RECORD_BYTES);
          }
          std::sort(records.begin(), records.end());
          records.erase(std::unique(records.begin(), records.end()), records.end());
          for (State const& state : records) {
            if (partition_of(state) != partition) {
              request_stop(7);
              return;
            }
          }
          fs::path output_path = level_path(work_root, depth + 1, partition);
          if (!records.empty()) {
            std::ofstream output(output_path, std::ios::binary);
            output.write(reinterpret_cast<char const*>(records.data()),
                         static_cast<std::streamsize>(records.size() * RECORD_BYTES));
            if (!output) throw std::runtime_error("short unique write");
            add_disk(records.size() * RECORD_BYTES);
          }
          for (int source = 0; source < threads; ++source) {
            std::uint64_t removed = remove_counted(
                shard_path(work_root, depth + 1, partition, source));
            subtract_disk(removed);
          }
        }
        } catch (std::bad_alloc const&) {
          request_stop(8);
        } catch (std::exception const&) {
          request_stop(6);
        }
      });
    }
    for (auto& deduper : dedupers) deduper.join();
    if (stopped.load(std::memory_order_relaxed)) break;
    for (int partition = 0; partition < PARTITIONS; ++partition) {
      subtract_disk(remove_counted(level_path(work_root, depth, partition)));
    }
  }

  std::vector<State> ordered(solutions.begin(), solutions.end());
  std::sort(ordered.begin(), ordered.end());
  double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  bool complete = !stopped.load(std::memory_order_relaxed) && completed_depth == k;
  static constexpr std::array<char const*, 9> reasons = {
      "UNKNOWN", "STATE_CAP", "TIMEOUT", "LEAF_CAP", "EDGE_CAP", "DISK_CAP",
      "IO_ERROR", "PARTITION_ERROR", "MEMORY_CAP"};
  std::cout << "status=" << (complete ? "COMPLETE" : "INCOMPLETE") << '\n';
  if (!complete) std::cout << "stop_reason=" << reasons[static_cast<std::size_t>(stop_code.load())] << '\n';
  std::cout << "k=" << k << '\n';
  std::cout << "p=" << p << '\n';
  std::cout << "primitive_root=" << engine.primitive_root << '\n';
  std::cout << "threads=" << threads << '\n';
  std::cout << "partitions=" << PARTITIONS << '\n';
  std::cout << "completed_depth=" << completed_depth << '\n';
  std::cout << "canonical_solutions=" << ordered.size() << '\n';
  std::cout << "expanded_states=" << expanded.load() << '\n';
  std::cout << "generated_edges=" << edges.load() << '\n';
  std::cout << "leaf_states=" << leaves.load() << '\n';
  std::cout << "peak_disk_bytes=" << peak_disk.load() << '\n';
  std::cout << "wall_seconds=" << elapsed << '\n';
  if (complete) {
    std::ofstream output(output_path);
    for (State const& tuple : ordered) {
      for (int i = 0; i < k; ++i) {
        output << (i == 0 ? "" : " ") << static_cast<int>(tuple.value[static_cast<std::size_t>(i)]);
      }
      output << '\n';
    }
  }
  std::uintmax_t removed_entries = fs::remove_all(work_root);
  std::cout << "cleanup_removed_entries=" << removed_entries << '\n';
  return complete ? 0 : 3;
} catch (std::bad_alloc const&) {
  std::cout << "status=INCOMPLETE\nstop_reason=MEMORY_CAP\n";
  return 3;
} catch (std::exception const& error) {
  std::cerr << "fatal=" << error.what() << '\n';
  return 4;
}
