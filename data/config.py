from pathlib import Path

from environs import Env
from dataclasses import dataclass


@dataclass
class FiveSimAPI:
    API_KEY: str


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
class I18N:
    I18N_DOMAIN: str
    BASE_DIR = Path(__file__).parent
    LOCALES_DIR = BASE_DIR / 'locales'


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase
    api: FiveSimAPI
    i18n: I18N


def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env()
    BOT_TOKEN = env.str('BOT_TOKEN')
    I18N_DOMAIN = env.str('I18N_DOMAIN')
    API_KEY = env.str('API_KEY')
    ADMINS = list(map(int, env.list('ADMINS')))
    DATABASE = env.str('DATABASE')
    DB_HOST = env.str('DB_HOST')
    DB_USER = env.str('DB_USER')
    DB_PASSWORD = env.str('DB_PASSWORD')

    return Config(tg_bot=TgBot(BOT_TOKEN=BOT_TOKEN, ADMINS=ADMINS), db=DataBase(
        database=DATABASE, db_host=DB_HOST, db_user=DB_USER, db_password=DB_PASSWORD
    ), api=FiveSimAPI(API_KEY=API_KEY), i18n=I18N(I18N_DOMAIN=I18N_DOMAIN))
