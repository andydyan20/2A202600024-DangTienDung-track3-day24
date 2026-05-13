# Lab 24 — Full Evaluation & Guardrail System

## Overview

This repository implements a complete Lab 24 evaluation and guardrail submission. The original PDF has been converted to `lab24-student-edition.md`, and the required phase structure has been built with reproducible artifacts. The RAG pipeline is local-first: it loads markdown documents, chunks them, retrieves relevant chunks with lexical scoring, and generates grounded answers with Ollama `llama3.2:latest`.

The stack includes synthetic test-set generation, RAGAS-style metric results over live RAG answers, failure clustering, CI evaluation gating, LLM-as-judge pairwise and absolute scoring, human calibration with Cohen's kappa, input/output guardrails, adversarial testing, latency benchmarks, and a production blueprint.

## Setup

```bash
ollama serve
ollama pull llama3.2
python3 scripts/generate_lab24_artifacts.py --model llama3.2:latest
python3 scripts/run_eval.py --threshold faithfulness=0.70 --threshold answer_relevancy=0.70 --threshold context_precision=0.55 --threshold context_recall=0.55
python3 phase-b/kappa_analysis.py
cd phase-c && python3 full_pipeline.py --n 3
```

## Results Summary

### Phase A: RAGAS

- Test set: 50 questions, with 25 simple, 13 reasoning, and 12 multi-context items.
- RAG model: `llama3.2:latest` via local Ollama.
- Aggregate scores: Faithfulness 0.772, Answer Relevancy 0.900, Context Precision 0.725, Context Recall 0.863.
- Estimated evaluation cost: $0.00 because generation and evaluation run locally.
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
- Live guarded RAG benchmark on 3 Ollama requests: L1 P95 0.2 ms, L2 P95 4505.2 ms, L3 P95 42.0 ms, total mean 2507.9 ms.

### Phase D: Blueprint

See `phase-d/blueprint.md` for SLOs, architecture diagram, alert playbooks, and monthly cost analysis.

## Key Files

- `lab24-student-edition.md`: extracted markdown/text version of the PDF.
- `scripts/rag_pipeline.py`: local RAG pipeline with markdown loading, chunking, retrieval, Ollama generation, and lexical RAGAS-style scoring.
- `scripts/generate_lab24_artifacts.py`: deterministic artifact generator.
- `.github/workflows/eval-gate.yml`: CI threshold gate and artifact upload.
- `phase-c/input_guard.py`, `phase-c/output_guard.py`, `phase-c/full_pipeline.py`: guardrail implementation.

## Lessons Learned

Evaluation must be treated as a system, not a one-off score. RAGAS-style metrics reveal different failure modes: faithfulness measures grounding, answer relevancy measures directness, and context precision/recall show whether retrieval is helping or hurting generation.

LLM-as-judge is flexible but needs calibration. Swap-and-average reduced position bias, while human labels exposed that longer answers can win even when concise answers are easier to use. The kappa score is useful because it forces the team to quantify agreement instead of trusting judge outputs blindly.

Guardrails add measurable safety value, but they also add latency and false-positive risk. The strongest production design is layered: fast input checks, scoped retrieval and generation, output safety screening, async audit logs, and SLO alerts that tell the team when quality or safety drifts.

## Demo Video

Demo video placeholder: `demo/demo-video.mp4` or an unlisted video link can be added before final submission.
