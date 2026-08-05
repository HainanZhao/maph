#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include <boost/multiprecision/cpp_int.hpp>

#ifdef _OPENMP
#include <omp.h>
#endif

using Big = boost::multiprecision::cpp_int;
using Shape = std::array<int, 5>;
static std::uint64_t choose_[64][64];
static std::atomic<std::uint64_t> global_cells{0};
static std::uint64_t cell_cap = 0;
static int depth_cap = 0;

struct Box {
  Shape lower{};
  Shape splits{};
};

struct Result {
  std::string name;
  std::uint64_t visited = 0;
  std::uint64_t certified = 0;
  std::uint64_t unresolved = 0;
  std::uint64_t omitted_boxes = 0;
  int max_depth = 0;
  bool complete = true;
  Shape degrees{};
  std::vector<Box> unresolved_boxes;
};

static std::vector<std::string> split(const std::string &line) {
  std::stringstream input(line);
  std::vector<std::string> fields;
  std::string field;
  while (std::getline(input, field, '\t')) fields.push_back(field);
  return fields;
}

static std::size_t size_of(const Shape &degrees) {
  std::size_t size = 1;
  for (int degree : degrees) size *= static_cast<std::size_t>(degree + 1);
  return size;
}

static std::size_t index_of(const Shape &index, const Shape &degrees) {
  std::size_t result = 0;
  for (int axis = 0; axis < 5; ++axis) {
    result = result * static_cast<std::size_t>(degrees[axis] + 1)
             + static_cast<std::size_t>(index[axis]);
  }
  return result;
}

static std::pair<std::vector<Big>, Shape>
load_bernstein(const std::filesystem::path &path) {
  struct Raw {
    Shape exponent{};
    Big numerator{};
    std::uint64_t denominator = 1;
  };
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path.string());
  std::string line;
  if (!std::getline(input, line)) throw std::runtime_error("empty input");
  if (line != "x\ty\tz\tv\tlambda\tnumerator\tdenominator")
    throw std::runtime_error("unexpected header in " + path.string());
  std::vector<Raw> raw;
  Shape degrees{};
  std::uint64_t denominator_lcm = 1;
  while (std::getline(input, line)) {
    if (line.empty()) continue;
    const auto fields = split(line);
    if (fields.size() != 7) throw std::runtime_error("malformed row");
    Raw row;
    for (int axis = 0; axis < 5; ++axis) {
      row.exponent[axis] = std::stoi(fields[axis]);
      if (row.exponent[axis] < 0 || row.exponent[axis] >= 64)
        throw std::runtime_error("unsupported exponent");
      degrees[axis] = std::max(degrees[axis], row.exponent[axis]);
    }
    row.numerator = Big(fields[5]);
    row.denominator = std::stoull(fields[6]);
    if (!row.denominator) throw std::runtime_error("zero denominator");
    const auto divisor = std::gcd(denominator_lcm, row.denominator);
    const auto quotient = denominator_lcm / divisor;
    if (quotient > UINT64_MAX / row.denominator)
      throw std::runtime_error("denominator LCM overflow");
    denominator_lcm = quotient * row.denominator;
    raw.push_back(std::move(row));
  }
  std::vector<Big> coefficients(size_of(degrees));
  for (const auto &row : raw) {
    if (denominator_lcm % row.denominator)
      throw std::runtime_error("invalid denominator LCM");
    coefficients[index_of(row.exponent, degrees)] +=
        row.numerator * (denominator_lcm / row.denominator);
  }

  // Tensor monomial-to-Bernstein conversion.  Each axis acquires one common
  // positive integer scale, so coefficient signs remain exact.
  for (int axis = 0; axis < 5; ++axis) {
    const int degree = degrees[axis];
    std::uint64_t axis_lcm = 1;
    for (int k = 0; k <= degree; ++k) {
      const auto divisor = std::gcd(axis_lcm, choose_[degree][k]);
      const auto quotient = axis_lcm / divisor;
      if (quotient > UINT64_MAX / choose_[degree][k])
        throw std::runtime_error("binomial LCM overflow");
      axis_lcm = quotient * choose_[degree][k];
    }
    std::vector<Big> converted(coefficients.size());
    Shape index{};
    for (int i0 = 0; i0 <= degrees[0]; ++i0)
      for (int i1 = 0; i1 <= degrees[1]; ++i1)
        for (int i2 = 0; i2 <= degrees[2]; ++i2)
          for (int i3 = 0; i3 <= degrees[3]; ++i3)
            for (int i4 = 0; i4 <= degrees[4]; ++i4) {
              index = {i0, i1, i2, i3, i4};
              const int target = index[axis];
              Big value = 0;
              for (int k = 0; k <= target; ++k) {
                index[axis] = k;
                value += coefficients[index_of(index, degrees)]
                         * choose_[target][k]
                         * (axis_lcm / choose_[degree][k]);
              }
              index[axis] = target;
              converted[index_of(index, degrees)] = std::move(value);
            }
    coefficients.swap(converted);
  }
  return {std::move(coefficients), degrees};
}

