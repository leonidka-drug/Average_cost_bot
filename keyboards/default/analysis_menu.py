from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

analysis_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Использовать старый URL"),
        ],
        [
            KeyboardButton(text="🔙Главное меню"),
            KeyboardButton(text="♻️Обновить URL"),
        ],
    ],
    resize_keyboard=True
)