/*
 * Direct modular baseline for the frozen B2 product merit.
 *
 * Usage:
 *   direct_modular N prime z_csv weight_numerator_csv weight_denominator_csv
 *
 * The output is the scaled error numerator modulo prime.  This is a
 * correctness/performance baseline, not the fast-CBC implementation.
 */

#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

static void fail(const char *message) {
    fprintf(stderr, "direct_modular: %s\n", message);
    exit(2);
}

static uint64_t parse_u64(const char *text) {
    char *end = NULL;
    errno = 0;
    unsigned long long value = strtoull(text, &end, 10);
    if (errno != 0 || end == text || *end != '\0') {
        fail("invalid unsigned integer");
    }
    return (uint64_t)value;
}

static uint64_t *parse_csv(const char *text, size_t *length) {
    char *copy = strdup(text);
    if (copy == NULL) {
        fail("allocation failed");
    }
    size_t capacity = 8;
    size_t count = 0;
    uint64_t *values = malloc(capacity * sizeof(*values));
    if (values == NULL) {
        free(copy);
        fail("allocation failed");
    }
    char *save = NULL;
    for (char *token = strtok_r(copy, ",", &save);
         token != NULL;
         token = strtok_r(NULL, ",", &save)) {
        if (count == capacity) {
            capacity *= 2;
            uint64_t *grown = realloc(values, capacity * sizeof(*values));
            if (grown == NULL) {
                free(values);
                free(copy);
                fail("allocation failed");
            }
            values = grown;
        }
        values[count++] = parse_u64(token);
    }
    free(copy);
    if (count == 0) {
        free(values);
        fail("empty CSV input");
    }
    *length = count;
    return values;
}

static uint64_t mul_mod(uint64_t left, uint64_t right, uint64_t modulus) {
    return (uint64_t)(((u128)left * right) % modulus);
}

static uint64_t signed_mod(i128 value, uint64_t modulus) {
    i128 reduced = value % (i128)modulus;
    if (reduced < 0) {
        reduced += modulus;
    }
    return (uint64_t)reduced;
}

static uint64_t factor_mod(
    uint64_t residue,
    uint64_t modulus,
    uint64_t weight_numerator,
    uint64_t weight_denominator,
    uint64_t prime
) {
    i128 r = residue;
    i128 n = modulus;
    i128 b2_numerator = 6 * r * r - 6 * r * n + n * n;
    i128 value =
        6 * (i128)weight_denominator * n * n
        + (i128)weight_numerator * b2_numerator;
    return signed_mod(value, prime);
}

int main(int argc, char **argv) {
    if (argc != 6) {
        fail("expected N prime z_csv numerator_csv denominator_csv");
    }
    uint64_t modulus = parse_u64(argv[1]);
    uint64_t prime = parse_u64(argv[2]);
    if (modulus < 2 || prime < 3) {
        fail("invalid modulus or prime");
    }

    size_t z_count = 0;
    size_t numerator_count = 0;
    size_t denominator_count = 0;
    uint64_t *generator = parse_csv(argv[3], &z_count);
    uint64_t *numerators = parse_csv(argv[4], &numerator_count);
    uint64_t *denominators = parse_csv(argv[5], &denominator_count);
    if (z_count != numerator_count || z_count != denominator_count) {
        fail("CSV lengths differ");
    }

    uint64_t denominator_product = 1;
    for (size_t j = 0; j < z_count; ++j) {
        if (denominators[j] == 0) {
            fail("zero weight denominator");
        }
        uint64_t c = factor_mod(
            0, modulus, 0, denominators[j], prime
        );
        denominator_product = mul_mod(denominator_product, c, prime);
    }

    uint64_t total = 0;
    for (uint64_t k = 0; k < modulus; ++k) {
        uint64_t term = 1;
        for (size_t j = 0; j < z_count; ++j) {
            uint64_t residue = (uint64_t)(
                ((u128)k * (generator[j] % modulus)) % modulus
            );
            uint64_t factor = factor_mod(
                residue,
                modulus,
                numerators[j],
                denominators[j],
                prime
            );
            term = mul_mod(term, factor, prime);
        }
        total += term;
        if (total >= prime) {
            total -= prime;
        }
    }
    uint64_t constant = mul_mod(
        modulus % prime, denominator_product, prime
    );
    uint64_t result =
        total >= constant ? total - constant : prime - (constant - total);
    printf("%" PRIu64 "\n", result);

    free(generator);
    free(numerators);
    free(denominators);
    return 0;
}
