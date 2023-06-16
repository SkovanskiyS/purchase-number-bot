from environs import Env
import os

env = Env()
env.read_env()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = env.list("ADMINS")
REQUEST_CHAT_ID = str(os.getenv("REQUEST_CHAT_ID"))
ADMIN_CHAT_ID = str(os.getenv("ADMIN_CHAT_ID"))

