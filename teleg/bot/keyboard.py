from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from teleg.database import ParsInfo


def start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ссылку.")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
        )


def get_flag_ikb(item: ParsInfo):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️',
                                     callback_data=f'previous-{item.ad_id}-{0}'),
                InlineKeyboardButton(text='➡️',
                                     callback_data=f'next_photo-{item.ad_id}-{0}')
             ],
            [InlineKeyboardButton(text='Ссылка на объявление', url=item.link)]
        ]
    )