/*
 * Prime-major incremental Workstream B evaluator pilot.
 *
 * Usage:
 *   streaming_pilot vector_file primes_file dimension threads checkpoint
 *
 * The vector file has "dimension component" rows. The primes file has
 * one verified prime per line; its final two primes are universal
 * overflow checks. Results are checkpointed prime-major, one uint64_t
 * residue for every prefix. Timings use the plain __int128 remainder
 * representation and exclude parsing.
 */

#include <errno.h>
#include <inttypes.h>
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

static void fail(const char *message) {
    fprintf(stderr, "streaming_pilot: %s\n", message);
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

static uint64_t elapsed_ns(
    const struct timespec *start,
    const struct timespec *end
) {
    int64_t seconds = end->tv_sec - start->tv_sec;
    int64_t nanoseconds = end->tv_nsec - start->tv_nsec;
    return (uint64_t)(
        seconds * INT64_C(1000000000) + nanoseconds
    );
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

static uint64_t *read_primes(const char *path, size_t *count) {
    FILE *stream = fopen(path, "r");
    if (stream == NULL) {
        fail("cannot open primes file");
    }
    size_t capacity = 256;
    size_t length = 0;
    uint64_t *primes = malloc(capacity * sizeof(*primes));
    if (primes == NULL) {
        fclose(stream);
        fail("prime allocation failed");
    }
    unsigned long long value = 0;
    while (fscanf(stream, "%llu", &value) == 1) {
        if (length == capacity) {
            capacity *= 2;
            uint64_t *grown = realloc(
                primes, capacity * sizeof(*primes)
            );
            if (grown == NULL) {
                free(primes);
                fclose(stream);
                fail("prime reallocation failed");
            }
            primes = grown;
        }
        primes[length++] = (uint64_t)value;
    }
    fclose(stream);
    if (length < 3) {
        free(primes);
        fail("need work primes and two overflow primes");
    }
    *count = length;
    return primes;
}

static void evaluate_prime(
    uint64_t modulus,
    const uint64_t *generator,
    size_t dimension,
    uint64_t prime,
    uint64_t *output
) {
    uint64_t *state = malloc(modulus * sizeof(*state));
    if (state == NULL) {
        fail("state allocation failed");
    }
    for (uint64_t k = 0; k < modulus; ++k) {
        state[k] = 1;
    }
    uint64_t denominator_product = 1;
    for (size_t j = 0; j < dimension; ++j) {
        uint64_t index = (uint64_t)j + 1;
        uint64_t weight_denominator = index * index;
        uint64_t c = signed_mod(
            6
            * (i128)weight_denominator
            * modulus
            * modulus,
            prime
        );
        denominator_product = mul_mod(
            denominator_product, c, prime
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
    free(state);
}

static uint64_t digest_words(const uint64_t *values, size_t count) {
    uint64_t digest = UINT64_C(1469598103934665603);
    for (size_t index = 0; index < count; ++index) {
        uint64_t word = values[index];
        for (unsigned byte = 0; byte < 8; ++byte) {
            digest ^= (word >> (8 * byte)) & UINT64_C(0xff);
            digest *= UINT64_C(1099511628211);
        }
    }
    return digest;
}

static void checkpoint_replay(
    const char *path,
    const uint64_t *values,
    size_t count
) {
    FILE *stream = fopen(path, "wb");
    if (stream == NULL) {
        fail("cannot create checkpoint");
    }
    if (fwrite(values, sizeof(*values), count, stream) != count) {
        fclose(stream);
        fail("checkpoint write failed");
    }
    if (fclose(stream) != 0) {
        fail("checkpoint close failed");
    }

    uint64_t *replay = malloc(count * sizeof(*replay));
    if (replay == NULL) {
        fail("checkpoint replay allocation failed");
    }
    stream = fopen(path, "rb");
    if (stream == NULL) {
        free(replay);
        fail("cannot reopen checkpoint");
    }
    if (fread(replay, sizeof(*replay), count, stream) != count) {
        free(replay);
        fclose(stream);
        fail("checkpoint read failed");
    }
    if (fgetc(stream) != EOF) {
        free(replay);
        fclose(stream);
        fail("checkpoint has trailing bytes");
    }
    fclose(stream);
    if (
        digest_words(replay, count)
        != digest_words(values, count)
    ) {
        free(replay);
        fail("checkpoint digest mismatch");
    }
    free(replay);
}

int main(int argc, char **argv) {
    if (argc != 6) {
        fail(
            "expected vector_file primes_file dimension threads checkpoint"
        );
    }
    const uint64_t modulus = 1024;
    size_t dimension = (size_t)parse_u64(argv[3]);
    int threads = (int)parse_u64(argv[4]);
    if (dimension < 1 || threads < 1) {
        fail("invalid dimension or thread count");
    }
    uint64_t *generator = read_vector(argv[1], dimension);
    size_t prime_count = 0;
    uint64_t *primes = read_primes(argv[2], &prime_count);
    size_t work_count = prime_count - 2;
    size_t output_count = prime_count * dimension;
    uint64_t *output = calloc(output_count, sizeof(*output));
    if (output == NULL) {
        free(generator);
        free(primes);
        fail("output allocation failed");
    }

    struct timespec start;
    struct timespec end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    #pragma omp parallel for schedule(static) num_threads(threads)
    for (size_t index = 0; index < work_count; ++index) {
        evaluate_prime(
            modulus,
            generator,
            dimension,
            primes[index],
            output + index * dimension
        );
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    uint64_t work_ns = elapsed_ns(&start, &end);

    clock_gettime(CLOCK_MONOTONIC, &start);
    #pragma omp parallel for schedule(static) num_threads(threads)
    for (size_t index = work_count; index < prime_count; ++index) {
        evaluate_prime(
            modulus,
            generator,
            dimension,
            primes[index],
            output + index * dimension
        );
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    uint64_t overflow_ns = elapsed_ns(&start, &end);

    clock_gettime(CLOCK_MONOTONIC, &start);
    checkpoint_replay(argv[5], output, output_count);
    clock_gettime(CLOCK_MONOTONIC, &end);
    uint64_t checkpoint_ns = elapsed_ns(&start, &end);

    printf("{\n");
    printf("  \"checkpoint_digest\": \"%" PRIu64 "\",\n",
           digest_words(output, output_count));
    printf("  \"checkpoint_ns\": %" PRIu64 ",\n", checkpoint_ns);
    printf("  \"checkpoint_replay\": true,\n");
    printf("  \"dimension\": %zu,\n", dimension);
    printf("  \"modulus\": %" PRIu64 ",\n", modulus);
    printf("  \"output_words\": %zu,\n", output_count);
    printf("  \"overflow_ns\": %" PRIu64 ",\n", overflow_ns);
    printf("  \"overflow_primes\": 2,\n");
    printf("  \"overflow_updates\": %" PRIu64 ",\n",
           modulus * (uint64_t)dimension * 2);
    printf("  \"state_bytes_per_prime\": %" PRIu64 ",\n",
           modulus * (uint64_t)sizeof(uint64_t));
    printf("  \"threads\": %d,\n", threads);
    printf("  \"work_ns\": %" PRIu64 ",\n", work_ns);
    printf("  \"work_primes\": %zu,\n", work_count);
    printf("  \"work_updates\": %" PRIu64 "\n",
           modulus * (uint64_t)dimension * (uint64_t)work_count);
    printf("}\n");

    free(output);
    free(primes);
    free(generator);
    return 0;
}
