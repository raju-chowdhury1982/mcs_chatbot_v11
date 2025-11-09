import re
from typing import Dict, Optional

from app.graph.state import GraphState

# more generalized patterns for various IDs are required here
ID_PATTERN = {
    "container_number": r"\b([A-Z]{4}\d{7})\b",
    "po_number": r"\b\d{8,}\b",
    "ocean_bl_number": r"\b[A-Z0-9]{6,}\b",
    "booking_number": r"\b[A-Z0-9]{6,}\b",
}

PAREN_CODE = re.compile(r"\((\d{6,})\)")


def extract_consignee_code_key(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    m = PAREN_CODE.search(raw)
    return m.group(1) if m else None


def run(state: GraphState) -> GraphState:
    q = state.question.strip()
    identifiers: Dict[str, Optional[str]] = {k: None for k in ID_PATTERNS}  # type: ignore

    for name, pat in ID_PATTERNS.items():  # type: ignore
        m = re.search(pat, q, flags=re.I)  # type: ignore
        if m:
            identifiers[name] = m.group(1)

    # Normalize consignee code key
    if state.consignee_code and state.consignee_code.isdigit():  # type: ignore
        ckey = state.consignee_code  # type: ignore
    else:
        # If a human name+code string was passed, attempt to parse (best-effort)
        ckey = extract_consignee_code_key(state.consignee_code or "")  # type: ignore

    state.identifiers = identifiers
    state.debug["consignee_code_key"] = ckey

    # If no identifiers and the question obviously needs one, we can mark for clarification
    needs_identifier = any(
        w in q.lower() for w in ["status of", "where is", "track"]
    ) and not any(identifiers.values())
    if needs_identifier:
        state.intent = "clarify_identifier"
    return state
