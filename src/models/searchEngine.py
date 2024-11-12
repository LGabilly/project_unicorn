from typing import Self

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from pydantic import BaseModel, ConfigDict, model_validator

from config import base_logger, base_settings
from src.helpers.query_builder import all_rules_query


class SearchEngine(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: Elasticsearch | None = None

    @model_validator(mode="after")
    def _force_client(self) -> Self:
        base_logger.debug(base_settings.ES_BASE_URL)
        self.client = Elasticsearch(base_settings.ES_BASE_URL)
        return self

    def syntaxic_search_rules(self, query: str, top_k: int = 5) -> list[str]:
        s = Search(using=self.client, index="game-rule")
        s.query(all_rules_query())
        response = s.execute()
        res: list[str] = []
        for hit in response:
            content = hit.to_dict().get("content")
            if content is not None:
                res.append(content)
        return res


ENGINE = SearchEngine()


if __name__ == "__main__":
    res = ENGINE.syntaxic_search_rules("azer", 5)
    print(res)
