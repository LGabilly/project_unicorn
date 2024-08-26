from pydantic import BaseModel


class UnicornChat(BaseModel):
    def call(self, user_query: str) -> dict:
        return {"ok": user_query}
