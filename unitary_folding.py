"""Unitary folding helpers for the simple single-qubit ZNE demo.

The functions here model a minimal single-qubit circuit built from rotation
operators. A "fold factor" repeats the base gate sequence, effectively
stretching circuit depth so that depolarizing noise compounds and can later be
extrapolated back to the zero-noise limit. The notebook and CLI sweep re-use
this module alongside :mod:`noise_model` and :mod:`extrapolation_methods` to
run folded circuits and estimate the probability of measuring ``|0⟩``.
"""
"""Utility functions for building and running folded single-qubit circuits."""
from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from noise_model import depolarize_density_matrix

Matrix2 = List[List[complex]]
LabeledGate = Tuple[str, Matrix2]

__all__ = [
    "BASE_SEQUENCE",
    "apply_unitary",
    "expectation_p0",
    "fold_sequence",
    "run_folded_circuit",
    "rx",
    "ry",
    "rz",
]


def matmul(A: Matrix2, B: Matrix2) -> Matrix2:
    """Matrix multiply two 2x2 matrices."""

def matmul(A: Matrix2, B: Matrix2) -> Matrix2:
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def dagger(A: Matrix2) -> Matrix2:
    """Conjugate transpose of a 2x2 matrix."""
    return [[A[j][i].conjugate() for j in range(2)] for i in range(2)]


def apply_unitary(rho: Matrix2, U: Matrix2) -> Matrix2:
    """Apply a unitary to a density matrix."""
    return matmul(matmul(U, rho), dagger(U))


def rx(theta: float) -> Matrix2:
    """Single-qubit rotation about X by ``theta`` radians."""
    c = math.cos(theta / 2)
    s = -1j * math.sin(theta / 2)
    return [[c, s], [s, c]]


def ry(theta: float) -> Matrix2:
    """Single-qubit rotation about Y by ``theta`` radians."""
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    return [[c, -s], [s, c]]


def rz(theta: float) -> Matrix2:
    """Single-qubit rotation about Z by ``theta`` radians."""
    epos = complex(math.cos(theta / 2), -math.sin(theta / 2))
    eneg = complex(math.cos(theta / 2), math.sin(theta / 2))
    return [[epos, 0], [0, eneg]]


BASE_SEQUENCE: Tuple[LabeledGate, ...] = (
    ("R_y(π/4)", ry(math.pi / 4)),
    ("R_z(π/3)", rz(math.pi / 3)),
    ("R_x(π/5)", rx(math.pi / 5)),
)


def fold_sequence(sequence: Sequence[LabeledGate], factor: int) -> List[LabeledGate]:
    """Repeat a labeled gate ``sequence`` ``factor`` times for folding."""
    """Repeat a labeled gate sequence ``factor`` times for unitary folding."""
    if factor < 1:
        raise ValueError("fold factor must be at least 1")
    return [gate for _ in range(factor) for gate in sequence]


def run_folded_circuit(
    base_error: float, fold_factor: int, base_sequence: Sequence[LabeledGate] | None = None
) -> Matrix2:
    """Simulate a folded single-qubit circuit with depolarizing noise.

    Args:
        base_error: Depolarizing probability assigned per gate in the base circuit.
        fold_factor: How many times to repeat the base gate sequence.
        base_sequence: Optional override for the base gate sequence.

    Returns:
        Density matrix after applying all folded gates and depolarizing noise.
    """
    Execute a folded single-qubit circuit with depolarizing noise.

    Args:
        base_error: The depolarizing probability assigned per gate in the base circuit.
        fold_factor: How many times to repeat the base sequence.
        base_sequence: Optional override for the base gate sequence.

    Returns:
        The final density matrix after all gates and noise are applied.
    """
    if fold_factor < 1:
        raise ValueError("fold factor must be at least 1")

    sequence = base_sequence or BASE_SEQUENCE
    noise_probability = base_error * fold_factor
    rho: Matrix2 = [[1.0, 0.0], [0.0, 0.0]]

    for _, gate in fold_sequence(sequence, fold_factor):
        rho = apply_unitary(rho, gate)
        rho = depolarize_density_matrix(rho, noise_probability)

    return rho


def expectation_p0(rho: Matrix2) -> float:
    """Return the probability of measuring ``|0⟩`` from a density matrix."""
    """Return the probability of measuring ``|0>`` from a density matrix."""
    return float(rho[0][0].real)
