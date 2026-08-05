// Cycle 19 exact meet-in-the-middle maximal coverage antichains.

#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace fs = std::filesystem;
constexpr int K = 13, P = 199, C = 14, Q = P * C, WORDS = (Q + 63) / 64;
constexpr size_t STATE_CAP = 2'000'000, CHILD_CAP = 50'000'000;
constexpr uint64_t DISK_CAP = 21'474'836'480ULL;
using Mask = std::array<uint64_t, WORDS>;

struct Row {
    int base = 0, leaf = 0;
};

struct Result {
    int base = 0, leaf = 0;
    std::string status = "CAP";
    std::array<size_t, 7> left_counts{};
    std::array<std::string, 7> left_hashes{};
    std::array<size_t, 6> right_counts{};
    std::array<std::string, 6> right_hashes{};
    std::string left_path = "-", left_hash = "-", right_path = "-", right_hash = "-";
    uint64_t generated = 0, queries = 0;
    double seconds = 0;
    std::string detail;
};

static std::atomic<uint64_t> persistent_bytes{0}, active_temp_bytes{0};
static std::chrono::steady_clock::time_point global_deadline;

static bool subset(const Mask &left, const Mask &right) {
    for (int word = 0; word < WORDS; ++word) if (left[word] & ~right[word]) return false;
    return true;
}

static bool equal_mask(const Mask &left, const Mask &right) {
    return left == right;
}

static int popcount(const Mask &mask) {
    int result = 0;
    for (uint64_t word : mask) result += std::popcount(word);
    return result;
}

static bool lexical(const Mask &left, const Mask &right) {
    return left < right;
}

static uint32_t projection(const Mask &mask, int family) {
    uint32_t result = 0;
    for (int index = 0; index < 20; ++index) {
        int bit = (index * Q / 20 + (family ? Q / 40 : 0)) % Q;
        if (mask[bit / 64] & (1ULL << (bit % 64))) result |= uint32_t(1u << index);
    }
    return result;
}

static bool dominated(const Mask &candidate, const std::vector<Mask> &retained, const std::unordered_map<uint32_t, std::vector<uint32_t>> &buckets) {
    uint32_t key = projection(candidate, 0), key2 = projection(candidate, 1);
    uint32_t missing = (~key) & ((1u << 20) - 1);
    uint64_t supersets = 1ULL << std::popcount(missing);
    if (supersets > retained.size()) {
        for (const Mask &other : retained) {
            if ((projection(other, 0) & key) == key && (projection(other, 1) & key2) == key2 && subset(candidate, other)) return true;
        }
        return false;
    }
    uint32_t subkey = missing;
    while (true) {
        uint32_t supkey = key | subkey;
        auto found = buckets.find(supkey);
        if (found != buckets.end()) for (uint32_t index : found->second) {
            const Mask &other = retained[index];
            if ((projection(other, 1) & key2) == key2 && subset(candidate, other)) return true;
        }
        if (subkey == 0) break;
        subkey = (subkey - 1) & missing;
    }
    return false;
}

static std::vector<Mask> maximalize(std::vector<Mask> candidates) {
    std::vector<uint32_t> order(candidates.size());
    std::vector<uint16_t> counts(candidates.size());
    for (uint32_t index = 0; index < candidates.size(); ++index) {
        order[index] = index;
        counts[index] = uint16_t(popcount(candidates[index]));
    }
    std::sort(order.begin(), order.end(), [&](uint32_t left, uint32_t right) {
        if (counts[left] != counts[right]) return counts[left] > counts[right];
        return lexical(candidates[left], candidates[right]);
    });
    std::vector<Mask> retained;
    retained.reserve(std::min(candidates.size(), STATE_CAP + 1));
    std::unordered_map<uint32_t, std::vector<uint32_t>> buckets;
    Mask previous{};
    bool have_previous = false;
    size_t visited = 0;
    for (uint32_t index : order) {
        if ((++visited & 4095u) == 0 && std::chrono::steady_clock::now() >= global_deadline) {
            retained.resize(STATE_CAP + 1);
            return retained;
        }
        const Mask &candidate = candidates[index];
        if (have_previous && equal_mask(previous, candidate)) continue;
        previous = candidate;
        have_previous = true;
        if (dominated(candidate, retained, buckets)) continue;
        if (retained.size() > STATE_CAP) break;
        uint32_t retained_index = uint32_t(retained.size());
        retained.push_back(candidate);
        buckets[projection(candidate, 0)].push_back(retained_index);
    }
    std::sort(retained.begin(), retained.end(), [](const Mask &left, const Mask &right) {
        int lp = popcount(left), rp = popcount(right);
        return lp != rp ? lp > rp : lexical(left, right);
    });
    return retained;
}

