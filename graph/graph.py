import asyncio
import time

from langgraph.graph import END, StateGraph  # type: ignore

from mcs_chatbot_v11.graph.nodes import (display_handler, execution_handler,
                                         intent_handler, judge_reflection,
                                         query_handler)
from mcs_chatbot_v11.graph.state import GraphState
from mcs_chatbot_v11.memory.memory_store import memory_store


# Edges logic
def needs_clarification(state: GraphState) -> bool:
    return state.intent == "clarify_identifier"


async def app_graph() -> StateGraph:  # type: ignore
    sg = StateGraph(GraphState)

    sg.add_node("query_handler", lambda s: query_handler.run(s))  # type: ignore
    sg.add_node("intent_handler", lambda s: intent_handler.run(s))  # type: ignore
    sg.add_node("execution_handler", lambda s: asyncio.run(execution_handler.run(s)))  # type: ignore
    sg.add_node("judge_reflection", lambda s: asyncio.run(judge_reflection.run(s)))  # type: ignore
    sg.add_node("display_handler", lambda s: display_handler.run(s))  # type: ignore

    sg.set_entry_point("query_handler")

    sg.add_edge("query_handler", "intent_handler")
    sg.add_conditional_edges("intent_handler", lambda s: "display_handler" if needs_clarification(s) else "execution_handler")  # type: ignore
    sg.add_edge("execution_handler", "judge_reflection")
    sg.add_edge("judge_reflection", "display_handler")
    sg.add_edge("display_handler", END)

    return sg


async def run_graph(question: str, consignee_code: str, conversation_id: str):
    state = GraphState(question=question, consignee_code=consignee_code)  # type: ignore

    # Memory window
    state.debug["memory_window"] = memory_store.window(conversation_id)

    g = await app_graph()  # type: ignore
    app = g.compile()  # type: ignore

    t0 = time.perf_counter()
    result: GraphState = app.invoke(state)  # type: ignore
    t1 = time.perf_counter()

    # Update memory
    memory_store.append(conversation_id, "user", question)
    memory_store.append(
        conversation_id, "assistant", result.final_answer or result.draft_answer or ""
    )

    timings = {"total_ms": (t1 - t0) * 1000}
    return result, timings
