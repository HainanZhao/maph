#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Clause = std::vector<int>;

struct Cube {
  int n;
  std::vector<std::pair<int, int>> edges;
  std::map<std::pair<int, int>, int> edge_var;
  std::vector<std::array<int, 4>> squares;
};

static Cube make_cube(int n) {
  Cube c{n, {}, {}, {}};
  const int vertices = 1 << n;
  for (int d = 0; d < n; ++d) {
    for (int u = 0; u < vertices; ++u) {
      if ((u >> d) & 1) continue;
      int v = u ^ (1 << d);
      int id = static_cast<int>(c.edges.size()) + 1;
      c.edges.push_back({u, v});
      c.edge_var[{u, v}] = id;
    }
  }
  auto edge = [&](int a, int b) {
    if (a > b) std::swap(a, b);
    return c.edge_var.at({a, b});
  };
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      for (int b = 0; b < vertices; ++b) {
        if (((b >> i) & 1) || ((b >> j) & 1)) continue;
        int bi = b ^ (1 << i), bj = b ^ (1 << j);
        int bij = b ^ (1 << i) ^ (1 << j);
        c.squares.push_back({edge(b, bi), edge(b, bj), edge(bi, bij),
                             edge(bj, bij)});
      }
    }
  }
  return c;
}

// Sinz sequential counter for at most k true input literals.  Here each input
// literal is -e: an absent cube edge.  Thus at most m-target absent edges is
// equivalent to at least target selected edges.
static void add_at_most_absent(int first_aux, int m, int k,
                               std::vector<Clause>& clauses) {
  if (k < 0) {
    clauses.push_back({});
    return;
  }
  if (k >= m) return;
  if (k == 0) {
    for (int e = 1; e <= m; ++e) clauses.push_back({e});
    return;
  }
  auto s = [&](int i, int j) { return first_aux + (i - 1) * k + (j - 1); };
  // Input y_i means edge i is absent, so -y_i is the positive edge literal i.
  for (int i = 1; i <= m - 1; ++i) clauses.push_back({i, s(i, 1)});
  for (int i = 2; i <= m - 1; ++i)
    clauses.push_back({-s(i - 1, 1), s(i, 1)});
  for (int i = 2; i <= m - 1; ++i) {
    for (int j = 2; j <= k; ++j) {
      clauses.push_back({i, -s(i - 1, j - 1), s(i, j)});
      clauses.push_back({-s(i - 1, j), s(i, j)});
    }
  }
  for (int i = 2; i <= m; ++i) clauses.push_back({i, -s(i - 1, k)});
}

int main(int argc, char** argv) {
  if (argc != 4 && argc != 5) {
    std::cerr << "usage: cycle73_hypercube_cnf N TARGET_EDGES OUTPUT.cnf"
                 " [MAX_DEGREE]\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  const int target = std::stoi(argv[2]);
  const std::string out_path = argv[3];
  const int max_degree = argc == 5 ? std::stoi(argv[4]) : -1;
  if (n < 2 || n > 12) throw std::runtime_error("unsupported dimension");
  if (max_degree != -1 && (max_degree < 1 || max_degree > n))
    throw std::runtime_error("bad maximum-degree branch");
  Cube cube = make_cube(n);
  const int m = static_cast<int>(cube.edges.size());
  if (target < 1 || target > m) throw std::runtime_error("bad target");
  std::vector<Clause> clauses;
  clauses.reserve(cube.squares.size() + m * (m - target + 1) * 2);
  for (const auto& q : cube.squares)
    clauses.push_back({-q[0], -q[1], -q[2], -q[3]});
  const int absent_cap = m - target;
  const int first_aux = m + 1;
  add_at_most_absent(first_aux, m, absent_cap, clauses);
  auto edge = [&](int a, int b) {
    if (a > b) std::swap(a, b);
    return cube.edge_var.at({a, b});
  };
  if (max_degree == -1) {
    // Any nonempty edge set can be mapped by Aut(Q_n) to contain edge 1.
    clauses.push_back({1});
  } else {
    // Translate a maximum-degree vertex to zero, then permute coordinates so
    // its selected incident directions are the first max_degree directions.
    for (int d = 0; d < n; ++d)
      clauses.push_back({d < max_degree ? edge(0, 1 << d)
                                        : -edge(0, 1 << d)});
    // This also proves that the chosen vertex really is maximum degree.
    for (int v = 0; v < (1 << n); ++v) {
      std::vector<int> incident;
      for (int d = 0; d < n; ++d) incident.push_back(edge(v, v ^ (1 << d)));
      for (unsigned mask = 0; mask < (1u << n); ++mask) {
        if (std::popcount(mask) != max_degree + 1) continue;
        Clause clause;
        for (int d = 0; d < n; ++d)
          if ((mask >> d) & 1u) clause.push_back(-incident[d]);
        clauses.push_back(std::move(clause));
      }
    }
  }
  int variables = m;
  if (absent_cap > 0 && absent_cap < m)
    variables = first_aux + (m - 1) * absent_cap - 1;

  std::ofstream out(out_path);
  if (!out) throw std::runtime_error("cannot open output");
  out << "c cycle73 canonical Q_" << n << " C4-free cardinality >= "
      << target << "\n";
  out << "c edge variables 1.." << m << "; max-degree branch "
      << max_degree << "\n";
  for (int id = 1; id <= m; ++id)
    out << "c edge " << id << " " << cube.edges[id - 1].first << " "
        << cube.edges[id - 1].second << "\n";
  out << "p cnf " << variables << " " << clauses.size() << "\n";
  for (const Clause& clause : clauses) {
    for (int lit : clause) out << lit << ' ';
    out << "0\n";
  }
  std::cout << "{\"dimension\":" << n << ",\"edge_variables\":" << m
            << ",\"squares\":" << cube.squares.size()
            << ",\"target_edges\":" << target
            << ",\"maximum_degree_branch\":" << max_degree
            << ",\"cnf_variables\":" << variables
            << ",\"cnf_clauses\":" << clauses.size() << "}\n";
}
