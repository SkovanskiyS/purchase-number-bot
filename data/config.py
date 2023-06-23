from dataclasses import dataclass
from environs import Env

@dataclass
class Tg_Bot:
    API_TOKEN:str

@dataclass
class Config:
    TgBot: Tg_Bot

def get_config(path:str|None)->Config:
    env = Env()
    env.read_env(path=path)
    bot_token =  env.str("API_TOKEN")
    return Config(TgBot=Tg_Bot(API_TOKEN=bot_token))
