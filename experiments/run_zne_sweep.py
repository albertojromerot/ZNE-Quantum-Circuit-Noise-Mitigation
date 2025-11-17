"""Run a configurable Zero-Noise Extrapolation sweep and export CSV results."""
from __future__ import annotations

import argparse
import csv
import random
import sys
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from extrapolation_methods import ExtrapolationError, linear_extrapolation
from unitary_folding import BASE_SEQUENCE, expectation_p0, run_folded_circuit


def _parse_float_list(text: str) -> List[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def run_sweep(
    noise_probs: Iterable[float],
    fold_factors: Iterable[int],
    shots: int,
    output: Path,
    ideal: float | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fold_factors = list(fold_factors)
    rows = []
    run_id = 1

    for base_prob in noise_probs:
        print(f"Base depolarizing probability: {base_prob}")
        noise_scales = []
        expectations = []
        for factor in fold_factors:
            rho = run_folded_circuit(base_error=base_prob, fold_factor=factor, base_sequence=BASE_SEQUENCE)
            prob_zero = expectation_p0(rho)
            counts = sum(1 for _ in range(shots) if random.random() < prob_zero)
            measured_expectation = counts / shots
            print(f"  factor={factor}, expectation={measured_expectation:.6f}")
            noise_scales.append(float(factor))
            expectations.append(measured_expectation)

        try:
            zne_estimate = linear_extrapolation(noise_scales, expectations)
        except ExtrapolationError as exc:
            print(f"  Skipping extrapolation due to error: {exc}")
            zne_estimate = float('nan')

        unmitigated = expectations[0] if expectations else float('nan')

        for factor, noise_scale, measured in zip(fold_factors, noise_scales, expectations):
            row = {
                "run_id": run_id,
                "base_noise_probability": base_prob,
                "fold_factor": factor,
                "noise_scale": noise_scale,
                "measured_expectation": measured,
                "unmitigated_expectation": unmitigated,
                "zne_estimate": zne_estimate,
            }
            if ideal is not None:
                row.update(
                    {
                        "ideal_expectation": ideal,
                        "absolute_error_unmitigated": abs(unmitigated - ideal),
                        "absolute_error_mitigated": abs(zne_estimate - ideal),
                    }
                )
            rows.append(row)
        run_id += 1

    fieldnames = list(rows[0].keys()) if rows else []
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--noise-probs",
        default="0.01,0.02,0.05",
        help="Comma-separated base depolarizing probabilities.",
    )
    parser.add_argument(
        "--fold-factors",
        default="1,3,5",
        help="Comma-separated noise scaling / folding factors.",
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Number of samples per circuit configuration.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/zne_sweep.csv"),
        help="Path to the CSV output file.",
    )
    parser.add_argument(
        "--ideal",
        type=float,
        default=None,
        help="Optional ideal expectation value for error metrics.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    noise_probs = _parse_float_list(args.noise_probs)
    fold_factors = [int(x) for x in _parse_float_list(args.fold_factors)]
    run_sweep(noise_probs, fold_factors, args.shots, args.output, args.ideal)


if __name__ == "__main__":
    main()
