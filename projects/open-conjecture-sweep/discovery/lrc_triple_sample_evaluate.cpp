#define main cycle3_in_memory_main
#include "lrc_coverage_levels.cpp"
#undef main

#include <fstream>
#include <optional>
#include <unordered_map>

namespace {

struct Triple { int a, b, c; };

bool includes(Mask const& mask, int value) {
  return (mask[static_cast<std::size_t>(value / 64)] & (1ULL << (value % 64))) != 0;
}

Mask subtract(Mask left, Mask const& right, int words) {
  for (int word = 0; word < words; ++word) {
    left[static_cast<std::size_t>(word)] &= ~right[static_cast<std::size_t>(word)];
  }
  return left;
}

class WeakColorSolver {
 public:
  WeakColorSolver(int vertices, std::vector<Triple> triples, std::vector<int> const& active_vertices,
                  int colors, std::uint64_t cap)
      : h_(vertices), colors_(colors), cap_(cap), full_domain_((1U << colors) - 1U),
        triples_(std::move(triples)) {
    for (int index = 0; index < static_cast<int>(triples_.size()); ++index) {
      Triple triple = triples_[static_cast<std::size_t>(index)];
      incident_[static_cast<std::size_t>(triple.a)].push_back(index);
      incident_[static_cast<std::size_t>(triple.b)].push_back(index);
      incident_[static_cast<std::size_t>(triple.c)].push_back(index);
    }
    for (int vertex : active_vertices) {
      active_[static_cast<std::size_t>(vertex)] = true;
    }
  }

  enum class Result { SAT, UNSAT, CAP };

  Result solve() {
    std::array<std::uint8_t, MAX_H> domain{};
    for (int vertex = 0; vertex < h_; ++vertex) {
      if (active_[static_cast<std::size_t>(vertex)]) domain[static_cast<std::size_t>(vertex)] = full_domain_;
    }
    return search(domain);
  }

  std::uint64_t nodes() const { return nodes_; }
  std::size_t triple_count() const { return triples_.size(); }
  std::vector<Triple> const& triples() const { return triples_; }

 private:
  static constexpr int MAX_H = 127;
  int h_;
  int colors_;
  std::uint64_t cap_;
  std::uint8_t full_domain_;
  std::vector<Triple> triples_;
  std::array<std::vector<int>, MAX_H> incident_{};
  std::array<bool, MAX_H> active_{};
  std::uint64_t nodes_ = 0;

  static int pop(std::uint8_t value) { return __builtin_popcount(static_cast<unsigned>(value)); }
  static bool singleton(std::uint8_t value) { return value && (value & (value - 1U)) == 0; }

  bool propagate(std::array<std::uint8_t, MAX_H>& domain, std::vector<int> changed) const {
    for (std::size_t cursor = 0; cursor < changed.size(); ++cursor) {
      int changed_vertex = changed[cursor];
      for (int triple_index : incident_[static_cast<std::size_t>(changed_vertex)]) {
        Triple triple = triples_[static_cast<std::size_t>(triple_index)];
        std::array<int, 3> vertices{triple.a, triple.b, triple.c};
        for (int color = 0; color < colors_; ++color) {
          std::uint8_t bit = static_cast<std::uint8_t>(1U << color);
          int fixed = 0;
          int candidate = -1;
          for (int vertex : vertices) {
            std::uint8_t value = domain[static_cast<std::size_t>(vertex)];
            if (value == bit) ++fixed;
            else if (value & bit) candidate = vertex;
          }
          if (fixed == 3) return false;
          if (fixed == 2 && candidate >= 0) {
            std::uint8_t& value = domain[static_cast<std::size_t>(candidate)];
            std::uint8_t old = value;
            value = static_cast<std::uint8_t>(value & ~bit);
            if (!value) return false;
            if (value != old) changed.push_back(candidate);
          }
        }
      }
    }
    return true;
  }

