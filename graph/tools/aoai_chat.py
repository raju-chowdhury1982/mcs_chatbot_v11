from openai import AzureOpenAI

from app.settings import settings

_client = AzureOpenAI(
    api_key=settings.aoai_api_key,
    api_version=settings.aoai_api_version,
    azure_endpoint=settings.aoai_endpoint,
)


async def chat_prompt(messages, temperature: float = 0.0, max_tokens: int = 1000):  # type: ignore
    resp = _client.chat.completions.create(
        model=settings.aoai_chat_deployment,
        messages=messages,  # type: ignore
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content


async def embed(text: str):
    resp = _client.embeddings.create(
        model=settings.aoai_embed_deployment,
        input=text,
    )
    return resp.data[0].embedding
