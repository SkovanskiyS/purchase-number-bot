from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

setting_inline_btn = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(text="🛠Поменять имя",callback_data="change_name"),
        InlineKeyboardButton(text="🛠Сменить номер",callback_data="change_number")
    ],
    [
        InlineKeyboardButton(
            text="↩Назад",
            callback_data="back_to_menu"
        )
    ]
])

