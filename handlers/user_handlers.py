import random
from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from keyboards.user_kb import znaki_kb, info_kb
from sql_requests.sql_user import show_goroscop, show_pic, check_user, create_user, change_user
from html import escape

router: Router = Router()

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


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Добро пожаловать в мир астрологии и предсказаний!\n'
                         'Я здесь, чтобы помочь тебе исследовать тайны звезд и найти ответы на вопросы о будущем. '
                         'Получай увлекательные прогнозы на каждый день. Давай вместе раскроем завесу загадок!\n\n'
                         'Выберите свой знак зодиака: 👇', reply_markup=znaki_kb)


@router.callback_query(Text(text='back_to_znaks'))
async def process_start_again_command(message: Message):
    await message.answer(text='Добро пожаловать в мир астрологии и предсказаний!\n'
                         'Я здесь, чтобы помочь тебе исследовать тайны звезд и найти ответы на вопросы о будущем. '
                         'Получай увлекательные прогнозы на каждый день. Давай вместе раскроем завесу загадок!\n\n'
                         'Выберите свой знак зодиака: 👇', reply_markup=znaki_kb)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Этот бот присылает <b>ежедневные гороскопы</b> для вашего знака зодиака.\n\n'
                         'Чтобы выбрать или изменить свой знак зодиака и получить гороскоп на сегодня, нажмите /start.\n\n'
                         'Чтобы ознакомиться со списком доступных команд, нажмите /help.\n\n'
                         'Чтобы ознакомиться с информацией о заказе рекламы и о разработчиках бота, нажмите /info')


@router.message(Command(commands='info'))
async def process_info_command(message: Message):
    await message.answer(text='Для заказа рекламы нажмите на кнопку <b>"Заказать рекламу"</b>.\n\n'
                         'Данный бот разработан командой <i>BotDesigners</i>. '
                         'Для более подробной информации о команде нажмите на кнопку <b>"Канал BotDesigners"</b>',
                         reply_markup=info_kb)


# Проверка того, что коллбек есть в списке знаков
def true_znak_b(callback: CallbackQuery):
    return callback.data in rus_znaks.keys()


@router.callback_query(true_znak_b)
async def give_random_goroscop(callback: CallbackQuery):
    is_user_in_db = await check_user(callback.from_user.id)
    if is_user_in_db == '<Record exists=False>':
        await create_user(user_id=callback.from_user.id, znak=callback.data)
    else:
        await change_user(user_id=callback.from_user.id, znak=callback.data)
    message = callback.message
    txt_goroscops = await show_goroscop()
    pics = await show_pic()
    txt_goroscop = str(random.choice(txt_goroscops)).replace("<Record txt_goroscop='", '').replace("'>", '')
    pic = str(random.choice(pics)).replace("<Record pic_id='", '').replace("'>", '')
    await callback.message.delete()
    await message.answer_photo(photo=str(pic), caption=f'Выбранный знак зодиака: <b>{rus_znaks[callback.data]}</b>\n\n<b>Гороскоп на сегодня:</b>\n{escape(txt_goroscop)}')
