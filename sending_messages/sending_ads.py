import asyncio
from aiogram import Bot
import datetime
from sql_requests.sql_user import show_ads, show_users, delete_ad


async def create_ad(bot: Bot):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(offset)
    formatted_now = datetime.datetime.strftime(now, '%d.%m.%Y %H:%M')
    list_of_ads = await show_ads(formatted_now)
    if list_of_ads:
        list_of_users = [i['user_id'] for i in (await show_users())]
        for ad in list_of_ads:
            if ad['ad_pic'] == 'no_pic':
                for user in list_of_users:
                    try:
                        await bot.send_message(chat_id=user, text=f'{ad["ad_text"]}\n\nСсылка: {ad["ad_url"]}')
                    except:
                        continue
            else:
                for user in list_of_users:
                    try:
                        await bot.send_photo(chat_id=user, photo=ad['ad_pic'], caption=f'{ad["ad_text"]}\n\nСсылка: {ad["ad_url"]}')
                    except:
                        continue
        await delete_ad(ad_datetime=formatted_now)


async def send_ad(bot: Bot):
    while True:
        await create_ad(bot=bot)
        await asyncio.sleep(60)
