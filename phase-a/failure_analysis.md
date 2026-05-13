# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Why should guardrail latency be benchmarked? | simple | 0.63 | 0.963 | 0.25 | 0.25 | 0.523 | C2 |
| 2 | Why should guardrail latency be benchmarked? | simple | 0.662 | 0.995 | 0.25 | 0.25 | 0.539 | C2 |
| 3 | How does Cohen's kappa help calibrate an LLM judge? | reasoning | 0.25 | 0.796 | 0.689 | 0.828 | 0.641 | C3 |
| 4 | How does Cohen's kappa help calibrate an LLM judge? | reasoning | 0.3 | 0.921 | 0.671 | 0.81 | 0.675 | C3 |
| 5 | How do SLO alerts and audit logs support incident response? | multi_context | 0.286 | 0.895 | 0.645 | 0.895 | 0.680 | C1 |
| 6 | How does Cohen's kappa help calibrate an LLM judge? | reasoning | 0.269 | 0.957 | 0.707 | 0.846 | 0.695 | C3 |
| 7 | How do SLO alerts and audit logs support incident response? | multi_context | 0.25 | 0.93 | 0.68 | 0.93 | 0.698 | C1 |
| 8 | Edited: How should an output guardrail handle unsafe generated conte | simple | 0.992 | 0.563 | 0.492 | 0.792 | 0.710 | C2 |
| 9 | How can low RAGAS scores guide retriever improvements? | reasoning | 0.587 | 0.92 | 0.626 | 0.72 | 0.713 | C3 |
| 10 | How should a team reduce continuous evaluation cost? | reasoning | 0.509 | 0.921 | 0.504 | 0.921 | 0.714 | C2 |

## Clusters Identified

### Cluster C1: Multi-context retrieval gaps

**Pattern:** Questions requiring evidence from multiple Lab 24 sections have lower context recall.

**Examples:** architecture and benchmark questions that combine guardrail, eval, and monitoring concepts.

**Root cause:** The lexical retriever returns one dominant context instead of combining evidence from separate sections.

**Proposed fix:** Increase `top_k` from 3 to 6, add hybrid BM25 + vector search, and add a cross-encoder reranker.

### Cluster C2: Low context precision

**Pattern:** Retrieved context is on the correct general topic but includes unrelated operational details.

**Examples:** cost, threshold, and failure-cluster questions.

**Root cause:** Retrieval is too broad and does not filter by phase metadata.

**Proposed fix:** Add metadata filters by phase, chunk documents by task heading, and use MMR to reduce redundant chunks.

### Cluster C3: Reasoning answer compression

**Pattern:** Reasoning answers are concise but omit one causal step.

**Examples:** judge calibration and CI gate questions.

**Root cause:** The generation prompt prioritizes short answers over explicit chain of evidence.

**Proposed fix:** Require answer plans with cited context ids before final generation.
