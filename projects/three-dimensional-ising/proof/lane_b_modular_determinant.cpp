// Exact central-flattening determinant for a Walsh character tensor.
//
// Input: dimension followed by 2^dimension residues, in low-bit-first order.
// MODE=0 ranks the input G tensor. MODE=1 first applies the canonical
// handle-local G -> F transform (inverse Walsh, q=sum a_i b_i, Walsh).

#include <NTL/ZZ_p.h>
#include <NTL/mat_ZZ_p.h>

#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

#ifndef MODULUS
#define MODULUS 1000000007ULL
#endif
#ifndef MODE
#define MODE 0
#endif
#ifndef RANK_TARGET
#define RANK_TARGET 0
#endif

using u64 = std::uint64_t;
static constexpr u64 P = MODULUS;

static inline u64 addmod(u64 a, u64 b) { a += b; return a >= P ? a - P : a; }
static inline u64 submod(u64 a, u64 b) { return a >= b ? a - b : a + P - b; }
static inline u64 mulmod(u64 a, u64 b) { return static_cast<u64>((__uint128_t)a * b % P); }

static u64 power(u64 a, u64 e) {
    u64 result = 1;
    while (e) {
        if (e & 1U) result = mulmod(result, a);
        a = mulmod(a, a);
        e >>= 1U;
    }
    return result;
}

static void fwht(std::vector<u64>& values, bool inverse) {
    const std::size_t size = values.size();
    for (std::size_t length = 1; length < size; length <<= 1U) {
        for (std::size_t start = 0; start < size; start += 2 * length) {
            for (std::size_t offset = 0; offset < length; ++offset) {
                const u64 a = values[start + offset];
                const u64 b = values[start + offset + length];
                values[start + offset] = addmod(a, b);
                values[start + offset + length] = submod(a, b);
            }
        }
    }
    if (inverse) {
        const u64 scale = power(static_cast<u64>(size % P), P - 2);
        for (u64& value : values) value = mulmod(value, scale);
    }
}

