/*
 * Falsify the smallest-three-base cover conjecture:
 *
 * If sum_{p|M} 1/p > 1 and p1 < p2 < p3 are the three smallest prime
 * divisors of M, then no multiplier 1 <= t <= (M-1)/2 passes the shifted
 * Lucas tests in all three bases.
 *
 * This is stronger than the reciprocal-threshold conjecture and does not
 * require M-1 to be prime.
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

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

int main(int argc, char **argv) {
    uint64_t limit = 100000;
    uint64_t m;
    uint64_t threshold_cases = 0;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);

    for (m = 4; m <= limit; ++m) {
        uint64_t factors[32];
        size_t count;
        size_t i;
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        uint64_t n;
        uint64_t t;

        count = prime_divisors(m, factors);
        if (count < 3) continue;
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        if (reciprocal_numerator <= radical) continue;
        ++threshold_cases;

        n = m * (m - 1);
        for (t = 1; t <= (m - 1) / 2; ++t) {
            uint64_t k = m * t;
            int passes = 1;
            for (i = 0; i < 3; ++i) {
                if (!lucas_nonzero(n, k, factors[i])) {
                    passes = 0;
                    break;
                }
            }
            if (passes) {
                printf(
                    "COUNTEREXAMPLE M=%" PRIu64
                    " primes=(%" PRIu64 ",%" PRIu64 ",%" PRIu64
                    ") t=%" PRIu64 "\n",
                    m, factors[0], factors[1], factors[2], t
                );
                return 1;
            }
        }
    }

    printf(
        "No smallest-three counterexample through M=%" PRIu64
        " across %" PRIu64 " reciprocal-supercritical cases\n",
        limit, threshold_cases
    );
    return 0;
}
