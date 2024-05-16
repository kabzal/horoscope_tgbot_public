from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='start',
                   description='Выбрать или изменить свой знак зодиака'),
        BotCommand(command='help',
                   description='Доступные команды бота'),
        BotCommand(command='info',
                   description='Инфо о боте')]
    await bot.set_my_commands(main_menu_commands)
