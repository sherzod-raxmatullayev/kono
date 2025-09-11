from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
admin_main_menyu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎬 Anime sozlamalari"),
            KeyboardButton(text="📺 Anime qismlari")
        ],
        [
            KeyboardButton(text="📢 Kanal sozlamalari"),
            KeyboardButton(text="👑 Admin sozlamalari")
        ],
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="📨 Xabar tarqatish")
        ]
    ],
    resize_keyboard=True  # Klaviaturani ixchamlashtiradi
)

def kanal_yuklash(ID):
    men = InlineKeyboardBuilder()
    men.button(text="Yuklash", url=f"https://t.me/FOX_TV_STUDIOS_ROBOT?start={ID}")
    men.adjust(1)
    return men.as_markup()

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bekor qilish.", callback_data="bekor")
        ]
    ]
)

anime_settings_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ 🎬 Anime qo'shish"),
            KeyboardButton(text="🗑 🎬 Anime o'chirish")
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True
)


anime_series_settings_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ 📺 Qisim qo'shish"),
            KeyboardButton(text="🗑 📺 Qisimni o'chirish")
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True
)


channels_settings_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ 📢 Kanal qo'shish"),
            KeyboardButton(text="🗑 📢 Kanal o'chirish")
        ],
        [
            KeyboardButton(text="📜 📢 Kanallar ro'yxati")
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True
)


admin_setting_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ 👑 Admin qo'shish"),
            KeyboardButton(text="🗑 👑 Admin o'chirish")
        ],
        [
            KeyboardButton(text="📜 👑 Adminlar ro'yxati")
        ],
        [
            KeyboardButton(text="Orqaga")
        ]
    ],
    resize_keyboard=True
)
