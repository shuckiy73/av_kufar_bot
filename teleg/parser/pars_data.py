import json
import datetime
from json import loads
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml

from .helpers_pars import create_first_data, headers
from teleg.database import ParsInfo, Users
from teleg.bot.core import bot_
from teleg.bot.keyboard import get_flag_ikb


async def first_pars(url, user_id) -> None:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')
    mass = []

    parsed = soup.find('script', id='__NEXT_DATA__')
    parsed_text = parsed.text
    parsed_json: dict = loads(parsed_text)
    ads = parsed_json['props']['initialState']['listing']['ads']
    for item in ads:
        mass.append(item['ad_id'])

    create_first_data(user_id, mass)


async def get_result_parser(url, user_id):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')

    parsed = soup.find('script', id='__NEXT_DATA__')
    parsed_text = parsed.text
    parsed_json: dict = loads(parsed_text)
    ads = parsed_json['props']['initialState']['listing']['ads']
    pattern = '%Y-%m-%dT%H:%M:%S'

    result_mass = []
    name, cre, crca, rgd, crg = '', '', '', '', ''
    for ad in ads:
        __id = ad['ad_id']
        _select = ParsInfo.select().where(ParsInfo.ad_id == __id)
        if _select.exists():
            continue

        time_publish = datetime.datetime.strptime(ad['list_time'][:-1], pattern)
        link_photo = []
        link = ad['ad_link']

        city_ = ''
        name_ = ''

        price = 'Договорная' if int(ad['price_usd']) == 0 else ad['price_usd'][:-2]

        for ac_param in ad['account_parameters']:
            try:
                if len(ad['account_parameters']) == 1:
                    name = ac_param['v']
                else:
                    if ac_param['p'] == 'contact_person':
                        name = ac_param['v']
            except ValueError:
                name = 'Имя продавца не найдено.'

        for item in ad['ad_parameters']:
            if item['p'] == 'regdate':
                rgd = item['v']
            elif item['p'] == 'cars_engine':
                cre = item['vl']
            elif item['p'] == 'cars_capacity':
                crca = item['vl']
            elif item['p'] == 'cars_gearbox':
                crg = item['vl']
            elif item['pl'] == 'Марка':
                name_ += item['vl']
            elif item['pl'] == 'Модель':
                name_ += f" / {item['vl']}"
            elif item['pl'] == 'Область':
                city_ += item['vl']
            elif item['pl'] == 'Город / Район':
                city_ += f" / {item['vl']}"

        for img in ad['images']:
            link_photo.append(f'https://rms.kufar.by/v1/gallery/{img["path"]}')

        if len(link_photo) == 0:
            link_photo.append(
                'https://avatars.mds.yandex.net/i?id=8f3d7581c4b4cef65478bc2e72c193a7-5233567-images-thumbs&n=13'
            )

        time_publish += datetime.timedelta(hours=3)

        per = ParsInfo.create(user=user_id,
                              ad_id=__id,
                              seller=name,
                              link_photo=' '.join(link_photo),
                              link=link,
                              time_publish=time_publish,
                              price_car=price,
                              car_name=name_,
                              city=city_,
                              cre=cre,
                              crca=crca,
                              rgd=rgd,
                              crg=crg,
                              )

        result_mass.append(per)

    return result_mass


async def send_ads(user_id: int, items: list):
    for item in items:
        text = repr(item)
        all_photos = item.link_photo.split(' ')

        await bot_.send_photo(
            chat_id=user_id,
            photo=all_photos[0],
            caption=text,
            reply_markup=get_flag_ikb(item=item)
        )

        await asyncio.sleep(0.5)


async def schedule():
    while True:
        await asyncio.sleep(2)
        select_: list[Users] = Users.select()

        for item in select_:
            user_id = item.user_id
            item = await get_result_parser(url=item.pars_link, user_id=user_id)

            if isinstance(item, list) and len(item) >= 1:
                await send_ads(
                    user_id=user_id,
                    items=item
                )

            await asyncio.sleep(0.5)


# asyncio.run(get_result_parser("https://auto.kufar.by/l/cars/audi"))