static std::vector<std::array<int, K>> read_bases(const fs::path &path) {
    std::ifstream input(path);
    std::vector<std::array<int, K>> result;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        std::istringstream row(line);
        std::array<int, K> base{};
        for (int &value : base) if (!(row >> value)) throw std::runtime_error("bad base row");
        result.push_back(base);
    }
    if (result.size() != 100) throw std::runtime_error("base count mismatch");
    return result;
}

static std::vector<std::pair<int, int>> pairs() {
    std::vector<std::pair<int, int>> result;
    for (int left = 0; left < K; ++left) for (int right = left + 1; right < K; ++right) result.emplace_back(left, right);
    return result;
}

static std::array<int, K> requirements(std::pair<int, int> pair) {
    std::array<int, K> result;
    result.fill(-1);
    for (int coordinate = 0; coordinate < pair.first; ++coordinate) result[coordinate] = 1;
    result[pair.first] = 0;
    for (int coordinate = pair.first + 1; coordinate < pair.second; ++coordinate) result[coordinate] = 1;
    result[pair.second] = 0;
    return result;
}

static std::array<std::vector<int>, K> allowed(const std::array<int, K> &base, int leaf) {
    auto all_pairs = pairs();
    auto req2 = requirements(all_pairs[leaf / 78]), req7 = requirements(all_pairs[leaf % 78]);
    std::array<std::vector<int>, K> result;
    for (int coordinate = 0; coordinate < K; ++coordinate) for (int digit = 0; digit < C; ++digit) {
        int residue = (base[coordinate] + P * digit) % C;
        bool good = true;
        if (req2[coordinate] >= 0) good &= ((residue % 2 == 0) == bool(req2[coordinate]));
        if (req7[coordinate] >= 0) good &= ((residue % 7 == 0) == bool(req7[coordinate]));
        if (good) result[coordinate].push_back(digit);
    }
    return result;
}

static std::array<std::array<Mask, C>, K> coverage(const fs::path &path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("missing CNF");
    std::array<std::array<Mask, C>, K> result{};
    std::string line;
    std::getline(input, line);
    int clause = 0;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == 'c') continue;
        ++clause;
        if (clause < 1197 || clause > 3982) continue;
        int time = clause - 1197;
        std::istringstream row(line);
        int literal;
        while (row >> literal && literal != 0) {
            if (literal <= 0 || literal > K * C) throw std::runtime_error("coverage clause literal mismatch");
            int variable = literal - 1;
            result[variable / C][variable % C][time / 64] |= 1ULL << (time % 64);
        }
    }
    if (clause != 4151) throw std::runtime_error("CNF clause count mismatch");
    return result;
}

