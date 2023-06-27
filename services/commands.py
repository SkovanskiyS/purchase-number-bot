from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from lexicon.lexicon_RU import LEXICON_COMMANDS_STARTUP


async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command,
    description in LEXICON_COMMANDS_STARTUP.items()]
    await bot.set_my_commands(main_menu_commands)
