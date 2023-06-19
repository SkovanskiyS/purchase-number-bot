from aiogram import Bot,Dispatcher,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import BOT_TOKEN
from utils.dp_api.sqlite import Database

storage = MemoryStorage()
bot = Bot(token=str(BOT_TOKEN), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage=storage)
db = Database()

