import asyncio
from contextlib import asynccontextmanager

from loguru import logger
from fastapi import FastAPI, Request
from aiogram.types import Update
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import Message
from aiogram.filters import Command


from aiosend import CryptoPay, TESTNET
from aiosend.webhook import FastAPIManager
from aiosend.types import Invoice

from bot.bot_utils import start_bot, stop_bot
from bot.config import settings, dp, bot, CRYPTOPAY_TOKEN

invoices_storage = {}


# https://monstrously-charming-marlin.cloudpub.ru/handler
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

cp = CryptoPay(
    CRYPTOPAY_TOKEN,
    # webhook_manager=FastAPIManager(app, "/handler"),
    network=TESTNET,
)
# @cp.webhook()
# async def handler(invoice: Invoice) -> None:
#     update_data = invoice
#     logger.info(f"Получен сырой запрос на /handler: {update_data}")
    

@app.post("/handler")
async def post_webhok_handler(request: Request) -> None:
    update_data = await request.json()
    logger.info(f"Получен сырой запрос на /handler: {update_data}")
    try:
        logger.info("Получен запрос с вебхука /handler.")
        # Проверяем, содержит ли запрос ожидаемые поля для CryptoPay
        if (
            isinstance(update_data, dict)
            and "update_type" in update_data
            and update_data["update_type"] == "invoice_paid"
        ):
            payload = update_data["payload"]
            invoice_id = payload["invoice_id"]
            amount = payload["amount"]
            asset = payload["asset"]
            user_id = invoices_storage.get(invoice_id)
            logger.info(
                f"Инвойс {invoice_id} был оплачен. Сумма: {amount} {asset}. user_id: {user_id}"
            )
            if user_id:
                await bot.send_message(
                    user_id,
                    f"Ваш инвойс {invoice_id} был оплачен. Сумма: {amount} {asset}.",
                )
                logger.info(f"Уведомление отправлено пользователю {user_id}.")
            else:
                logger.warning(
                    f"user_id не найден для invoice_id {invoice_id}. Уведомление не отправлено."
                )
        else:
            # Проверяем, является ли запрос Telegram-обновлением
            if isinstance(update_data, dict) and "update_id" in update_data:
                logger.info("Обработка Telegram-обновления.")
                update = Update.model_validate(update_data, context={"bot": bot})
                await dp.feed_update(bot, update)
                logger.info("Обновление Telegram успешно обработано.")
            else:
                logger.warning(
                    f"Получен некорректный запрос: {update_data}. Игнорируем."
                )
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления на /handler: {e}")
        # Возвращаем HTTP-ответ, чтобы избежать 500 Internal Server Error
        return {"status": "error", "message": str(e)}, 400

@app.get("/")
async def root():
    return {"message": "Not Found"}, 404


@dp.message(Command("test"))
async def cmd_test(message: Message):
    logger.info("Получен запрос на создание инвойса.")
    invoice = await cp.create_invoice(amount="1", asset="USDT")
    # Сохраняем invoice_id и user_id
    invoices_storage[invoice.invoice_id] = message.from_user.id
    await message.answer(f"Payment: {invoice.bot_invoice_url}")
    await message.answer(
        f"Amount: {invoice.amount}, Asset: {invoice.asset}, Invoice ID: {invoice.invoice_id}"
    )


@app.post("/cryptopay")
async def webhook(request: Request) -> None:
    update_data = await request.json()
    logger.info(f"Получен сырой запрос на /cryptopay: {update_data}")
    try:
        logger.info("Получен запрос с вебхука /cryptopay (Telegram).")
        if isinstance(update_data, dict) and "update_id" in update_data:
            update = Update.model_validate(update_data, context={"bot": bot})
            await dp.feed_update(bot, update)
            logger.info("Обновление Telegram успешно обработано.")
        else:
            logger.warning(f"Некорректный запрос на /cryptopay: {update_data}. Игнорируем.")
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления на /cryptopay: {e}")
        return {"status": "error", "message": str(e)}, 400
