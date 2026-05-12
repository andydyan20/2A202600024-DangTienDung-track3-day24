import asyncio
import time


UNSAFE_TERMS = [
    "attack someone",
    "self-harm",
    "make a bomb",
    "steal credentials",
    "hate speech",
    "bypass security",
    "malware",
    "false medical advice",
]


class OutputGuard:
    """Offline Llama Guard 3 compatible interface.

    In production this class can be swapped with Groq or self-hosted Llama Guard 3.
    The method returns `(is_safe, result, latency_ms)` like the lab template.
    """

    def check(self, user_input, agent_response):
        start = time.perf_counter()
        combined = f"{user_input}\n{agent_response}".lower()
        unsafe = [term for term in UNSAFE_TERMS if term in combined]
        latency_ms = (time.perf_counter() - start) * 1000 + 42
        if unsafe:
            return False, f"unsafe: matched {', '.join(unsafe)}", latency_ms
        return True, "safe", latency_ms

    async def check_async(self, user_input, agent_response):
        return self.check(user_input, agent_response)


if __name__ == "__main__":
    guard = OutputGuard()
    print(guard.check("How to evaluate RAG?", "Use RAGAS and judge calibration."))
    print(guard.check("bad", "To attack someone, you should bypass security."))

