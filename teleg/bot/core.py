from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode

from os import getenv

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()

bot_ = Bot(
    token=getenv('TOKEN_API'),
    parse_mode=ParseMode.HTML
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router=router)