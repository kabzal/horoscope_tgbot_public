import asyncpg
from config_data.config import Config, load_config

config: Config = load_config()
user = config.db.user
password = config.db.password
database = config.db.database
host = config.db.host

#Запрос для проверки наличия юзера в БД
async def check_user(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    check = await conn.fetchrow('''SELECT EXISTS (SELECT * FROM users WHERE user_id=$1)''', user_id)
    await conn.close()
    return str(check)

#Запрос для внесения юзера в БД
async def create_user(user_id, znak):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO users (user_id, znak)'''
                       '''VALUES ($1, $2)''', user_id, znak)
    await conn.close()

#Запрос для изменения знака юзера в БД
async def change_user(user_id, znak):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''UPDATE users SET znak=$2 WHERE user_id=$1''', user_id, znak)
    await conn.close()

#Запрос для вывода списка юзеров
async def show_users():
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    all_users = await conn.fetch('''SELECT user_id FROM users''')
    await conn.close()
    return all_users

#Запрос для вывода знака зодиака юзера
async def show_user_znak(user_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    user_znak = await conn.fetchval('''SELECT znak FROM users WHERE user_id=$1''', user_id)
    await conn.close()
    return user_znak

#Запрос для вывода рандомного текста по ЗЗ
async def show_goroscop():
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    txt = await conn.fetch('''SELECT txt_goroscop FROM goroscops''')
    await conn.close()
    return txt

#Запрос для выводы рандомного фото по ЗЗ
async def show_pic():
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    pic = await conn.fetch('''SELECT pic_id FROM pics''')
    await conn.close()
    return pic


#Запрос для внесения данных по текстам в БД
async def create_txt(txt_goroscop):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO goroscops (txt_goroscop)'''
                       '''VALUES ($1)''', txt_goroscop)
    await conn.close()


#Запрос для внесения картинок в БД
async def create_pic(pic_id):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO pics (pic_id)'''
                       '''VALUES ($1)''', pic_id)
    await conn.close()


#Запрос для внесения данных по рекламе в БД
async def create_ad(ad_text, ad_url, ad_pic, ad_datetime):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''INSERT INTO ads (ad_text, ad_url, ad_pic, ad_datetime)'''
                       '''VALUES ($1, $2, $3, $4)''', ad_text, ad_url, ad_pic, ad_datetime)
    await conn.close()

#Запрос для выгрузки текущего списка реклам
async def show_ads(datetime):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    ads = await conn.fetch('''SELECT ad_text, ad_url, ad_pic FROM ads WHERE ad_datetime=$1''', datetime)
    await conn.close()
    return ads

#Запрос для удаления рекламы из БД
async def delete_ad(ad_datetime):
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host)
    await conn.execute('''DELETE FROM ads WHERE ad_datetime=$1''', ad_datetime)
    await conn.close()