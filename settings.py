# pyright: reportUnknownVariableType=false

import os  # type: ignore

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(find_dotenv(), override=True)


class Settings(BaseSettings):  # type: ignore
    # Azure OpenAI
    aoai_endpoint: str = Field(env="AZURE_OPENAI_ENDPOINT")  # type: ignore
    aoai_api_key: str = Field(env="AZURE_OPENAI_API_KEY")  # type: ignore
    aoai_api_version: str = Field(default="2024-02-15-preview", env="AZURE_OPENAI_API_VERSION")  # type: ignore
    aoai_chat_deployment: str = Field(env="AZURE_OPENAI_CHAT_DEPLOYMENT")  # type: ignore
    aoai_embed_deployment: str = Field(env="AZURE_OPENAI_EMBED_DEPLOYMENT")  # type: ignore

    # Azure Search
    search_endpoint: str = Field(env="AZURE_SEARCH_ENDPOINT")  # type: ignore
    search_api_key: str = Field(env="AZURE_SEARCH_API_KEY")  # type: ignore
    search_index: str = Field(env="AZURE_SEARCH_INDEX_NAME")  # type: ignore
    search_embed_field: str = Field(default="content_vector", env="AZURE_SEARCH_EMBED_FIELD")  # type: ignore

    # App
    app_log_level: str = Field(default="INFO", env="APP_LOG_LEVEL")  # type: ignore
    allow_origins: str = Field(default="*", env="ALLOW_ORIGINS")  # type: ignore

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
