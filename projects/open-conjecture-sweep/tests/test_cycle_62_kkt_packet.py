import unittest

from proof.check_cycle_62_kkt_packet import audit


class Cycle62KktPacket(unittest.TestCase):
    def test_packet(self):
        self.assertEqual(audit()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
