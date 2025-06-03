from aiogram.filters import CommandStart
from loguru import logger
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.dispatcher.router import Router

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


# @user_router.message("update_id")
# async def cmd_test(message: Message):

#     await message.answer(invoice)
#     await message.answer(
#         f"amount: {invoice.amount}, asset:{invoice.asset}, invoice_id:{invoice.invoice_id}"
#     )
