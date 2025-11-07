from app.graph.state import GraphState  # type: ignore

TEMPLATE = "{answer}\n\n" "Citations:\n" "{cit_lines}"


def run(state: GraphState) -> GraphState:  # type: ignore
    answer = state.final_answer or state.draft_answer or "I couldn't draft an answer."  # type: ignore
    cit_lines = "\n".join(
        [
            f"- [doc: {c['document_id']}, container: {c['container_number']}]"
            for c in state.citations  # type: ignore
        ]
    )
    state.final_answer = TEMPLATE.format(answer=answer, cit_lines=cit_lines)  # type: ignore
    return state  # type: ignore
