from aiogram import executor
from loader import db,bot
from utils import notify_admins,set_bot_commands


async def start_up(_):
    await notify_admins.notify_on_startup(dp)
    await set_bot_commands.set_commands(dp)
    try:
        db.create_table_user()
    except Exception as err:
        print(err)
   # db.delete_users()

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp,skip_updates=True,on_startup=start_up)

