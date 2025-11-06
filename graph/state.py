from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field  # type: ignore


class RetrievalDoc(BaseModel):
    document_id: str  # type: ignore
    container_number: str  # type: ignore
    content: str
    score: float
    metadata: Optional[Dict[str, Any]] = None


class GraphState(BaseModel):
    question: str  # type: ignore
    consignee_codes: Optional[str]  # type: ignore
    identifiers: Dict[str, Optional[str]] = {}
    intent: Optional[str] = None
    retrieved: List[RetrievalDoc] = []
    draft_answer: Optional[str] = None
    final_answer: Optional[str] = None
    citations: List[Dict[str, str]] = []
    debug: Dict[str, Any] = {}
