from elasticsearch_dsl import Document, Text


class GameRule(Document):
    game_name = Text()
    content = Text()

    class Index:
        name = "game-rule"
