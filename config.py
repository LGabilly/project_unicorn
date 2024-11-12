import sys
from pathlib import Path

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    ES_BASE_URL: str = "http://elasticsearch:9200"
    PROJ_NAME: str = "Project Unicorn"
    PROJ_DIR: Path = Path(__file__).parent
    SRC_DIR: Path = PROJ_DIR / "src"
    DATA_DIR: Path = PROJ_DIR / "data"
    NB_DIR: Path = PROJ_DIR / "notebooks"
    ASSET_DIR: Path = PROJ_DIR / "assets"
    TEMPLATE_DIR: Path = ASSET_DIR / "templates"
    BENCHMARK_DIR: Path = ASSET_DIR / "benchmarks"


base_settings = Settings()


class LogSettings(BaseSettings):
    LOG_LEVEL: str = Field(default="DEBUG")
    LOG_FORMAT: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
    )
    LOG_FILE: str = Field(default="logs/app.log")
    LOG_ROTATION: str = Field(default="10 MB")  # Rotate after 10MB
    LOG_RETENTION: str = Field(default="10 days")  # Keep logs for 10 days
    LOG_COMPRESSION: str = Field(default="zip")  # Compress old logs with zip


def configure_logger():
    settings = LogSettings()

    # Remove any default logger configuration
    logger.remove()

    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
    )

    logger.add(
        settings.LOG_FILE,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression=settings.LOG_COMPRESSION,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
    )
    return logger


# The sexy logger
base_logger = configure_logger()
