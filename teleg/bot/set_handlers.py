from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F

from .core import router, dp
from .commands import set_commands
from .states import DeleteLink, AddState
from .keyboard import cancel_kb, start_kb
from .helpers import get_links

from teleg.parser.pars_data import first_pars


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await set_commands()
    await message.answer('Доброго времени суток', reply_markup=start_kb())
    await message.answer('✋')
    await message.answer('Нажмите на кнопку: "Добавить ссылку.", чтобы получать свежие уведомления по вашей ссылке')


@router.message(F.text == "Добавить ссылку.")
async def add_link(message: Message, state: FSMContext):
    await message.answer('Пришлите мне ссылку, по которой вы хотите узнавать самые свежие объявления авто.\n'
                         '(ссылка должна начинаться с "https://auto.kufar.by")')
    await state.set_state(AddState.add_id)


@router.message(Command(commands=['delete']))
async def delete_link(message: Message, state: FSMContext):
    await message.answer(
        text='Пришлите мне уникальный ID сылки, которую хотите удалить.',
        reply_markup=cancel_kb()
    )
    await state.set_state(DeleteLink.del_id)


@router.message(Command(commands=['all_links']))
async def get_all_links(message: Message, state: FSMContext):
    await message.answer(
        text='Вот все ваши ссылки в формате : уникальный ID, ваша ссылка',
        reply_markup=start_kb()
    )
    print(get_links(message.chat.id))
