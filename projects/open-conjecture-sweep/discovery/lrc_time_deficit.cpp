// Cycle 17 exact bounded-support weighted time-deficit search.

#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

using Mask = std::array<uint16_t, 13>;

struct Signature {
    int source_clause;
    Mask masks;
};

struct Certificate {
    std::string status = "UNCOVERED";
    std::vector<int> clauses;
    std::vector<int> weights;
    int total_weight = 0;
    int capacity = 0;
    std::array<int, 13> maxima{};
    int pool_size = 0;
};

static std::vector<std::array<int, 13>> read_bases(const std::string &path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot read bases");
    std::vector<std::array<int, 13>> bases;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        std::istringstream row(line);
        std::array<int, 13> base{};
        for (int &value : base) if (!(row >> value)) throw std::runtime_error("bad base row");
        bases.push_back(base);
    }
    if (bases.size() != 100) throw std::runtime_error("expected 100 bases");
    return bases;
}

static std::vector<Signature> read_time_signatures(const std::string &path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot read CNF");
    std::string line;
    std::getline(input, line);
    std::map<Mask, int> first;
    int clause_index = 0;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == 'c') continue;
        ++clause_index;
        if (clause_index < 1197 || clause_index > 3982) continue;
        std::istringstream row(line);
        int literal;
        Mask masks{};
        while (row >> literal && literal != 0) {
            if (literal <= 0 || literal > 182) throw std::runtime_error("non-choice literal in time clause");
            int variable = literal - 1;
            masks[variable / 14] |= uint16_t(1u << (variable % 14));
        }
        first.emplace(masks, clause_index);
    }
    if (clause_index != 4151 || first.empty()) throw std::runtime_error("CNF layout mismatch");
    std::vector<Signature> signatures;
    for (const auto &[masks, source] : first) signatures.push_back({source, masks});
    std::sort(signatures.begin(), signatures.end(), [](const auto &left, const auto &right) {
        return left.source_clause < right.source_clause;
    });
    return signatures;
}

static std::vector<std::pair<int, int>> pairs() {
    std::vector<std::pair<int, int>> result;
    for (int i = 0; i < 13; ++i) for (int j = i + 1; j < 13; ++j) result.emplace_back(i, j);
    return result;
}

static std::array<int, 13> requirements(std::pair<int, int> pair) {
    std::array<int, 13> req;
    req.fill(-1);
    for (int coordinate = 0; coordinate < pair.first; ++coordinate) req[coordinate] = 1;
    req[pair.first] = 0;
    for (int coordinate = pair.first + 1; coordinate < pair.second; ++coordinate) req[coordinate] = 1;
    req[pair.second] = 0;
    return req;
}

static std::array<uint16_t, 13> allowed_masks(const std::array<int, 13> &base, int ordinal) {
    const auto all_pairs = pairs();
    const auto req2 = requirements(all_pairs[ordinal / 78]);
    const auto req7 = requirements(all_pairs[ordinal % 78]);
    std::array<uint16_t, 13> allowed{};
    for (int coordinate = 0; coordinate < 13; ++coordinate) {
        for (int digit = 0; digit < 14; ++digit) {
            int residue = (base[coordinate] + 199 * digit) % 14;
            bool good = true;
            if (req2[coordinate] >= 0) good &= ((residue % 2 == 0) == bool(req2[coordinate]));
            if (req7[coordinate] >= 0) good &= ((residue % 7 == 0) == bool(req7[coordinate]));
            if (good) allowed[coordinate] |= uint16_t(1u << digit);
        }
    }
    return allowed;
}

static std::pair<int, std::array<int, 13>> capacity(
    const std::array<uint16_t, 13> &allowed,
    const std::vector<const Signature *> &support,
    const std::vector<int> &weights
) {
    std::array<int, 13> maxima{};
    int total = 0;
    for (int coordinate = 0; coordinate < 13; ++coordinate) {
        int best = 0;
        for (int digit = 0; digit < 14; ++digit) {
            if (!(allowed[coordinate] & uint16_t(1u << digit))) continue;
            int score = 0;
            for (size_t index = 0; index < support.size(); ++index)
                if (support[index]->masks[coordinate] & uint16_t(1u << digit)) score += weights[index];
            best = std::max(best, score);
        }
        maxima[coordinate] = best;
        total += best;
    }
    return {total, maxima};
}

