from fastapi.routing import APIRouter

from config import base_logger
from src.backend.config.routes import UnicornRoutes
from src.backend.handlers.handler_unicorn import UnicornChat

router = APIRouter(prefix=UnicornRoutes.prefix)

unicorn_chat = UnicornChat()


@router.post(UnicornRoutes.chat, tags=["Chat"])
def game_rule_query(user_query: str) -> str:
    base_logger.debug(f"Received : {user_query}")
    result = unicorn_chat.call(
        user_query=user_query,
    )
    base_logger.info(f"Response : {result}")

    return result
