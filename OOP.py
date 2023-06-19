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


class Teacher:
    def __init__(self):
        self.__name = 'Jahon'
        self.__surname = 'Masharipov'
        self.__age = 1

    @property
    def get_age(self):
        return self.__age

    @get_age.setter
    def set_age(self, age):
        if 70 > age >= 18:
            self.__age = age
            print('Welcome To UZB PORN')
        elif 60 < age > 70:
            print('BOBO NMA QVOSIZ BRAT')
        else:
            print('You are too young to watch porn videos')

    @staticmethod
    def whatismyname(self):
        pass


class Person2:
    def __init__(self, age, name, iq):
        self.__is_genius = None
        self.__age = age
        self.__name = name
        self.__iq = iq

    def is_genius(self):
        return self.__is_genius

    def check_iq(self):  # setter
        if self.__iq < 100:
            self.__is_genius = False
        else:
            self.__is_genius = True


class Employee:
    def __init__(self, name):
        self.__name = name

    def who_am_i(self):
        print('my name is ' + self.__name)


class Person:
    def __init__(self):
        self.__sex = None

    @property
    def get_sex(self):
        return self.__sex

    @get_sex.setter
    def set_gender(self, sex):
        self.__sex = sex


class ITSpecialist(Employee, Person):
    def __init__(self, name):
        super().__init__(name)


class Animals:
    def __init__(self, type):
        self.__type = type

    @property
    def type(self):
        return self.__type

    def return_type(self):
        print('Type of animal: ' + self.__type)


class Tiger(Animals):
    def __init__(self, type, sound):
        super().__init__(type)
        self.__sound = sound

    @property
    def sound(self):
        return self.__sound

    def return_type(self):
        super().return_type()
        print('i do ' + self.__sound)
        print()

