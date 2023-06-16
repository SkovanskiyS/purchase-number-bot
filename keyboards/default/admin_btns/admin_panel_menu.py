from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [
        KeyboardButton("📤Рассылка"),
        KeyboardButton("📜Все пользователи🔎")
    ],
    [
        KeyboardButton("🚫Заблокировать"),
        KeyboardButton("✅Разблокировать")
    ]
])