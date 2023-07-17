from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Constructor:
    def create_btn(
            btn: list
    ):
        keyBoardsBtnObject = []
        for i, j in enumerate(btn):
            if len(j) > 1:
                keyBoardsBtnObject.insert(i, [])
                for k in j:
                    keyBoardsBtnObject[i].append(KeyboardButton(
                        text=k
                    ))
            else:
                keyBoardsBtnObject.append([KeyboardButton(text=j[0]
                                                          )])

        return ReplyKeyboardMarkup(keyboard=keyBoardsBtnObject, resize_keyboard=True)
