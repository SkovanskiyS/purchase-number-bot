from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

menuR_btns = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [
        KeyboardButton("📛Оставить заявку"),
        KeyboardButton("📞Связаться")
    ],
    [
        KeyboardButton("⚙Настройки")
    ],
    [
        KeyboardButton("☎Полезные контакты")
    ]
])