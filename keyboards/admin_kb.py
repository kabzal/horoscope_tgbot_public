from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Кнопки со знаками зодиака
oven_b: InlineKeyboardButton = InlineKeyboardButton(text='Овен', callback_data='oven')
telec_b: InlineKeyboardButton = InlineKeyboardButton(text='Телец', callback_data='telec')
bliznecy_b: InlineKeyboardButton = InlineKeyboardButton(text='Близнецы', callback_data='bliznecy')
rak_b: InlineKeyboardButton = InlineKeyboardButton(text='Рак', callback_data='rak')
lev_b: InlineKeyboardButton = InlineKeyboardButton(text='Лев', callback_data='lev')
deva_b: InlineKeyboardButton = InlineKeyboardButton(text='Дева', callback_data='deva')
vesy_b: InlineKeyboardButton = InlineKeyboardButton(text='Весы', callback_data='vesy')
skorpion_b: InlineKeyboardButton = InlineKeyboardButton(text='Скорпион', callback_data='skorpion')
strelec_b: InlineKeyboardButton = InlineKeyboardButton(text='Стрелец', callback_data='strelec')
kozerog_b: InlineKeyboardButton = InlineKeyboardButton(text='Козерог', callback_data='kozerog')
vodolei_b: InlineKeyboardButton = InlineKeyboardButton(text='Водолей', callback_data='vodolei')
ryby_b: InlineKeyboardButton = InlineKeyboardButton(text='Рыбы', callback_data='ryby')

#Клавиатура со знаками зодиака
admin_znaki_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[oven_b, telec_b],
                                                                       [bliznecy_b, rak_b],
                                                                       [lev_b, deva_b],
                                                                       [vesy_b, skorpion_b],
                                                                       [strelec_b, kozerog_b],
                                                                       [vodolei_b, ryby_b]])