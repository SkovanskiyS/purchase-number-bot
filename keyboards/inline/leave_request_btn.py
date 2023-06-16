from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

leave_request_inline = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
         InlineKeyboardButton(
             text="📛Оставить заявку",
             callback_data="request"
         ),
        InlineKeyboardButton(
            text="💡Поделиться предложением",
            callback_data="share"
        ),
    ],
    [
        InlineKeyboardButton(
            text="↩Назад",
            callback_data="back_to_menu"
        )
    ]
])


step_btns = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="▶Пропустить",
            callback_data="skip"
        )
    ],
    [
        InlineKeyboardButton(
            text="↩Назад",
            callback_data="back"
        )
    ]
])

only_back = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(
            text="↩Назад",
            callback_data="back"
        )
    ]
])

