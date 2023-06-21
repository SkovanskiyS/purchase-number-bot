from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Constructor:
    def create_btn(
            btn: list,
            request_user=None,
            request_chat=None,
            request_contact=None,
            request_location=None,
            request_poll=None,
            web_app=None
    ):
        keyBoardsBtnObject = []
        for i, j in enumerate(btn):
            print(j[i])
            if len(j) > 1:
                keyBoardsBtnObject.insert(i, [])
                for k in j:
                    keyBoardsBtnObject[i].append(KeyboardButton(text=k, request_contact=request_contact))
            else:
                keyBoardsBtnObject.append([KeyboardButton(text=j[i], request_contact=request_contact)])
        print(keyBoardsBtnObject)

        return ReplyKeyboardMarkup(keyboard=keyBoardsBtnObject, resize_keyboard=True)
