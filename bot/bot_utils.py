from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger
from bot.users.handlers.user_pivate import user_router
from bot.config import bot, dp, settings


async def set_commands():
    commands = [
        BotCommand(command="start", description="▶️ Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def notify_admins(message):
    try:
        for admin in settings.ADMIN_IDS:
            await bot.send_message(admin, text=message)
            logger.info(f"Отправка сообщения администратору: {admin}")
    except Exception as e:
        logger.error(f"Ошибка при отправки сообщения администратору {admin}: {e}")


async def start_bot():
    try:
        await set_commands()
        dp.include_router(user_router)

        await notify_admins("Я запущен🥳.")
        logger.info("Бот успешно запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


async def stop_bot():
    await notify_admins("Бот остановлен. За что?😔")
    logger.info("Бот успешно остановлен.")
