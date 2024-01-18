from aiogram import types
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from core.utils.states_track import TrackStates
from core.keyboards.reply import main_keyboard
from core.utils.db import Database


async def add_track(message: types.Message, state: FSMContext):
    await message.answer(
        'Исполнитель:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(TrackStates.GET_TRACK_ARTIST)

async def add_track_artist(message: types.Message, state: FSMContext):
    await state.update_data(artist_name=message.text)
    await message.answer('Название трека:')
    await state.set_state(TrackStates.GET_TRACK_NAME)

async def add_track_name(message: types.Message, state: FSMContext, db: Database):
    await state.update_data(track_name=message.text)
    data = await state.get_data()
    await db.create_track(
        track_name=data.get('track_name'),
        artist_name=data.get('artist_name'),
        user_id=message.from_user.id
    )
    await message.answer(
        f'Отлично!\n\n<b>{data.get("artist_name")} — {data.get("track_name")}</b>\n\n' \
        'отправлен на проверку.',
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard()
    )
    await state.clear()

async def playlist(message: types.Message, db: Database):
    answer_text = 'Текущий плейлист:\n\n'
    tracks = await db.get_playlist()
    if tracks:
        for i in range(len(tracks)):
            answer_text += f'{i + 1}) {tracks[i][1]} — {tracks[i][2]}\n'
    else:
        answer_text += '<i>Пока пусто</i>'
    await message.answer(
        answer_text,
        parse_mode=ParseMode.HTML
    )