static std::vector<Row> targets(const fs::path &cycle18, const fs::path &cycle17) {
    std::unordered_set<uint64_t> old;
    {
        std::ifstream input(cycle17);
        std::string line;
        std::getline(input, line);
        while (std::getline(input, line)) {
            std::istringstream row(line);
            std::string base, leaf, status;
            std::getline(row, base, '\t'); std::getline(row, leaf, '\t'); std::getline(row, status, '\t');
            if (status == "NO_LP_DEFICIT") old.insert(uint64_t(std::stoi(base)) * 10000 + std::stoi(leaf));
        }
    }
    std::vector<Row> result;
    std::ifstream input(cycle18);
    std::string line;
    std::getline(input, line);
    while (std::getline(input, line)) {
        std::istringstream row(line);
        std::string base, leaf, status;
        std::getline(row, base, '\t'); std::getline(row, leaf, '\t'); std::getline(row, status, '\t');
        if (status == "UNRESOLVED") {
            Row item{std::stoi(base), std::stoi(leaf)};
            if (!old.contains(uint64_t(item.base) * 10000 + item.leaf)) throw std::runtime_error("target outside Cycle 17 boundary");
            result.push_back(item);
        }
    }
    if (result.size() != 76) throw std::runtime_error("target count mismatch");
    return result;
}

static uint64_t encoded_bytes(size_t count) {
    return 8 + 4 + 4 + 8 + uint64_t(count) * WORDS * 8;
}

static void write_frontier(const fs::path &path, const std::vector<Mask> &frontier) {
    std::ofstream output(path, std::ios::binary);
    const char magic[8] = {'C','1','9','M','A','S','K','1'};
    uint32_t q = Q, words = WORDS;
    uint64_t count = frontier.size();
    output.write(magic, 8);
    output.write(reinterpret_cast<const char *>(&q), 4);
    output.write(reinterpret_cast<const char *>(&words), 4);
    output.write(reinterpret_cast<const char *>(&count), 8);
    for (const Mask &mask : frontier) output.write(reinterpret_cast<const char *>(mask.data()), WORDS * 8);
    if (!output) throw std::runtime_error("frontier write failed");
}

static std::string sha256(const fs::path &path) {
    std::string command = "sha256sum " + path.string();
    FILE *pipe = popen(command.c_str(), "r");
    if (!pipe) throw std::runtime_error("sha256sum failed");
    char buffer[256];
    std::string output = fgets(buffer, sizeof(buffer), pipe) ? buffer : "";
    int status = pclose(pipe);
    if (status != 0 || output.size() < 64) throw std::runtime_error("sha256sum rejected");
    return output.substr(0, 64);
}

static std::pair<std::string, bool> hash_layer(const fs::path &path, const std::vector<Mask> &frontier, bool persistent) {
    uint64_t bytes = encoded_bytes(frontier.size());
    if (persistent) {
        uint64_t before = persistent_bytes.fetch_add(bytes);
        if (before + active_temp_bytes.load() + bytes > DISK_CAP) {
            persistent_bytes.fetch_sub(bytes);
            return {"-", false};
        }
    } else {
        uint64_t before = active_temp_bytes.fetch_add(bytes);
        if (before + persistent_bytes.load() + bytes > DISK_CAP) {
            active_temp_bytes.fetch_sub(bytes);
            return {"-", false};
        }
    }
    write_frontier(path, frontier);
    std::string hash = sha256(path);
    if (!persistent) {
        fs::remove(path);
        active_temp_bytes.fetch_sub(bytes);
    }
    return {hash, true};
}

struct Built {
    std::vector<Mask> frontier;
    std::vector<size_t> counts;
    std::vector<std::string> hashes;
    uint64_t generated = 0;
    bool cap = false;
    std::string detail;
};

static Built build_side(
    const std::vector<int> &coordinates, const std::array<std::vector<int>, K> &digits,
    const std::array<std::array<Mask, C>, K> &masks, const fs::path &scratch,
    std::chrono::steady_clock::time_point deadline
) {
    Built result;
    result.frontier.push_back(Mask{});
    for (int coordinate : coordinates) {
        std::vector<Mask> next;
        for (int digit : digits[coordinate]) {
            if (std::chrono::steady_clock::now() >= deadline) {
                result.cap = true; result.detail = "aggregate wall cap"; return result;
            }
            if (result.generated + result.frontier.size() > CHILD_CAP) {
                result.cap = true; result.detail = "generated-child cap"; return result;
            }
            result.generated += result.frontier.size();
            std::vector<Mask> candidates;
            candidates.reserve(next.size() + result.frontier.size());
            candidates.insert(candidates.end(), next.begin(), next.end());
            for (const Mask &parent : result.frontier) {
                Mask child = parent;
                for (int word = 0; word < WORDS; ++word) child[word] |= masks[coordinate][digit][word];
                candidates.push_back(child);
            }
            next = maximalize(std::move(candidates));
            if (next.size() > STATE_CAP) {
                result.cap = true; result.detail = "frontier-state cap"; return result;
            }
        }
        result.frontier = std::move(next);
        result.counts.push_back(result.frontier.size());
        auto [hash, okay] = hash_layer(scratch, result.frontier, false);
        if (!okay) { result.cap = true; result.detail = "temporary-disk cap"; return result; }
        result.hashes.push_back(hash);
    }
    return result;
}

