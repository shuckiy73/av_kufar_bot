from peewee import (
    TextField,
    BigIntegerField,
    Model,
    IntegerField,
    SqliteDatabase,
    ForeignKeyField,
    BooleanField,
    DateTimeField
)
from aiogram.utils.markdown import hbold, hitalic

from pathlib import Path
from os import getcwd

path = Path(getcwd()).joinpath('database_kufar.db')
db = SqliteDatabase(path)
print(path)


def send_text(string: str) -> str:
    arr = string.split()
    if len(arr) <= 75:
        return string
    return f"{' '.join(arr[:80])} ...(остальное на сайте)"


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    unique_id = TextField(null=True, unique=True, primary_key=True)
    user_id = BigIntegerField(unique=False)
    pars_link = TextField(null=True)


class ParsInfo(BaseModel):
    user = ForeignKeyField(Users)
    ad_id = BigIntegerField(default=0, null=True)
    seller = TextField(default='', null=True)
    link_photo = TextField(default='', null=True)
    link = TextField(default='', null=True)
    time_publish = DateTimeField(null=True)
    price_car = TextField(default='Договорная.', null=True)
    city = TextField(default='Неуказан.', null=True)
    car_name = TextField(default='', null=True)
    cre = TextField(default='', null=True)
    crca = TextField(default='', null=True)
    rgd = TextField(default='', null=True)
    crg = TextField(default='', null=True)
    descr = TextField(default='', null=True)

    def __repr__(self):
        return \
            f'''{f'{hitalic("Марка/Модель")}:  {hbold(self.car_name)}.'}\n\n''' \
            f'''{f'{hitalic("Продавец")}:  {hbold(self.seller)}.' if self.seller else 'Имя не указано.'}\n\n''' \
            f"{hitalic('Дата публикации объявления')}: \n" \
            f"{hbold(self.time_publish)}.\n\n" \
            f'''{f'{hitalic("Область/Город")}:  {hbold(self.city)}.'}\n\n''' \
            f'''{hitalic(f"Стоимость авто:")}  {hbold(self.price_car+' USD')}.\n\n''' \
            f'{hitalic("Другая информация:  ")}' \
            f'{hbold(self.cre)}, {hbold(self.crca)}, {hbold(self.rgd)}, {hbold(self.crg)}.\n\n' \
            f'{hitalic("Описание:  ")}{hbold(send_text(str(self.descr)))}'


def init():
    Users.create_table(safe=True)
    ParsInfo.create_table(safe=True)