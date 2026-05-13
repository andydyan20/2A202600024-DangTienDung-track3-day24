import json
import math
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "llama3.2:latest"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "why",
    "with",
}


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str
    tokens: set[str]


def tokenize(text):
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if len(token) > 2 and token not in STOPWORDS
    }


def read_corpus(paths=None):
    if paths is None:
        paths = [ROOT / "docs", ROOT / "lab24-student-edition.md"]

    files = []
    for path in paths:
        path = Path(path)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
            files.extend(sorted(path.rglob("*.txt")))
        elif path.exists():
            files.append(path)

    documents = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        if text.strip():
            documents.append((str(file_path.relative_to(ROOT)), text))
    return documents


def split_document(source, text, max_words=130, overlap=30):
    words = text.split()
    chunks = []
    if not words:
        return chunks
    step = max(1, max_words - overlap)
    for start in range(0, len(words), step):
        part = " ".join(words[start : start + max_words]).strip()
        if len(part) < 80:
            continue
        chunk_id = f"{source}#{len(chunks) + 1}"
        chunks.append(Chunk(chunk_id=chunk_id, source=source, text=part, tokens=tokenize(part)))
    return chunks


def build_index():
    chunks = []
    for source, text in read_corpus():
        chunks.extend(split_document(source, text))
    if not chunks:
        raise RuntimeError("No markdown/text corpus found. Add documents under docs/.")

    doc_freq = {}
    for chunk in chunks:
        for token in chunk.tokens:
            doc_freq[token] = doc_freq.get(token, 0) + 1
    idf = {token: math.log((len(chunks) + 1) / (freq + 1)) + 1 for token, freq in doc_freq.items()}
    return chunks, idf


class LocalRAGPipeline:
    def __init__(self, model=DEFAULT_MODEL, top_k=4, timeout=120):
        self.model = model
        self.top_k = top_k
        self.timeout = timeout
        self.chunks, self.idf = build_index()

    def retrieve(self, question):
        query_tokens = tokenize(question)
        scored = []
        for chunk in self.chunks:
            overlap = query_tokens & chunk.tokens
            if not overlap:
                continue
            score = sum(self.idf.get(token, 1.0) for token in overlap)
            score += 0.05 * len(overlap)
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        if not scored:
            return self.chunks[: self.top_k]
        return [chunk for _, chunk in scored[: self.top_k]]

    def answer(self, question):
        chunks = self.retrieve(question)
        context = "\n\n".join(
            f"[{idx + 1}] Source: {chunk.source}\n{chunk.text}" for idx, chunk in enumerate(chunks)
        )
        prompt = (
            "You are a concise RAG assistant for VinUniversity Lab 24.\n"
            "Answer only using the provided context. If the answer is not in the context, say so.\n"
            "Cite evidence with bracket numbers like [1].\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )
        start = time.perf_counter()
        answer = call_ollama(prompt, model=self.model, timeout=self.timeout)
        latency_ms = (time.perf_counter() - start) * 1000
        return {
            "question": question,
            "answer": answer,
            "contexts": [chunk.text for chunk in chunks],
            "context_ids": [chunk.chunk_id for chunk in chunks],
            "latency_ms": latency_ms,
            "model": self.model,
        }


def call_ollama(prompt, model=DEFAULT_MODEL, timeout=120):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_ctx": 4096,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "").strip()
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not reach Ollama. Start it with `ollama serve` and ensure `llama3.2` is pulled."
        ) from exc


def lexical_score(numerator_tokens, denominator_tokens):
    if not denominator_tokens:
        return 0.0
    return len(numerator_tokens & denominator_tokens) / len(denominator_tokens)


def evaluate_rag_output(question, answer, contexts, ground_truth):
    answer_tokens = tokenize(answer)
    question_tokens = tokenize(question)
    context_tokens = tokenize(" ".join(contexts))
    truth_tokens = tokenize(ground_truth)

    faithfulness = lexical_score(context_tokens, answer_tokens)
    answer_relevancy = lexical_score(answer_tokens, question_tokens)
    context_recall = lexical_score(context_tokens, truth_tokens)

    precision_values = []
    for context in contexts:
        chunk_tokens = tokenize(context)
        if chunk_tokens:
            precision_values.append(lexical_score(chunk_tokens, question_tokens | truth_tokens))
    context_precision = sum(precision_values) / len(precision_values) if precision_values else 0.0

    return {
        "faithfulness": round(min(1.0, faithfulness * 2.5), 3),
        "answer_relevancy": round(min(1.0, answer_relevancy * 2.0), 3),
        "context_precision": round(min(1.0, context_precision * 2.0), 3),
        "context_recall": round(min(1.0, context_recall * 2.0), 3),
    }


def main():
    rag = LocalRAGPipeline()
    result = rag.answer("How do input and output guardrails work together?")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
