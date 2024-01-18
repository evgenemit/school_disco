import logging
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command

from core.settings import settings
from core.handlers import basic, music
from core.utils.states_track import TrackStates
from core.utils.db import Database


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bot.token)
dp = Dispatcher()


async def main():

    pool_connect = await asyncpg.create_pool(
        user='school_disco_user',
        password='pass1234',
        database='school_disco',
        host='localhost',
        port=5432,
        command_timeout=60
    )
    dp['db'] = Database(pool_connect)
    dp.startup.register(basic.start_up)
    dp.shutdown.register(basic.shut_down)
    # messages
    dp.message.register(basic.start, Command('start'))
    dp.message.register(music.add_track, F.text == 'Предложить трек')
    dp.message.register(music.add_track_artist, TrackStates.GET_TRACK_ARTIST)
    dp.message.register(music.add_track_name, TrackStates.GET_TRACK_NAME)
    dp.message.register(music.playlist, F.text == 'Плейлист')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
