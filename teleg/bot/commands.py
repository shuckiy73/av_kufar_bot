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
        ),
        BotCommand(
            command="delete",
            description="Удалить ссылку."
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )