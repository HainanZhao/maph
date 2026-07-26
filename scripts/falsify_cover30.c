/*
 * Reproducible randomized falsifier for the 30-cover conjecture.
 *
 * For sampled M=30*b, search every 1 <= t < M/2 for which
 * C(M(M-1), M*t) is simultaneously nonzero modulo 2, 3, and 5.
 * Such a pair (M,t) disproves coverage by the fixed primes {2,3,5}.
 *
 * This does not require M-1 to be prime: the proposed covering lemma is
 * stronger than the application to Erdős Problem 700.
 */

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int lucas_nonzero(uint64_t n, uint64_t k, uint64_t p) {
    while (n || k) {
        if (k % p > n % p) {
            return 0;
        }
        n /= p;
        k /= p;
    }
    return 1;
}

static uint64_t next_random(uint64_t *state) {
    *state = *state * UINT64_C(6364136223846793005) + UINT64_C(1442695040888963407);
    return *state;
}

int main(int argc, char **argv) {
    uint64_t samples = 200;
    uint64_t max_b = 1000000;
    uint64_t state = UINT64_C(700);
    uint64_t i;
    int sequential = 0;

    if (argc > 1) {
        samples = strtoull(argv[1], NULL, 10);
    }
    if (argc > 2) {
        max_b = strtoull(argv[2], NULL, 10);
    }
    if (argc > 3 && argv[3][0] == 's') {
        sequential = 1;
        samples = max_b;
    }

    for (i = 0; i < samples; ++i) {
        uint64_t b = sequential ? i + 1 : 1 + next_random(&state) % max_b;
        uint64_t m = 30 * b;
        uint64_t n = m * (m - 1);
        uint64_t t;
        for (t = 1; t < m / 2; ++t) {
            uint64_t k = m * t;
            if (lucas_nonzero(n, k, 2) &&
                lucas_nonzero(n, k, 3) &&
                lucas_nonzero(n, k, 5)) {
                printf("COUNTEREXAMPLE M=%" PRIu64 " b=%" PRIu64
                       " t=%" PRIu64 "\n", m, b, t);
                return 1;
            }
        }
    }

    printf("No counterexample in %" PRIu64 " %s samples with b <= %" PRIu64 "\n",
           samples, sequential ? "sequential" : "deterministic random", max_b);
    return 0;
}
