// Exhaustive exact-mod-prime TT-rank search over Sp(6,2).
//
// Input: one prime followed by 64 integer residues F(0),...,F(63).
// Output: JSON containing the number of symplectic bases, rank-profile counts,
// and the first submaximal witness if one exists.
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using i64 = std::int64_t;

static i64 modulus;
static std::array<i64, 64> tensor;
static std::map<std::array<int, 5>, std::uint64_t> profiles;
static std::uint64_t basis_count = 0;
static std::array<int, 6> first_bad_basis{};
static std::array<int, 5> first_bad_profile{};
static bool found_bad = false;

static int parity(int value) { return __builtin_parity(static_cast<unsigned>(value)); }

static int pairing(int left, int right) {
  return parity((left & ((right << 1) & 0b101010)) |
                (left & ((right >> 1) & 0b010101)));
}

static int rank_matrix(std::array<std::array<i64, 32>, 32>& matrix, int rows, int columns) {
  int rank = 0;
  for (int column = 0; column < columns && rank < rows; ++column) {
    int pivot = rank;
    while (pivot < rows && matrix[pivot][column] == 0) ++pivot;
    if (pivot == rows) continue;
    std::swap(matrix[pivot], matrix[rank]);
    i64 pivot_value = matrix[rank][column];
    // Fraction-free field elimination: row <- pivot*row-factor*pivot_row.
    // Multiplication by the nonzero pivot is invertible, so rank is preserved
    // without a modular inverse at every pivot.
    for (int row = rank + 1; row < rows; ++row) {
      if (matrix[row][column] == 0) continue;
      i64 factor = matrix[row][column];
      for (int entry = column; entry < columns; ++entry) {
        matrix[row][entry] =
            (static_cast<i64>((__int128)pivot_value * matrix[row][entry] % modulus) -
             static_cast<i64>((__int128)factor * matrix[rank][entry] % modulus) + modulus) % modulus;
      }
    }
    ++rank;
  }
  return rank;
}

static std::array<int, 5> tt_profile(const std::array<int, 6>& basis) {
  std::array<int, 64> image{};
  for (int index = 1; index < 64; ++index) {
    int bit = __builtin_ctz(static_cast<unsigned>(index));
    image[index] = image[index ^ (1 << bit)] ^ basis[bit];
  }
  std::array<int, 5> result{};
  for (int cut = 1; cut < 6; ++cut) {
    int rows = 1 << cut;
    int columns = 1 << (6 - cut);
    std::array<std::array<i64, 32>, 32> matrix{};
    for (int row = 0; row < rows; ++row)
      for (int column = 0; column < columns; ++column)
        matrix[row][column] = tensor[image[row | (column << cut)]];
    result[cut - 1] = rank_matrix(matrix, rows, columns);
  }
  return result;
}

static bool orthogonal_to_pairs(int vector, const std::array<int, 6>& basis, int pair_count) {
  for (int index = 0; index < 2 * pair_count; ++index)
    if (pairing(vector, basis[index])) return false;
  return true;
}

static void enumerate_pair(std::array<int, 6>& basis, int pair_index) {
  if (pair_index == 3) {
    ++basis_count;
    auto profile = tt_profile(basis);
    ++profiles[profile];
    constexpr std::array<int, 5> maximum = {2, 4, 8, 4, 2};
    if (!found_bad && profile != maximum) {
      found_bad = true;
      first_bad_basis = basis;
      first_bad_profile = profile;
    }
    return;
  }
  for (int first = 1; first < 64; ++first) {
    if (!orthogonal_to_pairs(first, basis, pair_index)) continue;
    basis[2 * pair_index] = first;
    for (int second = 1; second < 64; ++second) {
      if (!orthogonal_to_pairs(second, basis, pair_index)) continue;
      if (!pairing(first, second)) continue;
      basis[2 * pair_index + 1] = second;
      enumerate_pair(basis, pair_index + 1);
    }
  }
}

static std::string array_json(const std::array<int, 5>& values) {
  std::ostringstream output;
  output << '[';
  for (int index = 0; index < 5; ++index) {
    if (index) output << ',';
    output << values[index];
  }
  output << ']';
  return output.str();
}

int main() {
  if (!(std::cin >> modulus)) return 2;
  for (i64& value : tensor) {
    if (!(std::cin >> value)) return 2;
    value %= modulus;
    if (value < 0) value += modulus;
  }
  std::array<int, 6> basis{};
  enumerate_pair(basis, 0);
  std::cout << "{\"modulus\":" << modulus << ",\"symplectic_bases\":" << basis_count
            << ",\"profiles\":{\"";
  bool first = true;
  for (const auto& [profile, count] : profiles) {
    if (!first) std::cout << ",\"";
    first = false;
    for (int index = 0; index < 5; ++index) {
      if (index) std::cout << ',';
      std::cout << profile[index];
    }
    std::cout << "\":" << count;
  }
  std::cout << "},\"submaximal_found\":" << (found_bad ? "true" : "false");
  if (found_bad) {
    std::cout << ",\"first_bad_basis\":[";
    for (int index = 0; index < 6; ++index) {
      if (index) std::cout << ',';
      std::cout << first_bad_basis[index];
    }
    std::cout << "],\"first_bad_profile\":" << array_json(first_bad_profile);
  }
  std::cout << "}\n";
  return basis_count == 1451520 ? 0 : 3;
}
