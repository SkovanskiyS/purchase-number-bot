from config import BOT_TOKEN,ADMIN_ID
from aiogram import Bot,Dispatcher,executor
import asyncio

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot,loop=loop)

if __name__ == '__main__':
    from handlers import dp,send_to_admin
    executor.start_polling(dp,on_startup=send_to_admin)



