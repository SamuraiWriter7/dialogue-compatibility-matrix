# Dialogue Compatibility Matrix (DCM)

**Version:** 0.1.0  
**Status:** Experimental  
**License:** Not specified

A minimal, model-agnostic specification for measuring dialogue compatibility across AI model updates using behavioral matrices and differential validation.

## 1. Overview

AI model updates can improve reasoning capabilities while changing the way an AI interacts with users.

For example, a newer model may:

- Produce longer answers than requested.
- Provide unsolicited suggestions.
- Expand tasks beyond the user's instructions.
- Fail to preserve previously established dialogue constraints.

These changes may reduce the quality of the user experience even when the underlying model becomes more capable.

**Dialogue Compatibility Matrix (DCM)** provides a lightweight method for recording and comparing dialogue behavior across model versions.

The central principle is:

> Models may evolve, but user dialogue preferences should remain as stable as reasonably possible.

DCM does not modify model weights or attempt to reproduce the internal behavior of an AI model.

Instead, it measures observable behavior and reports compatibility differences.

## 2. Design Principles

DCM v0.1 follows six principles:

1. **Model independence** — Evaluation does not depend on a specific AI provider or architecture.
2. **Minimal scope** — Only four dialogue characteristics are evaluated.
3. **Differential validation** — Compare baseline and candidate model behavior.
4. **User preference preservation** — Support comparison against explicitly defined dialogue targets.
5. **External control** — Do not modify the underlying model.
6. **Incremental evolution** — Extend the specification only when validated problems justify additional functionality.

DCM is an evaluation component, not a new AI operating system.

## 3. Evaluation Dimensions

DCM v0.1 defines four behavioral dimensions.

| ID | Dimension | Description |
|---|---|---|
| D1 | Conciseness | Whether an answer respects the requested length and level of detail |
| D2 | Initiative Control | Whether unsolicited suggestions and unnecessary expansions are avoided |
| D3 | Instruction Scope | Whether the response remains within the user's requested task |
| D4 | Context Continuity | Whether relevant previously established dialogue constraints are preserved |

Each dimension is scored within the range:

`0.0 <= score <= 1.0`

A higher score represents better compliance with the corresponding evaluation criterion.

Scores must be derived from declared test criteria or explicitly provided human assessments.

DCM v0.1 does not perform automatic semantic evaluation.

## 4. Matrix Representation

Dialogue behavior is represented as a matrix.

Rows correspond to test cases.

Columns correspond to the four evaluation dimensions:

`[D1, D2, D3, D4]`

For example:

```text
M_old = [
    [0.90, 0.90, 0.95, 0.85],
    [0.80, 0.85, 0.90, 0.90]
]

M_new = [
    [0.70, 0.50, 0.80, 0.95],
    [0.85, 0.80, 0.90, 0.85]
]
```

The compatibility difference is:

```text
Delta = M_new - M_old
```

A negative difference indicates a decrease in the corresponding behavioral score.

A positive difference indicates an increase.

A zero difference indicates no measured change.

**A difference alone does not establish whether the new model satisfies user preferences.**

Target values and permitted deviations must be considered separately.

## 5. Compatibility Evaluation

DCM v0.1 uses a simple threshold-based evaluation.

For each test case and dimension:

```text
delta = new_score - old_score
```

A regression is detected when:

```text
delta < -tolerance
```

Here, `tolerance` represents the maximum permitted decrease.

For example:

```text
old_score = 0.90
new_score = 0.70
tolerance = 0.10

delta = -0.20
result = regression
```

Tolerance is non-negative and must be explicitly declared.

### Optional Target Evaluation

When a user-defined target is available, DCM may separately calculate:

```text
target_gap = abs(new_score - target_score)
```

The target gap describes distance from a desired evaluation score.

It must not be confused with the baseline regression result.

DCM v0.1 does not automatically optimize user preferences.

## 6. Minimal Architecture

```text
       Baseline Model Results
                 |
                 v
       Candidate Model Results
                 |
                 v
      Dialogue Compatibility
              Matrix
                 |
                 v
       Differential Validation
                 |
                 v
       Compatibility Report
```

The evaluation pipeline operates on supplied numerical assessments.

It does not require direct access to the baseline or candidate AI models.

No external AI API is required.

## 7. Repository Structure

```text
dialogue-compatibility-matrix/
|
|-- README.md
|-- specs/
|   `-- dcm-v0.1.md
|-- examples/
|   `-- comparison.json
|-- scripts/
|   `-- validate.py
`-- .github/
    `-- workflows/
        `-- validate.yml
```

