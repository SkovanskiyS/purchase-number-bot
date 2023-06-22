from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', 'Launch a bot'),
            BotCommand('help', 'Support 25/8')
        ],
        scope=BotCommandScopeDefault
    )
