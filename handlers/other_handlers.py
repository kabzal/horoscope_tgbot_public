from aiogram import Router
from aiogram.types import Message

router: Router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer('Прошу прощения, я вас не понимаю. Вы можете ознакомиться со списком доступных команд с помощью /help')
