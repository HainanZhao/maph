from fractions import Fraction
from math import gcd
import unittest

from src.sic_stark import (
    IDENTITY_2,
    biquadratic_2_3_galois_action,
    biquadratic_2_3_multiply,
    canonical_beta_is_rational,
    canonical_beta_power_trace,
    canonical_characteristic_correction_index,
    canonical_cyclic_approximant_pair,
    canonical_cyclic_approximant_record,
    canonical_dimension_four_algebraic_unit_packet_record,
    canonical_dimension_four_countermodel,
    canonical_dimension_four_character_resolvents,
    canonical_dimension_four_distribution_relation_record,
    canonical_dimension_four_double_sine_factor_record,
    canonical_dimension_four_floquet_gate_record,
    canonical_dimension_four_fractional_cell_record,
    canonical_dimension_four_zak_gate_record,
    canonical_dimension_four_internal_distribution_maps,
    canonical_dimension_four_holomorphic_quartic_countermodel_record,
    canonical_dimension_four_laurent_action,
    canonical_dimension_four_localization_record,
    canonical_dimension_four_packet_directions,
    canonical_dimension_four_packet_evaluation,
    canonical_dimension_four_packet_permutations,
    canonical_dimension_four_packet_relation_residuals,
    canonical_dimension_four_perturbation_witness,
    canonical_dimension_four_relation_nullities,
    canonical_dimension_four_residual_laurent_packet,
    canonical_dimension_four_ray_class_record,
    canonical_dimension_four_trace_obstruction_record,
    canonical_equal_base_q_binomial_cancellation,
    canonical_family_record,
    canonical_form,
    canonical_form_stabilizer_residual,
    canonical_floquet_block_degrees,
    canonical_floquet_commutator_trace_signature,
    canonical_floquet_transfer_support,
    canonical_general_modular_characteristic,
    canonical_general_modular_modulus,
    canonical_general_modular_node_strip_margins,
    canonical_general_modular_parameters,
    canonical_ghost_minor_record,
    canonical_ghost_exterior_square_record,
    canonical_ghost_weyl_entry_terms,
    canonical_global_unit_residues,
    canonical_jacobi_scale_exponents,
    canonical_jacobi_word,
    canonical_kernel_identity,
    canonical_level_quotient,
    canonical_level_stabilizer,
    canonical_local_unit_cosets,
    canonical_pentagon_compatibility_record,
    canonical_primitive_correction_indices,
    canonical_primitive_direction_unit_stabilizers,
    canonical_primitive_sigma_shift_coordinates,
    canonical_primitive_sigma_shifts_are_quasiperiods,
    canonical_proper_scalar_distribution_divisors,
    canonical_quadratic_identity,
    canonical_quadratic_residue_multiply,
    canonical_quadratic_residue_norm,
    canonical_quadratic_residue_units,
    canonical_odd_constant_overlap_countermodel_record,
    canonical_parity_schatten_record,
    canonical_reciprocal_trace_moment_record,
    canonical_residue_multiplication_matrix,
    canonical_root_filtered_stokes_record,
    canonical_shift_partner,
    canonical_scalar_distribution_fibers,
    canonical_stabilizer,
    canonical_tcc_equation_count,
    canonical_tcc_equation_representatives,
    canonical_tcc_fourier_frequency,
    canonical_tcc_formal_signature,
    canonical_tcc_orbit_model_phase_totals,
    canonical_tcc_orbit_bound,
    canonical_twist_exponent,
    canonical_twist_kernel,
    canonical_twist_multiplier,
    canonical_zauner_action,
    canonical_zauner_block_multiplicities,
    canonical_zauner_orbit_representative,
    canonical_zauner_orbit_sum,
    canonical_zauner_orbits,
    canonical_zak_alternating_exponent,
    canonical_zak_cocycle_exponent,
    canonical_zak_matrix_entry_terms,
    canonical_zak_quadratic_exponent,
    canonical_zak_representation_action,
    canonical_zak_representation_product_defect,
    canonical_zak_reflection_quadratic_record,
    canonical_zak_zauner_block_record,
    determinant,
    extended_displacement_modulus,
    form_discriminant,
    matrix_multiply,
    matrix_exterior_square_energy,
    matrix_gram_second_elementary,
    matrix_parity_schatten_certificate,
    matrix_mod,
    matrix_power,
    matrix_vector_multiply,
    q_pochhammer_fractional_cell_determinant_coefficient,
    symplectic_pair,
    transform_form,
)


