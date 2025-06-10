from loguru import logger

from bot.users.schemas import Update
from bot.config import bot


async def payment_processor(data: dict) -> None:

    update = Update(**data)

    invoice_id = update.payload.invoice_id
    amount = update.payload.amount
    asset = update.payload.asset
    user_id = update.payload.payload

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