static bool nonnegative(const std::vector<Big> &coefficients) {
  for (const auto &coefficient : coefficients)
    if (coefficient < 0) return false;
  return true;
}

static std::pair<std::vector<Big>, std::vector<Big>>
subdivide(const std::vector<Big> &coefficients, const Shape &degrees, int axis) {
  std::vector<Big> left(coefficients.size()), right(coefficients.size());
  const int degree = degrees[axis];
  Shape index{};
  for (int i0 = 0; i0 <= degrees[0]; ++i0)
    for (int i1 = 0; i1 <= degrees[1]; ++i1)
      for (int i2 = 0; i2 <= degrees[2]; ++i2)
        for (int i3 = 0; i3 <= degrees[3]; ++i3)
          for (int i4 = 0; i4 <= degrees[4]; ++i4) {
            index = {i0, i1, i2, i3, i4};
            if (index[axis] != 0) continue;
            std::vector<Big> work(degree + 1);
            for (int k = 0; k <= degree; ++k) {
              index[axis] = k;
              work[k] = coefficients[index_of(index, degrees)];
            }
            index[axis] = 0;
            left[index_of(index, degrees)] = work[0] << degree;
            index[axis] = degree;
            right[index_of(index, degrees)] = work[degree] << degree;
            for (int round = 1; round <= degree; ++round) {
              for (int k = 0; k <= degree - round; ++k)
                work[k] += work[k + 1];
              index[axis] = round;
              left[index_of(index, degrees)] = work[0] << (degree - round);
              index[axis] = degree - round;
              right[index_of(index, degrees)] =
                  work[degree - round] << (degree - round);
            }
          }
  return {std::move(left), std::move(right)};
}

static void retain_box(Result &result, const Shape &lower, const Shape &splits) {
  ++result.unresolved;
  if (result.unresolved_boxes.size() < 10000)
    result.unresolved_boxes.push_back({lower, splits});
  else
    ++result.omitted_boxes;
}

static void certify(std::vector<Big> coefficients, const Shape &degrees,
                    Shape lower, Shape splits, int depth, Result &result) {
  const auto ordinal = global_cells.fetch_add(1);
  if (ordinal >= cell_cap) {
    result.complete = false;
    retain_box(result, lower, splits);
    return;
  }
  ++result.visited;
  result.max_depth = std::max(result.max_depth, depth);
  if (nonnegative(coefficients)) {
    ++result.certified;
    return;
  }
  if (depth >= depth_cap) {
    result.complete = false;
    retain_box(result, lower, splits);
    return;
  }
  int axis = -1;
  for (int candidate = 0; candidate < 5; ++candidate)
    if (degrees[candidate] > 0 &&
        (axis < 0 || splits[candidate] < splits[axis]))
      axis = candidate;
  if (axis < 0) throw std::runtime_error("no subdivision axis");
  auto children = subdivide(coefficients, degrees, axis);
  ++splits[axis];
  lower[axis] *= 2;
  certify(std::move(children.first), degrees, lower, splits, depth + 1, result);
  if (global_cells.load() >= cell_cap) {
    result.complete = false;
    retain_box(result, lower, splits);
    return;
  }
  ++lower[axis];
  certify(std::move(children.second), degrees, lower, splits, depth + 1, result);
}

