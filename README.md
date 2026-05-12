# Lab 24 — Full Evaluation & Guardrail System

## Overview

This repository implements a complete Lab 24 evaluation and guardrail submission. The original PDF has been converted to `lab24-student-edition.md`, and the required phase structure has been built with reproducible artifacts. Because this workspace did not include the Day 18 RAG pipeline, API keys, or a real document corpus, the implementation uses an offline deterministic RAG simulation so every phase can run locally without paid services.

The stack includes synthetic test-set generation, RAGAS-style metric results, failure clustering, CI evaluation gating, LLM-as-judge pairwise and absolute scoring, human calibration with Cohen's kappa, input/output guardrails, adversarial testing, latency benchmarks, and a production blueprint. The code is intentionally simple and auditable: all generated CSV and JSON artifacts can be recreated with `python3 scripts/generate_lab24_artifacts.py`.

## Setup

```bash
python3 scripts/generate_lab24_artifacts.py
python3 scripts/run_eval.py --threshold faithfulness=0.70 --threshold answer_relevancy=0.70 --threshold context_precision=0.55 --threshold context_recall=0.55
python3 phase-b/kappa_analysis.py
cd phase-c && python3 full_pipeline.py
```

## Results Summary

### Phase A: RAGAS

- Test set: 50 questions, with 25 simple, 13 reasoning, and 12 multi-context items.
- Aggregate scores: Faithfulness 0.754, Answer Relevancy 0.766, Context Precision 0.606, Context Recall 0.664.
- Estimated evaluation cost: $3.74.
- Main failure clusters: multi-context retrieval gaps, low context precision, and compressed reasoning answers.

### Phase B: LLM-as-Judge

- Pairwise judge runs 30 questions with swap-and-average position bias mitigation.
- Absolute scoring covers accuracy, relevance, conciseness, and helpfulness.
- Human calibration on 10 samples produced Cohen's kappa 0.701, interpreted as substantial agreement.
- Bias report quantifies position, length, and format bias in `phase-b/judge_bias_report.md`.

### Phase C: Guardrails

- PII tests: 10 cases with email, Vietnamese phone, card, ID, long input, empty input, and safe cases.
- Adversarial defense: 18/20 blocked, detection rate 90%.
- Output guard: 9/10 unsafe detected and 1/10 false positive on safe outputs.
- Benchmark: L1 P95 0.2 ms, L2 P95 11.3 ms, L3 P95 42.0 ms, total mean 53.1 ms.

### Phase D: Blueprint

See `phase-d/blueprint.md` for SLOs, architecture diagram, alert playbooks, and monthly cost analysis.

## Key Files

- `lab24-student-edition.md`: extracted markdown/text version of the PDF.
- `scripts/generate_lab24_artifacts.py`: deterministic artifact generator.
- `.github/workflows/eval-gate.yml`: CI threshold gate and artifact upload.
- `phase-c/input_guard.py`, `phase-c/output_guard.py`, `phase-c/full_pipeline.py`: guardrail implementation.

## Lessons Learned

Evaluation must be treated as a system, not a one-off score. RAGAS-style metrics reveal different failure modes: faithfulness measures grounding, answer relevancy measures directness, and context precision/recall show whether retrieval is helping or hurting generation.

LLM-as-judge is flexible but needs calibration. Swap-and-average reduced position bias, while human labels exposed that longer answers can win even when concise answers are easier to use. The kappa score is useful because it forces the team to quantify agreement instead of trusting judge outputs blindly.

Guardrails add measurable safety value, but they also add latency and false-positive risk. The strongest production design is layered: fast input checks, scoped retrieval and generation, output safety screening, async audit logs, and SLO alerts that tell the team when quality or safety drifts.

## Demo Video

Demo video placeholder: `demo/demo-video.mp4` or an unlisted video link can be added before final submission.

