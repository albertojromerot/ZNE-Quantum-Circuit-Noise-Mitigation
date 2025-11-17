"""Extrapolation helpers used by the ZNE demo and sweep harness."""
from __future__ import annotations

from typing import Mapping, Sequence

try:
    import numpy as np
except ImportError:  # pragma: no cover - fallback for environments without numpy
    np = None


class ExtrapolationError(ValueError):
    """Raised when extrapolation inputs are invalid."""


def _validate_inputs(noise_scales: Sequence[float], expectations: Sequence[float]) -> None:
    if len(noise_scales) != len(expectations):
        raise ExtrapolationError("noise_scales and expectations must have the same length")
    if len(noise_scales) < 2:
        raise ExtrapolationError("at least two points are required for linear extrapolation")


def _linear_fit(noise_scales: Sequence[float], expectations: Sequence[float]):
    if np is None:
        n = len(noise_scales)
        mean_x = sum(noise_scales) / n
        mean_y = sum(expectations) / n
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(noise_scales, expectations))
        den = sum((x - mean_x) ** 2 for x in noise_scales)
        slope = num / den if den else 0.0
        intercept = mean_y - slope * mean_x
        return float(slope), float(intercept)
    coeffs = np.polyfit(noise_scales, expectations, 1)
    slope, intercept = coeffs
    return float(slope), float(intercept)


def linear_extrapolation(noise_scales: Sequence[float], expectations: Sequence[float]) -> float:
    """Estimate the zero-noise expectation using a simple linear fit.

    Args:
        noise_scales: Sequence of noise scaling factors (e.g., fold factors).
        expectations: Measured expectation values corresponding to ``noise_scales``.

    Returns:
        The intercept at noise_scale = 0 from a first-degree polynomial fit.

    Raises:
        ExtrapolationError: If inputs have mismatched lengths or too few samples.
    """
    _validate_inputs(noise_scales, expectations)
    _, intercept = _linear_fit(noise_scales, expectations)
    return intercept


def linear_extrapolation_diagnostics(
    noise_scales: Sequence[float], expectations: Sequence[float]
) -> Mapping[str, float]:
    """Return slope, intercept, and r-squared for a linear fit."""
    _validate_inputs(noise_scales, expectations)
    slope, intercept = _linear_fit(noise_scales, expectations)
    if np is None:
        # Basic R^2 using manual calculations
        mean_y = sum(expectations) / len(expectations)
        ss_tot = sum((y - mean_y) ** 2 for y in expectations)
        ss_res = sum(
            (y - (slope * x + intercept)) ** 2 for x, y in zip(noise_scales, expectations)
        )
        r2 = 1.0 - ss_res / ss_tot if ss_tot else 1.0
    else:
        predicted = np.polyval([slope, intercept], noise_scales)
        residuals = np.array(expectations) - predicted
        ss_res = float(np.sum(residuals ** 2))
        ss_tot = float(np.sum((expectations - np.mean(expectations)) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot else 1.0
    return {"slope": slope, "intercept": intercept, "r2": float(r2)}
