"""Noise model utilities for single-qubit density matrices."""
from __future__ import annotations

from typing import List

Matrix2 = List[List[complex]]


def clamp_probability(probability: float) -> float:
    """Clamp a probability value to the inclusive range [0, 1]."""
    return max(0.0, min(1.0, probability))


def depolarize_density_matrix(rho: Matrix2, probability: float) -> Matrix2:
    """
    Apply a single-qubit depolarizing channel to ``rho``.

    Args:
        rho: 2x2 density matrix representing the state of one qubit.
        probability: Depolarizing probability (values outside [0, 1] are clamped).

    Returns:
        The density matrix after depolarizing noise is applied.
    """
    p = clamp_probability(probability)
    identity = [[1.0, 0.0], [0.0, 1.0]]
    return [[(1 - p) * rho[i][j] + p * 0.5 * identity[i][j] for j in range(2)] for i in range(2)]
