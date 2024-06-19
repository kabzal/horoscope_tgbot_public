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
Базу данных можете восстановить из файла ```horoscope_db.backup``` с помощью pgAdmin.

После этого запустите ```bot.py```

Админу необходимо через соответствующие команды (прямо через интерфейс бота) загрузить в БД тексты гороскопов. Бот настроен на их рассылку ежедневно в 9 утра. Также админ может добавлять рекламные сообщения (текст + картинка (опционально)) с указанием времени рассылки.
