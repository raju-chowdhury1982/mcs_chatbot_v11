import re  # type: ignore

from mcs_chatbot_v11.graph.state import GraphState
from mcs_chatbot_v11.graph.tools.aoai_chat import chat_prompt  # type: ignore

JUDGE_SYSTEM = (
    "You are a strict judge that checks grounding and consistency. "
    "If the draft answer includes facts not directly supported by the provided context, request refinement."
)


async def run(state: GraphState) -> GraphState:  # type: ignore
    if not state.draft_answer:
        return state

    context_refs = "\n\n".join(
        [
            f"[doc:{d.document_id} container:{d.container_number}]\n{d.content[:1200]}"
            for d in state.retrieved[:5]
        ]
    )
    messages = [  # type: ignore
        {"role": "system", "content": JUDGE_SYSTEM},
        {
            "role": "user",
            "content": (
                f"Draft Answer:\n{state.draft_answer}\n\n"
                f"Context:\n{context_refs}\n\n"
                f"Context:\n{context_refs}\n\n"
                f"Draft Answer:\n{state.draft_answer}\n\n"
                "Judge the draft answer for factual grounding and consistency with the context. "
                "If all facts fully grounded and are supported, respond with 'OK'. "
                "If there are unsupported or hallucinated facts, share a short list of issues and what is missing clearly for refinement."
            ),
        },
    ]
    verdict = await chat_prompt(messages, temperature=0.01, max_tokens=500)
    state.debug["judge_verdict"] = verdict
    if verdict.strip().upper().startswith("OK"):  # type: ignore
        state.final_answer = state.draft_answer
        return state

    # Reflective refinement: ask the model to refine using the same context (or trigger re-retrieval heuristics if needed)
    refine_msgs = [  # type: ignore
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},  # type: ignore
        {
            "role": "user",
            "content": (
                f"Context:\n{context_refs}\n\n"
                f"Draft Answer:\n{state.draft_answer}\n\n"
                f"Judge Verdict:\n{verdict}\n\n"
                "Refine the draft answer to address the issues raised in the verdict, using ONLY the provided context. "
                "If information is missing, state that you cannot answer based on the dataset."
            ),
        },
    ]
    refined = await chat_prompt(refine_msgs, temperature=0.01, max_tokens=800)
    state.final_answer = refined
    return state
