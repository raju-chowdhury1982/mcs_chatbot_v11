import os  # type: ignore
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

from app.graph.graph import run_graph
from app.middleware import ConsigneeScopeMiddleware
from app.schemas import ChatRequest, ChatResponse, Citation
from app.settings import settings

app = FastAPI(title="MCS Q&A Chatbot API", version="11.0.0")

app.add_middleware(ConsigneeScopeMiddleware)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.allow_origins.split[","] if settings.allow_origins else ["*"],  # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: Request, body: ChatRequest) -> ChatResponse:
    consignee_code = body.consignee_code or getattr(req.state, "consignee_code", None)
    if not consignee_code:
        raise HTTPException(
            status_code=400,
            detail="Missing consignee_code (header X-Consignee-Code or body)",
        )
    conversation_id = body.conversation_id or str(uuid.uuid4())

    # Security: if user tries to reference a different consignee explicitly in question, block it
    if "(" in (body.question or "") and ")" in body.question:
        # basic guard against code injection - real implementation should be validate extracte vs provided code be more robust
        pass

    result, timings = await run_graph(
        question=body.question,
        consignee_code=consignee_code,
        conversation_id=conversation_id,
    )

    process_response = ChatResponse(
        answer=result.final_answer or "",
        citations=[Citation(**d) for d in result.retrieved],  # type: ignore
        conversation_id=conversation_id,  # type: ignore
        timing_ms=timings,
        debug=result.debug,
        # document_id=d.document_id,
        # container_number=d.container_number,
        # score=d.score,
        # metadata=d.metadata,)
        # for d in result.retrieved
        # for d in result.citations],
        # conversation_id=conversation_id,
        # timing_ms=timings,
        # debug = result.debug
    )

    return process_response


# ============================================================================
"""
async def chat_endpoint(request: Request, chat_request: ChatRequest) -> ChatResponse:
    consignee_code = request.state.consignee_code or chat_request.consignee_code
    if not consignee_code:
        raise HTTPException(status_code=400, detail="Consignee code is required.")

    conversation_id = chat_request.conversation_id or str(uuid.uuid4())
    result_state, timings = await run_graph(
        question=chat_request.question,
        consignee_code=consignee_code,
        conversation_id=conversation_id,
    )

    citations = [
        Citation(
            document_id=d.document_id,
            container_number=d.container_number,
            score=d.score,
            metadata=d.metadata,
        )
        for d in result_state.retrieved
    ]

    return ChatResponse(
        answer=result_state.final_answer or result_state.draft_answer or "",
        citations=citations,
        conversation_id=conversation_id,
        timings=timings,
    )



def main():
    print("Hello from mcs-chatbot!")


if __name__ == "__main__":
    main()
"""
