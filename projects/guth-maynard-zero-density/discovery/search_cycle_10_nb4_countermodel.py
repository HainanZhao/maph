#!/usr/bin/env python3
"""Run the preregistered exact NB4 sign search and print its result."""
from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/e1_e2_engine_v1.py"


def load_conventions():
    spec = importlib.util.spec_from_file_location("e1_e2_engine_v1", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load E1/E2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def main() -> int:
    module = load_conventions()
    result = module.search_nb4_countermodel()
    print(json.dumps(exact_json(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
