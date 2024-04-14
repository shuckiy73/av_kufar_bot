from teleg.database import ParsInfo


def create_first_data(user_id, data):
    for id in data:
        ParsInfo.get_or_create(
            user_id=user_id,
            ad_id=id
        )


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36'
}