from aiogram import executor
from loader import db,bot


async def start_up(_):
    print('Bot is running')

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp,skip_updates=True,on_startup=start_up)
