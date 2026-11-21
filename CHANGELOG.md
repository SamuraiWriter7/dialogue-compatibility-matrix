# Changelog

All notable changes to Dialogue Compatibility Matrix (DCM) are documented in this file.

This project follows an evidence-driven, minimal development approach.

## [0.1.0] - 2026-11-21

### Initial Release

First experimental release of Dialogue Compatibility Matrix (DCM).

DCM v0.1.0 provides a minimal, model-agnostic framework for detecting changes in observable dialogue behavior across AI model updates.

### Added

- Initial DCM v0.1 specification.
- Four fixed dialogue evaluation dimensions:
  - D1: Conciseness
  - D2: Initiative Control
  - D3: Instruction Scope
  - D4: Context Continuity
- Numerical comparison of baseline and candidate behavior matrices.
- Element-wise delta calculation.
- Configurable regression tolerance.
- Optional user preference target comparison.
- Deterministic compatibility reports.
- JSON input validation.
- Rejection of invalid scores, duplicate JSON keys, and malformed inputs.
- Python 3.11+ reference validator using only the standard library.
- GitHub Actions workflow for automated validation.

### Validation

GitHub Actions validation passed.

The workflow verifies:

- Python syntax validity.
- Expected detection of three regressions in the example dataset.
- Successful evaluation of a non-regression dataset.
- Rejection of invalid Boolean scores.
- Rejection of duplicate JSON object keys.
- Correct exit code behavior.

### Exit Codes

- `0`: Valid input; no regression detected.
- `1`: Valid input; regression detected.
- `2`: Invalid input or validation error.

### Design Boundaries

DCM v0.1.0 intentionally does not include:

- Automatic dialogue correction.
- Model training or fine-tuning.
- Automatic model switching.
- Semantic evaluation using external AI models.
- Inference resource allocation.
- Energy consumption measurement.
- Real-time dialogue interception.

### Limitations

- Evaluation scores must be supplied externally.
- Four dimensions do not represent complete dialogue quality.
- Numerical compatibility does not guarantee semantic equivalence.
- Results depend on the quality and consistency of the supplied assessments.
- Real-world model compatibility has not yet been established.

### Development Policy

Future extensions will be considered only when supported by observed compatibility problems or reproducible validation evidence.

The priority is to validate the existing structure before increasing complexity.

---

## Project Principle

> Measure first. Adjust locally. Extend only when necessary.

**Model evolution should not require users to rebuild their dialogue preferences from scratch.**
