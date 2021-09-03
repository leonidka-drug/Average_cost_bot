from aiogram import executor

from loader import bot
from data.config import ADMINS


async def send_to_admins(dispatcher):
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text="БОТ запущен :)", )


async def on_shutdown(dispatcher):
    await bot.close()


async def on_startup(dispatcher):
    await send_to_admins(dispatcher)


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)