from environs import Env
from dataclasses import dataclass


@dataclass
class DataBase:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class TgBot:
    BOT_TOKEN: str
    ADMINS: list


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase


def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env()
    BOT_TOKEN = env.str('BOT_TOKEN')
    ADMINS = list(map(int, env.list('ADMINS')))
    DATABASE = env.str('DATABASE')
    DB_HOST = env.str('DB_HOST')
    DB_USER = env.str('DB_USER')
    DB_PASSWORD = env.str('DB_PASSWORD')

    return Config(tg_bot=TgBot(BOT_TOKEN=BOT_TOKEN, ADMINS=ADMINS), db=DataBase(
        database=DATABASE, db_host=DB_HOST, db_user=DB_USER, db_password=DB_PASSWORD
    ))



