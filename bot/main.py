import asyncio
from contextlib import asynccontextmanager

from loguru import logger
from fastapi import FastAPI, Request
from aiogram.types import Update
from aiogram.exceptions import TelegramRetryAfter

from bot.bot_utils import start_bot, stop_bot
from bot.config import settings, dp, bot


@asynccontextmanager
async def lifespan(app: FastAPI):

    await start_bot()
    webhook_url = settings.hook_url
    try:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != webhook_url:
            await bot.set_webhook(
                url=webhook_url,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True,
            )
            logger.success(f"Вебхук установлен: {webhook_url}")
        else:
            logger.info("Вебхук уже установлен, повторная установка не требуется.")
    except TelegramRetryAfter as e:
        logger.warning(
            f"Ошибка установки вебхука: {e}. Повторная попытка через {e.retry_after} секунд."
        )
        await asyncio.sleep(e.retry_after)
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")

    yield
    await stop_bot()



app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Not Found"}, 404


@app.post("/cryptopay")
async def webhook(request: Request) -> None:
    logger.info(f"Получен запрос: {await request.json()}")
    try:
        logger.info("Получен запрос с вебхука.")
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        logger.info("Обновление успешно обработано.")
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления: {e}")