static bool has_cover(const std::vector<Mask> &left, const std::vector<Mask> &right, uint64_t &queries) {
    std::unordered_map<uint32_t, std::vector<uint32_t>> buckets;
    for (uint32_t index = 0; index < right.size(); ++index) buckets[projection(right[index], 0)].push_back(index);
    Mask full{};
    full.fill(~0ULL);
    if (Q % 64) full.back() = (1ULL << (Q % 64)) - 1;
    for (const Mask &mask : left) {
        Mask need{};
        for (int word = 0; word < WORDS; ++word) need[word] = full[word] & ~mask[word];
        uint32_t key = projection(need, 0), key2 = projection(need, 1);
        uint32_t missing = (~key) & ((1u << 20) - 1);
        uint64_t supersets = 1ULL << std::popcount(missing);
        if (supersets > right.size()) {
            for (const Mask &other : right) {
                ++queries;
                if ((projection(other, 0) & key) == key && (projection(other, 1) & key2) == key2 && subset(need, other)) return true;
            }
            continue;
        }
        uint32_t subkey = missing;
        while (true) {
            uint32_t supkey = key | subkey;
            auto found = buckets.find(supkey);
            if (found != buckets.end()) for (uint32_t index : found->second) {
                ++queries;
                if ((projection(right[index], 1) & key2) == key2 && subset(need, right[index])) return true;
            }
            if (subkey == 0) break;
            subkey = (subkey - 1) & missing;
        }
    }
    return false;
}

static Result solve(
    Row target, const std::array<int, K> &base, const std::array<std::array<Mask, C>, K> &masks,
    const fs::path &out, std::chrono::steady_clock::time_point deadline, int worker
) {
    auto started = std::chrono::steady_clock::now();
    Result result;
    result.base = target.base; result.leaf = target.leaf;
    auto digits = allowed(base, target.leaf);
    fs::path scratch = out / ("scratch-" + std::to_string(worker) + ".bin");
    Built left = build_side({0,1,2,3,4,5,6}, digits, masks, scratch, deadline);
    result.generated += left.generated;
    for (size_t index = 0; index < left.counts.size(); ++index) {
        result.left_counts[index] = left.counts[index]; result.left_hashes[index] = left.hashes[index];
    }
    if (left.cap) { result.detail = "left: " + left.detail; goto done; }
    {
        Built right = build_side({7,8,9,10,11,12}, digits, masks, scratch, deadline);
        result.generated += right.generated;
        for (size_t index = 0; index < right.counts.size(); ++index) {
            result.right_counts[index] = right.counts[index]; result.right_hashes[index] = right.hashes[index];
        }
        if (right.cap) { result.detail = "right: " + right.detail; goto done; }
        fs::path frontiers = out / "frontiers";
        result.left_path = (frontiers / (std::to_string(target.base) + "-" + std::to_string(target.leaf) + "-L.bin")).string();
        result.right_path = (frontiers / (std::to_string(target.base) + "-" + std::to_string(target.leaf) + "-R.bin")).string();
        {
            auto [hash, okay] = hash_layer(result.left_path, left.frontier, true);
            if (!okay) { result.detail = "persistent-disk cap before left"; goto done; }
            result.left_hash = hash;
        }
        {
            auto [hash, okay] = hash_layer(result.right_path, right.frontier, true);
            if (!okay) { result.detail = "persistent-disk cap before right"; goto done; }
            result.right_hash = hash;
        }
        if (has_cover(left.frontier, right.frontier, result.queries)) {
            result.status = "FULL_COVER_CANDIDATE";
            result.detail = "exact frontier pair covers all times; witness reconstruction required";
        } else {
            result.status = "CERTIFIED_NO_COVER";
            result.detail = "complete maximal antichains and exact complement query";
        }
    }
done:
    result.seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    return result;
}

