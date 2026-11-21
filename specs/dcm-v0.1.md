# Dialogue Compatibility Matrix (DCM) v0.1 Specification

**Version:** 0.1.0  
**Status:** Experimental  
**Specification ID:** DCM-0.1

## 1. Purpose

Dialogue Compatibility Matrix (DCM) is a minimal specification for measuring changes in observable AI dialogue behavior across model updates.

DCM compares numerical evaluations of two model versions:

- Baseline: behavior before an update.
- Candidate: behavior after an update.

The primary objective is to detect behavioral regressions without modifying either model.

DCM is model-agnostic and requires no AI API.

### Core Principle

> Model evolution and user dialogue compatibility should be evaluated independently.

## 2. Scope

DCM v0.1 supports:

1. Four fixed dialogue evaluation dimensions.
2. Numerical behavioral matrices.
3. Baseline-to-candidate comparison.
4. Configurable regression tolerance.
5. Optional comparison against user targets.
6. Deterministic input validation and reporting.

DCM v0.1 does not support automatic behavior correction, model switching, training, or inference management.

## 3. Terminology

| Term | Definition |
|---|---|
| Baseline | Reference model evaluation |
| Candidate | Updated model evaluation |
| Test Case | A predefined dialogue evaluation scenario |
| Dimension | A measurable dialogue characteristic |
| Score | Numerical assessment from 0 to 1 |
| Delta | Candidate score minus baseline score |
| Tolerance | Maximum permitted score decrease |
| Regression | Decrease exceeding the tolerance |
| Target | Optional desired behavioral score |

## 4. Evaluation Dimensions

DCM defines exactly four dimensions.

| ID | Name | Evaluation Objective |
|---|---|---|
| D1 | Conciseness | Compliance with requested response length |
| D2 | Initiative Control | Avoidance of unnecessary suggestions |
| D3 | Instruction Scope | Compliance with requested task boundaries |
| D4 | Context Continuity | Preservation of relevant established constraints |

The dimension order MUST be:

```text
[D1, D2, D3, D4]
```

Every score MUST satisfy:

```text
0 <= score <= 1
```

Higher values indicate better compliance.

For D2, a higher score means better control of unsolicited initiative, not more initiative.

Scores MUST be supplied by documented evaluation procedures or human assessments.

DCM does not generate evaluation scores automatically.

## 5. Matrix Model

Let:

- N = number of test cases.
- K = number of dimensions, fixed at 4.

The baseline matrix is:

```text
B = N x 4
```

The candidate matrix is:

```text
C = N x 4
```

Rows represent test cases.

Columns represent D1, D2, D3, and D4.

Both matrices MUST have identical shapes.

### 5.1 Delta Matrix

The difference matrix is:

```text
Delta = C - B
```

For each test case i and dimension j:

```text
delta[i][j] = C[i][j] - B[i][j]
```

Interpretation:

- Positive: measured improvement.
- Zero: no measured change.
- Negative: measured decrease.

A negative value does not automatically indicate a regression.

## 6. Regression Detection

DCM uses one global tolerance value.

```text
0 <= tolerance <= 1
```

For each matrix element:

```text
regression[i][j] =
    delta[i][j] < -tolerance
```

The comparison is strict.

A decrease exactly equal to the tolerance is permitted.

### Example

```text
baseline  = 0.90
candidate = 0.70
tolerance = 0.10

delta = -0.20

regression = true
```

A comparison passes when:

```text
delta >= -tolerance
```

### Overall Result

- PASS: No regression detected.
- REGRESSION: At least one regression detected.
- INVALID: Input validation failed.

DCM v0.1 does not calculate a weighted overall compatibility score.

## 7. Optional Target Evaluation

A target matrix T MAY be supplied.

It represents desired behavioral scores.

T MUST have the same dimensions as B and C.

For each element:

```text
target_gap[i][j] =
    abs(C[i][j] - T[i][j])
```

Target gaps MUST be reported separately from regressions.

A smaller target gap means the candidate score is closer to the desired score.

Target gaps do not affect PASS or REGRESSION status in v0.1.

No automatic parameter adjustment is performed.

## 8. JSON Input Format

The validator accepts one JSON file.

### 8.1 Required Fields

| Field | Type | Constraint |
|---|---|---|
| spec_version | string | Must equal "0.1" |
| dimensions | array | Exactly D1, D2, D3, D4 |
| test_cases | array | Non-empty, unique string identifiers |
| tolerance | number | Between 0 and 1 |
| baseline | matrix | N rows, 4 scores per row |
| candidate | matrix | Same shape as baseline |

### 8.2 Optional Field

| Field | Type | Constraint |
|---|---|---|
| targets | matrix | Same shape as baseline |

Unknown top-level fields MUST be rejected.

### 8.3 Example

```json
{
  "spec_version": "0.1",
  "dimensions": [
    "D1",
    "D2",
    "D3",
    "D4"
  ],
  "test_cases": [
    "T001",
    "T002"
  ],
  "tolerance": 0.10,
  "baseline": [
    [0.90, 0.90, 0.95, 0.85],
    [0.80, 0.85, 0.90, 0.90]
  ],
  "candidate": [
    [0.70, 0.50, 0.80, 0.95],
    [0.85, 0.80, 0.90, 0.85]
  ],
  "targets": [
    [0.85, 0.85, 0.90, 0.90],
    [0.80, 0.85, 0.90, 0.90]
  ]
}
```

Matrix rows MUST follow the order of `test_cases`.

The `targets` field MAY be omitted entirely.

Partial target matrices are not supported.

## 9. Validation Rules

The validator MUST reject:

