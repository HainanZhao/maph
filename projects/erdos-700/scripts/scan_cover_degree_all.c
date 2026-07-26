/*
 * Compute exact Lucas cover degrees without a reciprocal-defect filter.
 *
 * For each M with at least four distinct prime factors, record every pass
 * mask attained by 1 <= t <= (M-1)/2.  A downward Boolean transform then
 * determines which subsets of bases have a common witness.
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_FACTORS 15
#define MAX_MASKS (1U << MAX_FACTORS)

static int lucas_nonzero(uint64_t n, uint64_t k, uint64_t p) {
    while (n || k) {
        if (k % p > n % p) return 0;
        n /= p;
        k /= p;
    }
    return 1;
}

static size_t prime_divisors(uint64_t n, uint64_t *out) {
    uint64_t d;
    size_t count = 0;
    if (n % 2 == 0) {
        out[count++] = 2;
        while (n % 2 == 0) n /= 2;
    }
    for (d = 3; d <= n / d; d += 2) {
        if (n % d == 0) {
            out[count++] = d;
            while (n % d == 0) n /= d;
        }
    }
    if (n > 1) out[count++] = n;
    return count;
}

static unsigned popcount_u32(uint32_t value) {
    unsigned count = 0;
    while (value) {
        value &= value - 1;
        ++count;
    }
    return count;
}

int main(int argc, char **argv) {
    uint64_t limit = 100000;
    int only_supercritical = 0;
    uint64_t histogram[MAX_FACTORS + 1] = {0};
    uint64_t negative_histogram[MAX_FACTORS + 1] = {0};
    uint64_t examples[MAX_FACTORS + 1][10] = {{0}};
    uint64_t m;
    uint64_t full_witness_cases = 0;
    uint64_t empty_full_cases = 0;
    uint64_t witness_counts[MAX_MASKS];
    uint64_t greedy_failures = 0;
    uint64_t greedy_failure_examples[10] = {0};
    uint64_t maximum_greedy_pair_count = 0;
    uint64_t maximum_greedy_pair_m = 0;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);
    if (argc > 2 && argv[2][0] == 's') only_supercritical = 1;

    for (m = 4; m <= limit; ++m) {
        uint64_t factors[MAX_FACTORS];
        size_t count = prime_divisors(m, factors);
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        uint64_t n;
        uint64_t t;
        uint32_t mask_count;
        uint32_t full_mask;
        uint32_t mask;
        size_t i;
        unsigned degree = 0;

        if (count < (only_supercritical ? 3U : 4U)) continue;
        if (count > MAX_FACTORS) {
            fprintf(stderr, "too many prime factors at M=%" PRIu64 "\n", m);
            return 2;
        }
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        if (only_supercritical && reciprocal_numerator <= radical) continue;

        mask_count = 1U << count;
        full_mask = mask_count - 1;
        memset(witness_counts, 0, mask_count * sizeof(witness_counts[0]));
        n = m * (m - 1);
        for (t = 1; t <= (m - 1) / 2; ++t) {
            uint32_t pass_mask = 0;
            for (i = 0; i < count; ++i) {
                if (lucas_nonzero(n, m * t, factors[i])) {
                    pass_mask |= 1U << i;
                }
            }
            ++witness_counts[pass_mask];
            if (pass_mask == full_mask) break;
        }
        if (witness_counts[full_mask]) {
            ++full_witness_cases;
            continue;
        }
        ++empty_full_cases;

        /*
         * Replace "this exact pass mask occurs" by "some occurring pass
         * mask contains this subset."
         */
        for (i = 0; i < count; ++i) {
            uint32_t bit = 1U << i;
            for (mask = 0; mask < mask_count; ++mask) {
                if (!(mask & bit)) {
                    witness_counts[mask] += witness_counts[mask | bit];
                }
            }
        }

        for (i = 1; i <= count && degree == 0; ++i) {
            for (mask = 1; mask < mask_count; ++mask) {
                if (popcount_u32(mask) == i && !witness_counts[mask]) {
                    degree = (unsigned)i;
                    break;
                }
            }
        }
        if (degree == 0) {
            fprintf(stderr, "no empty certificate at M=%" PRIu64 "\n", m);
            return 2;
        }

        if (histogram[degree] < 10) {
            examples[degree][histogram[degree]] = m;
        }
        ++histogram[degree];
        if (reciprocal_numerator > radical) {
            ++negative_histogram[degree];
        }

        if (only_supercritical) {
            uint32_t selected = 0;
            unsigned step;
            for (step = 0; step < 3; ++step) {
                uint32_t best_bit = 0;
                uint64_t best_count = UINT64_MAX;
                for (i = 0; i < count; ++i) {
                    uint32_t bit = 1U << i;
                    uint64_t candidate_count;
                    if (selected & bit) continue;
                    candidate_count = witness_counts[selected | bit];
                    if (candidate_count < best_count) {
                        best_count = candidate_count;
                        best_bit = bit;
                    }
                }
                selected |= best_bit;
                if (
                    step == 1
                    && witness_counts[selected] > maximum_greedy_pair_count
                ) {
                    maximum_greedy_pair_count = witness_counts[selected];
                    maximum_greedy_pair_m = m;
                }
            }
            if (witness_counts[selected] != 0) {
                if (greedy_failures < 10) {
                    greedy_failure_examples[greedy_failures] = m;
                }
                ++greedy_failures;
            }
        }
    }

    printf(
        "Cover-degree survey through M=%" PRIu64 " (%s)"
        ": empty-full=%" PRIu64 ", full-witness=%" PRIu64 "\n",
        limit,
        only_supercritical ? "supercritical only" : "at least four primes",
        empty_full_cases,
        full_witness_cases
    );
    for (size_t degree = 1; degree <= MAX_FACTORS; ++degree) {
        size_t index;
        if (!histogram[degree]) continue;
        printf(
            "degree=%zu count=%" PRIu64 " negative-defect=%" PRIu64
            " examples=",
            degree, histogram[degree], negative_histogram[degree]
        );
        for (index = 0; index < 10 && examples[degree][index]; ++index) {
            printf(
                "%s%" PRIu64,
                index ? "," : "",
                examples[degree][index]
            );
        }
        printf("\n");
    }
    if (only_supercritical) {
        size_t index;
        printf("three-step greedy failures=%" PRIu64 " examples=", greedy_failures);
        for (
            index = 0;
            index < 10 && greedy_failure_examples[index];
            ++index
        ) {
            printf(
                "%s%" PRIu64,
                index ? "," : "",
                greedy_failure_examples[index]
            );
        }
        printf("\n");
        printf(
            "maximum greedy-pair survivors=%" PRIu64 " at M=%" PRIu64
            "\n",
            maximum_greedy_pair_count,
            maximum_greedy_pair_m
        );
    }
    return 0;
}