  Result search(std::array<std::uint8_t, MAX_H> domain) {
    if (nodes_++ >= cap_) return Result::CAP;
    int chosen = -1;
    int best_domain = colors_ + 1;
    int best_incident = -1;
    for (int vertex = 0; vertex < h_; ++vertex) {
      std::uint8_t value = domain[static_cast<std::size_t>(vertex)];
      if (!active_[static_cast<std::size_t>(vertex)] || singleton(value)) continue;
      int width = pop(value);
      int degree = static_cast<int>(incident_[static_cast<std::size_t>(vertex)].size());
      if (width < best_domain || (width == best_domain && degree > best_incident)) {
        chosen = vertex;
        best_domain = width;
        best_incident = degree;
      }
    }
    if (chosen < 0) return Result::SAT;
    std::uint8_t options = domain[static_cast<std::size_t>(chosen)];
    int max_used = -1;
    for (int vertex = 0; vertex < h_; ++vertex) {
      std::uint8_t value = domain[static_cast<std::size_t>(vertex)];
      if (!active_[static_cast<std::size_t>(vertex)] || !singleton(value)) continue;
      max_used = std::max(max_used, __builtin_ctz(static_cast<unsigned>(value)));
    }
    int max_new_color = std::min(colors_ - 1, max_used + 1);
    for (int color = 0; color <= max_new_color; ++color) {
      std::uint8_t bit = static_cast<std::uint8_t>(1U << color);
      if (!(options & bit)) continue;
      auto next = domain;
      next[static_cast<std::size_t>(chosen)] = bit;
      Result result = propagate(next, {chosen}) ? search(next) : Result::UNSAT;
      if (result != Result::UNSAT) return result;
    }
    return Result::UNSAT;
  }
};

bool common_cover_recheck(Engine const& engine, Triple triple) {
  for (Mask const& cover : engine.covers) {
    if (includes(cover, triple.a) && includes(cover, triple.b) && includes(cover, triple.c)) return false;
  }
  return true;
}

bool find_triple_clique(std::vector<int> candidates, int need,
                        std::vector<char> const& forbidden, int h,
                        std::vector<int>& chosen, bool require_forbidden) {
  if (static_cast<int>(chosen.size()) == need) return true;
  if (static_cast<int>(chosen.size() + candidates.size()) < need) return false;
  while (static_cast<int>(chosen.size() + candidates.size()) >= need) {
    int vertex = candidates.front();
    candidates.erase(candidates.begin());
    std::vector<int> next;
    for (int candidate : candidates) {
      bool compatible = true;
      for (std::size_t left = 0; left < chosen.size() && compatible; ++left) {
        for (std::size_t right = 0; right < left; ++right) {
          std::array<int, 3> triple{chosen[right], chosen[left], candidate};
          std::sort(triple.begin(), triple.end());
          bool is_forbidden = forbidden[static_cast<std::size_t>((triple[0] * h + triple[1]) * h + triple[2])];
          if (is_forbidden != require_forbidden) {
            compatible = false;
            break;
          }
        }
      }
      if (compatible) next.push_back(candidate);
    }
    chosen.push_back(vertex);
    if (find_triple_clique(next, need, forbidden, h, chosen, require_forbidden)) return true;
    chosen.pop_back();
  }
  return false;
}

bool direct_coverable(Engine const& engine, Mask uncovered, int remaining,
                      std::unordered_map<std::string, bool>& memo) {
  if (uncovered == Mask{}) return true;
  if (remaining == 0) return false;
  std::string key(reinterpret_cast<char const*>(uncovered.data()), sizeof(uncovered));
  key.push_back(static_cast<char>(remaining));
  if (auto found = memo.find(key); found != memo.end()) return found->second;
  int target = engine.first_uncovered(subtract(engine.full, uncovered, engine.words));
  bool result = false;
  for (int center : engine.covering_centers[static_cast<std::size_t>(target)]) {
    if (direct_coverable(engine, subtract(uncovered, engine.covers[static_cast<std::size_t>(center)], engine.words),
                         remaining - 1, memo)) {
      result = true;
      break;
    }
  }
  memo.emplace(std::move(key), result);
  return result;
}

}  // namespace

