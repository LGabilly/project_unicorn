from pydantic import BaseModel

from config import base_logger
from src.models.localLLM import GEMMA
from src.models.searchEngine import ENGINE


class UnicornChat(BaseModel):
    def call(self, user_query: str) -> str:
        docs: list[str] = ENGINE.syntaxic_search_rules(user_query)  # Retrieval
        base_logger.debug(f"{docs=}")
        res = GEMMA.call(query=user_query, docs=docs)  # Generativ
        return res
