from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

phone_number_btn = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [
        KeyboardButton("📱Отправить номер телефона",request_contact=True)
    ]
])


