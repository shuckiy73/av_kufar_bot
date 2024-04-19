import asyncio
import json

import requests
from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup
import lxml
from pprint import pprint
import datetime


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
    'Accept': '*/*',
    'Cookie': 'lang=ru; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX19U4ONPcJ573t5jKjJe4tTwfnps7WymHh4GNj1BiOw4yAItscxEYbA2by2jOFcRsbambR%2BY7mqhtHfEN21yMiNVmVNSqOkzBWCGjorrVfPY6MQMRa4Jn6fs; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FJ8qFBm8rc890gGaoKQmIQvbL8%2BqFijxA%3D; _ym_uid=1686675951727172833; tmr_lvid=5bc3101dd650ac40b70298bb77e3a3a9; tmr_lvidTS=1686675951392; fullscreen_cookie=1; _hjSessionUser_2040951=eyJpZCI6ImY3MGU3N2ZiLTU2NmYtNWU0OS1hMzQ3LWQyNzc5NWEwNjkyYSIsImNyZWF0ZWQiOjE2ODY2NzU5NTE0NTIsImV4aXN0aW5nIjp0cnVlfQ==; mindboxDeviceUUID=0f2bdfcd-b5d3-4c87-86b6-b708d5ec31c1; directCrm-session=%7B%22deviceGuid%22%3A%220f2bdfcd-b5d3-4c87-86b6-b708d5ec31c1%22%7D; _pulse2data=d492ca55-9800-40f4-82a3-877410d4d66d%2Cv%2C%2C1686747614974%2CeyJpc3N1ZWRBdCI6IjIwMjMtMDYtMTNUMTc6MDU6NDhaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..DIiDMqmUtYX4la7n-ZLU4g.zpEs1sEWgF3vb4_H4W4RV096JUz4pfJYHqPchCtdS36xaOsH3zygwFckApOWiZtHmp47kwY6wi0gHtSvBaWHO8FaSXKa47_CUVTUgfulzEdvkdUb-deWBJ2rKMRb5SePBCxhH-qFLXZaGH3AWnC0W4qtash3oGCXGioePp8rVdvJBI5sWtNUoMJcEPEUVzYfRt4sUXIEYQUbL9Mi0_DM9A.11H0_amiT3NV0boL6Nq3yQ%2C0%2C1686761114974%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..i2fG3vElWoVMKzToIJmOeVgQ4mFXWONlryeWReG0ApM; kuf_SA_subscribe_user_attention=1; _ym_d=1704918893; _fbp=fb.1.1704918895459.982426883; _gcl_au=1.1.1955840774.1713041135; web_push_banner_listings=3; web_push_banner_auto=3; kuf_auth_last_login_type=google; _ga=GA1.3.2143074030.1686675949; kufar-mb-check-name_6006867=1; kuf_agr={%22advertisements%22:true%2C%22advertisements-non-personalized%22:false%2C%22statistic%22:true%2C%22mindbox%22:true}; kufar-test-variant-web-ab-top-header-v1=edca2cfb-6100-43fb-b8e5-3c664dc9d89a__1; _gid=GA1.2.755533813.1713543183; kuf_SA_BookingPromoMay24=1; _ym_isad=2; domain_sid=UZouHFEs3Ru7kQec-oQLz%3A1713553235862; _ym_visorc=w; _gid=GA1.3.755533813.1713543183; kuf_auth_last_logins=[{%22accountId%22:%226006867%22%2C%22name%22:%22%D0%9A%D0%BE%D0%BD%D0%BE%D0%BD%D0%B5%D1%86%20%D0%95%D0%B3%D0%BE%D1%80%22%2C%22login%22:%22egorkononec64@gmail.com%22%2C%22loginType%22:%22google%22}]; KUF_SUGGESTER_SHOW_2_ITERATION=1; _gat_UA-64831541-3=1; __gads=ID=e59f7798469f14c4:T=1686675953:RT=1713555186:S=ALNI_MaMO3y0CV847NlQ84TdfKVo8XS5Yw; __gpi=UID=00000c2f6fb5e79e:T=1686675953:RT=1713555186:S=ALNI_MZYZhHU2Lp-Z_6coQg_u2YGAQksMg; __eoi=ID=7b6347145ae65c43:T=1713041139:RT=1713555186:S=AA-Afjby7MFNQOqb-Fi04NMPQ3Yp; kufar_cart_id=899b45d0-2ebe-4023-a6c5-cfbb6a7dc839; _ga_WLP2F7MG5H=GS1.1.1713553235.91.1.1713555219.23.0.0; _ga_D1TYH5F4Z4=GS1.1.1713553235.17.1.1713555219.23.0.0; kuf_oauth_st=821e5665-34ab-4ae7-a8a2-0e8eeda92384; kuf_oauth_nonce=6757f366-e92a-4433-8c7b-a939ced5a3d2; tmr_detect=0%7C1713555224954; rl_session=RudderEncrypt%3AU2FsdGVkX1%2FBj4VrwkcQ07CI3M2pcZFcB1wJsjIGdr7cdtomoTOBzonV%2B3zWECInqcqpoTWnsvjUT50gHo6kEFIJpvVvmHMd2815feFBM8Z3FekFNxbu9aReh%2BZPabSBb%2FiI8%2Fzj0J%2F1w5n7%2FjOXdw%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2FqA6%2B5A5y0KPW%2BPDQ1CHISYZ7JtdMrUiw%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2FuQ4gIXTk%2BgVbCQik2gbKUPErDco0ayIc%3D; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2Fjqf5ZupQEZmphXKorh1RfNC2pe5YrWOY%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2FX%2BHf5i59YsS1t%2BnuB9fPy6Oqh4qjFLAc%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX19v4KgwMmlBArM34cbINIimkucXibBUgDSj1CYgj51vugZ5vvTpjzjQH%2FUszbWRK%2BxznZ1LBHubeg%3D%3D; kuf_oauth_received_state=821e5665-34ab-4ae7-a8a2-0e8eeda92384; kuf_oauth_received_data={"token":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjZjZTExYWVjZjllYjE0MDI0YTQ0YmJmZDFiY2Y4YjMyYTEyMjg3ZmEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzODU4OTQyMDcyOTgtNXFtbGo0cXBnNGRyb2RsNnMzaXJjMjd1M20zNDA4MTMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzODU4OTQyMDcyOTgtNXFtbGo0cXBnNGRyb2RsNnMzaXJjMjd1M20zNDA4MTMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDM3MTIzMTMzNDA5MDMwMzkyNDAiLCJlbWFpbCI6ImVnb3Jrb25vbmVjNjRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5vbmNlIjoiNjc1N2YzNjYtZTkyYS00NDMzLThjN2ItYTkzOWNlZDVhM2QyIiwibmJmIjoxNzEzNTU0OTI3LCJuYW1lIjoi0JXQs9C-0YAg0JrQvtC90L7QvdC10YYiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSi1fcDMxM1JaWTVZRVlsX0xuYjZIRWJvU2tTdmhNSTlSMElYMFI5aVIzNjBwbjNzams9czk2LWMiLCJnaXZlbl9uYW1lIjoi0JXQs9C-0YAiLCJmYW1pbHlfbmFtZSI6ItCa0L7QvdC-0L3QtdGGIiwiaWF0IjoxNzEzNTU1MjI3LCJleHAiOjE3MTM1NTg4MjcsImp0aSI6ImMyN2JiZTA5YTJmODY5ZDY4ZDI4NjA5N2I3MjRmYWZiOTQ2ZDliY2QifQ.d9cbj2Po9S-j_go9B6mHRw2TXvlWRTum5oosoh3jkyHVkI51WuHTB7M2Hx6KzmlZdSk9gs-Oyap8Wc_gy1I5pRV6OaAPZ8dsZ4YoXU5uNRUZRPvNdWFn2QmMCUc2kC8J64NgfrLnl5U_imoJcBd9Tb2ZeN-r7ZBs31R5vJazDSX5klJr3JTTTID72Br3vcifKDM4Wx__2o7bAM-Z4AYSxMTzAeZhdVZEOpc3gIpK4DmABsfkWYpTbkJrRRyDB9DWuJPrunwLwdvJuX03e8xEpmw_kHUodfR8i2K8Oq34iICKN_HOHs3MwW5G3ASARZey7PaT9uH2KxMrq755kt_nuw"}; _ga=GA1.1.2143074030.1686675949; _ga_QTFZM0D0BE=GS1.1.1713553231.16.1.1713555229.16.0.0; _ga_4DSS63YZ2R=GS1.1.1713554488.2.1.1713555229.0.0.0'
    # 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6InYyMCIsInNjaHYiOiIyIiwidHlwIjoiSldUIn0.eyJhaWQiOiI2MDA2ODY3IiwiY2FkIjpmYWxzZSwiZGlkIjoiOTljOWFkZTM2YWQ4MTM3ODI1NTFkMzgzYjMwOWUzZjgiLCJleHAiOjE3NDU2OTUyOTYsImlhdCI6MTcxMzU1NDQ5NiwianRpIjoiNjAwNjg2NzpERFNtQm5iOCIsInB0ciI6ZmFsc2UsInR5cCI6InVzZXIifQ.RScmy05koUAFLf0fKmJqlcxNq6VAntbODYd'
}


# async def get_phone_av(url):
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(url) as response:
#             soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')
#
#     parsed = soup.find('script', id='__NEXT_DATA__')
#     parsed_text = parsed.text
#     parsed_json: dict = json.loads(parsed_text)
#     # dirty_phone = parsed_json['props']['initialState']
#
#     with open('ads.json', 'w', encoding='utf-8') as f:
#         json.dump(parsed_json, f, ensure_ascii=False, indent=4)
#
#     return soup.select_one('div.styles_description_content__raCHR').text, 1
#
# asyncio.run(get_phone_av('https://auto.kufar.by/vi/cars/232036958?searchId=a8ad45cc561accde8396c02a854fe074d48c'))

# response = requests.post(
#     'https://auto.kufar.by/react/api/login/v2/auth/signin/google',
#     headers=headers
# )

from random import choices
print(choices(['💣', '🧨']))