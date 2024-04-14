from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from .core import router
from .helpers import delete_link, get_user
from .keyboard import start_kb

from teleg.parser.pars_data import first_pars


class DeleteLink(StatesGroup):
    del_id = State()

class AddState(StatesGroup):
    add_id = State()


@router.message(F.text == 'Отмена')  # exit the state
async def exit_the_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вурнулись в главное меню.',
        reply_markup=start_kb()
    )
    await state.clear()


@router.message(AddState.add_id, F.text.startswith('https://'))
async def add_link_(message: Message, state: FSMContext):
    get_user(
        id_user=message.from_user.id,
        link=message.text
    )
    await first_pars(url=message.text, user_id=message.from_user.id)

    await message.answer(
        text='Ваша ссылка успешно установлена!',
        reply_markup=start_kb()
    )

    await state.clear()


@router.message(DeleteLink.del_id, F.text)
async def delete_link_(message: Message, state: FSMContext):
    delete_link(user_id=message.from_user.id, unique_id=message.text)
    await message.answer(
        text='Ваша ссылка была успешно удалена!',
        reply_markup=start_kb()
    )
    await state.clear()