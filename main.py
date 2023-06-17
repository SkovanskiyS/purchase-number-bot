# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.dispatcher.filters import Command
# import logging
#
# API_TOKEN = '1355012700:AAGZAeq9HihUdmwhbb_R-y-uMMgu4N0PJg4'
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
#
# @dp.message_handler(Command('help'))
# async def echo(message: types.Message):
#     await message.answer(message.text)
#
#
# @dp.message_handler(Command('start'))
# async def replier(message: types.Message):
#     await message.reply('My name is chiki')
#
#
# executor.start_polling(dp, skip_updates=True)


# class Teacher:
#     def __init__(self):
#         self.__name = 'Jahon'
#         self.__surname = 'Masharipov'
#         self.__age = 1
#
#     @property
#     def get_age(self):
#         return self.__age
#
#     @age.setter
#     def set_age(self, age):
#         if 70 > age >= 18:
#             self.__age = age
#             print('Welcome To UZB PORN')
#         elif 60 < age > 70:
#             print('BOBO NMA QVOSIZ BRAT')
#         else:
#             print('You are too young to watch porn videos')
#
#     @staticmethod
#     def whatismyname(self):
#         pass
#
#
# teacher = Teacher()


class Person:
    def __int__(self, age, name, iq):
        self.__age = age
        self.__name = name
        self.__iq = iq

    def is_genius(self):
        return self.__is_genius

    def set_iq(self, iq):
        if iq < 100:
            self.__is_genius = 0
        else:
            self.__is_genius = 1


baxti = Person(18, 'Baxtiyor',75)
baxti.is_genius()




