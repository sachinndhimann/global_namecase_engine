import unittest

from global_namecase_engine import discover_particles


class ParticleDiscoveryTests(unittest.TestCase):
    def test_discovers_repeated_middle_tokens(self) -> None:
        names = [
            "Asha ap Devi",
            "Mina ap Noor",
            "Leela ap Karim",
            "Tara ap Singh",
        ]

        self.assertEqual(discover_particles(names, min_count=2), ["ap"])

    def test_rejects_invalid_min_count(self) -> None:
        with self.assertRaises(ValueError):
            discover_particles(["Juan de la Cruz"], min_count=0)


if __name__ == "__main__":
    unittest.main()
