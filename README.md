# mcs_chatbot_v11

# project details:
# chatbot based on BYOD
# service required as follows: azure blobservice, ai-search, open-ai
# orchestration done with: langchain-minor and langgraph-major

## Flow of query to answers are as follows:

flowchart TD
UI[Streamlit UI] -->|/chat| API[FastAPI]
API --> MW[ConsigneeScopeMiddleware]
MW --> G[LangGraph]


subgraph LangGraph
QH[Query Handler\n(normalize + extract IDs + parse consignee)] --> IH[Intent Handler]
IH -->|clarify| DH[Display Handler]
IH -->|else| EXE[Execution Handler\n(Azure Search hybrid)]
EXE --> J[JUDGE\nCorrective]
J -->|OK| DH
J -->|Issues| REF[Reflective Refine]
REF --> DH
end


EXE -->|needs more| EXE


G --> RESP[Answer + Citations]
RESP --> API


# Shipment Q&A Bot (LangGraph + Azure)


## 1) Setup
- Python 3.11
- `cp .env.example .env` and fill values
- `pip install -r requirements.txt`


## 2) Indexing
- Put your BYOD JSONL at `./data/shipments.jsonl`
- `python indexing/index_jsonl_to_azure_search.py ./data/shipments.jsonl`


## 3) Run API
- `uvicorn app.main:app --reload --port 8000`


## 4) Run Streamlit
- `streamlit run frontend/streamlit_app.py`


## Notes
- All queries are filtered by `consignee_code_key` to enforce tenant-style isolation.
- The LangGraph implements Corrective (judge) + Reflective (refine) RAG.
- Every answer includes citations like `[doc: <document_id>, container: <container_number>]`.