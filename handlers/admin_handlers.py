from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, PhotoSize
from aiogram.fsm.storage.memory import MemoryStorage
from filters.filters import IsAdminMess, IsAdminCall
from sql_requests.sql_user import create_pic, create_txt, create_ad, count_users
from datetime import datetime

router: Router = Router()
router.message.filter(IsAdminMess())
router.callback_query.filter(IsAdminCall())

storage: MemoryStorage = MemoryStorage()

new_pic_dict: dict[int, dict[str, str | int | bool]] = {}
new_text_dict: dict[int, dict[str, str | int | bool]] = {}
new_ad_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMPic(StatesGroup):
    fill_pic = State()

class FSMText(StatesGroup):
    fill_text = State()

class FSMAd(StatesGroup):
    fill_ad_text = State()
    fill_ad_url = State()
    fill_ad_pic = State()
    fill_ad_datetime = State()

@router.message(Command(commands='help'), StateFilter(default_state))
async def help_command(message: Message):
    await message.answer(text='Вы являетесь администратором бота.\n\n'
                         'Чтобы добавить картинку в базу данных, '
                         'нажмите /new_pic\n\n'
                         'Чтобы добавить текст в базу данных, '
                         'нажмите /new_text\n\n'
                         'Чтобы добавить рекламу, '
                         'нажмите /new_ad\n\n'
                         'Чтобы увидеть количество пользователей бота, нажмите /count_users\n\n'
                         'Команда /start позволяет выбрать или изменить Ваш знак зодиака')


@router.message(Command(commands='count_users'), StateFilter(default_state))
async def count_users_command(message: Message):
    number_of_users = await count_users()
    await message.answer(text=f'Текущее количество пользователей бота: <b>{number_of_users}</b>')


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_process_in_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Процесс прерван.')


@router.message(Command(commands='cancel'))
async def cancel_process(message: Message):
    await message.answer(text='Отменять нечего.')


#Машина состояний для картинок
@router.message(Command(commands='new_pic'), StateFilter(default_state))
async def new_pic_command(message: Message, state: FSMContext):
    await message.answer(text='Пришлите картинку.\n\nЕсли хотите отменить загрузку картинки, нажмите /cancel')
    await state.set_state(FSMPic.fill_pic)


@router.message(StateFilter(FSMPic.fill_pic), F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    await state.update_data(pic=largest_photo.file_id)
    new_pic_dict = {}
    new_pic_dict[message.from_user.id] = await state.get_data()
    await create_pic(pic_id=new_pic_dict[message.from_user.id]['pic'])
    new_pic_dict = {}
    await message.answer(text='Фото сохранено')
    await state.clear()


@router.message(StateFilter(FSMPic.fill_pic))
async def warning_not_photo(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\nЕсли хотите отменить загрузку картинки, нажмите /cancel')


#Машина состояний для текстов гороскопов
@router.message(Command(commands='new_text'), StateFilter(default_state))
async def new_text_command(message: Message, state: FSMContext):
    await message.answer(text='Пришлите новый текст.\n\nЕсли хотите отменить загрузку текста, нажмите /cancel')
    await state.set_state(FSMText.fill_text)


@router.message(StateFilter(FSMText.fill_text), F.text)
async def process_text_sent(message: Message, state: FSMContext):
    await state.update_data(txt=message.text)
    new_text_dict = {}
    new_text_dict[message.from_user.id] = await state.get_data()
    await create_txt(txt_goroscop=new_text_dict[message.from_user.id]['txt'])
    new_text_dict = {}
    await message.answer(text='Текст гороскопа сохранен')
    await state.clear()


@router.message(StateFilter(FSMText.fill_text))
async def warning_not_text(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\nЕсли хотите отменить загрузку текста, нажмите /cancel')


#Машина состояний для рекламы
@router.message(Command(commands='new_ad'), StateFilter(default_state))
async def new_ad_command(message: Message, state: FSMContext):
    await message.answer(text='Введите текст рекламного сообщения\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')
    await state.set_state(FSMAd.fill_ad_text)


@router.message(StateFilter(FSMAd.fill_ad_text), F.text)
async def ad_text_process(message: Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await message.answer(text='Пришлите ссылку рекламного сообщения\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')
    await state.set_state(FSMAd.fill_ad_url)


@router.message(StateFilter(FSMAd.fill_ad_text))
async def warning_not_ad_text(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')


# Функция для проверки того, что была вставлена правильная ссылка
def is_valid_url(message: Message):
    try:
        if message.text.startswith('https://'):
            return True
        else:
            return False
    except:
        return False


@router.message(StateFilter(FSMAd.fill_ad_url), F.text, is_valid_url)
async def ad_url_process(message: Message, state: FSMContext):
    await state.update_data(ad_url=message.text)
    await message.answer(text='Пришлите картинку для рекламного сообщения. Если хотите создать рекламное сообщение без картинки, нажмите на команду /no_pic\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')
    await state.set_state(FSMAd.fill_ad_pic)


@router.message(StateFilter(FSMAd.fill_ad_url))
async def warning_not_ad_url(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')


@router.message(StateFilter(FSMAd.fill_ad_pic), F.photo[-1].as_('largest_photo'))
async def process_photo_ad_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    await state.update_data(ad_pic=largest_photo.file_id)
    await message.answer(text='Пришлите дату и время рассылки рекламного сообщения в формате:\n'
                         '<i>01.01.2023 12:00</i>\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')
    await state.set_state(FSMAd.fill_ad_datetime)


@router.message(StateFilter(FSMAd.fill_ad_pic), Command(commands='no_pic'))
async def process_no_photo_ad_sent(message: Message, state: FSMContext):
    await state.update_data(ad_pic='no_pic')
    await message.answer(text='Пришлите дату и время рассылки рекламного сообщения в формате:\n'
                         '<i>01.01.2023 12:00</i>\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')
    await state.set_state(FSMAd.fill_ad_datetime)


@router.message(StateFilter(FSMAd.fill_ad_pic))
async def warning_not_ad_pic(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\nЕсли хотите отменить создание рекламного сообщения, нажмите /cancel')


# Функция для проверки того, что была введена корректная дата
def is_true_datetime(message: Message):
    try:
        l_text = message.text
        check = datetime.strptime(l_text, "%d.%m.%Y %H:%M")
        return True
    except:
        return False


@router.message(StateFilter(FSMAd.fill_ad_datetime), is_true_datetime)
async def process_datetime_ad(message: Message, state: FSMContext):
    await state.update_data(ad_datetime=message.text)
    new_ad_dict = {}
    new_ad_dict[message.from_user.id] = await state.get_data()
    ad_text = new_ad_dict[message.from_user.id]['ad_text']
    ad_url = new_ad_dict[message.from_user.id]['ad_url']
    ad_pic = new_ad_dict[message.from_user.id]['ad_pic']
    ad_datetime = new_ad_dict[message.from_user.id]['ad_datetime']
    await create_ad(ad_text=ad_text, ad_url=ad_url, ad_pic=ad_pic, ad_datetime=ad_datetime)
    new_ad_dict = {}
    await message.answer(text='Рекламное сообщение сохранено')
    await state.clear()


@router.message(StateFilter(FSMAd.fill_ad_datetime))
async def warning_not_ad_datetime(message: Message):
    await message.answer(text='Кажется, вы прислали что-то не то. Попробуйте снова.\n\n'
                         'Пришлите дату и время рассылки рекламного сообщения в формате:\n'
                         '<i>01.01.2023 12:00</i>\n\n'
                         'Если хотите отменить создание рекламного сообщения, нажмите /cancel')