import unittest

from extrapolation_methods import ExtrapolationError, linear_extrapolation, linear_extrapolation_diagnostics


class TestLinearExtrapolation(unittest.TestCase):
    def test_recovers_intercept(self):
        xs = [1, 2, 4]
        ys = [2.0, 3.0, 5.0]  # slope 1, intercept 1
        intercept = linear_extrapolation(xs, ys)
        self.assertAlmostEqual(intercept, 1.0, places=6)

    def test_requires_matching_lengths(self):
        with self.assertRaises(ExtrapolationError):
            linear_extrapolation([1, 2], [0.1])

    def test_diagnostics_include_r2(self):
        diag = linear_extrapolation_diagnostics([1, 2], [2.0, 4.0])
        self.assertIn("r2", diag)
        self.assertAlmostEqual(diag["intercept"], 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
