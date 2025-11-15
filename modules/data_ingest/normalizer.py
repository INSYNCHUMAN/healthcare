"""Utilities to normalize raw vital sign readings.

The first prototype mutated the dictionary that was passed in, which leaked normalized
values back to upstream collectors that still needed the original readings. That was a
hard-to-track bug that made alerts fire with normalized values instead of the raw ones.

`normalize_vitals` now clones the payload before computing normalized values and keeps the
function free of side effects.
"""
from __future__ import annotations

from typing import Dict, Iterable, Mapping, Tuple

Bounds = Mapping[str, Tuple[float, float]]

DEFAULT_BOUNDS: Bounds = {
    "heart_rate": (40.0, 180.0),
    "spo2": (85.0, 100.0),
    "respiration": (8.0, 32.0),
    "temperature": (35.0, 40.0),
}


def _validate_bounds(bounds: Bounds, metrics: Iterable[str]) -> None:
    for metric in metrics:
        if metric not in bounds:
            raise KeyError(f"No bounds configured for '{metric}'.")
        low, high = bounds[metric]
        if high <= low:
            raise ValueError(
                f"Upper bound must be greater than lower bound for '{metric}'."
            )


def normalize_vitals(
    reading: Mapping[str, float],
    *,
    bounds: Bounds | None = None,
    clamp_output: bool = True,
) -> Dict[str, float]:
    """Return a normalized copy of ``reading``.

    Args:
        reading: Dictionary of vital names to numeric values.
        bounds: Optional override for the normalization bounds.
        clamp_output: When ``True`` the result is clamped to the ``0..1`` interval.

    Returns:
        A **new** dictionary that contains the normalized readings.
    """

    bounds = bounds or DEFAULT_BOUNDS
    # Validate before computing any derived values so we fail fast with a helpful error.
    _validate_bounds(bounds, reading.keys())

    normalized: Dict[str, float] = {}
    for metric, value in reading.items():
        low, high = bounds[metric]
        span = high - low
        normalized_value = (float(value) - low) / span
        if clamp_output:
            normalized_value = max(0.0, min(1.0, normalized_value))
        normalized[metric] = normalized_value

    return normalized