class CanonicalSicStarkTests(unittest.TestCase):
    def test_canonical_discriminant_identity(self) -> None:
        for dimension in range(4, 501):
            discriminant = form_discriminant(canonical_form(dimension))
            self.assertEqual(
                discriminant, (dimension + 1) * (dimension - 3)
            )

    def test_canonical_stabilizer_quadratic_identity(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_quadratic_identity(dimension),
                ((0, 0), (0, 0)),
            )

    def test_canonical_stabilizer_is_unimodular(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(determinant(canonical_stabilizer(dimension)), 1)

    def test_canonical_stabilizer_fixes_form(self) -> None:
        for dimension in range(4, 501):
            form = canonical_form(dimension)
            stabilizer = canonical_stabilizer(dimension)
            self.assertEqual(transform_form(form, stabilizer), form)
            self.assertEqual(
                canonical_form_stabilizer_residual(dimension), (0, 0, 0)
            )

    def test_canonical_stabilizer_cube_is_identity_mod_d(self) -> None:
        for dimension in range(4, 501):
            cube = canonical_level_stabilizer(dimension)
            self.assertEqual(matrix_mod(cube, dimension), IDENTITY_2)

    def test_exact_level_stabilizer_lift(self) -> None:
        for dimension in range(4, 501):
            quotient = canonical_level_quotient(dimension)
            reconstructed = tuple(
                tuple(
                    IDENTITY_2[row][column]
                    + dimension * quotient[row][column]
                    for column in range(2)
                )
                for row in range(2)
            )
            self.assertEqual(
                reconstructed, canonical_level_stabilizer(dimension)
            )

    def test_beta_is_irrational_in_the_canonical_range(self) -> None:
        for dimension in range(4, 501):
            self.assertFalse(canonical_beta_is_rational(dimension))

    def test_general_modular_modulus_differs_from_tcc_modulus(self) -> None:
        for dimension in range(4, 501):
            modulus = canonical_general_modular_modulus(dimension)
            self.assertEqual(modulus, dimension * (dimension - 2))
            self.assertEqual(
                modulus,
                abs(canonical_level_stabilizer(dimension)[1][0]),
            )
            self.assertNotEqual(modulus, dimension)

    def test_general_modular_parameter_dictionary(self) -> None:
        self.assertEqual(
            canonical_general_modular_parameters(4),
            (8, -21, 3, 8),
        )
        for dimension in range(4, 501):
            k, p, r, s = canonical_general_modular_parameters(
                dimension
            )
            matrix = canonical_level_stabilizer(dimension)
            self.assertEqual(matrix, ((-p, -s), (k, -r)))
            self.assertEqual(p * r + k * s, 1)
            self.assertEqual(k, dimension * (dimension - 2))
            self.assertEqual(r, dimension - 1)
            self.assertEqual(s, k)

    def test_quadratic_residue_multiplication_representation(
        self,
    ) -> None:
        for dimension in range(4, 31):
            global_units = canonical_global_unit_residues(dimension)
            self.assertEqual(
                global_units,
                ((1, 0), (0, 1), (dimension - 1, dimension - 1)),
            )
            self.assertEqual(
                canonical_quadratic_residue_multiply(
                    dimension, global_units[1], global_units[1]
                ),
                global_units[2],
            )
            self.assertEqual(
                canonical_quadratic_residue_multiply(
                    dimension, global_units[2], global_units[1]
                ),
                global_units[0],
            )
            for unit in canonical_quadratic_residue_units(dimension):
                matrix = canonical_residue_multiplication_matrix(
                    dimension, unit
                )
                self.assertEqual(
                    determinant(matrix) % dimension,
                    canonical_quadratic_residue_norm(
                        dimension, unit
                    ),
                )
                for global_unit in global_units:
                    product = canonical_quadratic_residue_multiply(
                        dimension, unit, global_unit
                    )
                    self.assertEqual(
                        canonical_residue_multiplication_matrix(
                            dimension, product
                        ),
                        matrix_mod(
                            matrix_multiply(
                                matrix,
                                canonical_residue_multiplication_matrix(
                                    dimension, global_unit
                                ),
                            ),
                            dimension,
                        ),
                    )

    def test_primitive_direction_has_no_new_local_stabilizer(
        self,
    ) -> None:
        for dimension in range(4, 101):
            stabilizers = (
                canonical_primitive_direction_unit_stabilizers(
                    dimension
                )
            )
            self.assertEqual(stabilizers["exact"], ((1, 0),))
            self.assertEqual(
                set(stabilizers["up_to_zauner"]),
                set(canonical_global_unit_residues(dimension)),
            )

    def test_dimension_four_local_ray_quotient_and_phase_failure(
        self,
    ) -> None:
        record = canonical_dimension_four_trace_obstruction_record()
        self.assertEqual(record["local_unit_count"], 12)
        self.assertEqual(record["local_unit_quotient_order"], 4)
        self.assertTrue(record["local_unit_quotient_exponent_two"])
        self.assertEqual(
            record["local_unit_quotient_structure"], "C2 x C2"
        )
        cosets = record["local_unit_quotient_cosets"]
        self.assertTrue(all(len(coset) == 3 for coset in cosets))
        self.assertEqual(
            {unit for coset in cosets for unit in coset},
            set(canonical_quadratic_residue_units(4)),
        )
        witness = record["phase_descent_witness"]
        self.assertEqual(witness["acted_direction"], (0, 3))
        self.assertEqual(witness["acted_characteristic"], (0, 3))
        self.assertNotEqual(
            witness["original_phase"],
            witness["fixed_direction_phase"],
        )
        self.assertEqual(
            witness["original_phase"],
            witness["simultaneous_phase"],
        )

    def test_dimension_four_residual_packet_is_the_regular_action(
        self,
    ) -> None:
        packet = canonical_dimension_four_residual_laurent_packet()
        self.assertEqual(
            canonical_dimension_four_packet_directions(),
            ((0, 3), (0, 1), (1, 1), (2, 3)),
        )
        permutations = canonical_dimension_four_packet_permutations()
        self.assertEqual(len(set(permutations)), 4)
        for group_index, permutation in enumerate(permutations):
            self.assertEqual(set(permutation), set(range(4)))
            for packet_index, polynomial in enumerate(packet):
                self.assertEqual(
                    canonical_dimension_four_laurent_action(
                        polynomial, group_index
                    ),
                    packet[permutation[packet_index]],
                )

    def test_dimension_four_character_resolvents_are_eigenvectors(
        self,
    ) -> None:
        resolvents = canonical_dimension_four_character_resolvents()
        character_table = {
            "T": (1, 1, 1, 1),
            "U": (1, -1, 1, -1),
            "V": (1, 1, -1, -1),
            "W": (1, -1, -1, 1),
        }
        for name, signs in character_table.items():
            polynomial = resolvents[name]
            self.assertTrue(polynomial)
            for group_index, sign in enumerate(signs):
                self.assertEqual(
                    canonical_dimension_four_laurent_action(
                        polynomial, group_index
                    ),
                    {
                        exponent: sign * coefficient
                        for exponent, coefficient in polynomial.items()
                    },
                )

    def test_dimension_four_first_packet_relations_do_not_force_zero(
        self,
    ) -> None:
        self.assertEqual(
            canonical_dimension_four_relation_nullities(5),
            (0, 0, 0, 0, 1),
        )
        self.assertEqual(
            canonical_dimension_four_packet_relation_residuals(),
            {"degree_five": {}, "degree_six": {}},
        )
        packet = canonical_dimension_four_packet_evaluation(2, 1)
        self.assertEqual(
            packet,
            (
                Fraction(3, 2),
                Fraction(3, 4),
                Fraction(3),
                Fraction(-3),
            ),
        )
        character_values = (
            packet[0] + packet[1] + packet[2] + packet[3],
            packet[0] - packet[1] + packet[2] - packet[3],
            packet[0] + packet[1] - packet[2] - packet[3],
            packet[0] - packet[1] - packet[2] + packet[3],
        )
        self.assertEqual(
            character_values,
            (
                Fraction(9, 4),
                Fraction(27, 4),
                Fraction(9, 4),
                Fraction(-21, 4),
            ),
        )
        self.assertTrue(all(character_values))

    def test_dimension_four_algebraic_units_give_nonzero_galois_packet(
        self,
    ) -> None:
        record = (
            canonical_dimension_four_algebraic_unit_packet_record()
        )
        one = (
            Fraction(1),
            Fraction(0),
            Fraction(0),
            Fraction(0),
        )
        self.assertEqual(record["unit_products"], (one, one))
        units = record["units"]
        permutations = canonical_dimension_four_packet_permutations()
        for group_index, permutation in enumerate(permutations):
            for unit_index, unit in enumerate(units):
                self.assertEqual(
                    biquadratic_2_3_galois_action(
                        unit, group_index
                    ),
                    units[permutation[unit_index]],
                )

        packet = record["packet"]
        for group_index, permutation in enumerate(permutations):
            for packet_index, value in enumerate(packet):
                self.assertEqual(
                    biquadratic_2_3_galois_action(
                        value, group_index
                    ),
                    packet[permutation[packet_index]],
                )
        self.assertEqual(
            record["character_values"],
            (
                (Fraction(3200), Fraction(0), Fraction(0), Fraction(0)),
                (Fraction(0), Fraction(0), Fraction(0), Fraction(1440)),
                (Fraction(0), Fraction(0), Fraction(1920), Fraction(0)),
                (Fraction(0), Fraction(2144), Fraction(0), Fraction(0)),
            ),
        )
        self.assertTrue(record["all_packet_components_nonzero"])
        self.assertTrue(record["all_character_values_nonzero"])
        self.assertEqual(
            biquadratic_2_3_multiply(units[0], units[1]), one
        )

    def test_dimension_four_distribution_relations_are_not_specific(
        self,
    ) -> None:
        second_fibers = canonical_scalar_distribution_fibers(4, 2)
        fourth_fibers = canonical_scalar_distribution_fibers(4, 4)
        self.assertEqual(
            set(second_fibers),
            {(0, 0), (0, 2), (2, 0), (2, 2)},
        )
        self.assertTrue(
            all(len(fiber) == 4 for fiber in second_fibers.values())
        )
        self.assertEqual(set(fourth_fibers), {(0, 0)})
        self.assertEqual(len(fourth_fibers[(0, 0)]), 16)
        self.assertEqual(
            canonical_dimension_four_internal_distribution_maps(),
            (
                ((2, 0), (0, 2)),
                ((0, 2), (2, 2)),
                ((2, 2), (2, 0)),
                ((0, 0), (0, 0)),
            ),
        )

        record = canonical_dimension_four_distribution_relation_record()
        self.assertEqual(record["fiber_sizes"], {2: (4, 4, 4, 4), 4: (16,)})
        self.assertTrue(record["all_formal_relations_hold"])
        self.assertTrue(record["all_algebraic_relations_hold"])
        self.assertTrue(
            all(
                defect == (0, 0)
                for defect in record[
                    "formal_exponent_defects"
                ].values()
            )
        )
        self.assertEqual(
            canonical_proper_scalar_distribution_divisors(4), (2,)
        )
        for prime in (5, 7, 11, 13, 17, 19):
            self.assertEqual(
                canonical_proper_scalar_distribution_divisors(prime),
                (),
            )

    def test_multiplicative_perturbation_forces_nonzero_coefficient(
        self,
    ) -> None:
        witness = canonical_dimension_four_perturbation_witness()
        self.assertEqual(witness["output"], (1, 0))
        self.assertEqual(witness["laurent_exponent"], (2, 0))
        self.assertEqual(
            tuple(term[:2] for term in witness["terms"]),
            (((0, 1), 3), ((1, 3), 0)),
        )
        self.assertEqual(witness["phase_sum"], (1, -1))
        self.assertEqual(
            witness["baseline_orbit_ratios"],
            (((0, 1), (0, 3)), ((0, 1), (0, 3))),
        )
        self.assertTrue(witness["ratios_are_identical"])
        self.assertTrue(witness["coefficient_is_forced_nonzero"])

    def test_fractional_cell_elimination_fails_both_candidate_gates(
        self,
    ) -> None:
        coefficient = (
            q_pochhammer_fractional_cell_determinant_coefficient()
        )
        self.assertEqual(
            coefficient,
            {
                (0, 0): Fraction(-1),
                (1, 0): Fraction(1),
                (0, 1): Fraction(1),
                (1, 1): Fraction(-1),
            },
        )

        record = canonical_dimension_four_fractional_cell_record()
        self.assertEqual(record["cell_count"], 16)
        self.assertTrue(record["all_holonomies_are_trivial"])
        self.assertFalse(record["flatness_rejects_deformation"])
        self.assertTrue(
            record["bilinear_rejects_deformation_on_every_cell"]
        )
        self.assertFalse(
            record["q_pochhammer_bilinear_identity_holds"]
        )
        self.assertEqual(
            record["bilinear_deformation_defects"][(0, 0)],
            (0, 1),
        )
        self.assertEqual(
            record["gate_table"],
            {
                "closed_cell_flatness": {
                    "analytic_identity": True,
                    "rejects_deformation": False,
                    "viable": False,
                },
                "rank_one_bilinear": {
                    "analytic_identity": False,
                    "rejects_deformation": True,
                    "viable": False,
                },
            },
        )
        self.assertFalse(record["any_candidate_passes_both_gates"])

    def test_floquet_transfer_is_only_a_weighted_permutation(
        self,
    ) -> None:
        for dimension in range(4, 31):
            support = canonical_floquet_transfer_support(dimension)
            self.assertEqual(len(support), dimension * dimension)
            self.assertEqual(
                len({source for source, _ in support}),
                dimension * dimension,
            )
            self.assertEqual(
                len({target for _, target in support}),
                dimension * dimension,
            )
            self.assertEqual(
                canonical_floquet_block_degrees(dimension),
                tuple(
                    len(orbit)
                    for orbit in canonical_zauner_orbits(dimension)
                ),
            )
            self.assertTrue(
                all(
                    degree in (1, 3)
                    for degree in (
                        canonical_floquet_block_degrees(dimension)
                    )
                )
            )
            if dimension <= 12:
                for output in canonical_tcc_equation_representatives(
                    dimension
                ):
                    self.assertEqual(
                        canonical_floquet_commutator_trace_signature(
                            dimension, output
                        ),
                        canonical_tcc_formal_signature(
                            dimension, output
                        ),
                    )

    def test_floquet_spectrum_does_not_reject_deformation(
        self,
    ) -> None:
        record = canonical_dimension_four_floquet_gate_record()
        self.assertEqual(record["block_degrees"], (1, 3, 3, 3, 3, 3))
        self.assertEqual(record["gauge_invariant_cycle_count"], 6)
        self.assertEqual(record["transfer_nonzero_count"], 16)
        self.assertTrue(record["one_nonzero_per_source"])
        self.assertTrue(record["one_nonzero_per_target"])
        self.assertTrue(
            record["deformation_lifts_to_weighted_transfer"]
        )
        self.assertFalse(
            record["weighted_transfer_rejects_deformation"]
        )
        self.assertTrue(
            all(
                defect == (0, 0)
                for defect in record["monodromy_defects"].values()
            )
        )
        self.assertEqual(
            record["primitive_commutator_trace_signature"],
            canonical_tcc_formal_signature(4, (1, 0)),
        )
        self.assertEqual(
            canonical_floquet_commutator_trace_signature(4, (1, 0)),
            canonical_tcc_formal_signature(4, (1, 0)),
        )
        self.assertTrue(
            record["primitive_trace_coefficient_is_forced_nonzero"]
        )
        self.assertTrue(
            record["algebraic_commutator_trace_packet_is_nonzero"]
        )
        self.assertFalse(record["floquet_spectrum_alone_can_force_tcc"])

    def test_zak_cocycle_and_weyl_representation_are_exact(
        self,
    ) -> None:
        for dimension in range(4, 11):
            for left_first in range(dimension):
                for left_second in range(dimension):
                    left = (left_first, left_second)
                    for right_first in range(dimension):
                        for right_second in range(dimension):
                            right = (right_first, right_second)
                            self.assertEqual(
                                canonical_zak_alternating_exponent(
                                    dimension, left, right
                                ),
                                (
                                    -symplectic_pair(left, right)
                                )
                                % dimension,
                            )
                            for basis_index in range(dimension):
                                self.assertEqual(
                                    canonical_zak_representation_product_defect(
                                        dimension,
                                        left,
                                        right,
                                        basis_index,
                                    ),
                                    (0, 0),
                                )

    def test_zak_twisted_convolution_matches_tcc_phase(
        self,
    ) -> None:
        for dimension in range(4, 14):
            for output_first in range(dimension):
                for output_second in range(dimension):
                    output = (output_first, output_second)
                    for first in range(dimension):
                        for second in range(dimension):
                            characteristic = (first, second)
                            remainder = (
                                (output_first - first) % dimension,
                                (output_second - second) % dimension,
                            )
                            self.assertEqual(
                                (
                                    canonical_zak_cocycle_exponent(
                                        dimension,
                                        characteristic,
                                        remainder,
                                    )
                                    + canonical_zak_quadratic_exponent(
                                        dimension, characteristic
                                    )
                                )
                                % dimension,
                                canonical_twist_exponent(
                                    dimension,
                                    output,
                                    characteristic,
                                ),
                            )

        record = canonical_dimension_four_zak_gate_record()
        self.assertEqual(record["group_order"], 16)
        self.assertEqual(record["matrix_dimension"], 4)
        self.assertEqual(record["twisted_algebra_dimension"], 16)
        self.assertEqual(record["terms_per_matrix_entry"], (4,) * 16)
        self.assertTrue(record["all_residual_phases_match"])
        self.assertTrue(record["representation_is_exact"])
        self.assertTrue(
            record["alternating_bicharacter_is_nondegenerate"]
        )
        self.assertTrue(
            record["zak_transform_closes_on_finite_matrices"]
        )
        self.assertEqual(
            record["matrix_target"],
            "Zak(F) Zak(V) = d^2 I_d",
        )
        self.assertTrue(record["deformation_rejects_matrix_target"])
        self.assertFalse(record["matrix_target_proved_for_rm_values"])

    def test_zak_representation_action_uses_extended_phase_modulus(
        self,
    ) -> None:
        self.assertEqual(
            canonical_zak_representation_action(4, (1, 2), 3),
            (0, 1),
        )
        self.assertEqual(
            canonical_zak_representation_action(5, (1, 2), 3),
            (4, 3),
        )
        self.assertEqual(
            canonical_zak_matrix_entry_terms(4, 0, 3),
            (
                ((1, 0), 1),
                ((1, 1), 4),
                ((1, 2), 1),
                ((1, 3), 0),
            ),
        )

    def test_characteristic_embedding_into_general_modular_gamma(
        self,
    ) -> None:
        for dimension in range(4, 51):
            modulus = canonical_general_modular_modulus(dimension)
            samples = set()
            for first in range(dimension):
                for second in range(dimension):
                    continuous, discrete = (
                        canonical_general_modular_characteristic(
                            dimension, (first, second)
                        )
                    )
                    self.assertEqual(
                        continuous,
                        (
                            Fraction(1 - second),
                            Fraction((dimension - 2) * second),
                        ),
                    )
                    self.assertEqual(
                        discrete,
                        (
                            second
                            - (dimension - 2) * first
                            - 1
                        )
                        % modulus,
                    )
                    self.assertEqual(
                        discrete % (dimension - 2),
                        (second - 1) % (dimension - 2),
                    )
                    samples.add((continuous, discrete))
            self.assertEqual(len(samples), dimension * dimension)

    def test_general_modular_nodes_are_inside_the_pole_free_strip(
        self,
    ) -> None:
        for dimension in range(4, 501):
            for second in range(dimension):
                lower, upper = (
                    canonical_general_modular_node_strip_margins(
                        dimension, (0, second)
                    )
                )
                self.assertEqual(lower, (1, second))
                self.assertEqual(upper, (1, dimension - second))
                self.assertGreaterEqual(lower[1], 0)
                self.assertGreater(upper[1], 0)

    def test_dimension_four_localization_phase_match(self) -> None:
        record = canonical_dimension_four_localization_record()
        self.assertEqual(record["parameters"], (8, -21, 3, 8))
        self.assertEqual(
            record["beta_integral_parameters"],
            {"N": 3, "g": "Q", "alpha": "-3D"},
        )
        nodes = record["nodes"]
        self.assertEqual(len(nodes), 16)
        self.assertEqual(
            {
                (
                    node["continuous_coordinates"],
                    node["discrete"],
                )
                for node in nodes
            },
            {
                (
                    (
                        Fraction(1 - second),
                        Fraction(2 * second),
                    ),
                    (second - 2 * first - 1) % 8,
                )
                for first in range(4)
                for second in range(4)
            },
        )
        for node in nodes:
            first, second = node["characteristic"]
            discrete = node["discrete"]
            self.assertEqual(
                node["selection_parity"],
                discrete % 2,
            )
            self.assertEqual(
                node["tcc_phase"],
                (-2 * (first + second)) % 8,
            )
            self.assertEqual(
                node["normalized_tcc_phase"],
                (
                    node["tcc_phase"]
                    + node["normalization_ratio"]
                )
                % 8,
            )
            self.assertEqual(node["global_phase_difference"], 3)
            self.assertGreaterEqual(node["lower_strip_margin"][1], 0)
            self.assertGreater(node["upper_strip_margin"][1], 0)

    def test_primitive_sigma_shifts_miss_the_period_lattice(self) -> None:
        for dimension in range(4, 501):
            coordinates = canonical_primitive_sigma_shift_coordinates(
                dimension
            )
            self.assertEqual(
                coordinates,
                (
                    (Fraction(1, dimension), Fraction(0)),
                    (
                        Fraction(dimension - 1, dimension),
                        Fraction(-1, dimension),
                    ),
                    (
                        Fraction(dimension - 2),
                        Fraction(-(dimension - 1), dimension),
                    ),
                ),
            )
            self.assertEqual(
                canonical_primitive_sigma_shifts_are_quasiperiods(
                    dimension
                ),
                (False, False, False),
            )

            # Pair multiplication in Q(beta), with
            # beta^2=(d-1)beta-1, checks d*delta_k*beta^k=1.
            def multiply(
                left: tuple[Fraction, Fraction],
                right: tuple[Fraction, Fraction],
            ) -> tuple[Fraction, Fraction]:
                a, b = left
                c, e = right
                return (
                    a * c - b * e,
                    a * e + b * c + (dimension - 1) * b * e,
                )

            beta = (Fraction(0), Fraction(1))
            beta_power = (Fraction(1), Fraction(0))
            for coordinate in coordinates:
                scaled = (
                    dimension * coordinate[0],
                    dimension * coordinate[1],
                )
                self.assertEqual(
                    multiply(scaled, beta_power),
                    (Fraction(1), Fraction(0)),
                )
                beta_power = multiply(beta_power, beta)

    def test_dimension_four_pentagon_compatibility_record(self) -> None:
        record = canonical_pentagon_compatibility_record(4)
        self.assertFalse(record["beta_rational"])
        self.assertFalse(record["cyclic_parameter_is_root_of_unity"])
        self.assertEqual(record["characteristic_modulus"], 4)
        self.assertEqual(record["general_modular_modulus"], 8)
        self.assertFalse(record["moduli_match"])
        self.assertEqual(
            record["primitive_shift_coordinates"],
            (
                (Fraction(1, 4), Fraction(0)),
                (Fraction(3, 4), Fraction(-1, 4)),
                (Fraction(2), Fraction(-3, 4)),
            ),
        )
        self.assertEqual(
            record["primitive_shifts_are_quasiperiods"],
            (False, False, False),
        )

    def test_twist_kernel_has_dimension_independent_representative(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_twist_kernel(dimension),
                ((0, dimension - 1), (1, 1)),
            )
            self.assertEqual(
                canonical_kernel_identity(dimension), ((0, 0), (0, 0))
            )

    def test_shift_one_is_compatible_with_identity_twist(self) -> None:
        for dimension in range(4, 501):
            modulus = extended_displacement_modulus(dimension)
            self.assertEqual(
                canonical_twist_multiplier(dimension, 1),
                1 % modulus,
            )
            self.assertEqual(
                canonical_twist_multiplier(dimension, 0),
                -1 % modulus,
            )

    def test_shift_conjugation_pairs_zero_and_one(self) -> None:
        for dimension in range(4, 501):
            modulus = extended_displacement_modulus(dimension)
            self.assertEqual(canonical_shift_partner(dimension, 0), 1)
            self.assertEqual(canonical_shift_partner(dimension, 1), 0)
            for shift in range(dimension):
                partner = canonical_shift_partner(dimension, shift)
                self.assertEqual(
                    canonical_shift_partner(dimension, partner), shift
                )
                self.assertEqual(
                    canonical_twist_multiplier(dimension, partner),
                    -canonical_twist_multiplier(dimension, shift)
                    % modulus,
                )

    def test_characteristic_correction_index(self) -> None:
        for dimension in range(4, 101):
            level = canonical_level_stabilizer(dimension)
            for vector in (
                (0, 0),
                (1, 0),
                (0, 1),
                (dimension - 1, dimension - 2),
            ):
                transformed = matrix_vector_multiply(level, vector)
                difference = (
                    vector[0] - transformed[0],
                    vector[1] - transformed[1],
                )
                self.assertEqual(difference[0] % dimension, 0)
                self.assertEqual(difference[1] % dimension, 0)
                self.assertEqual(
                    difference[1] // dimension,
                    canonical_characteristic_correction_index(
                        dimension, vector
                    ),
                )

    def test_canonical_zauner_orbits_have_length_one_or_three(self) -> None:
        for dimension in range(4, 101):
            orbits = canonical_zauner_orbits(dimension)
            self.assertTrue(all(len(orbit) in (1, 3) for orbit in orbits))
            self.assertEqual(
                sum(len(orbit) for orbit in orbits), dimension * dimension
            )
            fixed_count = sum(len(orbit) == 1 for orbit in orbits)
            self.assertEqual(fixed_count, 3 if dimension % 3 == 0 else 1)
            self.assertEqual(
                len(orbits), canonical_tcc_orbit_bound(dimension)
            )
            self.assertEqual(
                len(orbits) - 1,
                canonical_tcc_equation_count(dimension),
            )
            self.assertEqual(
                len(orbits) - 1,
                len(canonical_tcc_equation_representatives(dimension)),
            )

    def test_nonzero_fixed_vectors_when_three_divides_dimension(self) -> None:
        for dimension in (6, 9, 12, 15):
            step = dimension // 3
            expected = {(0, 0), (step, step), (2 * step, 2 * step)}
            fixed = {
                vector
                for vector in expected
                if canonical_zauner_action(dimension, vector) == vector
            }
            self.assertEqual(fixed, expected)

    def test_each_zauner_orbit_sums_to_zero(self) -> None:
        for dimension in range(4, 101):
            for first in range(dimension):
                for second in range(dimension):
                    self.assertEqual(
                        canonical_zauner_orbit_sum(
                            dimension, (first, second)
                        ),
                        (0, 0),
                    )

    def test_twist_phase_is_zauner_invariant(self) -> None:
        for dimension in range(4, 13):
            for p_1 in range(dimension):
                for p_2 in range(dimension):
                    left = (p_1, p_2)
                    acted_left = canonical_zauner_action(
                        dimension, left
                    )
                    for q_1 in range(dimension):
                        for q_2 in range(dimension):
                            right = (q_1, q_2)
                            acted_right = canonical_zauner_action(
                                dimension, right
                            )
                            self.assertEqual(
                                canonical_twist_exponent(
                                    dimension, acted_left, acted_right
                                ),
                                canonical_twist_exponent(
                                    dimension, left, right
                                ),
                            )

    def test_formal_tcc_signature_is_zauner_invariant(self) -> None:
        for dimension in range(4, 16):
            representatives = canonical_tcc_equation_representatives(
                dimension
            )
            self.assertEqual(
                representatives, tuple(sorted(representatives))
            )
            for first in range(dimension):
                for second in range(dimension):
                    output = (first, second)
                    acted_output = canonical_zauner_action(
                        dimension, output
                    )
                    self.assertEqual(
                        canonical_tcc_formal_signature(
                            dimension, acted_output
                        ),
                        canonical_tcc_formal_signature(
                            dimension, output
                        ),
                    )

    def test_zero_output_tcc_signature_is_automatic(self) -> None:
        for dimension in range(4, 101):
            signature = canonical_tcc_formal_signature(
                dimension, (0, 0)
            )
            self.assertEqual(sum(signature.values()), dimension * dimension)
            for (exponent, numerator, denominator), multiplicity in (
                signature.items()
            ):
                self.assertEqual(exponent, 0)
                self.assertEqual(numerator, denominator)
                self.assertGreater(multiplicity, 0)

    def test_tcc_twist_is_a_symplectic_fourier_frequency(self) -> None:
        for dimension in range(4, 21):
            for output in (
                (0, 0),
                (1, 0),
                (0, 1),
                (dimension - 1, dimension - 2),
            ):
                frequency = canonical_tcc_fourier_frequency(
                    dimension, output
                )
                for first in range(dimension):
                    for second in range(dimension):
                        characteristic = (first, second)
                        self.assertEqual(
                            canonical_twist_exponent(
                                dimension, output, characteristic
                            ),
                            symplectic_pair(
                                frequency, characteristic
                            )
                            % dimension,
                        )

    def test_primitive_tcc_frequency_and_correction_shift(self) -> None:
        for dimension in range(4, 101):
            self.assertEqual(
                canonical_tcc_fourier_frequency(
                    dimension, (1, 0)
                ),
                (1, dimension - 1),
            )
            for characteristic in (
                (0, 0),
                (1, 0),
                (0, 1),
                (dimension - 1, dimension - 2),
            ):
                first, shifted = canonical_primitive_correction_indices(
                    dimension, characteristic
                )
                self.assertEqual(shifted, first + dimension - 2)

    def test_exact_dimension_four_countermodel(self) -> None:
        dimension = 4
        values = canonical_dimension_four_countermodel()
        for first in range(dimension):
            for second in range(dimension):
                characteristic = (first, second)
                negative = (-first, -second)
                value = values[
                    canonical_zauner_orbit_representative(
                        dimension, characteristic
                    )
                ]
                negative_value = values[
                    canonical_zauner_orbit_representative(
                        dimension, negative
                    )
                ]
                self.assertEqual(value * negative_value, 1)

        for second in range(dimension):
            product = Fraction(1)
            for first in range(dimension):
                numerator = values[
                    canonical_zauner_orbit_representative(
                        dimension, (first, second)
                    )
                ]
                denominator = values[
                    canonical_zauner_orbit_representative(
                        dimension, (first - 1, second)
                    )
                ]
                product *= numerator / denominator
            self.assertEqual(product, 1)

        totals = canonical_tcc_orbit_model_phase_totals(
            dimension, (1, 0), values
        )
        self.assertEqual(
            totals,
            {
                0: Fraction(6),
                1: Fraction(9, 2),
                2: Fraction(9, 2),
                3: Fraction(6),
            },
        )
        self.assertEqual(totals[0] - totals[2], Fraction(3, 2))
        self.assertEqual(totals[1] - totals[3], Fraction(-3, 2))

    def test_orbit_model_rejects_incomplete_or_zero_values(self) -> None:
        with self.assertRaises(ValueError):
            canonical_tcc_orbit_model_phase_totals(
                4, (1, 0), {(0, 0): 1}
            )
        values = canonical_dimension_four_countermodel()
        values[(0, 0)] = Fraction(0)
        with self.assertRaises(ValueError):
            canonical_tcc_orbit_model_phase_totals(
                4, (1, 0), values
            )

    def test_uniform_jacobi_word_and_scales(self) -> None:
        self.assertEqual(
            canonical_jacobi_scale_exponents(), (-2, -1, 0)
        )
        for dimension in range(4, 501):
            self.assertEqual(
                canonical_jacobi_word(dimension),
                (dimension - 1, dimension - 1, dimension - 1),
            )
            stabilizer = canonical_stabilizer(dimension)
            self.assertEqual(
                matrix_power(stabilizer, 3),
                matrix_multiply(
                    matrix_multiply(stabilizer, stabilizer), stabilizer
                ),
            )

    def test_beta_power_trace_recurrence(self) -> None:
        for dimension in range(4, 501):
            self.assertEqual(canonical_beta_power_trace(dimension, 0), 2)
            self.assertEqual(
                canonical_beta_power_trace(dimension, 1),
                dimension - 1,
            )
            self.assertEqual(
                canonical_beta_power_trace(dimension, 3),
                dimension**3 - 3 * dimension**2 + 2,
            )

    def test_cyclic_approximants_align_with_level_three_step(
        self,
    ) -> None:
        for dimension in range(4, 101):
            for index in range(1, 13):
                numerator, denominator = (
                    canonical_cyclic_approximant_pair(
                        dimension, index
                    )
                )
                self.assertEqual(gcd(numerator, denominator), 1)
                record = canonical_cyclic_approximant_record(
                    dimension, index, 1
                )
                self.assertTrue(record["approximants_are_reduced"])
                self.assertTrue(
                    record["same_residues_after_conductor_step"]
                )
                self.assertTrue(record["level_step_is_identity"])
                self.assertTrue(record["off_grid_factor_is_retained"])
                if index % 3 in (1, 2):
                    self.assertTrue(
                        record["denominator_coprime_to_dimension"]
                    )
                    self.assertTrue(
                        record["safe_universal_subsequence"]
                    )

            constant = canonical_cyclic_approximant_record(
                dimension, 4, 0
            )
            self.assertTrue(
                constant["rational_boundary_monomial_is_one"]
            )
            self.assertFalse(constant["off_grid_factor_is_retained"])
            self.assertFalse(
                constant[
                    "cyclic_limit_covers_full_characteristic_packet"
                ]
            )
            self.assertFalse(
                constant["cyclic_limit_retains_signed_sf_phases"]
            )
            self.assertFalse(
                constant["finite_five_term_tcc_identity_proved"]
            )

    def test_reflection_reduces_tcc_to_one_involution(self) -> None:
        for dimension in range(4, 501):
            record = canonical_zak_reflection_quadratic_record(
                dimension
            )
            self.assertEqual(
                record["sqrt_lambda_sum_square_residual"], 0
            )
            self.assertEqual(
                record["sqrt_lambda_difference_square_residual"], 0
            )
            self.assertTrue(
                record["zero_characteristic_correction_is_required"]
            )
            self.assertEqual(record["normalized_target"], "H^2 = I_d")
            self.assertEqual(record["trace_h"], 2 - dimension)
            self.assertEqual(
                record["conditional_eigenvalue_multiplicities"],
                (1, dimension - 1),
            )
            self.assertFalse(
                record["reflection_alone_proves_involution"]
            )
            self.assertFalse(record["rm_involution_proved"])

    def test_reciprocity_forces_only_two_trace_moments(self) -> None:
        for dimension in range(4, 501):
            record = canonical_reciprocal_trace_moment_record(
                dimension
            )
            self.assertEqual(record["trace_pi"], 1)
            self.assertEqual(record["trace_pi_square"], 1)
            self.assertEqual(record["trace_h"], 2 - dimension)
            self.assertEqual(record["trace_h_square"], dimension)
            self.assertEqual(
                record["second_elementary_symmetric_h"],
                (dimension - 1) * (dimension - 4) // 2,
            )
            self.assertEqual(
                record["first_unforced_spectral_moment_degree"], 3
            )
            self.assertTrue(
                record["identity_coefficient_of_h_square_is_forced"]
            )
            self.assertFalse(
                record[
                    "traceless_coefficients_of_h_square_are_forced"
                ]
            )
            self.assertTrue(
                record["idempotency_equivalent_to_rank_one"]
            )
            self.assertTrue(
                record[
                    "rank_one_equivalent_to_vanishing_two_by_two_minors"
                ]
            )

    def test_odd_constant_overlap_model_has_all_coarse_moments(
        self,
    ) -> None:
        for dimension in range(5, 101, 2):
            record = (
                canonical_odd_constant_overlap_countermodel_record(
                    dimension
                )
            )
            self.assertTrue(record["real"])
            self.assertTrue(record["reciprocal"])
            self.assertTrue(record["zauner_invariant"])
            self.assertTrue(record["ordinarily_hermitian"])
            self.assertEqual(record["trace_pi"], 1)
            self.assertEqual(record["trace_pi_square"], 1)
            self.assertEqual(record["trace_h_square"], dimension)
            self.assertEqual(record["zero_twisted_residual"], 0)
            self.assertTrue(
                record["nonzero_twisted_residual_is_negative"]
            )
            self.assertFalse(record["is_idempotent"])
            self.assertFalse(record["h_is_involution"])

    def test_ghost_rank_one_target_is_an_explicit_minor_system(
        self,
    ) -> None:
        for dimension in range(4, 31):
            for row in range(dimension):
                for column in range(dimension):
                    terms = canonical_ghost_weyl_entry_terms(
                        dimension, row, column
                    )
                    self.assertEqual(len(terms), dimension)
                    self.assertEqual(
                        {node[0][0] for node in terms},
                        {(row - column) % dimension},
                    )
                    self.assertEqual(
                        [node[0][1] for node in terms],
                        list(range(dimension)),
                    )

            record = canonical_ghost_minor_record(
                dimension, (0, 1), (0, 1)
            )
            self.assertEqual(
                record["terms_per_product"], dimension * dimension
            )
            self.assertEqual(
                record["expanded_signed_term_count"],
                2 * dimension * dimension,
            )
            self.assertEqual(
                record["all_two_by_two_minor_count"],
                (dimension * (dimension - 1) // 2) ** 2,
            )
            self.assertTrue(
                record[
                    "minor_vanishing_equivalent_to_rank_one_collectively"
                ]
            )

    def test_exterior_square_compresses_all_ghost_minors(self) -> None:
        matrices = (
            ((1 + 0j, 2 + 0j), (2 + 0j, 4 + 0j)),
            ((1 + 1j, 2 - 1j), (3 + 0j, -1 + 2j)),
            (
                (1 + 0j, 2 + 1j, 0 + 0j),
                (0 + 1j, 3 + 0j, 4 - 2j),
                (2 + 0j, 0 + 0j, 1 + 1j),
            ),
        )
        for matrix in matrices:
            self.assertAlmostEqual(
                matrix_exterior_square_energy(matrix),
                matrix_gram_second_elementary(matrix),
                places=10,
            )
        self.assertEqual(matrix_exterior_square_energy(matrices[0]), 0)
        self.assertGreater(matrix_exterior_square_energy(matrices[1]), 0)

        for dimension in range(4, 101):
            record = canonical_ghost_exterior_square_record(dimension)
            pair_count = dimension * (dimension - 1) // 2
            self.assertEqual(record["row_pair_count"], pair_count)
            self.assertEqual(record["column_pair_count"], pair_count)
            self.assertEqual(
                record["exchange_residual_count"], pair_count**2
            )
            self.assertEqual(
                record["energy_scale"], (dimension + 1) ** 2
            )
            self.assertEqual(
                record["zauner_positive_sector_count"],
                dimension * (dimension - 1) // 2,
            )
            self.assertTrue(
                record["certificate_zero_equivalent_to_tcc"]
            )

    def test_parity_hermiticity_makes_the_certificate_polynomial(
        self,
    ) -> None:
        hermitian_matrices = (
            (
                (2 + 0j, 1 + 1j, -1 + 0j),
                (1 - 1j, 3 + 0j, 2 + 2j),
                (-1 + 0j, 2 - 2j, 4 + 0j),
            ),
            (
                (1 + 0j, 2 - 1j, 0 + 0j),
                (2 + 1j, 5 + 0j, 0 + 0j),
                (0 + 0j, 0 + 0j, 0 + 0j),
            ),
        )
        dimension = 3
        for hermitian in hermitian_matrices:
            ghost = tuple(
                tuple(
                    hermitian[(-row) % dimension][column]
                    for column in range(dimension)
                )
                for row in range(dimension)
            )
            certificate = matrix_parity_schatten_certificate(ghost)
            self.assertAlmostEqual(
                certificate["parity_hermiticity_max_defect"], 0.0
            )
            self.assertAlmostEqual(
                certificate["parity_moment_energy"],
                certificate["exterior_square_energy"],
                places=9,
            )

        for dimension in range(4, 101):
            record = canonical_parity_schatten_record(dimension)
            expected_fixed = 4 if dimension % 2 == 0 else 1
            self.assertEqual(
                record["self_inverse_characteristic_count"],
                expected_fixed,
            )
            self.assertEqual(
                2 * record["nontrivial_reciprocal_pair_count"]
                + expected_fixed,
                dimension * dimension,
            )
            self.assertTrue(
                record["adjoint_eliminated_on_parity_hermitian_locus"]
            )
            self.assertTrue(record["fourth_moment_equivalent_to_tcc"])

    def test_holomorphic_quartic_needs_its_unit_torus_hypothesis(
        self,
    ) -> None:
        record = (
            canonical_dimension_four_holomorphic_quartic_countermodel_record()
        )
        self.assertEqual(record["characteristic_polynomial"], "(x-1)(x^3-1)")
        self.assertEqual(record["trace_power_1"], 1)
        self.assertEqual(record["trace_power_2"], 1)
        self.assertEqual(record["trace_power_3"], 4)
        self.assertEqual(record["trace_power_4"], 1)
        self.assertEqual(record["determinant"], 1)
        self.assertEqual(record["rank"], 4)
        self.assertTrue(record["parity_hermitian"])
        self.assertFalse(record["ordinary_hermitian"])
        self.assertTrue(record["bos_waldron_quartic_holds"])
        self.assertFalse(record["rank_one"])
        self.assertFalse(record["tcc_holds"])
        self.assertTrue(record["unit_torus_hypothesis_is_essential"])
        self.assertFalse(record["correct_rm_positive_quartic_holds"])

    def test_dimension_four_minors_share_one_double_sine_factor(
        self,
    ) -> None:
        record = canonical_dimension_four_double_sine_factor_record()
        self.assertEqual(record["dimension"], 4)
        self.assertEqual(record["all_minor_count"], 36)
        self.assertEqual(
            record["formally_nonzero_minor_count_before_relation"], 34
        )
        self.assertEqual(
            record["nonzero_remainder_count_after_relation"], 0
        )
        self.assertTrue(record["every_minor_is_in_principal_ideal"])
        self.assertTrue(
            record[
                "single_special_value_identity_implies_dimension_four_ghost_rank_one"
            ]
        )
        self.assertFalse(record["both_shifts_checked_by_minor_file_alone"])
        self.assertEqual(record["matrix_trace"], "1")
        self.assertTrue(record["nonzero_entry_positive_under_relation"])
        self.assertEqual(
            record["coefficient_basis"],
            ["1", "sqrt(2)", "sqrt(5)", "sqrt(10)"],
        )
        self.assertEqual(len(record["matrix_entries"]), 4)
        self.assertEqual(len(record["minor_certificates"]), 36)
        self.assertTrue(
            all(
                not certificate["division_remainder"]
                for certificate in record["minor_certificates"]
            )
        )
        self.assertFalse(
            record["special_value_identity_proved_analytically"]
        )

    def test_zauner_blocks_do_not_improve_orbit_reduction(self) -> None:
        for dimension in range(4, 501):
            multiplicities = canonical_zauner_block_multiplicities(
                dimension
            )
            self.assertEqual(sum(multiplicities), dimension)
            record = canonical_zak_zauner_block_record(dimension)
            self.assertEqual(record["multiplicities"], multiplicities)
            self.assertEqual(record["dimension_defect"], 0)
            self.assertFalse(
                record["block_diagonalization_reduces_equation_count"]
            )

    def test_dimension_four_ray_modulus_four_matches_stark_square(
        self,
    ) -> None:
        record = canonical_dimension_four_ray_class_record()
        modulus_four = record["modulus_audits"][4]
        modulus_eight = record["modulus_audits"][8]
        self.assertEqual(
            modulus_four["one_real_place_ray_group_order"], 2
        )
        self.assertEqual(
            modulus_eight["one_real_place_ray_group_order"], 4
        )
        self.assertEqual(
            modulus_eight["quotient_element_orders"], (1, 2, 2, 2)
        )
        self.assertEqual(
            record["modulus_eight_phase_cover_group"], "C2 x C2"
        )
        self.assertTrue(
            record["modulus_four_matches_stark_square_degree"]
        )
        self.assertEqual(
            record["candidate_stark_square_polynomial_over_base"],
            "U^2 - (1 + sqrt(5)) U + 1",
        )
        self.assertEqual(record["candidate_relative_discriminant"], "(4)")
        self.assertEqual(record["candidate_absolute_discriminant"], 400)
        self.assertTrue(record["minkowski_bound_below_three"])
        self.assertEqual(record["smallest_dyadic_prime_norm"], 4)
        self.assertEqual(record["candidate_class_number"], 1)
        self.assertEqual(
            record["candidate_infinite_ramification"],
            "second real place",
        )
        self.assertTrue(record["ray_field_degree_matches_ray_group"])
        self.assertTrue(record["ray_class_identification_proved"])
        self.assertTrue(record["fundamental_units_verified_by_pari_bnf"])
        self.assertTrue(record["pari_bnfcertify_required"])
        self.assertEqual(record["kopp_exponent_n"], 1)
        self.assertEqual(
            record["kopp_positive_stabilizer"],
            ((21, -8), (8, -3)),
        )
        self.assertEqual(record["kopp_multiplier"], "-i")
        self.assertEqual(record["rademacher_dedekind_sum"], "-1/16")
        self.assertEqual(record["rademacher_invariant"], 0)
        self.assertTrue(record["partial_zeta_normalization_matched"])
        self.assertTrue(record["kopp_specialization_proved"])
        self.assertTrue(record["both_formal_tcc_shifts_proved"])

    def test_equal_base_q_binomial_cancellation(self) -> None:
        self.assertEqual(
            canonical_equal_base_q_binomial_cancellation(0), (1,)
        )
        for degree in range(1, 21):
            self.assertEqual(
                canonical_equal_base_q_binomial_cancellation(degree),
                (0,),
            )

    def test_root_filtered_stokes_gate_retains_off_grid_factor(
        self,
    ) -> None:
        for dimension in range(4, 31):
            constant = canonical_root_filtered_stokes_record(
                dimension, 0, 0
            )
            self.assertTrue(
                constant["boundary_monomial_is_root_of_unity"]
            )
            self.assertFalse(
                constant["equal_base_coefficient_vanishes"]
            )
            for numerator, denominator in ((1, 0), (2, 3)):
                record = canonical_root_filtered_stokes_record(
                    dimension, numerator, denominator
                )
                self.assertFalse(
                    record["boundary_monomial_is_root_of_unity"]
                )
                self.assertTrue(
                    record["equal_base_coefficient_vanishes"]
                )
                self.assertFalse(
                    record["uniform_root_filtered_stokes_limit_proved"]
                )

    def test_family_record_is_internally_consistent(self) -> None:
        record = canonical_family_record(4)
        self.assertEqual(record["form"], (1, -3, 1))
        self.assertEqual(record["discriminant"], 5)
        self.assertEqual(record["cube_mod_dimension"], IDENTITY_2)
        self.assertEqual(record["shift_zero_partner"], 1)
        self.assertEqual(record["jacobi_scale_exponents"], (-2, -1, 0))
        self.assertEqual(record["form_stabilizer_residual"], (0, 0, 0))
        self.assertEqual(record["tcc_equation_count"], 5)
        self.assertEqual(
            record["pentagon_compatibility"]["general_modular_modulus"],
            8,
        )
        self.assertEqual(
            record["zak_reflection_quadratic"]["normalized_target"],
            "H^2 = I_d",
        )
        self.assertEqual(
            record["zak_zauner_blocks"]["dimension_defect"], 0
        )
        self.assertTrue(
            record["cyclic_approximant"][
                "same_residues_after_conductor_step"
            ]
        )
        self.assertEqual(
            record["reciprocal_trace_moments"]["trace_h_square"], 4
        )
        self.assertEqual(
            record["ghost_rank_one_minor"][
                "all_two_by_two_minor_count"
            ],
            36,
        )

    def test_invalid_dimensions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_form(3)
        with self.assertRaises(ValueError):
            canonical_stabilizer(0)
        with self.assertRaises(ValueError):
            extended_displacement_modulus(0)
        with self.assertRaises(ValueError):
            canonical_beta_is_rational(3)
        with self.assertRaises(ValueError):
            canonical_beta_power_trace(3, 0)
        with self.assertRaises(ValueError):
            canonical_cyclic_approximant_pair(4, 0)
        with self.assertRaises(ValueError):
            canonical_cyclic_approximant_record(4, 1, -1)
        with self.assertRaises(ValueError):
            canonical_odd_constant_overlap_countermodel_record(4)
        with self.assertRaises(ValueError):
            canonical_ghost_minor_record(4, (0, 4), (0, 1))
        with self.assertRaises(ValueError):
            canonical_ghost_minor_record(4, (0, 1), (2, 6))
        with self.assertRaises(ValueError):
            canonical_beta_power_trace(4, -1)
        with self.assertRaises(ValueError):
            canonical_general_modular_modulus(3)
        with self.assertRaises(ValueError):
            canonical_general_modular_parameters(3)
        with self.assertRaises(ValueError):
            canonical_general_modular_characteristic(3, (0, 0))
        with self.assertRaises(ValueError):
            canonical_general_modular_node_strip_margins(3, (0, 0))
        with self.assertRaises(ValueError):
            canonical_primitive_sigma_shift_coordinates(3)
        with self.assertRaises(ValueError):
            canonical_quadratic_residue_units(3)
        with self.assertRaises(ValueError):
            canonical_global_unit_residues(3)
        with self.assertRaises(ValueError):
            canonical_local_unit_cosets(3)
        with self.assertRaises(ValueError):
            canonical_primitive_direction_unit_stabilizers(3)
        with self.assertRaises(ValueError):
            canonical_dimension_four_laurent_action({}, 4)
        with self.assertRaises(ValueError):
            canonical_dimension_four_relation_nullities(0)
        with self.assertRaises(ValueError):
            canonical_dimension_four_packet_evaluation(0, 1)
        with self.assertRaises(ValueError):
            biquadratic_2_3_galois_action(
                (Fraction(0),) * 4, -1
            )
        with self.assertRaises(ValueError):
            canonical_scalar_distribution_fibers(4, 3)
        with self.assertRaises(ValueError):
            canonical_equal_base_q_binomial_cancellation(-1)
        with self.assertRaises(ValueError):
            canonical_root_filtered_stokes_record(4, -1, 0)


if __name__ == "__main__":
    unittest.main()
