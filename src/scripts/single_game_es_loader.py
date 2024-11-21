import json

from elasticsearch import Elasticsearch
from tqdm import tqdm

from config import base_settings
from src.models.gameRule import GameRule

els = Elasticsearch(base_settings.ES_BASE_URL)


def load_example_rules(game_name: str):
    with open(base_settings.DATA_DIR / f"{game_name}.json", "r") as f:
        data = json.loads(f.read())

    # GameRule._index.delete(ignore_unavailable=True, using=els)
    GameRule.init(using=els)

    for data_line in tqdm(data, desc="Indexing documents..."):
        doc = GameRule(
            game_name=data_line["game_name"],  # type: ignore
            content=data_line["content"],  # type: ignore
            breadcrumb=data_line["breadcrumb"],  # type: ignore
        )
        doc.save(using=els)

    GameRule._index.refresh(using=els)


if __name__ == "__main__":
    load_example_rules("seven_wonders")
