from typing import Callable, Dict, Any, Awaitable

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message


class TestMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update, data):
        print('pre process')

    async def on_process_update(self, update: types.Update, data: dict):
        print('on process update')
