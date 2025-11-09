"""_summary_: Simple evaluation of harness about bot performance 
Simple eval: precision@5 for retrieval and hallucination rate.
Prepare a JSON eval set with entries: {question, consignee_code, expected_docs:[document_id,...]}
"""

import json
from statistics import mean
from typing import List

from app.graph.tools.azure_search import hybrid_search


async def precision_at_k(retrieved: List[str], gold: List[str], k: int = 5) -> float:
    if not gold:
        return 1.0
    topk = retrieved[:k]
    inter = len(set(topk) & set(gold))
    return inter / min(k, len(gold))


async def run_eval(path: str):
    with open(path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    p5_scores = []
    halluc_flags = []  # type: ignore

    for c in cases:
        hits = await hybrid_search(c["question"], c["consignee_code"], k=8)
        retrieved_ids = [h["document_id"] for h in hits]
        p5 = await precision_at_k(retrieved_ids, c.get("expected_docs", []), k=5)
        p5_scores.append(p5)  # type: ignore

    # Hallucination proxy: if no retrieved doc overlaps but answer (not computed here) would claim facts → flag.
    halluc_flags.append(0 if set(retrieved_ids[:5]) & set(c.get("expected_docs", [])) else 1)  # type: ignore

    print(
        {
            "precision@5": mean(p5_scores),  # type: ignore
            "hallucination_rate_proxy": mean(halluc_flags),  # type: ignore
        }
    )


if __name__ == "__main__":
    import asyncio
    import sys

    asyncio.run(run_eval(sys.argv[1] if len(sys.argv) > 1 else "./eval/eval_set.json"))
