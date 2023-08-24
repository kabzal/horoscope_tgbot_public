from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class DatabaseConfig:
    user: str
    password: str
    database: str
    host: str

@dataclass
class AdminId:
    adminid: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    admin_id: AdminId

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  db=DatabaseConfig(user=env('user'),
                                    password=env('password'),
                                    database=env('database'),
                                    host=env('host')),
                  admin_id=AdminId(adminid=env('ADMIN_ID')))