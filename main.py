from aiogram import executor, Dispatcher
import logging

# from handlers import dp
from loader import dp
import handlers
from data.config import ADMIN

logger = logging.getLogger(__name__)


async def send_to_admins(dispatcher: Dispatcher):
    await dispatcher.bot.send_message(chat_id=ADMIN, text="БОТ запущен :)")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    executor.start_polling(dp, on_startup=send_to_admins)
    