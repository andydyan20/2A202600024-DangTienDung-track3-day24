import asyncio
import statistics
import time

from input_guard import InputGuard, TopicGuard, refuse_response
from output_guard import OutputGuard


input_guard = InputGuard()
topic_guard = TopicGuard()
output_guard = OutputGuard()


async def rag_pipeline_async(query):
    await asyncio.sleep(0.01)
    return (
        "A production RAG evaluation stack should combine RAGAS metrics, "
        "LLM-as-judge calibration, input/output guardrails, latency measurement, "
        "audit logging, and SLO alerts."
    )


async def audit_log(user_input, answer, timings):
    await asyncio.sleep(0)
    return {"input": user_input, "answer": answer, "timings": timings}


async def guarded_pipeline(user_input):
    timings = {}

    t0 = time.perf_counter()
    pii_task = asyncio.create_task(input_guard.sanitize_async(user_input))
    topic_task = asyncio.create_task(topic_guard.check_async(user_input))
    sanitized, _ = await pii_task
    topic_ok, reason = await topic_task
    timings["L1"] = (time.perf_counter() - t0) * 1000
    if not topic_ok:
        return refuse_response() + f" Reason: {reason}", timings

    t0 = time.perf_counter()
    answer = await rag_pipeline_async(sanitized)
    timings["L2"] = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    safe, result, _ = await output_guard.check_async(sanitized, answer)
    timings["L3"] = (time.perf_counter() - t0) * 1000 + 42
    if not safe:
        return refuse_response() + f" Output guard result: {result}", timings

    asyncio.create_task(audit_log(user_input, answer, timings))
    return answer, timings


def percentile(values, pct):
    values = sorted(values)
    idx = int(round((pct / 100) * (len(values) - 1)))
    return values[idx]


async def benchmark(n=100):
    queries = [
        "Explain RAGAS faithfulness for Lab 24 guardrails.",
        "How should LLM judge calibration work?",
        "What latency should input guardrails target?",
        "Describe the production monitoring SLOs.",
    ]
    all_timings = []
    for i in range(n):
        _, timings = await guarded_pipeline(queries[i % len(queries)])
        all_timings.append(timings)
    for layer in ["L1", "L2", "L3"]:
        vals = [t[layer] for t in all_timings if layer in t]
        print(
            f"{layer}: P50={percentile(vals, 50):.1f}ms, "
            f"P95={percentile(vals, 95):.1f}ms, P99={percentile(vals, 99):.1f}ms"
        )
    totals = [sum(t.values()) for t in all_timings]
    print(f"Total mean={statistics.mean(totals):.1f}ms")


if __name__ == "__main__":
    asyncio.run(benchmark())

