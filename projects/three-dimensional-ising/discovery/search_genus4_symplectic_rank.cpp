// Discovery-only random middle-rank search over symplectic bases of F_2^8.
#include <array>
#include <cstdint>
#include <iostream>
#include <random>

using i64 = std::int64_t;
static i64 modulus;
static std::array<i64, 256> tensor;

static int parity(int value) { return __builtin_parity(static_cast<unsigned>(value)); }
static int pairing(int left, int right) {
  return parity((left & ((right << 1) & 0b10101010)) |
                (left & ((right >> 1) & 0b01010101)));
}
static bool orthogonal(int vector, const std::array<int, 8>& basis, int count) {
  for (int i = 0; i < count; ++i) if (pairing(vector, basis[i])) return false;
  return true;
}
static int middle_rank(const std::array<int, 8>& basis) {
  std::array<int, 256> image{};
  for (int x = 1; x < 256; ++x) {
    int bit = __builtin_ctz(static_cast<unsigned>(x));
    image[x] = image[x ^ (1 << bit)] ^ basis[bit];
  }
  std::array<std::array<i64, 16>, 16> matrix{};
  for (int row = 0; row < 16; ++row)
    for (int column = 0; column < 16; ++column)
      matrix[row][column] = tensor[image[row | (column << 4)]];
  int rank = 0;
  for (int column = 0; column < 16 && rank < 16; ++column) {
    int pivot = rank;
    while (pivot < 16 && matrix[pivot][column] == 0) ++pivot;
    if (pivot == 16) continue;
    std::swap(matrix[pivot], matrix[rank]);
    i64 pivot_value = matrix[rank][column];
    for (int row = rank + 1; row < 16; ++row) {
      if (!matrix[row][column]) continue;
      i64 factor = matrix[row][column];
      for (int entry = column; entry < 16; ++entry)
        matrix[row][entry] =
            (static_cast<i64>((__int128)pivot_value * matrix[row][entry] % modulus) -
             static_cast<i64>((__int128)factor * matrix[rank][entry] % modulus) + modulus) % modulus;
    }
    ++rank;
  }
  return rank;
}

int main(int argc, char** argv) {
  std::uint64_t seed = argc > 1 ? std::stoull(argv[1]) : 20260807ULL;
  std::uint64_t iterations = argc > 2 ? std::stoull(argv[2]) : 100000ULL;
  if (!(std::cin >> modulus)) return 2;
  for (auto& value : tensor) {
    if (!(std::cin >> value)) return 2;
    value %= modulus; if (value < 0) value += modulus;
  }
  std::mt19937_64 random(seed);
  std::array<std::uint64_t, 17> counts{};
  std::array<int, 8> first_bad{};
  int first_bad_rank = 16;
  for (std::uint64_t iteration = 0; iteration < iterations; ++iteration) {
    std::array<int, 8> basis{};
    for (int pair = 0; pair < 4; ++pair) {
      do basis[2 * pair] = 1 + random() % 255;
      while (!orthogonal(basis[2 * pair], basis, 2 * pair));
      do basis[2 * pair + 1] = 1 + random() % 255;
      while (!orthogonal(basis[2 * pair + 1], basis, 2 * pair) ||
             !pairing(basis[2 * pair], basis[2 * pair + 1]));
    }
    int rank = middle_rank(basis);
    ++counts[rank];
    if (rank < first_bad_rank) { first_bad_rank = rank; first_bad = basis; }
  }
  std::cout << "{\"iterations\":" << iterations << ",\"rank_counts\":{";
  bool comma = false;
  for (int rank = 0; rank <= 16; ++rank) if (counts[rank]) {
    if (comma) std::cout << ','; comma = true;
    std::cout << '\"' << rank << "\":" << counts[rank];
  }
  std::cout << "},\"minimum_rank\":" << first_bad_rank << ",\"basis\":[";
  for (int i = 0; i < 8; ++i) { if (i) std::cout << ','; std::cout << first_bad[i]; }
  std::cout << "]}\n";
}
