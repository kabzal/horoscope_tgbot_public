from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config_data.config import Config, load_config

config: Config = load_config()
admin_ids = config.admin_id.adminid.split(', ')


# Фильтр для проверки админа сообщений
class IsAdminMess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        id = str(message.from_user.id)
        return (id in admin_ids)


# Фильтр для проверки админа коллбэков
class IsAdminCall(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        id = str(callback.from_user.id)
        return (id in admin_ids)