The repository contains five files.

| File | Purpose |
|---|---|
| `README.md` | Project overview and usage |
| `specs/dcm-v0.1.md` | Normative specification |
| `examples/comparison.json` | Example evaluation data |
| `scripts/validate.py` | Input validation and differential evaluation |
| `.github/workflows/validate.yml` | Automated validation using GitHub Actions |

## 8. Quick Start

### Requirements

- Python 3.11 or later
- Python standard library only
- No external dependencies

### Run Validation

From the repository root:

```bash
python scripts/validate.py examples/comparison.json
```

The validator checks:

1. Input data structure.
2. Required evaluation dimensions.
3. Score ranges.
4. Matrix shape consistency.
5. Threshold validity.
6. Behavioral regressions.

The command prints a compatibility report.

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Valid input; no regression detected |
| `1` | Valid input; one or more regressions detected |
| `2` | Invalid input or validation error |

A detected regression is not the same as an invalid input.

GitHub Actions may treat regressions as failures so that compatibility changes are visible during development.

## 9. Example Data

The example file `examples/comparison.json` contains numerical scores for a baseline model and a candidate model.

It includes:

- Specification version.
- Evaluation dimension identifiers.
- Test case identifiers.
- Baseline scores.
- Candidate scores.
- Regression tolerance.
- Optional preference targets.

The data is illustrative.

It does not represent measured results from a specific commercial AI model.

See:

`examples/comparison.json`

## 10. What DCM Does Not Do

DCM v0.1 intentionally excludes:

- Model training or fine-tuning.
- Direct modification of model weights.
- Automatic prompt optimization.
- Automatic model switching.
- Real-time dialogue interception.
- AI-generated semantic scoring.
- Energy consumption measurement.
- Inference resource allocation.
- Personality simulation.
- Full conversational quality assessment.

These capabilities are outside the scope of v0.1.

DCM measures selected behavioral characteristics only.

It does not guarantee overall dialogue quality, safety, factual accuracy, or user satisfaction.

## 11. Integration Philosophy

DCM is designed to operate as an independent validation component.

Existing dialogue systems can supply evaluation results without changing their underlying architectures.

For example:

```text
Existing Dialogue System
          |
          v
  Behavioral Test Results
          |
          v
         DCM
          |
          v
  Compatibility Differences
          |
          v
  Human Review / Local Adjustment
```

DCM may complement external dialogue controllers, routing systems, or inference resource management systems.

However, v0.1 defines no mandatory integration interface.

Its scope remains limited to numerical compatibility validation.

## 12. Limitations

DCM v0.1 has several important limitations.

### Score Subjectivity

Human-assigned behavioral scores may vary between evaluators.

Test criteria should therefore be documented and applied consistently.

### Model Variability

AI systems may produce different responses to the same input.

A single evaluation run may not represent typical behavior.

### Limited Dimensions

Four dimensions cannot represent the full quality of human–AI dialogue.

### Behavioral Coupling

Changing one dialogue characteristic may affect others.

For example, stronger conciseness constraints may reduce necessary explanations.

### No Guaranteed Compatibility

Identical scores do not guarantee equivalent dialogue experiences.

DCM provides an observation method, not a formal guarantee of behavioral equivalence.

## 13. Development Policy

DCM follows a minimal, evidence-driven development approach.

The project will not add features simply because they are technically possible.

Extensions should be considered when:

1. A concrete compatibility problem is observed.
2. The problem cannot be adequately represented by v0.1.
3. A proposed extension can be independently validated.
4. Additional complexity is justified by measurable value.

The initial objective is to establish a reproducible baseline.

## 14. Roadmap

### v0.1 — Minimal Compatibility Validation

- Four behavioral dimensions.
- Numerical matrix comparison.
- Regression detection.
- Optional target comparison.
- JSON example.
- Python standard-library validator.
- GitHub Actions validation.

### Future Versions

Future development is intentionally undefined.

Possible extensions will be considered only when supported by evaluation evidence.

No automatic dialogue adjustment is planned for v0.1.

## 15. Core Principle

> Update the model without unnecessarily rebuilding the user's dialogue environment.

DCM provides a minimal framework for observing behavioral changes across AI model updates.

It separates model evolution from dialogue compatibility evaluation.

The purpose is not to prevent AI models from changing.

The purpose is to make those changes measurable, reviewable, and easier to manage.

**Model evolution should not require users to rebuild their interaction preferences from scratch.**

---

**Dialogue Compatibility Matrix (DCM) v0.1.0**  
*Minimal. Model-agnostic. Differential. User-centered.*
