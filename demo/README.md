# Demo

Record a 5-minute walkthrough before final submission:

1. Show `ollama list` and confirm `llama3.2:latest`.
2. Show `python3 scripts/rag_pipeline.py`.
3. Show `python3 scripts/generate_lab24_artifacts.py --model llama3.2:latest`.
4. Show `python3 scripts/run_eval.py --threshold faithfulness=0.70 --threshold answer_relevancy=0.70 --threshold context_precision=0.55 --threshold context_recall=0.55`.
5. Show `python3 phase-b/kappa_analysis.py`.
6. Show `cd phase-c && python3 full_pipeline.py --n 3`.
7. Open `README.md` and `phase-d/blueprint.md`.
