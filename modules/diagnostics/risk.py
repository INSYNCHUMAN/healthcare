"""Simple diagnostic helpers built on top of normalized vitals."""
from __future__ import annotations

from typing import Mapping

WEIGHTS = {
    "heart_rate": 0.35,
    "spo2": -0.25,
    "respiration": 0.25,
    "temperature": 0.15,
}


def cardio_risk_score(normalized_vitals: Mapping[str, float]) -> float:
    """Return a pseudo cardio-risk score between 0 and 1.

    The function expects that each vital has already been normalized to the ``0..1``
    range. Missing data results in a ``KeyError`` so callers are forced to make the
    requirement explicit.
    """

    missing = sorted(v for v in WEIGHTS if v not in normalized_vitals)
    if missing:
        raise KeyError(f"Missing normalized readings for: {', '.join(missing)}")

    score = 0.5  # baseline
    for metric, weight in WEIGHTS.items():
        score += weight * (normalized_vitals[metric] - 0.5)
    return max(0.0, min(1.0, score))