int main() {
    int dimension;
    if (!(std::cin >> dimension) || dimension <= 0 || (dimension & 1)) return 2;
    const std::size_t count = std::size_t{1} << dimension;
    std::vector<u64> values(count);
    for (u64& value : values) {
        if (!(std::cin >> value) || value >= P) return 3;
    }

    if constexpr (MODE == 1) {
        fwht(values, true);
        for (std::size_t homology = 0; homology < count; ++homology) {
            unsigned parity = 0;
            for (int bit = 0; bit < dimension; bit += 2) {
                parity ^= ((homology >> bit) & 1U) & ((homology >> (bit + 1)) & 1U);
            }
            if (parity && values[homology]) values[homology] = P - values[homology];
        }
        fwht(values, false);
    }

    const int cut = dimension / 2;
    const long side = 1L << cut;
    NTL::ZZ_p::init(NTL::ZZ(static_cast<long>(P)));
    if constexpr (RANK_TARGET > 0) {
        if (RANK_TARGET > side) return 5;
        for (long row = 0; row < side; ++row) {
            const u64 row_scale = 1 + (static_cast<u64>(row + 1) * 104729ULL) % (P - 1);
            for (long column = 0; column < side; ++column) {
                const u64 column_scale = 1 + (static_cast<u64>(column + 1) * 130363ULL) % (P - 1);
                const std::size_t index = static_cast<std::size_t>(row) |
                                          (static_cast<std::size_t>(column) << cut);
                values[index] = mulmod(values[index], mulmod(row_scale, column_scale));
            }
        }
        // H D_row M D_column H.  A single full Walsh transform applies the
        // row and column transforms because the flattened index is row|column.
        fwht(values, false);
        NTL::mat_ZZ_p projected;
        projected.SetDims(RANK_TARGET, RANK_TARGET);
        for (long row = 0; row < RANK_TARGET; ++row) {
            for (long column = 0; column < RANK_TARGET; ++column) {
                projected[row][column] = NTL::conv<NTL::ZZ_p>(
                    static_cast<long>(values[static_cast<std::size_t>(row) |
                                                    (static_cast<std::size_t>(column) << cut)]));
            }
        }
        const NTL::ZZ_p projected_determinant = NTL::determinant(projected);
        std::cout << "{\"dimension\":" << dimension
                  << ",\"mode\":\"" << (MODE == 1 ? "F" : "G")
                  << "\",\"side\":" << side
                  << ",\"rank_lower_bound\":" << RANK_TARGET
                  << ",\"projected_determinant\":" << NTL::rep(projected_determinant)
                  << ",\"projection\":{\"row_diagonal\":\"1+((row+1)*104729) mod (p-1)\""
                  << ",\"column_diagonal\":\"1+((column+1)*130363) mod (p-1)\""
                  << ",\"transform\":\"unnormalized low-bit-first Walsh on rows and columns\""
                  << ",\"selected_rows\":\"0.." << (RANK_TARGET - 1)
                  << "\",\"selected_columns\":\"0.." << (RANK_TARGET - 1) << "\"}}\n";
        return NTL::IsZero(projected_determinant) ? 6 : 0;
    }
    NTL::mat_ZZ_p matrix;
    matrix.SetDims(side, side);
    for (long row = 0; row < side; ++row) {
        for (long column = 0; column < side; ++column) {
            matrix[row][column] = NTL::conv<NTL::ZZ_p>(
                static_cast<long>(values[static_cast<std::size_t>(row) |
                                                (static_cast<std::size_t>(column) << cut)]));
        }
    }
    NTL::ZZ_p determinant;
    determinant = NTL::determinant(matrix);
    NTL::mat_ZZ_p echelon = matrix;
    const long rank = NTL::gauss(echelon);
    std::vector<long> pivot_columns;
    for (long row = 0; row < rank; ++row) {
        long pivot = 0;
        while (pivot < side && NTL::IsZero(echelon[row][pivot])) ++pivot;
        if (pivot == side) throw std::runtime_error("echelon row has no pivot");
        pivot_columns.push_back(pivot);
    }
    NTL::mat_ZZ_p restricted_transpose;
    restricted_transpose.SetDims(rank, side);
    for (long column = 0; column < rank; ++column) {
        for (long row = 0; row < side; ++row) {
            restricted_transpose[column][row] = matrix[row][pivot_columns[column]];
        }
    }
    const long transpose_rank = NTL::gauss(restricted_transpose);
    if (transpose_rank != rank) throw std::runtime_error("restricted transpose lost rank");
    std::vector<long> pivot_rows;
    for (long row = 0; row < rank; ++row) {
        long pivot = 0;
        while (pivot < side && NTL::IsZero(restricted_transpose[row][pivot])) ++pivot;
        if (pivot == side) throw std::runtime_error("transpose echelon row has no pivot");
        pivot_rows.push_back(pivot);
    }
    NTL::mat_ZZ_p minor;
    minor.SetDims(rank, rank);
    for (long row = 0; row < rank; ++row) {
        for (long column = 0; column < rank; ++column) {
            minor[row][column] = matrix[pivot_rows[row]][pivot_columns[column]];
        }
    }
    const NTL::ZZ_p minor_determinant = NTL::determinant(minor);
    if (NTL::IsZero(minor_determinant)) throw std::runtime_error("selected rank minor vanished");
    std::cout << "{\"dimension\":" << dimension
              << ",\"mode\":\"" << (MODE == 1 ? "F" : "G")
              << "\",\"side\":" << side
              << ",\"rank\":" << rank
              << ",\"determinant\":" << NTL::rep(determinant)
              << ",\"minor_determinant\":" << NTL::rep(minor_determinant)
              << ",\"pivot_rows\":[";
    for (long index = 0; index < rank; ++index) {
        if (index) std::cout << ',';
        std::cout << pivot_rows[index];
    }
    std::cout << "],\"pivot_columns\":[";
    for (long index = 0; index < rank; ++index) {
        if (index) std::cout << ',';
        std::cout << pivot_columns[index];
    }
    std::cout << "]}\n";
    return 0;
}
