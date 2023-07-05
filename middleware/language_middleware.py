from typing import Tuple, Any, Optional

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from data.config import load_config, Config
from database.dbApi import DB_API
from aiogram import types, Dispatcher


async def get_lang(user_id):
    db_api = DB_API()
    db_api.connect()
    lang = db_api.get_current_language(user_id)
    if lang:
        return lang[0]
    return None


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale


def setup_middleware():
    config: Config = load_config('../.env')
    i18n = ACLMiddleware(config.i18n.I18N_DOMAIN, config.i18n.LOCALES_DIR)
    #dp.middleware.setup(i18n)
    return i18n

