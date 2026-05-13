# AI Prompts Log

This lab was completed with assistance from Codex.

## Prompt 1

> from this pdf, convert it to file md or text then process to done every phare for me. Then write me a report in readme

## Prompt 2

> make for me a  RAG pipeline and use it to evaluation, use model local ollama llama3.2

## Notes

- The original lab PDF was converted into `lab24-student-edition.md`.
- The workspace did not contain a prior Day 18 RAG pipeline, so `scripts/rag_pipeline.py` implements a local markdown RAG pipeline.
- RAG generation and Phase A evaluation artifacts were regenerated with local Ollama `llama3.2:latest`.
- Production integrations are documented in `phase-d/blueprint.md` and the CI gate in `.github/workflows/eval-gate.yml`.
