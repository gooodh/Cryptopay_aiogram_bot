from aiogram.filters import CommandStart
from loguru import logger
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router

from bot.config import cp
user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        user = message.from_user.username

        message_text = f"<b>👋 Привет, {user}!</b>"
        await message.answer(message_text)

    except Exception as e:
        logger.error(
            f"Ошибка при выполнении команды /start для пользователя {message.from_user.id}: {e}"
        )
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже."
        )


@user_router.message(Command("test"))
async def cmd_test(message: Message):
    logger.info("Получен запрос на создание инвойса.")
    user_id = message.from_user.id
    invoice = await cp.create_invoice(
        amount="1", asset="USDT", payload=str(user_id)
    )
    await message.answer(f"Payment: {invoice.bot_invoice_url}")
    await message.answer(
        f"Amount: {invoice.amount}, Asset: {invoice.asset}, Invoice ID: {invoice.invoice_id}"
    )
