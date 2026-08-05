#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>

namespace {

std::uint64_t inverse_mod(std::uint64_t p, std::uint64_t c) {
    for (std::uint64_t value = 0; value < c; ++value) {
        if ((p * value) % c == 1 % c) return value;
    }
    return c;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 5) {
        std::cerr << "usage: lrc_crt_diagonal P C SUMMARY_TSV MISMATCH_TSV\n";
        return 2;
    }

    const std::uint64_t p = std::stoull(argv[1]);
    const std::uint64_t c = std::stoull(argv[2]);
    if (p == 0 || c == 0 || std::gcd(p, c) != 1) {
        std::cerr << "P and C must be positive and coprime\n";
        return 3;
    }
    const std::uint64_t q = p * c;
    const std::uint64_t inv = inverse_mod(p, c);
    if (inv == c) {
        std::cerr << "modular inverse not found\n";
        return 4;
    }

    std::ofstream mismatches(argv[4], std::ios::trunc);
    if (!mismatches) return 5;
    mismatches << "p\tc\ts\ta\tx\txp\txc\tj\tdirect_bad\tcrt_bad\n";

    std::uint64_t comparisons = 0;
    std::uint64_t direct_bad_count = 0;
    std::uint64_t crt_bad_count = 0;
    std::uint64_t mismatch_count = 0;
    std::uint64_t strict_boundary_rows = 0;

    for (std::uint64_t s = 0; s < q; ++s) {
        for (std::uint64_t a = 0; a < q; ++a) {
            const std::uint64_t x = (a * s) % q;
            const std::uint64_t xp = ((a % p) * (s % p)) % p;
            const std::uint64_t xc = ((a % c) * (s % c)) % c;
            const std::uint64_t delta = (xc + c - (xp % c)) % c;
            const std::uint64_t j = (delta * inv) % c;
            const bool direct_bad = c * std::min(x, q - x) < q;
            const bool crt_bad = j == 0 || (j == c - 1 && xp != 0);
            ++comparisons;
            direct_bad_count += direct_bad;
            crt_bad_count += crt_bad;
            strict_boundary_rows += (j == c - 1 && xp == 0);
            if (direct_bad != crt_bad) {
                ++mismatch_count;
                mismatches << p << '\t' << c << '\t' << s << '\t' << a
                           << '\t' << x << '\t' << xp << '\t' << xc
                           << '\t' << j << '\t' << direct_bad << '\t'
                           << crt_bad << '\n';
            }
        }
    }

    std::ofstream summary(argv[3], std::ios::trunc);
    if (!summary) return 6;
    summary << "p\tc\tq\tinverse\tcomparisons\tdirect_bad\tcrt_bad"
               "\tmismatches\tstrict_boundary_rows\n";
    summary << p << '\t' << c << '\t' << q << '\t' << inv << '\t'
            << comparisons << '\t' << direct_bad_count << '\t'
            << crt_bad_count << '\t' << mismatch_count << '\t'
            << strict_boundary_rows << '\n';
    return mismatch_count == 0 ? 0 : 1;
}
