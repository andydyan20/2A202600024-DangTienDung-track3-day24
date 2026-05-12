# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | How should latency be compared with and without guardrails? | multi_context | 0.554 | 0.625 | 0.31 | 0.53 | 0.505 | C1 |
| 2 | What components are needed for a production evaluation blueprint? | multi_context | 0.505 | 0.67 | 0.385 | 0.464 | 0.506 | C1 |
| 3 | How can low RAGAS scores guide retriever improvements? | reasoning | 0.612 | 0.645 | 0.375 | 0.504 | 0.534 | C2 |
| 4 | How can low RAGAS scores guide retriever improvements? | reasoning | 0.541 | 0.645 | 0.425 | 0.526 | 0.534 | C2 |
| 5 | How do SLO alerts and audit logs support incident response? | multi_context | 0.512 | 0.64 | 0.46 | 0.53 | 0.535 | C1 |
| 6 | What components are needed for a production evaluation blueprint? | multi_context | 0.559 | 0.67 | 0.435 | 0.486 | 0.537 | C1 |
| 7 | How should a team reduce continuous evaluation cost? | reasoning | 0.631 | 0.63 | 0.475 | 0.46 | 0.549 | C2 |
| 8 | What does context recall show about evidence retrieval? | simple | 0.648 | 0.66 | 0.485 | 0.63 | 0.606 | C2 |
| 9 | Why should guardrail latency be benchmarked? | simple | 0.686 | 0.675 | 0.46 | 0.63 | 0.613 | C2 |
| 10 | What does context recall show about evidence retrieval? | simple | 0.699 | 0.66 | 0.56 | 0.586 | 0.626 | C3 |

## Clusters Identified

### Cluster C1: Multi-context retrieval gaps

**Pattern:** Questions requiring evidence from multiple Lab 24 sections have lower context recall.

**Examples:** architecture and benchmark questions that combine guardrail, eval, and monitoring concepts.

**Root cause:** The simulated retriever returns one dominant context instead of combining evidence from separate sections.

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
