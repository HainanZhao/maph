/*
 * Search all M for a genuine Lucas cover degree of at least four.
 *
 * Unlike the reciprocal-supercritical falsifiers, this program imposes no
 * condition on sum_{p|M} 1/p.  It asks whether the full shifted-Lucas
 * intersection is empty while every triple intersection is nonempty.
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
    uint64_t empty_full_cases = 0;
    uint64_t full_witness_cases = 0;
    uint64_t degree_four_cases = 0;
    uint64_t closest_m = 0;
    uint64_t closest_seen = 0;
    uint64_t closest_total = 1;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);

    for (m = 4; m <= limit; ++m) {
        uint64_t factors[32];
        size_t count = prime_divisors(m, factors);
        size_t i;
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        uint64_t n;
        uint64_t t;
        unsigned char seen[32][32][32];
        uint64_t triples_seen = 0;
        uint64_t triples_total;
        int full_witness = 0;

        if (count < 4) continue;
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        memset(seen, 0, sizeof(seen));
        triples_total = triple_count(count);
        n = m * (m - 1);

        for (t = 1; t <= (m - 1) / 2; ++t) {
            unsigned char passes[32];
            size_t passed_count = 0;
            size_t j;
            size_t k;
            for (i = 0; i < count; ++i) {
                passes[i] = lucas_nonzero(n, m * t, factors[i]);
                passed_count += passes[i];
            }
            if (passed_count == count) {
                full_witness = 1;
                break;
            }
            if (passed_count < 3) continue;
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
        }

        if (full_witness) {
            ++full_witness_cases;
            continue;
        }
        ++empty_full_cases;
        if (triples_seen == triples_total) {
            ++degree_four_cases;
            if (degree_four_cases <= 20) {
                printf(
                    "DEGREE-AT-LEAST-FOUR M=%" PRIu64
                    " prime-count=%zu triples=%" PRIu64
                    " defect=%" PRId64 "\n",
                    m,
                    count,
                    triples_total,
                    (int64_t)radical - (int64_t)reciprocal_numerator
                );
            }
            continue;
        }
        if (triples_seen * closest_total > closest_seen * triples_total) {
            closest_m = m;
            closest_seen = triples_seen;
            closest_total = triples_total;
        }
    }

    printf(
        "Survey through M=%" PRIu64
        ": degree-at-least-four cases=%" PRIu64
        ", empty-full cases=%" PRIu64 ", full-witness cases=%" PRIu64
        "; closest M=%" PRIu64 " witnessed triples=%" PRIu64 "/%" PRIu64
        "\n",
        limit,
        degree_four_cases,
        empty_full_cases,
        full_witness_cases,
        closest_m,
        closest_seen,
        closest_total
    );
    return 0;
}
