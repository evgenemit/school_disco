from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Предложить трек')
    kb.button(text='Плейлист')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
