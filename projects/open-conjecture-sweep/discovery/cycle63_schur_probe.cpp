// Deterministic high-throughput C63 class-exchange falsifier probe.
#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;

struct Term {
    std::array<unsigned, 6> exponent{};
    long double coefficient{};
    cpp_int scaled_coefficient{};
};

struct Xoshiro256StarStar {
    std::array<uint64_t, 4> state{};
    static uint64_t rotate_left(uint64_t value, int shift) {
        return (value << shift) | (value >> (64 - shift));
    }
    static uint64_t splitmix64(uint64_t& value) {
        uint64_t z = (value += UINT64_C(0x9e3779b97f4a7c15));
        z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
        return z ^ (z >> 31);
    }
    explicit Xoshiro256StarStar(uint64_t seed) {
        for (auto& word : state) word = splitmix64(seed);
    }
    uint64_t next() {
        const uint64_t result = rotate_left(state[1] * 5, 7) * 9;
        const uint64_t temporary = state[1] << 17;
        state[2] ^= state[0]; state[3] ^= state[1];
        state[1] ^= state[2]; state[0] ^= state[3];
        state[2] ^= temporary; state[3] = rotate_left(state[3], 45);
        return result;
    }
    uint64_t coordinate() { return next() % 1000 + 1; }
};

static std::vector<std::string> split(const std::string& line) {
    std::vector<std::string> fields;
    std::stringstream stream(line);
    std::string field;
    while (std::getline(stream, field, '\t')) fields.push_back(field);
    return fields;
}

static cpp_int parse_integer(const std::string& text) {
    cpp_int value;
    std::stringstream stream(text);
    stream >> value;
    return value;
}

static std::vector<Term> load_terms(const std::string& path, const cpp_int& denominator_lcm) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open elementary polynomial");
    std::string line;
    std::getline(input, line);
    std::vector<Term> terms;
    while (std::getline(input, line)) {
        const auto fields = split(line);
        if (fields.size() != 8) throw std::runtime_error("bad TSV row");
        Term term;
        for (int i = 0; i < 6; ++i) term.exponent[i] = std::stoul(fields[i]);
        const long double numerator = std::stold(fields[6]);
        const long double denominator = std::stold(fields[7]);
        term.coefficient = numerator / denominator;
        term.scaled_coefficient = parse_integer(fields[6]) * (denominator_lcm / parse_integer(fields[7]));
        terms.push_back(std::move(term));
    }
    return terms;
}

static std::array<cpp_int, 4> exact_bad_factors(
    const std::vector<Term>& terms,
    const std::array<uint64_t, 6>& original
) {
    const cpp_int e = original[0];
    const cpp_int q1 = original[1], q2 = original[2], q3 = original[3];
    const cpp_int v1 = original[4], v2 = original[5];
    const std::array<cpp_int, 6> value{
        e,
        q1 + q2 + q3,
        q1*q2 + q1*q3 + q2*q3,
        q1*q2*q3,
        v1 + v2,
        v1*v2,
    };
    std::array<std::array<cpp_int, 16>, 6> powers{};
    for (int i = 0; i < 6; ++i) {
        powers[i][0] = 1;
        for (int degree = 1; degree < 16; ++degree) powers[i][degree] = powers[i][degree-1] * value[i];
    }
    cpp_int d_t2 = 0, d_t3 = 0, d_c2 = 0;
    for (const auto& term : terms) {
        if (term.exponent[2]) {
            cpp_int monomial = term.scaled_coefficient * term.exponent[2];
            for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 2)];
            d_t2 += monomial;
        }
        if (term.exponent[3]) {
            cpp_int monomial = term.scaled_coefficient * term.exponent[3];
            for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 3)];
            d_t3 += monomial;
        }
        if (term.exponent[5]) {
            cpp_int monomial = term.scaled_coefficient * term.exponent[5];
            for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 5)];
            d_c2 += monomial;
        }
    }
    return {-(d_t2 + q1*d_t3), -(d_t2 + q2*d_t3), -(d_t2 + q3*d_t3), -d_c2};
}

