from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Посмотреть средний чек номера"),
            KeyboardButton(text="Подписаться на рассылку"),
        ],
        [
            KeyboardButton(text="Проанализировать канкурентов"),
        ],
    ],
    resize_keyboard=True
)
