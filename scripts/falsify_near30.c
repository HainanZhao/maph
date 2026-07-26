/*
 * Search the actual near-multiple conjecture:
 *
 *   M = modulus*b, r = M-1 prime  =>  f(M*r) = M.
 *
 * Proposition 12 reduces a counterexample to a multiplier 1 <= t <= r/2
 * for which C(M*r, M*t) is nonzero modulo every prime divisor of M.
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

static int is_prime(uint64_t n) {
    uint64_t d;
    if (n < 2) return 0;
    if (n % 2 == 0) return n == 2;
    for (d = 3; d <= n / d; d += 2) {
        if (n % d == 0) return 0;
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
    uint64_t max_b = 10000;
    uint64_t start_b = 1;
    uint64_t modulus = 30;
    uint64_t b;
    uint64_t prime_cases = 0;
    if (argc > 1) max_b = strtoull(argv[1], NULL, 10);
    if (argc > 2) start_b = strtoull(argv[2], NULL, 10);
    if (argc > 3) modulus = strtoull(argv[3], NULL, 10);
    if (start_b < 1 || start_b > max_b) {
        fprintf(stderr, "require 1 <= start_b <= max_b\n");
        return 2;
    }

    for (b = start_b; b <= max_b; ++b) {
        uint64_t m = modulus * b;
        uint64_t r = m - 1;
        uint64_t n;
        uint64_t factors[32];
        size_t factor_count;
        uint64_t t;
        if (!is_prime(r)) continue;
        ++prime_cases;
        n = m * r;
        factor_count = prime_divisors(m, factors);

        for (t = 1; t <= r / 2; ++t) {
            uint64_t k = m * t;
            size_t i;
            int coprime = 1;
            for (i = 0; i < factor_count; ++i) {
                if (!lucas_nonzero(n, k, factors[i])) {
                    coprime = 0;
                    break;
                }
            }
            if (coprime) {
                printf("COUNTEREXAMPLE b=%" PRIu64 " M=%" PRIu64
                       " r=%" PRIu64 " t=%" PRIu64 "\n", b, m, r, t);
                return 1;
            }
        }
    }

    printf("No counterexample for %" PRIu64 " <= b <= %" PRIu64
           " across %" PRIu64 " prime values of %" PRIu64 "*b-1\n",
           start_b, max_b, prime_cases, modulus);
    return 0;
}
