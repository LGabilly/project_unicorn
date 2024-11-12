import json

from elasticsearch import Elasticsearch
from tqdm import tqdm

from config import base_settings
from src.models.gameRule import GameRule

els = Elasticsearch(base_settings.ES_BASE_URL)


def load_example_rules():
    with open(base_settings.DATA_DIR / "example_rules.json", "r") as f:
        data = json.loads(f.read())

    GameRule._index.delete(ignore_unavailable=True, using=els)
    GameRule.init(using=els)

    for data in tqdm(data, desc="Indexing documents..."):
        doc = GameRule(game_name=data["game_name"], content=data["content"])  # type: ignore
        doc.save(using=els)

    GameRule._index.refresh(using=els)


if __name__ == "__main__":
    load_example_rules()
