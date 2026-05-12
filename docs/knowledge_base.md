# Sample RAG Corpus

This sample corpus is used for the offline Lab 24 implementation.

VinUniversity AICB labs teach retrieval augmented generation, evaluation, guardrails, and production monitoring.

RAGAS metrics include faithfulness, answer relevancy, context precision, and context recall. Faithfulness checks whether the answer is grounded in retrieved context. Answer relevancy checks whether the response addresses the question. Context precision checks whether retrieved chunks are useful. Context recall checks whether the required evidence was retrieved.

LLM-as-judge workflows compare answers pairwise and can also score absolute quality with rubrics. Common judge biases include position bias, verbosity bias, self-enhancement bias, and format bias. Swap-and-average helps reduce position bias.

Input guardrails should redact personal information, validate topic scope, and detect prompt injection. Output guardrails should screen unsafe responses before returning them to the user. Latency must be measured per layer to understand overhead.

Production blueprints should define SLOs, architecture, alert playbooks, and cost estimates.

