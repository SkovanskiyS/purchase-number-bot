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
    degree = 'High degree'
    unversity = 'Amity'

    def teach(self):
        print('i am teaching')


parveen = Teacher()
jahongir = Teacher()
print(parveen.degree)
parveen.teach()