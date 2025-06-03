import os
from typing import List

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    PORT: int
    HOST: str
    BASE_URL: str
    ADMIN_IDS: List[int]
    CRYPTOPAY_TOKEN: str
    FORMAT_LOG: str = (
        "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    LOG_ROTATION: str = "10 MB"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    @property
    def hook_url(self) -> str:
        """Возвращает URL вебхука"""
        return f"{self.BASE_URL}/cryptopay"


# Получаем параметры для загрузки переменных среды
settings = Settings()

# Инициализируем бота и диспетчер
bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

PORT = settings.PORT
HOST = settings.HOST
BASE_URL = settings.BASE_URL
WEBHOOK_PATH = "/cryptopay"
CRYPTOPAY_TOKEN = settings.CRYPTOPAY_TOKEN
admins = settings.ADMIN_IDS
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log")
logger.add(
    log_file_path,
    format=settings.FORMAT_LOG,
    level="INFO",
    rotation=settings.LOG_ROTATION,
)
