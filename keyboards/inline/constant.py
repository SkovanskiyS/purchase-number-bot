from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Constructor:
    def create_inline_btn(
            btn: list,
            url=None,
            web_app=None,
            login_url=None,
            switch_inline_query=None,
            switch_inline_query_current_chat=None,
            switch_inline_query_chosen_chat=None,
            callback_game=None,
            pay=None,
    ):
        inlineBtnObject = []
        for i, j in enumerate(btn):
            if len(j) > 1:
                inlineBtnObject.insert(i, [])
                for k in j:
                    for key, value in k.items():
                        inlineBtnObject[i].append(InlineKeyboardButton(
                            text=key, callback_data=value, url=url,
                            web_app=web_app,
                            login_url=login_url,
                            switch_inline_query=switch_inline_query,
                            switch_inline_query_current_chat=switch_inline_query_current_chat,
                            switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
                            callback_game=callback_game,
                            pay=pay,
                        ))
            else:
                for key, value in j:
                    inlineBtnObject.append([InlineKeyboardButton(text=key, callback_data=value, url=url,
                                                                 web_app=web_app,
                                                                 login_url=login_url,
                                                                 switch_inline_query=switch_inline_query,
                                                                 switch_inline_query_current_chat=switch_inline_query_current_chat,
                                                                 switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
                                                                 callback_game=callback_game,
                                                                 pay=pay, )])

        return InlineKeyboardMarkup(inline_keyboard=inlineBtnObject)