static Certificate solve_leaf(const std::array<int, 13> &base, int ordinal, const std::vector<Signature> &signatures) {
    Certificate result;
    auto allowed = allowed_masks(base, ordinal);
    if (std::any_of(allowed.begin(), allowed.end(), [](uint16_t mask) { return mask == 0; })) {
        result.status = "EMPTY_DOMAIN";
        return result;
    }
    std::vector<std::pair<int, const Signature *>> ranked;
    for (const auto &signature : signatures) {
        int singleton = 0;
        for (int coordinate = 0; coordinate < 13; ++coordinate)
            singleton += bool(allowed[coordinate] & signature.masks[coordinate]);
        if (singleton == 0) {
            result.status = "CERTIFIED_DEFICIT";
            result.clauses = {signature.source_clause};
            result.weights = {1};
            result.total_weight = 1;
            result.capacity = 0;
            return result;
        }
        if (singleton <= 5) ranked.emplace_back(singleton, &signature);
    }
    std::sort(ranked.begin(), ranked.end(), [](const auto &left, const auto &right) {
        if (left.first != right.first) return left.first < right.first;
        if (left.second->source_clause != right.second->source_clause) return left.second->source_clause < right.second->source_clause;
        return left.second->masks < right.second->masks;
    });
    if (ranked.size() > 24) ranked.resize(24);
    result.pool_size = int(ranked.size());
    for (int weight_sum = 2; weight_sum <= 6; ++weight_sum) {
        for (int support_size = 2; support_size <= 3; ++support_size) {
            if (support_size > int(ranked.size()) || support_size > weight_sum) continue;
            for (int a = 0; a < int(ranked.size()); ++a) {
                int b_start = a + 1;
                for (int b = b_start; b < int(ranked.size()); ++b) {
                    int c_start = support_size == 3 ? b + 1 : b;
                    int c_end = support_size == 3 ? int(ranked.size()) : b + 1;
                    for (int c = c_start; c < c_end; ++c) {
                        for (int w1 = 1; w1 <= weight_sum - support_size + 1; ++w1) {
                            int w2_max = support_size == 2 ? weight_sum - w1 : weight_sum - w1 - 1;
                            for (int w2 = 1; w2 <= w2_max; ++w2) {
                                int w3 = support_size == 3 ? weight_sum - w1 - w2 : 0;
                                if ((support_size == 2 && w1 + w2 != weight_sum) || (support_size == 3 && w3 < 1)) continue;
                                std::vector<const Signature *> support = {ranked[a].second, ranked[b].second};
                                std::vector<int> weights = {w1, w2};
                                if (support_size == 3) { support.push_back(ranked[c].second); weights.push_back(w3); }
                                bool impossible = false;
                                for (int index = 0; index < support_size; ++index)
                                    if (weights[index] * ranked[index == 0 ? a : (index == 1 ? b : c)].first >= weight_sum) impossible = true;
                                if (impossible) continue;
                                auto [upper, maxima] = capacity(allowed, support, weights);
                                if (upper < weight_sum) {
                                    result.status = "CERTIFIED_DEFICIT";
                                    for (const auto *signature : support) result.clauses.push_back(signature->source_clause);
                                    result.weights = weights;
                                    result.total_weight = weight_sum;
                                    result.capacity = upper;
                                    result.maxima = maxima;
                                    return result;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return result;
}

static std::string join(const std::vector<int> &values) {
    std::ostringstream out;
    for (size_t index = 0; index < values.size(); ++index) {
        if (index) out << ',';
        out << values[index];
    }
    return out.str();
}

static std::string join(const std::array<int, 13> &values) {
    std::ostringstream out;
    for (size_t index = 0; index < values.size(); ++index) {
        if (index) out << ',';
        out << values[index];
    }
    return out.str();
}

int main(int argc, char **argv) {
    if (argc != 6) {
        std::cerr << "usage: lrc_time_deficit BASES CNF4 CNF3 CNF7 OUTPUT\n";
        return 2;
    }
    try {
        auto bases = read_bases(argv[1]);
        std::array<std::vector<Signature>, 2> signatures{
            read_time_signatures(argv[2]), read_time_signatures(argv[3])
        };
        auto control_signatures = read_time_signatures(argv[4]);
        Certificate control = solve_leaf(bases[7], 74, control_signatures);
        if (control.status != "CERTIFIED_DEFICIT" || control.total_weight != 1 || control.capacity != 0)
            throw std::runtime_error("base-7 leaf-74 positive control failed");
        std::array<int, 2> base_indices{4, 3};
        std::array<std::vector<Certificate>, 2> results;
        for (auto &rows : results) rows.resize(6084);
        std::atomic<int> next{0};
        auto worker = [&]() {
            while (true) {
                int job = next.fetch_add(1);
                if (job >= 12168) return;
                int group = job / 6084, ordinal = job % 6084;
                results[group][ordinal] = solve_leaf(bases[base_indices[group]], ordinal, signatures[group]);
            }
        };
        std::vector<std::thread> workers;
        for (int index = 0; index < 3; ++index) workers.emplace_back(worker);
        for (auto &thread : workers) thread.join();
        std::ofstream output(argv[5]);
        if (!output) throw std::runtime_error("cannot write output");
        output << "base_index\tleaf_ordinal\tstatus\tsource_clauses\tweights\tW\tU\tcoordinate_maxima\tpool_size\n";
        for (int group = 0; group < 2; ++group) for (int ordinal = 0; ordinal < 6084; ++ordinal) {
            const auto &row = results[group][ordinal];
            output << base_indices[group] << '\t' << ordinal << '\t' << row.status << '\t'
                   << join(row.clauses) << '\t' << join(row.weights) << '\t' << row.total_weight << '\t'
                   << row.capacity << '\t' << join(row.maxima) << '\t' << row.pool_size << '\n';
        }
        for (int group = 0; group < 2; ++group) {
            int certified = std::count_if(results[group].begin(), results[group].end(), [](const auto &row) {
                return row.status == "CERTIFIED_DEFICIT" || row.status == "EMPTY_DOMAIN";
            });
            std::cout << "base=" << base_indices[group] << " certified=" << certified
                      << " uncovered=" << 6084 - certified << '\n';
        }
        std::cout << "unique_time_signatures_base4=" << signatures[0].size()
                  << " unique_time_signatures_base3=" << signatures[1].size()
                  << " unique_time_signatures_control=" << control_signatures.size() << " control=PASS\n";
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
