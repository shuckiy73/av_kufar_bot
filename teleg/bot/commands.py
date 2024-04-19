from .core import *
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot = bot_):
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота."
        ),
        BotCommand(
            command="help",
            description="Как использовать бота?"
        ),
        BotCommand(
            command="all_links",
            description="Список установленных ссылок."
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )