import unittest

from unitary_folding import BASE_SEQUENCE, apply_unitary, expectation_p0, fold_sequence, run_folded_circuit


class TestUnitaryFolding(unittest.TestCase):
    def test_fold_sequence_repeats_base(self):
        folded = fold_sequence(BASE_SEQUENCE, 3)
        self.assertEqual(len(folded), len(BASE_SEQUENCE) * 3)
        self.assertEqual([name for name, _ in folded[:3]], [name for name, _ in BASE_SEQUENCE])

    def test_run_folded_circuit_matches_manual_application_without_noise(self):
        rho_manual = [[1.0, 0.0], [0.0, 0.0]]
        for _, gate in fold_sequence(BASE_SEQUENCE, 2):
            rho_manual = apply_unitary(rho_manual, gate)

        rho_folded = run_folded_circuit(base_error=0.0, fold_factor=2)
        self.assertAlmostEqual(rho_manual[0][0].real, rho_folded[0][0].real, places=12)
        self.assertAlmostEqual(rho_manual[1][1].real, rho_folded[1][1].real, places=12)

    def test_increasing_fold_factor_increases_noise_effect(self):
        rho_single = run_folded_circuit(base_error=0.05, fold_factor=1)
        rho_folded = run_folded_circuit(base_error=0.05, fold_factor=3)
        self.assertLess(expectation_p0(rho_folded), expectation_p0(rho_single))


if __name__ == "__main__":
    unittest.main()