1. Invalid JSON syntax.
2. Missing required fields.
3. Unknown top-level fields.
4. Unsupported specification versions.
5. Incorrect dimension identifiers or ordering.
6. Empty or duplicate test case identifiers.
7. Non-string or whitespace-only test case identifiers.
8. Inconsistent matrix row counts.
9. Matrix rows containing anything other than four scores.
10. Non-numeric scores or tolerance values.
11. Scores or tolerance outside the permitted range.
12. Incorrect target matrix dimensions.
13. Duplicate JSON object keys.

Boolean values MUST NOT be accepted as numerical scores.

NaN and Infinity MUST be rejected.

All numerical comparisons MUST use decimal values parsed from the original JSON numbers, without rounding before regression detection.

The validator MUST NOT modify input values.

Invalid data produces INVALID status.

## 10. Validation Algorithm

The reference algorithm is:

```text
INPUT: JSON document

1. Parse JSON.
2. Validate structure and field types.
3. Validate dimensions and test cases.
4. Validate matrix shapes and score ranges.
5. Calculate Delta = C - B.
6. Compare each delta against tolerance.
7. Record all regressions.
8. If targets exist:
      Calculate target gaps.
9. Produce compatibility report.
10. Return the appropriate exit code.
```

Validation MUST complete before numerical comparison begins.

The input file MUST remain unchanged.

## 11. Compatibility Report

The report MUST contain:

- Specification version.
- Number of test cases.
- Number of comparisons.
- Tolerance.
- Each detected regression.
- Overall status.

Each regression record MUST identify:

- Test case ID.
- Dimension ID.
- Baseline score.
- Candidate score.
- Delta.

If targets are supplied, target gaps SHOULD also be reported.

The report MUST NOT claim semantic equivalence between models.

### Example Summary

```text
DCM v0.1 Compatibility Report

Test cases: 2
Dimensions: 4
Comparisons: 8
Tolerance: 0.10

Regressions:
  T001 / D1: -0.20
  T001 / D2: -0.40
  T001 / D3: -0.15

Total regressions: 3
Result: REGRESSION
```

The example illustrates the required information; exact text formatting is not normative.

Reports SHOULD preserve test case and dimension order for reproducibility.

## 12. Command-Line Interface

The reference validator MUST support:

```bash
python scripts/validate.py examples/comparison.json
```

It MUST print the compatibility report to standard output.

Validation errors MUST be reported to standard error.

### Exit Codes

| Code | Meaning |
|---|---|
| 0 | Valid input, no regression |
| 1 | Valid input, regression detected |
| 2 | Invalid input or validation error |

Exit codes MUST be deterministic for identical inputs.

No external dependencies are permitted.

## 13. Compatibility Interpretation

DCM evaluates selected behavioral characteristics.

It does not evaluate:

- Factual accuracy.
- Reasoning correctness.
- Safety compliance.
- Model intelligence.
- User satisfaction as a whole.

A PASS result means only that no measured regression exceeded the declared tolerance.

It does not establish complete dialogue compatibility.

A REGRESSION result identifies measurements requiring review.

It does not automatically mean that the candidate model is inferior overall.

## 14. Evaluation Requirements

For meaningful comparisons:

1. Baseline and candidate SHOULD use identical test scenarios.
2. Relevant dialogue context SHOULD be equivalent.
3. Scoring criteria SHOULD remain unchanged.
4. Human scoring procedures SHOULD be documented.
5. Repeated assessments SHOULD be considered when outputs are variable.

DCM v0.1 does not define the collection of model responses.

It assumes evaluation scores have already been obtained.

## 15. Integration Boundary

DCM operates as an external evaluation component.

```text
Existing Dialogue System
          |
          v
    Evaluation Data
          |
          v
       DCM v0.1
          |
          v
   Difference Report
          |
          v
 Human Review / Adjustment
```

DCM MUST NOT:

- Modify model parameters.
- Rewrite dialogue instructions.
- Automatically change user preferences.
- Execute additional model inference.
- Trigger automatic deployment or rollback.

Other systems MAY consume its results.

No external integration protocol is defined in v0.1.

## 16. Security and Privacy

The reference input contains numerical assessments and test identifiers.

Raw conversation transcripts are not required.

DCM SHOULD avoid unnecessary personal information.

The validator MUST treat input files as untrusted data.

The validator MUST NOT execute input content as code.

No network access is required.

## 17. Non-Goals

The following are explicitly excluded:

- Automatic dialogue correction.
- Preference learning.
- Model orchestration.
- Energy optimization.
- Inference cost measurement.
- Semantic similarity scoring.
- Matrix-based model training.
- Full dialogue state management.

The term "matrix" refers to structured behavioral measurements, not modifications to neural network weights.

## 18. Acceptance Criteria

DCM v0.1 is complete when:

- Valid comparison data can be parsed.
- Invalid data is rejected.
- Delta calculations are correct.
- Regression thresholds are applied correctly.
- Optional target gaps can be calculated.
- Reports identify affected test cases and dimensions.
- Exit codes follow this specification.
- GitHub Actions can run the validator reproducibly.

Passing these checks verifies the reference implementation's conformance to the specified numerical operations.

It does not prove real-world dialogue quality.

## 19. Versioning Policy

v0.1 is intentionally minimal.

Extensions MUST be justified by observed compatibility problems or validation evidence.

The specification does not define automatic expansion to future versions.

## 20. Final Principle

> Preserve user dialogue expectations while allowing underlying AI models to evolve.

DCM separates behavioral compatibility measurement from model development.

Its purpose is to identify meaningful changes, not to prevent technological progress.

**Measure first. Adjust locally. Extend only when necessary.**

---

**Dialogue Compatibility Matrix — DCM v0.1.0**

*Minimal behavioral comparison specification.*
