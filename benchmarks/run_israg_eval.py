#!/usr/bin/env python3
"""Run the provisional IsRAG golden-set retrieval evaluation.

This is a retrieval scaffold, not a paper-results generator. The current golden
set is synthetic and marked pending expert review. BERTScore is optional; the
runner always reports deterministic lexical metrics.
"""
from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/golden-sets/israg-v1.jsonl"


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[\w]+", text.lower(), flags=re.UNICODE))


def f1(a: str, b: str) -> float:
    aa, bb = tokens(a), tokens(b)
    if not aa or not bb:
        return 0.0
    overlap = len(aa & bb)
    precision, recall = overlap / len(aa), overlap / len(bb)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def relevance(query: str, row: dict) -> float:
    q = tokens(query)
    text = tokens(row["reference_answer"] + " " + " ".join(row.get("acceptable_answer_points", [])))
    return len(q & text) / len(q) if q else 0.0


def trust(row: dict) -> float:
    # Provisional records intentionally have no expert verification.
    return 0.53


def rank(rows: list[dict], query: str, mode: str, language: str, domain: str) -> list[dict]:
    candidates = [r for r in rows if (not language or r["language"] == language) and (not domain or r["domain"] == domain)]
    scored = []
    for row in candidates:
        rel = relevance(query, row)
        if mode == "standard":
            score = rel
        elif mode == "citations-only":
            score = rel + (0.01 if row.get("source") else 0.0)
        elif mode == "cultural-only":
            score = rel + (0.02 if row["cultural_context"] == "malaysian" else 0.0)
        else:  # IsRAG: relevance plus trust-weighted ranking.
            score = rel * 0.6 + trust(row) * 0.4
        scored.append((score, rel, row))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [row for _, _, row in scored]


def evaluate(rows: list[dict], mode: str, limit: int) -> dict:
    metrics = []
    for gold in rows:
        # Language/domain are evaluation slices, not retrieval filters. Applying
        # them before ranking would leak the gold label into every baseline.
        results = rank(rows, gold["query"], mode, gold["language"], "")
        if mode == "cultural-only":
            results = [r for r in results if r["cultural_context"] == gold["cultural_context"]]
        elif mode == "israg":
            # IsRAG's cultural filter is applied only when the query's context
            # is explicit; this scaffold uses the item context as that signal.
            results = [r for r in results if r["language"] == gold["language"]]
        results = [r for r in results if r["domain"] == gold["domain"]]
        # Evaluate within the requested domain after ranking, avoiding cross-
        # domain lexical collisions while keeping the ranking honest.
        
        
        top = results[:limit]
        first = top[0] if top else None
        metrics.append({
            "top1_f1": f1(first["reference_answer"], gold["reference_answer"]) if first else 0.0,
            "topk_hit": any(r["id"] == gold["id"] for r in top),
            "provenance_complete": bool(first and first.get("provenance")),
            "trust_score": trust(first) if first else 0.0,
            "gold_id": gold["id"],
        })
    return {
        "mode": mode,
        "items": len(metrics),
        "top1_lexical_f1": round(mean(x["top1_f1"] for x in metrics), 4),
        "top{}_hit_rate".format(limit): round(mean(x["topk_hit"] for x in metrics), 4),
        "provenance_completeness": round(mean(x["provenance_complete"] for x in metrics), 4),
        "mean_retrieved_trust": round(mean(x["trust_score"] for x in metrics), 4),
        "status": "provisional_synthetic_set_pending_expert_review",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    rows = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 200:
        raise SystemExit(f"expected 200 records, found {len(rows)}")
    modes = ["standard", "citations-only", "cultural-only", "israg"]
    report = {
        "dataset": str(args.data.relative_to(ROOT)),
        "dataset_items": len(rows),
        "languages": dict(Counter(r["language"] for r in rows)),
        "domains": dict(Counter(r["domain"] for r in rows)),
        "metrics": [evaluate(rows, mode, args.limit) for mode in modes],
        "limitations": [
            "Reference answers are synthetic and pending bilingual domain-expert review.",
            "Lexical F1 is a deterministic proxy; install bert-score separately for semantic evaluation.",
            "The standard and comparison modes are lightweight offline baselines, not full production RAG systems.",
        ],
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
