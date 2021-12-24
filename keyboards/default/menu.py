from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📈Cредний чек номера"),
            KeyboardButton(text="✉️Еженедельная Рассылка"),
        ],
        [
            KeyboardButton(text="🏨Проанализировать конкурентов"),
        ],
    ],
    resize_keyboard=True
)

back_to_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙Главное меню"),
        ],
    ],
    resize_keyboard=True
)