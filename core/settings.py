from environs import Env
from dataclasses import dataclass


@dataclass
class Admin:
    id: int


@dataclass
class Bot:
    token: str


@dataclass
class Settings:
    bot: Bot
    admin: Admin


def get_settings(path: str = '.env'):
    env = Env()
    env.read_env(path)

    return Settings(
        bot=Bot(token=env.str('TOKEN')),
        admin=Admin(id=env.int('ADMIN_ID'))
    )

settings = get_settings()

