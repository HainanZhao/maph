import unittest

from conventions.source_coupled_label_energy_v1 import (
    SourceAtom,
    anticorrelated_model,
    mixed_label_energy,
    pair_sum_identity,
    pushforwards,
    source_diagonal_mass,
    verify_all,
)


class Cycle169SourceCoupledLabelEnergyTests(unittest.TestCase):
    def test_pair_identity_with_multiplicities(self):
        atoms = (
            SourceAtom("e", 3, 4, None, edge_multiplicity=2),
            SourceAtom("p", 5, None, 4, packet_multiplicity=3),
        )
        edges, packets = pushforwards(atoms)
        self.assertEqual(edges, {4: 6})
        self.assertEqual(packets, {4: 15})
        self.assertEqual(mixed_label_energy(edges, packets), 90)
        self.assertEqual(pair_sum_identity(atoms), 90)
        self.assertEqual(source_diagonal_mass(atoms), 0)

    def test_arbitrary_margins_admit_zero_energy_two_label_model(self):
        for edge_mass in (0, 1, 7, 31):
            for packet_mass in (0, 2, 11, 29):
                atoms = anticorrelated_model(edge_mass, packet_mass)
                edges, packets = pushforwards(atoms)
                self.assertEqual(sum(edges.values()), edge_mass)
                self.assertEqual(sum(packets.values()), packet_mass)
                self.assertEqual(mixed_label_energy(edges, packets), 0)
                self.assertEqual(pair_sum_identity(atoms), 0)

    def test_complete_ledger(self):
        checked = verify_all()
        self.assertIn("two-independent-source-copy", checked["identity"])
        self.assertIn("does not use the actual exponential geometry", checked["boundary"])


if __name__ == "__main__":
    unittest.main()
