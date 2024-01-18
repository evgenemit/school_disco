from aiogram import Bot, types
from aiogram.enums import ParseMode

from core.settings import settings
from core.utils.commands import set_commands
from core.keyboards.reply import main_keyboard
from core.utils.db import Database


async def start_up(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.admin.id, 'Бот запущен')


async def shut_down(bot: Bot, db: Database):
    await db.close()
    await bot.send_message(settings.admin.id, 'Бот Остановлен')


async def start(message: types.Message, db: Database):
    await db.create_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name
    )
    await message.answer(
        "Привет, это бот школьной дискотеки!\n\n" \
        "Отправляй названия треков, которые хочешь услышать на дикотеке," \
        "и, если они не нарушают правила, они будут добавлены в плейлист.",
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard()
    )
