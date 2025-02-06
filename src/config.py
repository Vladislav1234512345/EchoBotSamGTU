from pydantic_settings import BaseSettings, SettingsConfigDict
from src.container import BASE_DIR
import logging


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO

    model_config = SettingsConfigDict(case_sensitive=True)


class BotSettings(BaseSettings):
    BOT_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "env/bot/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class WebSettings(BaseSettings):
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/webhook"
    WEB_HOST: str
    WEB_PORT: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "env/web/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


bot_settings = BotSettings()  # type: ignore
web_settings = WebSettings()  # type: ignore
logging_settings = LoggingSettings()  # type: ignore
