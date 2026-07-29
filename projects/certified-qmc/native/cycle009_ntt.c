/*
 * Plain-__int128 valuation-stratified candidate scores for Cycle 009.
 *
 * Usage:
 *   cycle009_ntt N prime primitive_root prefix_csv output
 *
 * The prefix contains already selected CBC components.  Product weights
 * are gamma_j=1/j^2, and the emitted scores are for the next component.
 * Output is N/4 unsigned 64-bit residues in ascending power-of-five
 * candidate order, little-endian.
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
    fprintf(stderr, "cycle009_ntt: %s\n", message);
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
    for (
        char *token = strtok_r(copy, ",", &save);
        token != NULL;
        token = strtok_r(NULL, ",", &save)
    ) {
        if (count == capacity) {
            capacity *= 2;
            uint64_t *grown = realloc(
                values, capacity * sizeof(*values)
            );
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
        fail("empty prefix");
    }
    *length = count;
    return values;
}

static uint64_t mul_mod(
    uint64_t left, uint64_t right, uint64_t prime
) {
    return (uint64_t)(((u128)left * right) % prime);
}

static uint64_t add_mod(
    uint64_t left, uint64_t right, uint64_t prime
) {
    uint64_t result = left + right;
    return result >= prime ? result - prime : result;
}

static uint64_t sub_mod(
    uint64_t left, uint64_t right, uint64_t prime
) {
    return left >= right ? left - right : prime - (right - left);
}

static uint64_t pow_mod(
    uint64_t base, uint64_t exponent, uint64_t prime
) {
    uint64_t result = 1;
    while (exponent != 0) {
        if (exponent & 1) {
            result = mul_mod(result, base, prime);
        }
        base = mul_mod(base, base, prime);
        exponent >>= 1;
    }
    return result;
}

static uint64_t signed_mod(i128 value, uint64_t prime) {
    i128 reduced = value % (i128)prime;
    if (reduced < 0) {
        reduced += prime;
    }
    return (uint64_t)reduced;
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

static unsigned power_two_exponent(uint64_t value) {
    if (value < 8 || (value & (value - 1)) != 0) {
        fail("N must be 2^m with m>=3");
    }
    unsigned exponent = 0;
    while ((UINT64_C(1) << exponent) != value) {
        ++exponent;
        if (exponent >= 63) {
            fail("unsupported modulus");
        }
    }
    return exponent;
}

static void ntt(
    uint64_t *values,
    size_t length,
    uint64_t prime,
    uint64_t primitive_root,
    int inverse
) {
    for (size_t index = 1, reversed = 0; index < length; ++index) {
        size_t bit = length >> 1;
        while (reversed & bit) {
            reversed ^= bit;
            bit >>= 1;
        }
        reversed ^= bit;
        if (index < reversed) {
            uint64_t temporary = values[index];
            values[index] = values[reversed];
            values[reversed] = temporary;
        }
    }

    for (size_t block = 2; block <= length; block <<= 1) {
        uint64_t root = pow_mod(
            primitive_root, (prime - 1) / block, prime
        );
        if (inverse) {
            root = pow_mod(root, prime - 2, prime);
        }
        size_t half = block >> 1;
        for (size_t start = 0; start < length; start += block) {
            uint64_t twiddle = 1;
            for (size_t offset = 0; offset < half; ++offset) {
                uint64_t even = values[start + offset];
                uint64_t odd = mul_mod(
                    values[start + offset + half],
                    twiddle,
                    prime
                );
                values[start + offset] = add_mod(
                    even, odd, prime
                );
                values[start + offset + half] = sub_mod(
                    even, odd, prime
                );
                twiddle = mul_mod(twiddle, root, prime);
            }
        }
    }
    if (inverse) {
        uint64_t inverse_length = pow_mod(
            (uint64_t)length, prime - 2, prime
        );
        for (size_t index = 0; index < length; ++index) {
            values[index] = mul_mod(
                values[index], inverse_length, prime
            );
        }
    }
}

static void plus_correlation(
    const uint64_t *left,
    const uint64_t *right,
    uint64_t *result,
    size_t length,
    uint64_t prime,
    uint64_t primitive_root
) {
    uint64_t *left_hat = malloc(length * sizeof(*left_hat));
    uint64_t *right_hat = malloc(length * sizeof(*right_hat));
    if (left_hat == NULL || right_hat == NULL) {
        free(right_hat);
        free(left_hat);
        fail("correlation allocation failed");
    }
    for (size_t index = 0; index < length; ++index) {
        left_hat[index] = left[(length - index) % length];
        right_hat[index] = right[index];
    }
    ntt(left_hat, length, prime, primitive_root, 0);
    ntt(right_hat, length, prime, primitive_root, 0);
    for (size_t index = 0; index < length; ++index) {
        result[index] = mul_mod(
            left_hat[index], right_hat[index], prime
        );
    }
    ntt(result, length, prime, primitive_root, 1);
    free(right_hat);
    free(left_hat);
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
    if (argc != 6) {
        fail("expected N prime primitive_root prefix_csv output");
    }
    uint64_t modulus = parse_u64(argv[1]);
    uint64_t prime = parse_u64(argv[2]);
    uint64_t primitive_root = parse_u64(argv[3]);
    unsigned exponent = power_two_exponent(modulus);
    size_t prefix_length = 0;
    uint64_t *prefix = parse_csv(argv[4], &prefix_length);
    if (prefix_length >= UINT32_MAX) {
        free(prefix);
        fail("prefix is too long");
    }

    size_t candidate_count = (size_t)modulus / 4;
    uint64_t *state = malloc((size_t)modulus * sizeof(*state));
    uint64_t *kernel = malloc((size_t)modulus * sizeof(*kernel));
    uint64_t *scores = malloc(candidate_count * sizeof(*scores));
    if (state == NULL || kernel == NULL || scores == NULL) {
        free(scores);
        free(kernel);
        free(state);
        free(prefix);
        fail("main allocation failed");
    }
    for (uint64_t k = 0; k < modulus; ++k) {
        state[k] = 1;
    }
    for (size_t dimension = 0; dimension < prefix_length; ++dimension) {
        uint64_t weight_denominator =
            (uint64_t)(dimension + 1) * (dimension + 1);
        uint64_t component = prefix[dimension] % modulus;
        for (uint64_t k = 0; k < modulus; ++k) {
            uint64_t residue = (uint64_t)(
                ((u128)k * component) % modulus
            );
            state[k] = mul_mod(
                state[k],
                factor_mod(
                    residue, modulus, weight_denominator, prime
                ),
                prime
            );
        }
    }
    uint64_t new_index = (uint64_t)prefix_length + 1;
    uint64_t new_denominator = new_index * new_index;
    for (uint64_t k = 0; k < modulus; ++k) {
        kernel[k] = factor_mod(
            k, modulus, new_denominator, prime
        );
    }
    uint64_t zero = mul_mod(state[0], kernel[0], prime);
    for (size_t index = 0; index < candidate_count; ++index) {
        scores[index] = zero;
    }

    for (unsigned valuation = 0; valuation < exponent; ++valuation) {
        unsigned unit_exponent = exponent - valuation;
        uint64_t unit_modulus = UINT64_C(1) << unit_exponent;
        uint64_t scale = UINT64_C(1) << valuation;
        if (unit_exponent <= 2) {
            uint64_t contribution = 0;
            for (
                uint64_t odd_part = 1;
                odd_part < unit_modulus;
                odd_part += 2
            ) {
                uint64_t k = scale * odd_part;
                contribution = add_mod(
                    contribution,
                    mul_mod(state[k], kernel[k], prime),
                    prime
                );
            }
            for (size_t index = 0; index < candidate_count; ++index) {
                scores[index] = add_mod(
                    scores[index], contribution, prime
                );
            }
            continue;
        }

        size_t cyclic_length =
            (size_t)UINT64_C(1) << (unit_exponent - 2);
        uint64_t *left = malloc(cyclic_length * sizeof(*left));
        uint64_t *right = malloc(cyclic_length * sizeof(*right));
        uint64_t *correlation = malloc(
            cyclic_length * sizeof(*correlation)
        );
        if (left == NULL || right == NULL || correlation == NULL) {
            free(correlation);
            free(right);
            free(left);
            free(scores);
            free(kernel);
            free(state);
            free(prefix);
            fail("stratum allocation failed");
        }
        uint64_t odd_part = 1;
        for (size_t index = 0; index < cyclic_length; ++index) {
            uint64_t k = scale * odd_part;
            left[index] = add_mod(state[k], state[k], prime);
            right[index] = kernel[k];
            odd_part = (odd_part * 5) % unit_modulus;
        }
        plus_correlation(
            left,
            right,
            correlation,
            cyclic_length,
            prime,
            primitive_root
        );
        for (size_t index = 0; index < candidate_count; ++index) {
            scores[index] = add_mod(
                scores[index],
                correlation[index % cyclic_length],
                prime
            );
        }
        free(correlation);
        free(right);
        free(left);
    }

    FILE *stream = fopen(argv[5], "wb");
    if (stream == NULL) {
        free(scores);
        free(kernel);
        free(state);
        free(prefix);
        fail("cannot create output");
    }
    for (size_t index = 0; index < candidate_count; ++index) {
        write_little_endian_u64(stream, scores[index]);
    }
    if (fclose(stream) != 0) {
        free(scores);
        free(kernel);
        free(state);
        free(prefix);
        fail("output close failed");
    }

    free(scores);
    free(kernel);
    free(state);
    free(prefix);
    return 0;
}
