from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold

from .core import router, dp
from .commands import set_commands
from .states import DeleteLink, AddState
from .keyboard import cancel_kb, start_kb
from .helpers import get_links

from teleg.parser.pars_data import first_pars


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await set_commands()
    await message.answer(f'{hbold("Доброго времени суток")}', reply_markup=start_kb())
    await message.answer('✋')
    await message.answer('Нажмите на кнопку: "Добавить ссылку.", чтобы получать свежие уведомления по вашей ссылке')


@router.message(F.text == "Добавить ссылку.")
async def add_link(message: Message, state: FSMContext):
    await message.answer('Пришлите мне ссылку, по которой вы хотите узнавать самые свежие объявления авто.\n'
                         '(ссылка должна начинаться с "https://auto.kufar.by")',
                         reply_markup=cancel_kb()
                         )
    await state.set_state(AddState.add_id)


@router.message(Command(commands=['delete']))
async def delete_link(message: Message, state: FSMContext):
    await message.answer(
        text=f'Пришлите мне {hbold("уникальный ID")} сылки, которую хотите удалить.\n'
             f'Просто нажмите на {hbold("уникальный ID")} и он автоматически скопируется, '
             f'вам останется просто отправить его в бот.',
        reply_markup=cancel_kb()
    )
    await state.set_state(DeleteLink.del_id)


@router.message(Command(commands=['all_links']))
async def get_all_links(message: Message, state: FSMContext):
    all_links = get_links(message.chat.id)
    send_text = 'Вот все ваши ссылки в формате : \n\nуникальный ID\nваша ссылка'
    if len(all_links) == 0:
        send_text = 'У вас нет сохранённых ссылок(\nЧтобы добавить ссылку, нажмите на кнопку - "Добавить ссылку."'

    await message.answer(
        text=send_text,
        reply_markup=start_kb(),
    )
    for item in all_links:
        await message.answer(
            text=f'`{item[0]}`\n{item[1]}',
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True
        )


@router.message(Command(commands=['help']))
async def delete_link(message: Message, state: FSMContext):
    await message.answer(
        text=f'Команда /start - {hbold("запустит бота.")}\n'
             f'Команда /all_links - {hbold("выведет список сохранённых ссылок.")}\n'
             f'Команда /delete - {hbold("удалит выбранную вами ссылку.")}\n'
             f'''Чтобы установить ссылку, нажмите на кнопку - "{hbold('Добавить ссылку.')}"\n''',
        reply_markup=start_kb()
    )
