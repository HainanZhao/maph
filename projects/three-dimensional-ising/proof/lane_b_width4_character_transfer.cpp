#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;
#ifndef MODULUS
#define MODULUS 1000000007ULL
#endif
static constexpr u64 P = MODULUS;

struct EdgeData {
    int layer, axis, left, right;
    std::uint32_t label;
};

static inline u64 addmod(u64 a, u64 b) { a += b; return a >= P ? a - P : a; }
static inline u64 submod(u64 a, u64 b) { return a >= b ? a - b : a + P - b; }
static inline u64 mulmod(u64 a, u64 b) { return (a * b) % P; }

static u64 power(u64 a, u64 e) {
    u64 result = 1;
    while (e) {
        if (e & 1) result = mulmod(result, a);
        a = mulmod(a, a);
        e >>= 1;
    }
    return result;
}

static void fwht(std::vector<u64>& values, bool inverse) {
    const int size = static_cast<int>(values.size());
    for (int length = 1; length < size; length <<= 1) {
        for (int start = 0; start < size; start += 2 * length) {
            for (int offset = 0; offset < length; ++offset) {
                const u64 a = values[start + offset];
                const u64 b = values[start + offset + length];
                values[start + offset] = addmod(a, b);
                values[start + offset + length] = submod(a, b);
            }
        }
    }
    if (inverse) {
        const u64 scale = power(size, P - 2);
        for (u64& value : values) value = mulmod(value, scale);
    }
}

static u64 signed_weight(u64 weight, std::uint32_t character, std::uint32_t label) {
    return (__builtin_popcount(character & label) & 1) ? (weight ? P - weight : 0) : weight;
}

static int project_bits(std::uint32_t character, std::uint32_t support) {
    int result = 0, output = 0;
    for (int bit = 0; support; ++bit, support >>= 1) {
        if (!(support & 1U)) continue;
        if (character & (1U << bit)) result |= 1 << output;
        ++output;
    }
    return result;
}

static std::uint32_t expand_bits(int local, std::uint32_t support) {
    std::uint32_t result = 0;
    int input = 0;
    for (int bit = 0; support; ++bit, support >>= 1) {
        if (!(support & 1U)) continue;
        if (local & (1 << input)) result |= 1U << bit;
        ++input;
    }
    return result;
}

int main() {
    int n, w, dimension, edge_count, regime;
    if (!(std::cin >> n >> w >> dimension >> edge_count >> regime)) return 2;
    std::vector<EdgeData> edges(edge_count);
    for (auto& edge : edges) {
        std::cin >> edge.layer >> edge.axis >> edge.left >> edge.right >> edge.label;
    }
    const int m = w * w;
    const int states = 1 << (m - 1);
    const int characters = 1 << dimension;
    std::vector<std::vector<EdgeData>> transverse(n), connector(n - 1);
    for (const auto& edge : edges) {
        if (edge.axis == 0) connector[edge.layer].push_back(edge);
        else transverse[edge.layer].push_back(edge);
    }
    std::vector<u64> answer(characters);

    auto base_weight = [regime](int edge_index, int axis) -> u64 {
        if (regime == 0) {
            // Independent nonzero specializations: deterministic and pinned.
            return 2 + (static_cast<u64>(edge_index + 1) * 104729ULL) % (P - 3);
        }
        if (regime == 2) return 2;
        // Homogeneous anisotropic specialization (tx,ty,tz)=(2,3,5).
        static constexpr u64 axis_weight[3] = {2, 3, 5};
        return axis_weight[axis];
    };

    // Cache every distinct local-character diagonal.  For the certified
    // width-four embedding this is 2+32+256+32 rather than 1024 copies.
    std::vector<std::uint32_t> transverse_support(n, 0);
    std::vector<int> transverse_variants(n, 1);
    std::vector<std::vector<u64>> intra_cache(n);
    for (int layer = 0; layer < n; ++layer) {
        for (const auto& edge : transverse[layer]) transverse_support[layer] |= edge.label;
        transverse_variants[layer] = 1 << __builtin_popcount(transverse_support[layer]);
        intra_cache[layer].resize(static_cast<std::size_t>(transverse_variants[layer]) * states);
        #pragma omp parallel for schedule(static)
        for (int local = 0; local < transverse_variants[layer]; ++local) {
            const std::uint32_t character = expand_bits(local, transverse_support[layer]);
            for (int spin = 0; spin < states; ++spin) {
                u64 value = 1;
                for (const auto& edge : transverse[layer]) {
                    const int hash = ((layer * m + edge.left) * m + edge.right) * 3 + edge.axis;
                    u64 weight = signed_weight(base_weight(hash, edge.axis), character, edge.label);
                    const int left_bit = edge.left == 0 ? 0 : ((spin >> (edge.left - 1)) & 1);
                    const int right_bit = edge.right == 0 ? 0 : ((spin >> (edge.right - 1)) & 1);
                    value = mulmod(value, left_bit == right_bit ? addmod(1, weight) : submod(1, weight));
                }
                intra_cache[layer][static_cast<std::size_t>(local) * states + spin] = value;
            }
        }
    }

    // In the pinned width-three/four homology coordinates all longitudinal
    // labels vanish.  Their convolution kernels therefore need one transform
    // per layer and weight regime, not one per character.
    std::vector<std::vector<u64>> kernel_hat(n - 1, std::vector<u64>(states));
    for (int layer = 0; layer + 1 < n; ++layer) {
        std::uint32_t support = 0;
        for (const auto& edge : connector[layer]) support |= edge.label;
        if (support) {
            std::cerr << "nonzero connector labels are outside this optimized certificate\n";
            return 3;
        }
        for (int difference = 0; difference < states; ++difference) {
            u64 plus = 1, minus = 1;
            for (const auto& edge : connector[layer]) {
                const int hash = ((layer * m + edge.left) * m + edge.right) * 3 + edge.axis;
                const u64 weight = base_weight(hash, edge.axis);
                const int bit = edge.left == 0 ? 0 : ((difference >> (edge.left - 1)) & 1);
                plus = mulmod(plus, bit ? submod(1, weight) : addmod(1, weight));
                minus = mulmod(minus, bit ? addmod(1, weight) : submod(1, weight));
            }
            kernel_hat[layer][difference] = addmod(plus, minus);
        }
        fwht(kernel_hat[layer], false);
    }

    #pragma omp parallel for schedule(dynamic)
    for (int character = 0; character < characters; ++character) {
        std::vector<u64> state(states), transformed(states);
        int local = project_bits(character, transverse_support[0]);
        std::copy_n(intra_cache[0].data() + static_cast<std::size_t>(local) * states, states, state.data());
        for (int layer = 0; layer + 1 < n; ++layer) {
            transformed = state;
            fwht(transformed, false);
            for (int index = 0; index < states; ++index) transformed[index] = mulmod(transformed[index], kernel_hat[layer][index]);
            fwht(transformed, true);
            local = project_bits(character, transverse_support[layer + 1]);
            const u64* diagonal = intra_cache[layer + 1].data() + static_cast<std::size_t>(local) * states;
            for (int spin = 0; spin < states; ++spin) state[spin] = mulmod(transformed[spin], diagonal[spin]);
        }
        u64 total = 0;
        for (u64 value : state) total = addmod(total, value);
        answer[character] = addmod(total, total); // restore the two global representatives
    }
    for (u64 value : answer) std::cout << value << '\n';
    return 0;
}
