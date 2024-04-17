from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .core import router_admin
from teleg.parser.pars_data import first_pars

import os


ADMIN_ID = int(os.getenv('ADMIN_ID'))


@router_admin.message(F.text == "Добавить юзера👨‍👩‍👦‍👦")
async def add_link(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Wait...')


@router_admin.message(F.text)
async def add_link(message: Message):
    if message.from_user.id == ADMIN_ID:
        user_id, url = message.text.split()
        await first_pars(url, user_id, admin=True)
        await message.answer('added')