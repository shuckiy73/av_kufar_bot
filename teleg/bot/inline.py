from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, InputMediaPhoto

from .core import router
from .helpers import return_prefix

from teleg.database import ParsInfo


@router.callback_query(lambda query: query.data.startswith('next_photo'))
async def next_photo_filter(query: CallbackQuery):
    user_id = query.from_user.id
    id_ad, num_caption = [int(i) for i in query.data.split('-')[1:]]  # 200521266 0

    ads = ParsInfo.select().where(ParsInfo.ad_id == id_ad, ParsInfo.user_id == user_id)[0]
    all_photos: str = ads.link_photo.split(' ')

    if len(all_photos) == num_caption+1:
        await query.answer(text='Изображения закончились!')

        return

    await query.answer(text=f'{num_caption+2}-е изображение из {return_prefix(len(all_photos))}')

    await query.message.edit_media(
        InputMediaPhoto(
            media=all_photos[num_caption+1],
            type='photo',
            caption=repr(ads)),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️',
                                         callback_data=f'previous-{ads.ad_id}-{num_caption+1}'),
                    InlineKeyboardButton(text='➡️',
                                         callback_data=f'next_photo-{ads.ad_id}-{num_caption+1}')
                ],
                [InlineKeyboardButton(text='Ссылка на объявление', url=ads.link)]
            ]
        )
    )


@router.callback_query(lambda query: query.data.startswith('previous'))
async def next_photo_filter(query: CallbackQuery):
    user_id = query.from_user.id
    id_ad, num_caption = [int(i) for i in query.data.split('-')[1:]]  # 200521266 0

    ads = ParsInfo.select().where(ParsInfo.ad_id == id_ad, ParsInfo.user_id == user_id)[0]
    all_photos: str = ads.link_photo.split(' ')

    if num_caption-1 < 0:
        await query.answer(text='Это первое изображение!')

        return

    await query.answer(text=f'{num_caption-1}-е изображение из {return_prefix(len(all_photos))}')

    await query.message.edit_media(
        InputMediaPhoto(
            media=all_photos[num_caption-1],
            type='photo',
            caption=repr(ads)),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️',
                                         callback_data=f'previous-{ads.ad_id}-{num_caption-1}'),
                    InlineKeyboardButton(text='➡️',
                                         callback_data=f'next_photo-{ads.ad_id}-{num_caption-1}')
                ],
                [InlineKeyboardButton(text='Ссылка на объявление', url=ads.link)]
            ]
        )
    )
