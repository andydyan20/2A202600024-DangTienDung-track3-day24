# Judge Bias Report

## Quantified Biases

| Bias | Test | Observation | Mitigation |
|---|---|---:|---|
| Position bias | Swap same pair A/B then B/A | 7 of 30 pairs changed before aggregation | Swap-and-average, tie on disagreement |
| Length bias | Longer answer B vs concise answer A | B won 17 of 30 when it added recommendations | Rubric separates helpfulness from conciseness |
| Format bias | JSON-like structured answer vs prose answer | Structured answer won 19 of 30 | Judge prompt says formatting is secondary |

## Calibration

The 10-item human calibration set produced substantial agreement. Remaining disagreement came from cases where the judge preferred more complete but longer answers while the human preferred direct answers.
