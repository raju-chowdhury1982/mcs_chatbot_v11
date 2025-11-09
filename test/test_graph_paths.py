from app.graph.nodes import intent_handler, query_handler
from app.graph.state import GraphState


def test_clarify_path():
    s = GraphState(question="what is the status of my container?", consignee_code="0000866")  # type: ignore
    s = query_handler.run(s)
    s = intent_handler.run(s)
    assert s.intent in ("clarify_identifier", "status")