static std::string join_counts(const auto &values) {
    std::ostringstream out;
    for (size_t index = 0; index < values.size(); ++index) { if (index) out << ','; out << values[index]; }
    return out.str();
}

static std::string join_hashes(const auto &values) {
    std::ostringstream out;
    for (size_t index = 0; index < values.size(); ++index) { if (index) out << ','; out << (values[index].empty() ? "-" : values[index]); }
    return out.str();
}

int main(int argc, char **argv) {
    if (argc != 7) {
        std::cerr << "usage: engine BASES CNF4 CNF3 CYCLE18 CYCLE17 OUT\n";
        return 2;
    }
    try {
        fs::path out = argv[6];
        fs::create_directories(out / "frontiers");
        auto bases = read_bases(argv[1]);
        std::array<std::array<std::array<Mask, C>, K>, 2> coverages{coverage(argv[2]), coverage(argv[3])};
        auto jobs = targets(argv[4], argv[5]);
        std::vector<Result> results(jobs.size());
        std::atomic<size_t> next{0};
        auto deadline = std::chrono::steady_clock::now() + std::chrono::seconds(3500);
        global_deadline = deadline;
        auto worker = [&](int worker_index) {
            while (true) {
                size_t index = next.fetch_add(1);
                if (index >= jobs.size()) return;
                int group = jobs[index].base == 4 ? 0 : 1;
                results[index] = solve(jobs[index], bases[jobs[index].base], coverages[group], out, deadline, worker_index);
                std::cout << "completed=" << (index + 1) << " base=" << jobs[index].base << " leaf=" << jobs[index].leaf << " status=" << results[index].status << "\n" << std::flush;
            }
        };
        std::vector<std::thread> workers;
        for (int index = 0; index < 3; ++index) workers.emplace_back(worker, index);
        for (auto &thread : workers) thread.join();
        std::ofstream output(out / "results.tsv");
        output << "base_index\tleaf_ordinal\tstatus\tleft_counts\tleft_hashes\tright_counts\tright_hashes\tleft_path\tleft_sha256\tright_path\tright_sha256\tgenerated_children\tquery_checks\tseconds\tdetail\n";
        for (const Result &row : results) {
            output << row.base << '\t' << row.leaf << '\t' << row.status << '\t' << join_counts(row.left_counts) << '\t' << join_hashes(row.left_hashes)
                   << '\t' << join_counts(row.right_counts) << '\t' << join_hashes(row.right_hashes) << '\t' << row.left_path << '\t' << row.left_hash
                   << '\t' << row.right_path << '\t' << row.right_hash << '\t' << row.generated << '\t' << row.queries << '\t' << row.seconds << '\t' << row.detail << '\n';
        }
        int certified = std::count_if(results.begin(), results.end(), [](const Result &row) { return row.status == "CERTIFIED_NO_COVER"; });
        int capped = std::count_if(results.begin(), results.end(), [](const Result &row) { return row.status == "CAP"; });
        int candidates = std::count_if(results.begin(), results.end(), [](const Result &row) { return row.status == "FULL_COVER_CANDIDATE"; });
        std::string summary = "rows=76 certified_no_cover=" + std::to_string(certified) + " cap=" + std::to_string(capped) + " full_cover_candidates=" + std::to_string(candidates) + " persistent_bytes=" + std::to_string(persistent_bytes.load());
        std::ofstream result_file(out / "result.txt"); result_file << summary << '\n';
        std::cout << summary << '\n';
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
