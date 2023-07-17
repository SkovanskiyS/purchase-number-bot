from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Constructor:
    def create_inline_btn(
            btn: list,
            url=None
    ):
        inlineBtnObject = []
        for i, j in enumerate(btn):
            if len(j) > 1:
                index = len(inlineBtnObject)
                inlineBtnObject.insert(index, [])
                for k in j:
                    for key, value in k.items():
                        inlineBtnObject[index].append(InlineKeyboardButton(
                            text=value, callback_data=key, url=url))
            else:
                for key, value in j[0].items():
                    inlineBtnObject.append([InlineKeyboardButton(text=value, callback_data=key, url=url)])

        return InlineKeyboardMarkup(inline_keyboard=inlineBtnObject)
