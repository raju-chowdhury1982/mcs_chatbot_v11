from collections import defaultdict, deque
from typing import Deque, Dict, List, Tuple

# Simple in-memory summary + window memory (will replace with Redis for prod- after discussion with BalaramDa!!!)


class MemoryStore:
    def __init__(self, max_turns: int = 8):
        self.store: Dict[str, Deque[Tuple[str, str]]] = defaultdict(
            lambda: deque(maxlen=max_turns)
        )
        self.summaries: Dict[str, str] = {}

    def append(self, conversation_id: str, role: str, text: str):
        self.store[conversation_id].append((role, text))

    def window(self, conversation_id: str) -> List[Tuple[str, str]]:
        return list(self.store[conversation_id])

    def get_summary(self, conversation_id: str) -> str:
        return self.summaries.get(conversation_id, "")

    def set_summary(self, conversation_id: str, text: str):
        self.summaries[conversation_id] = text


memory_store = MemoryStore()
