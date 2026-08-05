// Exact source polynomial N(a) for the C63 S3 orbit reduction.
#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <map>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;
using Key = uint32_t;
using Poly = std::map<Key, cpp_int>;

static constexpr std::array<std::array<int, 3>, 5> NEIGHBORS{{
    {{2, 3, 4}}, {{0, 3, 4}}, {{0, 1, 4}}, {{0, 1, 2}}, {{1, 2, 3}}
}};

static Key add_key(Key a, Key b) {
    Key result = 0;
    Key place = 1;
    for (int i = 0; i < 6; ++i) {
        const unsigned exponent = (a / place % 16) + (b / place % 16);
        if (exponent > 15) std::abort();
        result += place * exponent;
        place *= 16;
    }
    return result;
}

static Poly add(Poly lhs, const Poly& rhs) {
    for (const auto& [key, coefficient] : rhs) lhs[key] += coefficient;
    return lhs;
}

static Poly multiply(const Poly& lhs, const Poly& rhs) {
    Poly result;
    for (const auto& [left_key, left_coefficient] : lhs) {
        for (const auto& [right_key, right_coefficient] : rhs) {
            result[add_key(left_key, right_key)] += left_coefficient * right_coefficient;
        }
    }
    return result;
}

static Poly variable(int index) {
    return {{Key(1) << (4 * index), cpp_int(1)}};
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;

    std::vector<std::array<int, 3>> permutations;
    std::array<int, 3> permutation{0, 1, 2};
    do permutations.push_back(permutation);
    while (std::next_permutation(permutation.begin(), permutation.end()));

    std::map<std::array<int, 3>, int> index;
    for (int i = 0; i < 6; ++i) index[permutations[i]] = i;

    int product[6][6];
    int inverse[6];
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            std::array<int, 3> composed{};
            for (int k = 0; k < 3; ++k) {
                composed[k] = permutations[i][permutations[j][k]];
            }
            product[i][j] = index.at(composed);
        }
    }
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            if (product[i][j] == 0 && product[j][i] == 0) inverse[i] = j;
        }
    }

    std::array<Poly, 6> value{
        variable(0), variable(1), variable(2),
        variable(3), variable(4), variable(5)
    };
    Poly one{{0, cpp_int(1)}};
    Poly total;

    for (int x1 = 0; x1 < 6; ++x1) {
        for (int x2 = 0; x2 < 6; ++x2) {
            for (int x3 = 0; x3 < 6; ++x3) {
                for (int x4 = 0; x4 < 6; ++x4) {
                    int x[5]{0, x1, x2, x3, x4};
                    Poly graph = one;
                    for (const auto& neighborhood : NEIGHBORS) {
                        Poly sum;
                        for (int y = 0; y < 6; ++y) {
                            Poly term = one;
                            for (int vertex : neighborhood) {
                                const int h = product[inverse[x[vertex]]][y];
                                term = multiply(term, value[h]);
                            }
                            sum = add(std::move(sum), term);
                        }
                        graph = multiply(graph, sum);
                    }
                    total = add(std::move(total), graph);
                }
            }
        }
    }

    std::filesystem::create_directories(argv[1]);
    std::ofstream output(std::string(argv[1]) + "/source-polynomial.tsv");
    output << "a0\ta1\ta2\ta5\ta3\ta4\tcoefficient\n";
    const std::array<int, 6> display_order{0, 1, 2, 5, 3, 4};
    for (const auto& [key, coefficient] : total) {
        if (coefficient == 0) continue;
        for (int index_position : display_order) {
            output << ((key >> (4 * index_position)) & 15) << '\t';
        }
        output << coefficient << '\n';
    }
}
