from aiogram.fsm.state import State, StatesGroup


class TrackStates(StatesGroup):
    GET_TRACK_ARTIST = State()
    GET_TRACK_NAME = State()
