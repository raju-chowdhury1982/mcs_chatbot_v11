from typing import Any, Dict, List

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorQuery
from mcs_chatbot_v11.settings import settings

from .aoai_chat import embed

_client = SearchClient(
    endpoint=settings.search_endpoint,
    index_name=settings.search_index,
    credential=AzureKeyCredential(settings.search_api_key),
)


async def hybrid_search(
    query: str, consignee_code_key: str, k: int = 10
) -> List[Dict[str, Any]]:

    # Vector for hybrid scoring
    vec = await embed(query)
    vq = VectorQuery(vector=vec, k=k, fields=settings.search_embed_field)

    # Strict consignee filter
    filter_expr = f"consignee_code_key eq '{consignee_code_key}'"

    results = _client.search(  # type: ignore
        search_text=query,
        vector_queries=[vq],
        filter=filter_expr,
        query_type="simple",  # BM25 + vector
        select=["document_id", "container_number", "content", "metadata"],
    )

    out = []
    for r in results:  # type: ignore
        out.append(  # type: ignore
            {  # type: ignore
                "document_id": r["document_id"],
                "container_number": r.get("container_number"),  # type: ignore
                "content": r["content"],
                "metadata": r.get("metadata", {}),  # type: ignore
                "score": r.get("@search.score", 0.0),  # type: ignore
            }
        )
    return out  # type: ignore