int main(int argc, char** argv) {
    if (argc != 5) return 2;
    const std::string input_path = argv[1];
    const std::string output_path = argv[2];
    const uint64_t seed = std::stoull(argv[3]);
    const uint64_t samples = std::stoull(argv[4]);
    const cpp_int denominator_lcm("11943936");
    const auto terms = load_terms(input_path, denominator_lcm);
    Xoshiro256StarStar generator(seed);

    long double minimum_trans = std::numeric_limits<long double>::infinity();
    long double minimum_cycle = std::numeric_limits<long double>::infinity();
    uint64_t exact_candidates = 0;
    bool reversal = false;
    std::array<uint64_t, 6> first_reversal{};

    for (uint64_t sample = 0; sample < samples && !reversal; ++sample) {
        std::array<uint64_t, 6> original{};
        uint64_t total = 0;
        for (auto& coordinate : original) { coordinate = generator.coordinate(); total += coordinate; }
        const long double scale = 1.0L / static_cast<long double>(total);
        const std::array<long double, 6> value{
            original[0] * scale,
            (original[1] + original[2] + original[3]) * scale,
            (original[1]*original[2] + original[1]*original[3] + original[2]*original[3]) * scale * scale,
            original[1]*original[2]*original[3] * scale * scale * scale,
            (original[4] + original[5]) * scale,
            original[4]*original[5] * scale * scale,
        };
        std::array<std::array<long double, 16>, 6> powers{};
        for (int i = 0; i < 6; ++i) {
            powers[i][0] = 1;
            for (int degree = 1; degree < 16; ++degree) powers[i][degree] = powers[i][degree-1] * value[i];
        }
        long double d_t2 = 0, d_t3 = 0, d_c2 = 0;
        for (const auto& term : terms) {
            if (term.exponent[2]) {
                long double monomial = term.coefficient * term.exponent[2];
                for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 2)];
                d_t2 += monomial;
            }
            if (term.exponent[3]) {
                long double monomial = term.coefficient * term.exponent[3];
                for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 3)];
                d_t3 += monomial;
            }
            if (term.exponent[5]) {
                long double monomial = term.coefficient * term.exponent[5];
                for (int i = 0; i < 6; ++i) monomial *= powers[i][term.exponent[i] - (i == 5)];
                d_c2 += monomial;
            }
        }
        const long double bad1 = -(d_t2 + original[1]*scale*d_t3);
        const long double bad2 = -(d_t2 + original[2]*scale*d_t3);
        const long double bad3 = -(d_t2 + original[3]*scale*d_t3);
        const long double bad_cycle = -d_c2;
        minimum_trans = std::min({minimum_trans, bad1, bad2, bad3});
        minimum_cycle = std::min(minimum_cycle, bad_cycle);
        if (bad1 < 0 || bad2 < 0 || bad3 < 0 || bad_cycle < 0) {
            ++exact_candidates;
            const auto exact = exact_bad_factors(terms, original);
            if (exact[0] < 0 || exact[1] < 0 || exact[2] < 0 || exact[3] < 0) {
                reversal = true;
                first_reversal = original;
            }
        }
    }

    std::filesystem::create_directories(std::filesystem::path(output_path).parent_path());
    std::ofstream output(output_path);
    output << std::setprecision(20);
    output << "{\n"
           << "  \"claim_boundary\": \"Deterministic exchange-sign falsifier probe; absence of a reversal is OBSERVED only.\",\n"
           << "  \"epistemic_status\": \"OBSERVED\",\n"
           << "  \"exact_candidates\": " << exact_candidates << ",\n"
           << "  \"exact_reversal\": " << (reversal ? "true" : "false") << ",\n"
           << "  \"minimum_cycle_factor\": " << minimum_cycle << ",\n"
           << "  \"minimum_trans_factor\": " << minimum_trans << ",\n"
           << "  \"samples\": " << samples << ",\n"
           << "  \"seed\": " << seed;
    if (reversal) {
        output << ",\n  \"first_reversal\": [";
        for (int i = 0; i < 6; ++i) output << (i ? "," : "") << first_reversal[i];
        output << "]";
    }
    output << "\n}\n";
    return reversal ? 1 : 0;
}
