from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

start_dialog = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [
        KeyboardButton("▶Начать"),
        KeyboardButton("❌Завершить")
    ]
])