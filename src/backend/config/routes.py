from enum import Enum, unique


@unique
class UnicornRoutes(str, Enum):
    prefix = "/v1/unicorn"
    chat = "/chat"
