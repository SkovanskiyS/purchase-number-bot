from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

chatting_btn = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(text='📞Перезвонить мне',callback_data='recall')
    ],
    [
        InlineKeyboardButton(text="📞Свяжитесь со мной в чат-боте",callback_data='chat_with_me')
    ],
    [
        InlineKeyboardButton(
            text="↩Назад",
            callback_data="back_to_menu"
        )
    ]
])

recall_btns = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(text='✅Да',callback_data="yes"),
        InlineKeyboardButton(text='🔙Оставить номер телефона',callback_data="leave_phone")
    ]
])

stop_dialog = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(text="⛔📞Завершить диалог",callback_data='stop_dialog')
    ]
])
