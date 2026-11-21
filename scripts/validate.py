#!/usr/bin/env python3
"""DCM v0.1: deterministic dialogue compatibility validation."""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
import json
import sys


DIMENSIONS = ["D1", "D2", "D3", "D4"]

REQUIRED = {
    "spec_version",
    "dimensions",
    "test_cases",
    "tolerance",
    "baseline",
    "candidate",
}

ALLOWED = REQUIRED | {"targets"}


def reject_duplicates(pairs):
    """Reject duplicate JSON object keys."""
    result = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value

    return result


def reject_constant(value):
    """Reject NaN and Infinity."""
    raise ValueError(
        f"non-finite JSON number is not allowed: {value}"
    )


def require_score(value, location):
    """Validate a score or tolerance in [0, 1]."""
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError(
            f"{location} must be a finite JSON number"
        )

    if not Decimal(0) <= value <= Decimal(1):
        raise ValueError(
            f"{location} must be between 0 and 1"
        )

    return value


def validate_matrix(value, name, rows):
    """Validate matrix dimensions and numerical values."""
    if not isinstance(value, list) or len(value) != rows:
        raise ValueError(
            f"{name} must contain exactly {rows} rows"
        )

    for i, row in enumerate(value):
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError(
                f"{name}[{i}] must contain exactly four scores"
            )

        for j, score in enumerate(row):
            require_score(
                score,
                f"{name}[{i}][{j}]"
            )

    return value


def validate(document):
    """Validate a DCM v0.1 comparison document."""
    if not isinstance(document, dict):
        raise ValueError(
            "top-level JSON value must be an object"
        )

    missing = REQUIRED - document.keys()
    unknown = document.keys() - ALLOWED

    if missing:
        raise ValueError(
            f"missing required fields: {', '.join(sorted(missing))}"
        )

    if unknown:
        raise ValueError(
            f"unknown fields: {', '.join(sorted(unknown))}"
        )

    if (
        not isinstance(document["spec_version"], str)
        or document["spec_version"] != "0.1"
    ):
        raise ValueError(
            "spec_version must equal '0.1'"
        )

    if document["dimensions"] != DIMENSIONS:
        raise ValueError(
            "dimensions must be exactly "
            "['D1', 'D2', 'D3', 'D4']"
        )

    cases = document["test_cases"]

    if not isinstance(cases, list) or not cases:
        raise ValueError(
            "test_cases must be a non-empty array"
        )

    if any(
        not isinstance(case, str) or not case.strip()
        for case in cases
    ):
        raise ValueError(
            "every test case ID must be a non-empty string"
        )

    if len(cases) != len(set(cases)):
        raise ValueError(
            "test case IDs must be unique"
        )

    require_score(
        document["tolerance"],
        "tolerance"
    )

    for name in ("baseline", "candidate"):
        validate_matrix(
            document[name],
            name,
            len(cases)
        )

    if "targets" in document:
        validate_matrix(
            document["targets"],
            "targets",
            len(cases)
        )

    return document


def exact_precision(document):
    """Select precision sufficient for exact decimal subtraction."""
    values = [document["tolerance"]]

    for name in ("baseline", "candidate", "targets"):
        for row in document.get(name, []):
            values.extend(row)

    places = (
        max(0, -value.as_tuple().exponent)
        for value in values
        if value != 0
    )

    return max(28, max(places, default=0) + 4)


def compare(document):
    """Calculate regressions and optional target gaps."""
    regressions = []
    gaps = []

    tolerance = document["tolerance"]

    with localcontext() as context:
        context.prec = exact_precision(document)

        for i, case in enumerate(document["test_cases"]):
            for j, dimension in enumerate(DIMENSIONS):
                before = document["baseline"][i][j]
                after = document["candidate"][i][j]

                delta = after - before

                if delta < -tolerance:
                    regressions.append(
                        (case, dimension, before, after, delta)
                    )

                if "targets" in document:
                    target = document["targets"][i][j]
                    gaps.append(
                        (case, dimension, abs(after - target))
                    )

    return regressions, gaps


def print_report(document, regressions, gaps):
    """Print a deterministic compatibility report."""
    count = len(document["test_cases"])

    print("DCM v0.1 Compatibility Report")
    print(f"Test cases: {count}")
    print(f"Dimensions: {len(DIMENSIONS)}")
    print(f"Comparisons: {count * len(DIMENSIONS)}")
    print(f"Tolerance: {document['tolerance']}")

    print("\nRegressions:")

    if not regressions:
        print("  None")

    for case, dimension, before, after, delta in regressions:
        print(
            f"  {case} / {dimension}: "
            f"baseline={before}, "
            f"candidate={after}, "
            f"delta={delta}"
        )

    print(f"\nTotal regressions: {len(regressions)}")

    if "targets" in document:
        print(
            "\nTarget gaps (candidate vs. desired score):"
        )

        for case, dimension, gap in gaps:
            print(
                f"  {case} / {dimension}: {gap}"
            )

    result = "REGRESSION" if regressions else "PASS"
    print(f"\nResult: {result}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="DCM v0.1 compatibility validator"
    )

    parser.add_argument(
        "input",
        help="path to the comparison JSON file"
    )

    args = parser.parse_args(argv)

    try:
        with open(
            args.input,
            "r",
            encoding="utf-8"
        ) as source:
            document = json.load(
                source,
                parse_float=Decimal,
                parse_int=Decimal,
                parse_constant=reject_constant,
                object_pairs_hook=reject_duplicates,
            )

        validate(document)

        regressions, gaps = compare(document)

    except (
        OSError,
        UnicodeError,
        ValueError,
        ArithmeticError,
    ) as exc:
        print(
            f"DCM INVALID: {exc}",
            file=sys.stderr
        )
        return 2

    print_report(document, regressions, gaps)

    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
