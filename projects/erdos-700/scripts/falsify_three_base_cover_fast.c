/*
 * Fast falsifier for the adaptive three-base cover conjecture.
 *
 * For each reciprocal-supercritical M, test triples lexicographically and
 * stop as soon as one triple is proved to have no shifted-Lucas witness.
 * A counterexample is reported only if every triple has an explicit
 * witness.  This avoids computing the complete triple-survival profile.
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

static uint64_t triple_count(size_t count) {
    return count * (count - 1) * (count - 2) / 6;
}

int main(int argc, char **argv) {
    uint64_t limit = 1000000;
    uint64_t m;
    uint64_t threshold_cases = 0;
    uint64_t smallest_triple_failures = 0;
    uint64_t record_m = 0;
    uint64_t record_initial_witnessed = 0;
    uint64_t record_total_triples = 0;
    uint64_t exceptional_cases_reported = 0;
    if (argc > 1) limit = strtoull(argv[1], NULL, 10);

    for (m = 4; m <= limit; ++m) {
        uint64_t factors[32];
        size_t count;
        size_t i;
        size_t j;
        size_t k;
        uint64_t radical = 1;
        uint64_t reciprocal_numerator = 0;
        uint64_t n;
        uint64_t initial_witnessed = 0;
        size_t killing_i = 0;
        size_t killing_j = 0;
        size_t killing_k = 0;
        int empty_found = 0;

        count = prime_divisors(m, factors);
        if (count < 3) continue;
        for (i = 0; i < count; ++i) radical *= factors[i];
        for (i = 0; i < count; ++i) {
            reciprocal_numerator += radical / factors[i];
        }
        if (reciprocal_numerator <= radical) continue;
        ++threshold_cases;

        n = m * (m - 1);
        for (i = 0; i < count && !empty_found; ++i) {
            for (j = i + 1; j < count && !empty_found; ++j) {
                for (k = j + 1; k < count; ++k) {
                    uint64_t t;
                    int witness_found = 0;
                    for (t = 1; t <= (m - 1) / 2; ++t) {
                        uint64_t choice = m * t;
                        if (
                            lucas_nonzero(n, choice, factors[i])
                            && lucas_nonzero(n, choice, factors[j])
                            && lucas_nonzero(n, choice, factors[k])
                        ) {
                            witness_found = 1;
                            break;
                        }
                    }
                    if (!witness_found) {
                        killing_i = i;
                        killing_j = j;
                        killing_k = k;
                        empty_found = 1;
                        break;
                    }
                    ++initial_witnessed;
                }
            }
        }

        if (!empty_found) {
            printf(
                "COUNTEREXAMPLE M=%" PRIu64
                " has witnesses for all %" PRIu64 " triples\n",
                m, triple_count(count)
            );
            return 1;
        }
        if (initial_witnessed > 0) {
            ++smallest_triple_failures;
            if (exceptional_cases_reported < 20) {
                printf(
                    "smallest-triple exception M=%" PRIu64
                    " initial witnessed=%" PRIu64
                    " first empty=(%" PRIu64 ",%" PRIu64 ",%" PRIu64
                    ")\n",
                    m,
                    initial_witnessed,
                    factors[killing_i],
                    factors[killing_j],
                    factors[killing_k]
                );
                ++exceptional_cases_reported;
            }
        }
        if (initial_witnessed > record_initial_witnessed) {
            record_m = m;
            record_initial_witnessed = initial_witnessed;
            record_total_triples = triple_count(count);
        }
    }

    printf(
        "No adaptive-three-base counterexample through M=%" PRIu64
        " across %" PRIu64 " reciprocal-supercritical cases; "
        "smallest-triple failures=%" PRIu64 "; "
        "longest initial witnessed run at M=%" PRIu64 ": %" PRIu64
        "/%" PRIu64 " triples\n",
        limit,
        threshold_cases,
        smallest_triple_failures,
        record_m,
        record_initial_witnessed,
        record_total_triples
    );
    return 0;
}
