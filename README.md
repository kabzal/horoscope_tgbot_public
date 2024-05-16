# Бот для рассылки гороскопов

Можете скачать себе данный репозиторий с помощью ```git clone```

Установите виртуальное коружение командой:
```python -m venv venv```

...и активируйте его:
```venv\scripts\activate```

После этого установите нужные зависимости из файла requirements.txt с помощью команды:
```pip install -r requirements.txt```

Для работы бота вам необходимо создать в папке проекта файл .env , в котором будут чувствительные конфигуционные данные: 
токен телеграм-бота, полученный от BotFather, данные для подключения к БД PostgreSQL (имя пользователя, пароль, название БД, хост - БД необходимо создать предварительно), а также телеграм-id админов бота, например:

```
BOT_TOKEN = '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXabcdefghijklmnopqrstuvw'
user = 'tgbot_admin'
password = 'tgbot_admin_psw'
database = 'horoscope_db'
host = 'localhost'
ADMIN_ID = '123456, 654321'
```

После этого запустите bot.py

Админу необходимо через соответствующие команды (прямо через интерфейс бота) загрузить в БД тексты гороскопов. Бот настроен на их рассылку ежедневно в 9 утра.

В базе данных необходимо создать следующие таблицы:

* users (поля user_id, где будут храниться телеграм-id пользователей; znak, где будет храниться выбранный ими знак в виде строки);

* goroscops (поле txt_goroscop, которое будет содержать текст предсказаний)

* pics (поле pic_id, где будут храниться id загруженных админом изображений)

* ads (поля: ad_text для хранения текста рекламного сообщения; ad_url для хранения рекламной ссылки; ad_pic для хранения загруженного id картинки для рекламы; ad_datetime для хранения даты и времени рассылки рекламного сообщения)
