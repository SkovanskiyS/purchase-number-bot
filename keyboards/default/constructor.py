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
            if len(j) > 1:
                keyBoardsBtnObject.insert(i, [])
                for k in j:
                    keyBoardsBtnObject[i].append(KeyboardButton(
                        text=k, request_user=request_user, request_chat=request_chat, request_location=request_location,
                        request_contact=request_contact,request_poll=request_poll,web_app=web_app
                    ))
            else:
                keyBoardsBtnObject.append([KeyboardButton(text=j[0],
                                                          request_user=request_user, request_chat=request_chat,
                                                          request_location=request_location,
                                                          request_contact=request_contact, request_poll=request_poll,
                                                          web_app=web_app
                                                          )])

        return ReplyKeyboardMarkup(keyboard=keyBoardsBtnObject, resize_keyboard=True)