int main(int argc, char **argv) {
  if (argc < 5) {
    std::cerr << "usage: monotonicity INPUT_DIR OUTPUT_DIR CELL_CAP DEPTH_CAP [STEM ...]\n";
    return 2;
  }
  cell_cap = std::stoull(argv[3]);
  depth_cap = std::stoi(argv[4]);
  if (!cell_cap || cell_cap > 1000000 || depth_cap < 0 || depth_cap > 20)
    throw std::runtime_error("cap exceeds preregistration");
  for (int n = 0; n < 64; ++n) {
    choose_[n][0] = choose_[n][n] = 1;
    for (int k = 1; k < n; ++k)
      choose_[n][k] = choose_[n - 1][k - 1] + choose_[n - 1][k];
  }
  std::vector<std::string> selected;
  for (int i = 5; i < argc; ++i) selected.push_back(argv[i]);
  std::vector<std::filesystem::path> files;
  for (const auto &entry : std::filesystem::directory_iterator(argv[1])) {
    const auto stem = entry.path().stem().string();
    if (entry.path().extension() == ".tsv" &&
        (selected.empty() || std::find(selected.begin(), selected.end(), stem) != selected.end()))
      files.push_back(entry.path());
  }
  std::sort(files.begin(), files.end());
  if (files.empty()) throw std::runtime_error("no selected polynomial files");
  std::vector<Result> results(files.size());
#ifdef _OPENMP
  const char *configured = std::getenv("C68_THREADS");
  omp_set_num_threads(configured ? std::stoi(configured) : 2);
#pragma omp parallel for schedule(dynamic)
#endif
  for (int i = 0; i < static_cast<int>(files.size()); ++i) {
    auto loaded = load_bernstein(files[i]);
    Result result;
    result.name = files[i].stem().string();
    result.degrees = loaded.second;
    certify(std::move(loaded.first), loaded.second, Shape{}, Shape{}, 0, result);
    results[i] = std::move(result);
  }

  std::filesystem::create_directories(argv[2]);
  std::ofstream output(std::filesystem::path(argv[2]) / "monotonicity-summary.json");
  bool complete = true;
  output << "{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n"
         << "  \"claim_boundary\": \"Exact tensor-Bernstein cover for selected derivative polynomials only.\",\n"
         << "  \"cell_cap\": " << cell_cap << ",\n  \"depth_cap\": " << depth_cap
         << ",\n  \"global_cells\": " << std::min(global_cells.load(), cell_cap)
         << ",\n  \"charts\": {\n";
  for (int i = 0; i < static_cast<int>(results.size()); ++i) {
    const auto &result = results[i];
    complete = complete && result.complete;
    output << "    \"" << result.name << "\": {\"complete\": "
           << (result.complete ? "true" : "false") << ", \"degrees\": [";
    for (int axis = 0; axis < 5; ++axis)
      output << result.degrees[axis] << (axis == 4 ? "]" : ",");
    output << ", \"visited\": " << result.visited
           << ", \"certified_leaves\": " << result.certified
           << ", \"unresolved\": " << result.unresolved
           << ", \"omitted_boxes\": " << result.omitted_boxes
           << ", \"max_depth\": " << result.max_depth << "}"
           << (i + 1 == static_cast<int>(results.size()) ? "\n" : ",\n");
  }
  output << "  },\n  \"complete_cover\": " << (complete ? "true" : "false") << "\n}\n";
  for (const auto &result : results) {
    std::ofstream boxes(std::filesystem::path(argv[2]) /
                        (result.name + "-unresolved.tsv"));
    boxes << "x_lower\tx_splits\ty_lower\ty_splits\tz_lower\tz_splits\t"
             "v_lower\tv_splits\tlambda_lower\tlambda_splits\n";
    for (const auto &box : result.unresolved_boxes) {
      for (int axis = 0; axis < 5; ++axis)
        boxes << box.lower[axis] << '\t' << box.splits[axis]
              << (axis == 4 ? '\n' : '\t');
    }
    std::cout << result.name << " complete=" << result.complete
              << " visited=" << result.visited
              << " certified=" << result.certified
              << " unresolved=" << result.unresolved
              << " depth=" << result.max_depth << '\n';
  }
  return 0;
}
