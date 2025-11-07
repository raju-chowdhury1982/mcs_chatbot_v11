from typing import List

from mcs_chatbot_v11.graph.nodes.query_handler import \
    run as query_handler_run  # type: ignore
from mcs_chatbot_v11.graph.state import GraphState, RetrievalDoc
from mcs_chatbot_v11.graph.tools.aoai_chat import chat_prompt  # type: ignore
from mcs_chatbot_v11.graph.tools.azure_search import hybrid_search

SYSTEM_INSTRUCTIONS = (
    "You are a shipment QA assistant. Answer ONLY using the provided documents. "
    "If unavailable, say you cannot answer from the dataset. Always include citations as [doc: <document_id>, container: <container_number>]."
)


def _to_messages(state: GraphState, draft: bool = False) -> List[dict]:  # type: ignore
    msgs = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        # {"role": "user", "content": state.question},
    ]
    for role, text in state.debug.get("memory_window", []):
        msgs.append({"role": role, "content": text})

    msgs.append({"role": "user", "content": state.question})
    if draft and state.retrieved:
        # Provide top retrieved documents as context snippets
        snippets = "\n\n".join(  # type: ignore
            [
                f"[doc: {d.document_id} Container Number: {d.container_number}]\nContent: {d.content}"
                for d in state.retrieved[:5]
            ]
        )
        msgs.append({"role": "system", "content": f"Context:\n{snippets}"})
    return msgs


async def run(state: GraphState) -> GraphState:
    ckey = state.debug.get("consignee_code_key")
    if not ckey:
        state.draft_answer = (
            "Can not show the container as consignee code did not match."
        )
        return state

    # Retrieve [hybrid] from the question, run the query handler to extract identifiers

    hits = await hybrid_search(state.question, consignee_code_key=ckey, k=10)
    state.retrieved = [
        RetrievalDoc(
            document_id=h["document_id"],
            container_number=h.get("container_number"),  # type: ignore
            content=h["content"],
            score=h["score"],
            metadata=h.get("metadata", {}),
        )
        for h in hits
    ]

    # Draft answer with provided context
    draft = await chat_prompt(
        _to_messages(state, draft=True), temperature=0.02, max_tokens=800
    )
    state.draft_answer = draft

    # Extract provisional citations by regex fallbacks
    cits: List[dict] = []  # type: ignore
    for d in state.retrieved[:5]:
        cits.append({"document_id": d.document_id, "container_number": d.container_number or ""})  # type: ignore
        state.citations = cits
    return state

    # state = query_handler_run(state)

    # if state.intent == "clarify_identifier":
    #     state.final_answer = "Could you please provide a container number, PO number, or other identifier for your shipment?"
    #     return state

    # # Perform hybrid search using extracted identifiers
    # id_values = [v for v in state.identifiers.values() if v]
    # if id_values:

    # else:
    #     state.retrieved = []

    # # Generate draft answer using retrieved documents
    # draft_msgs = _to_messages(state, draft=True)
    # draft_response = await chat_prompt(draft_msgs)
    # state.draft_answer = draft_response["content"]

    # # Generate final answer
    # final_msgs = _to_messages(state, draft=False)
    # final_response = await chat_prompt(final_msgs)
    # state.final_answer = final_response["content"]

    # # Extract citations from the final response (simple heuristic)
    # citations = []
    # for doc in state.retrieved:
    #     if f"doc: {doc.document_id}" in state.final_answer:
    #         citations.append({
    #             "document_id": doc.document_id,
    #             "container_number": doc.container_number,
    #         })
    # state.citations = citations

    # return state
