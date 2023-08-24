import asyncio
import random
from aiogram import Bot
import datetime
from sql_requests.sql_user import show_users, show_user_znak, show_goroscop, show_pic
from html import escape

rus_znaks = {'oven': 'Овен',
             'telec': 'Телец',
             'bliznecy': 'Близнецы',
             'rak': 'Рак',
             'lev': 'Лев',
             'deva': 'Дева',
             'vesy': 'Весы',
             'skorpion': 'Скорпион',
             'strelec': 'Стрелец',
             'kozerog': 'Козерог',
             'vodolei': 'Водолей',
             'ryby': 'Рыбы'}

async def prepare_today_goroscop(bot: Bot):
    list_of_users = [i['user_id'] for i in (await show_users())]

    for user in list_of_users:
        user_znak = await show_user_znak(user_id=user)
        txt_goroscops = await show_goroscop()
        pics = await show_pic()
        txt_goroscop = str(random.choice(txt_goroscops)).replace("<Record txt_goroscop='", '').replace("'>", '')
        pic = str(random.choice(pics)).replace("<Record pic_id='", '').replace("'>", '')
        try:
            await bot.send_photo(chat_id=user, photo=pic, caption=f'Ваш знак зодиака: <b>{rus_znaks[user_znak]}</b>\n\n<b>Гороскоп на сегодня:</b>\n{escape(txt_goroscop)}')
        except:
            continue

async def send_today_goroscop(bot: Bot):
    while True:
        offset = datetime.timezone(datetime.timedelta(hours=3))
        now = datetime.datetime.now(offset)
        if now.hour == 9 and now.minute == 0:
            await prepare_today_goroscop(bot=bot)
        await asyncio.sleep(60)
