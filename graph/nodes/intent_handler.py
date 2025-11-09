from app.graph.state import GraphState

INTENTS = {  # type: ignore
    "status": ["status", "where is", "track", "milestone"],  # benchmark achievement
    "eta_window": [
        "arriving",
        "next",
        "eta",
        "coming",
    ],  # estimated time of arrival @dport from */origin/load_port
    "eta_window_delivery": [
        "arriving",
        "next",
        "eta",
        "coming",
    ],  # estimated time of arrival for delivery @fd/in-dc/dc
    "delay_reason": [
        "delay",
        "delayed",
        "late",
        "early",
    ],  # reason for delay/early arrival
    "priority_handling": [
        "priority",
        "urgent",
        "hot",
    ],  # hot containers/pos/obls handler
    "route": [
        "route",
        "port",
        "origin",
        "destination",
        "transshipment",
        "discharge",
    ],  # route information
    "sustainability": ["co2", "carbon", "footprint"],  # sustainability information
    "transport_options": [
        "options",
        "transport",
        "delivery",
        "in-dc",
        "fd",
    ],  # transport/delivery options
    "mode": ["mode", "modes", "sea", "rail", "road", "air"],  # transport modes
    "generic_freetext": [],
}

# next, within,

DURATION_INTENTS = {
    -30: ["last month", "30 days ago", "one month ago"],
    -15: ["last 15 days", "15 days ago", "half month ago", "last fortnight"],
    -7: ["last week", "7 days ago", "one week ago"],
    -1: ["last day", "yesterday", "1 day ago", "one day ago"],
    0: ["today", "current day"],
    1: ["next day", "tomorrow", "1 day", "one day"],
    3: ["in 3 days", "three days", "next 3 days"],
    7: ["in a week", "one week", "7 days"],
}  # type: ignore


def classify_intent(question: str) -> str:
    q_lower = question.lower()
    for intent, keywords in INTENTS.items():  # type: ignore
        if any(keyword in q_lower for keyword in keywords):  # type: ignore
            return intent
    return "generic_freetext"


def run(state: GraphState) -> GraphState:  # type: ignore
    if state.intent == "clarify_identifier":
        return state
    state.intent = classify_intent(state.question)  # type: ignore
    return state  # type: ignore
