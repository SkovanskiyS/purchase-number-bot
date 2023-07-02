from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery


# class HandleProcessData(BaseMiddleware):
#     async def on_process_callback_query(self, call: CallbackQuery, data: dict):
#         user_id = call.from_user.id
#         user_name = call.from_user.username
#         user_first_name = call.from_user.first_name
#         user_last_name = call.from_user.last_name
#         user_language = lang[1]
#         user_data = dict(
#             id=user_id,
#             username=user_name,
#             firstName=user_first_name,
#             lastName=user_last_name,
#             language=user_language
#         )
#         data['userInfo'] = user_data
