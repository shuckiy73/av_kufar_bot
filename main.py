from aiogram.methods import DeleteWebhook

from teleg.bot.core import bot_, dp
from teleg.database import init
from teleg.parser.pars_data import schedule

import sys
import logging
import asyncio


async def main():
    await bot_(DeleteWebhook(drop_pending_updates=True))
    init()
    await asyncio.gather(dp.start_polling(bot_), schedule())


def start_dev():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())