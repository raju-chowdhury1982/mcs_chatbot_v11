from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str  # type: ignore
    consignee_code: Optional[str] = Field(
        default=None, description="Normalized consignee code like 0000866"
    )
    container_number: Optional[str] = None  # type: ignore
    po_number: Optional[str] = None  # type: ignore
    ocean_bl_number: Optional[str] = None
    booking_number: Optional[str] = None
    conversation_id: Optional[str] = None


class Citation(BaseModel):
    document_id: str  # type: ignore
    container_number: str


class ChatResponse(BaseModel):
    answer: str  # type: ignore
    citations: List[Citation]
    timing_ms: Dict[str, float]
    debug: Optional[Dict[str, Any]] = None
