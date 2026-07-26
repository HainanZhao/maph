/*
 * Falsify the reciprocal-threshold conjecture:
 *
 * If M-1 is prime and sum_{p|M} 1/p > 1, then f(M(M-1)) = M.
 *
 * Proposition 12 says a counterexample is a multiplier t for which the
 * relevant binomial coefficient is nonzero modulo every p|M.
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
    uint64_t limit = 100000;
    uint64_t m;
    uint64_t threshold_cases = 0;
    uint64_t witness_cases = 0;
    uint64_t max_witness_m = 0;
    uint64_t max_witness_t = 0;
    double max_witness_sum = 0.0;
    int require_predecessor_prime = 1;
    int survey_all_sums = 0;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);
    if (argc > 2 && argv[2][0] == 'a') require_predecessor_prime = 0;
    if (argc > 2 && argv[2][0] == 's') survey_all_sums = 1;

    for (m = 4; m <= limit; m += 2) {
        uint64_t factors[32];
        size_t count;
        size_t i;
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        double reciprocal_sum;
        uint64_t n;
        uint64_t t;

        if (require_predecessor_prime && !is_prime(m - 1)) continue;
        count = prime_divisors(m, factors);
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        reciprocal_sum = (double)reciprocal_numerator / (double)radical;
        if (reciprocal_numerator > radical) {
            ++threshold_cases;
        } else if (!survey_all_sums) {
            continue;
        }
        n = m * (m - 1);

        for (t = 1; t <= (m - 1) / 2; ++t) {
            uint64_t k = m * t;
            int coprime = 1;
            for (i = 0; i < count; ++i) {
                if (!lucas_nonzero(n, k, factors[i])) {
                    coprime = 0;
                    break;
                }
            }
            if (coprime) {
                if (survey_all_sums) {
                    ++witness_cases;
                    if (reciprocal_sum > max_witness_sum) {
                        max_witness_sum = reciprocal_sum;
                        max_witness_m = m;
                        max_witness_t = t;
                    }
                    break;
                }
                printf("COUNTEREXAMPLE M=%" PRIu64 " r=%" PRIu64
                       " t=%" PRIu64 " reciprocal_sum=%.12f\n",
                       m, m - 1, t, reciprocal_sum);
                return 1;
            }
        }
    }

    if (survey_all_sums) {
        printf("Survey through M=%" PRIu64 ": witnesses=%" PRIu64
               " max_sum=%.12f at M=%" PRIu64 " t=%" PRIu64
               "; threshold_cases=%" PRIu64 "\n",
               limit, witness_cases, max_witness_sum,
               max_witness_m, max_witness_t, threshold_cases);
        return 0;
    }

    printf("No counterexample through M=%" PRIu64
           " across %" PRIu64 " reciprocal-threshold cases (%s)\n",
           limit, threshold_cases,
           require_predecessor_prime ? "M-1 prime" : "all M");
    return 0;
}