int main(int argc, char** argv) try {
  bool minimize_core = argc == 5 && std::string(argv[4]) == "--minimize-core";
  if (argc != 4 && !minimize_core) {
    std::cerr << "usage: lrc_triple_sample_evaluate INPUT OUTPUT NODE_CAP [--minimize-core]\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  std::ofstream output(argv[2]);
  std::uint64_t node_cap = std::stoull(argv[3]);
  bool direct_only = std::getenv("LRC_TRIPLE_DIRECT_ONLY") != nullptr;
  Engine engine(13, 199);
  std::vector<Triple> forbidden;
  std::vector<char> forbidden_lookup(static_cast<std::size_t>(engine.h * engine.h * engine.h), 0);
  for (int a = 0; a < engine.h; ++a) {
    for (int b = a + 1; b < engine.h; ++b) {
      for (int c = b + 1; c < engine.h; ++c) {
        bool common = false;
        for (Mask const& cover : engine.covers) {
          if (includes(cover, a) && includes(cover, b) && includes(cover, c)) {
            common = true;
            break;
          }
        }
        if (!common) {
          forbidden.push_back({a, b, c});
          forbidden_lookup[static_cast<std::size_t>((a * engine.h + b) * engine.h + c)] = 1;
        }
      }
    }
  }
  std::uint64_t rows = 0, sat = 0, unsat = 0, capped = 0, clique_prunes = 0,
      direct_errors = 0, total_nodes = 0;
  auto relevant_triples = [&](std::vector<int> const& vertices) {
    std::vector<Triple> relevant;
    for (std::size_t left = 0; left < vertices.size(); ++left) {
      for (std::size_t middle = left + 1; middle < vertices.size(); ++middle) {
        for (std::size_t right = middle + 1; right < vertices.size(); ++right) {
          int a = vertices[left], b = vertices[middle], c = vertices[right];
          if (forbidden_lookup[static_cast<std::size_t>((a * engine.h + b) * engine.h + c)]) {
            relevant.push_back({a, b, c});
          }
        }
      }
    }
    return relevant;
  };
  State state;
  while (true) {
    state = {};
    for (int index = 0; index < 8; ++index) {
      int value;
      if (!(input >> value)) goto done;
      state.value[static_cast<std::size_t>(index)] = static_cast<std::uint8_t>(value);
    }
    Mask covered = engine.covered_by(state, 8);
    Mask uncovered = subtract(engine.full, covered, engine.words);
    std::vector<int> vertices;
    for (int vertex = 0; vertex < engine.h; ++vertex) {
      if (includes(uncovered, vertex)) vertices.push_back(vertex);
    }
    if (direct_only) {
      std::unordered_map<std::string, bool> memo;
      bool feasible = direct_coverable(engine, uncovered, 5, memo);
      if (feasible) ++sat;
      else ++unsat;
      output << (feasible ? "DIRECT_SAT" : "DIRECT_UNSAT") << ' '
             << popcount(uncovered, engine.words) << " 0 0 0\n";
      ++rows;
      continue;
    }
    std::vector<int> clique;
    bool has_clique = find_triple_clique(vertices, 11, forbidden_lookup, engine.h, clique, true);
    std::vector<int> independent;
    bool has_independent_seven = find_triple_clique(vertices, 7, forbidden_lookup, engine.h, independent, false);
    bool alpha_bound_unsat = !has_independent_seven && vertices.size() > 30;
    WeakColorSolver solver(engine.h, relevant_triples(vertices), vertices, 5, node_cap);
    auto result = (alpha_bound_unsat || has_clique) ? WeakColorSolver::Result::UNSAT : solver.solve();
    total_nodes += solver.nodes();
    char const* label = alpha_bound_unsat ? "ALPHA_UNSAT" : has_clique ? "CLIQUE_UNSAT" :
                        result == WeakColorSolver::Result::SAT ? "SAT" :
                        result == WeakColorSolver::Result::UNSAT ? "UNSAT" : "CAP";
    if (result == WeakColorSolver::Result::SAT) ++sat;
    else if (result == WeakColorSolver::Result::UNSAT) {
      ++unsat;
      if (alpha_bound_unsat) {
        ++clique_prunes;
      } else if (has_clique) {
        ++clique_prunes;
        for (std::size_t left = 0; left < clique.size(); ++left) {
          for (std::size_t middle = left + 1; middle < clique.size(); ++middle) {
            for (std::size_t right = middle + 1; right < clique.size(); ++right) {
              if (!common_cover_recheck(engine, {clique[left], clique[middle], clique[right]})) {
                throw std::runtime_error("clique triple recheck failed");
              }
            }
          }
        }
      }
      if (!has_clique) {
        for (Triple triple : solver.triples()) {
          if (!common_cover_recheck(engine, triple)) throw std::runtime_error("triple recheck failed");
        }
      }
      if (!direct_only && std::getenv("LRC_TRIPLE_SKIP_DIRECT") == nullptr) {
        std::unordered_map<std::string, bool> memo;
        if (direct_coverable(engine, uncovered, 5, memo)) ++direct_errors;
      }
    } else ++capped;
    output << label << ' ' << popcount(uncovered, engine.words) << ' ' << solver.triple_count()
           << ' ' << solver.nodes() << ' ' << clique.size() << '\n';
    ++rows;
    if (minimize_core && result == WeakColorSolver::Result::UNSAT) {
      std::vector<int> core = vertices;
      for (std::size_t index = 0; index < core.size();) {
        std::vector<int> trial = core;
        trial.erase(trial.begin() + static_cast<std::ptrdiff_t>(index));
        WeakColorSolver trial_solver(engine.h, relevant_triples(trial), trial, 5, node_cap);
        if (trial_solver.solve() == WeakColorSolver::Result::UNSAT) core = std::move(trial);
        else ++index;
      }
      output << "core_size=" << core.size() << " core_vertices=";
      for (int vertex : core) output << vertex << ',';
      output << '\n';
      break;
    }
  }
done:
  if (!input.eof() && !minimize_core) throw std::runtime_error("malformed sample input");
  output << "summary rows=" << rows << " sat=" << sat << " unsat=" << unsat
         << " cap=" << capped << " clique_prunes=" << clique_prunes << " direct_errors=" << direct_errors
         << " total_nodes=" << total_nodes << " forbidden=" << forbidden.size() << '\n';
  if (!output) throw std::runtime_error("output failure");
  return direct_errors == 0 ? 0 : 3;
} catch (std::exception const& error) {
  std::cerr << "fatal=" << error.what() << '\n';
  return 4;
}
