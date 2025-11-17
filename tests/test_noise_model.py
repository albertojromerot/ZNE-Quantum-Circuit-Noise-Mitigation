import unittest

from noise_model import clamp_probability, depolarize_density_matrix


class TestNoiseModel(unittest.TestCase):
    def test_probability_clamped(self):
        self.assertEqual(clamp_probability(-0.5), 0.0)
        self.assertEqual(clamp_probability(0.5), 0.5)
        self.assertEqual(clamp_probability(2.0), 1.0)

    def test_depolarize_moves_toward_mixed_state(self):
        rho = [[1.0, 0.0], [0.0, 0.0]]
        depolarized = depolarize_density_matrix(rho, 0.4)
        self.assertAlmostEqual(depolarized[0][0].real, 0.8, places=10)
        self.assertAlmostEqual(depolarized[1][1].real, 0.2, places=10)
        self.assertAlmostEqual(depolarized[0][1].real, 0.0, places=10)


if __name__ == "__main__":
    unittest.main()
