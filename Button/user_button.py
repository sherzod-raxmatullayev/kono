from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from baza import get_qisimlar_by_anime

def yuklash(id):
    builder = InlineKeyboardBuilder()
    builder.button(text="Yuklash", callback_data=f"qisimlar_{id}")
    builder.adjust(1)
    return builder.as_markup()


def qism(anime_id: int):
    builder = InlineKeyboardBuilder()
    sm = get_qisimlar_by_anime(anime_id)
    if sm:
        for qisim in sm:
            builder.button(text=f"{qisim[1]}", callback_data=f"qism_{qisim[0]}")
    builder.adjust(6)
    return builder.as_markup()
