/*
 * Falsify the three-base cover conjecture:
 *
 * If sum_{p|M} 1/p > 1, then some set of at most three prime divisors of M
 * has no common shifted-Lucas multiplier 1 <= t <= (M-1)/2.
 *
 * Since a smaller empty set extends to an empty triple, it is enough to
 * check whether every triple has at least one witness.
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

static uint64_t triple_count(size_t count) {
    return count * (count - 1) * (count - 2) / 6;
}

int main(int argc, char **argv) {
    uint64_t limit = 100000;
    uint64_t m;
    uint64_t threshold_cases = 0;
    uint64_t closest_m = 0;
    uint64_t closest_seen = 0;
    uint64_t closest_total = 1;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);

    for (m = 4; m <= limit; ++m) {
        uint64_t factors[32];
        size_t count;
        size_t i;
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        uint64_t n;
        uint64_t t;
        unsigned char seen[32][32][32];
        uint64_t triples_seen = 0;
        uint64_t triples_total;

        count = prime_divisors(m, factors);
        if (count < 3) continue;
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        if (reciprocal_numerator <= radical) continue;
        ++threshold_cases;

        memset(seen, 0, sizeof(seen));
        triples_total = triple_count(count);
        n = m * (m - 1);
        for (t = 1; t <= (m - 1) / 2; ++t) {
            unsigned char passes[32];
            size_t j;
            size_t k;
            for (i = 0; i < count; ++i) {
                passes[i] = lucas_nonzero(n, m * t, factors[i]);
            }
            for (i = 0; i < count; ++i) {
                if (!passes[i]) continue;
                for (j = i + 1; j < count; ++j) {
                    if (!passes[j]) continue;
                    for (k = j + 1; k < count; ++k) {
                        if (passes[k] && !seen[i][j][k]) {
                            seen[i][j][k] = 1;
                            ++triples_seen;
                        }
                    }
                }
            }
            if (triples_seen == triples_total) {
                printf(
                    "COUNTEREXAMPLE M=%" PRIu64
                    " has witnesses for all %" PRIu64 " triples\n",
                    m, triples_total
                );
                return 1;
            }
        }
        if (triples_seen * closest_total > closest_seen * triples_total) {
            closest_m = m;
            closest_seen = triples_seen;
            closest_total = triples_total;
        }
    }

    printf(
        "No three-base-cover counterexample through M=%" PRIu64
        " across %" PRIu64 " reciprocal-supercritical cases; "
        "closest M=%" PRIu64 " witnessed triples=%" PRIu64 "/%" PRIu64
        "\n",
        limit, threshold_cases, closest_m, closest_seen, closest_total
    );
    return 0;
}
