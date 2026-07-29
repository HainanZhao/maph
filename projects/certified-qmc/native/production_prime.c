/*
 * One-prime, dimension-incremental production evaluator.
 *
 * The modular representation and inner update are the plain __int128
 * implementation banked by the passing streaming pilot.  This program
 * only generalizes the CLI modulus and weight power and emits fixed
 * little-endian prefix residues for chunk orchestration.
 *
 * Usage:
 *   production_prime vector N dimension weight_power prime output
 */

#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

static void fail(const char *message) {
    fprintf(stderr, "production_prime: %s\n", message);
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

static uint64_t mul_mod(uint64_t left, uint64_t right, uint64_t prime) {
    return (uint64_t)(((u128)left * right) % prime);
}

static uint64_t signed_mod(i128 value, uint64_t prime) {
    i128 reduced = value % (i128)prime;
    if (reduced < 0) {
        reduced += prime;
    }
    return (uint64_t)reduced;
}

static uint64_t integer_power(uint64_t value, unsigned power) {
    u128 result = 1;
    for (unsigned index = 0; index < power; ++index) {
        result *= value;
    }
    if (result > UINT64_MAX) {
        fail("weight denominator overflow");
    }
    return (uint64_t)result;
}

static uint64_t factor_mod(
    uint64_t residue,
    uint64_t modulus,
    uint64_t weight_denominator,
    uint64_t prime
) {
    i128 r = residue;
    i128 n = modulus;
    i128 b2_numerator = 6 * r * r - 6 * r * n + n * n;
    i128 value =
        6 * (i128)weight_denominator * n * n + b2_numerator;
    return signed_mod(value, prime);
}

static uint64_t *read_vector(const char *path, size_t dimension) {
    FILE *stream = fopen(path, "r");
    if (stream == NULL) {
        fail("cannot open vector file");
    }
    uint64_t *generator = calloc(dimension, sizeof(*generator));
    if (generator == NULL) {
        fclose(stream);
        fail("vector allocation failed");
    }
    for (size_t index = 0; index < dimension; ++index) {
        unsigned long long row = 0;
        unsigned long long component = 0;
        if (fscanf(stream, "%llu %llu", &row, &component) != 2) {
            free(generator);
            fclose(stream);
            fail("vector file ended before requested dimension");
        }
        if (row != index + 1) {
            free(generator);
            fclose(stream);
            fail("vector row index mismatch");
        }
        generator[index] = (uint64_t)component;
    }
    fclose(stream);
    return generator;
}

static void write_little_endian_u64(FILE *stream, uint64_t value) {
    unsigned char bytes[8];
    for (unsigned index = 0; index < 8; ++index) {
        bytes[index] = (unsigned char)(value >> (8 * index));
    }
    if (fwrite(bytes, 1, sizeof(bytes), stream) != sizeof(bytes)) {
        fail("output write failed");
    }
}

int main(int argc, char **argv) {
    if (argc != 7) {
        fail("expected vector N dimension weight_power prime output");
    }
    uint64_t modulus = parse_u64(argv[2]);
    size_t dimension = (size_t)parse_u64(argv[3]);
    unsigned weight_power = (unsigned)parse_u64(argv[4]);
    uint64_t prime = parse_u64(argv[5]);
    if (
        modulus < 2
        || (modulus & (modulus - 1)) != 0
        || dimension < 1
        || weight_power < 1
        || weight_power > 3
        || prime < 3
    ) {
        fail("invalid modulus, dimension, weight power, or prime");
    }

    uint64_t *generator = read_vector(argv[1], dimension);
    uint64_t *state = malloc(modulus * sizeof(*state));
    uint64_t *output = malloc(dimension * sizeof(*output));
    if (state == NULL || output == NULL) {
        free(output);
        free(state);
        free(generator);
        fail("allocation failed");
    }
    for (uint64_t k = 0; k < modulus; ++k) {
        state[k] = 1;
    }

    uint64_t denominator_product = 1;
    for (size_t j = 0; j < dimension; ++j) {
        uint64_t index = (uint64_t)j + 1;
        uint64_t weight_denominator = integer_power(
            index, weight_power
        );
        uint64_t denominator_factor = signed_mod(
            6
            * (i128)weight_denominator
            * modulus
            * modulus,
            prime
        );
        denominator_product = mul_mod(
            denominator_product, denominator_factor, prime
        );

        uint64_t total = 0;
        uint64_t component = generator[j] % modulus;
        for (uint64_t k = 0; k < modulus; ++k) {
            uint64_t residue = (uint64_t)(
                ((u128)k * component) % modulus
            );
            uint64_t factor = factor_mod(
                residue, modulus, weight_denominator, prime
            );
            state[k] = mul_mod(state[k], factor, prime);
            total += state[k];
            if (total >= prime) {
                total -= prime;
            }
        }
        uint64_t constant = mul_mod(
            modulus % prime, denominator_product, prime
        );
        output[j] = (
            total >= constant
            ? total - constant
            : prime - (constant - total)
        );
    }

    FILE *stream = fopen(argv[6], "wb");
    if (stream == NULL) {
        free(output);
        free(state);
        free(generator);
        fail("cannot create output");
    }
    for (size_t index = 0; index < dimension; ++index) {
        write_little_endian_u64(stream, output[index]);
    }
    if (fclose(stream) != 0) {
        free(output);
        free(state);
        free(generator);
        fail("output close failed");
    }

    free(output);
    free(state);
    free(generator);
    return 0;
}
