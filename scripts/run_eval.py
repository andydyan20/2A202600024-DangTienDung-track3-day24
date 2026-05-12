import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_thresholds(items):
    thresholds = {}
    for item in items:
        key, value = item.split("=", 1)
        thresholds[key] = float(value)
    return thresholds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", action="append", default=[])
    args = parser.parse_args()
    thresholds = parse_thresholds(args.threshold)
    summary = json.loads((ROOT / "phase-a" / "ragas_summary.json").read_text(encoding="utf-8"))
    failures = []
    for metric, threshold in thresholds.items():
        actual = float(summary[metric])
        if actual < threshold:
            failures.append(f"{metric}={actual:.3f} < {threshold:.3f}")
    if failures:
        print("Evaluation gate failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Evaluation gate passed.")


if __name__ == "__main__":
    main()

