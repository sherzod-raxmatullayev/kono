from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command,  CommandStart, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio


from Button.admin_button import (admin_main_menyu,
                                anime_settings_buttons,
                                anime_series_settings_button, 
                                channels_settings_button,
                                back,
                                admin_setting_button)

from baza import (
    get_all_admin_ids,
    get_users_count,
    get_admin_count,
    get_anime_count,
    get_series_count,
    get_channels_count,
    get_all_users
    
                  )

admin_router = Router()

ADMIN_IDS = [8153447771, 6950463049]
def adminss():
    admins = get_all_admin_ids()
    
    return admins

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        adminss = get_all_admin_ids()  
        return message.from_user.id in adminss

class messagesClass(StatesGroup):
    mess = State()

@admin_router.message(F.text == "Orqaga", IsAdmin())
async def back_hendler(message: Message):
    await message.answer(text="Bosh menyu!", reply_markup=admin_main_menyu)

@admin_router.callback_query(F.data == "bekor", IsAdmin())
async def vlear(message: CallbackQuery,  state: FSMContext):
    try: 
        await message.message.delete()
        await state.clear()
        await message.message.answer(text="Bosh menyu!", reply_markup=admin_main_menyu)
    except:
        await message.message.answer(text="Bosh menyu!", reply_markup=admin_main_menyu)







@admin_router.message(messagesClass.mess)
async def message_state(message: Message, state: FSMContext):
    message_text = message.text
    users = get_all_users()

    error = 0

    count = 0
    for user in users:
        try:
            await message.bot.send_message(chat_id=user[1], text=message_text)
            count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            error += 1
    await message.answer(text=f"✅ Xabar yetkazildi: {count}\nTarqatilmadi: {error}",  reply_markup=admin_main_menyu)
    await state.clear()
            


@admin_router.message(F.text == "📨 Xabar tarqatish", IsAdmin())
async def message_hendlar(message:Message, state: FSMContext):
    await message.answer(text="Tarqatmoqchi bo'lgan xabaringizni yuboring.", reply_markup=back)
    await state.set_state(messagesClass.mess)

@admin_router.message(F.text == "📊 Statistika",IsAdmin())
async def statistika_handler(message: Message):
    data_user = get_users_count()
    data_anime = get_anime_count()
    data_admin = get_admin_count()
    data_channel = get_channels_count()
    data_series = get_series_count()
    await message.answer(text=f"Foydalanuvchilar soni: {data_user}\nAnimelar soni: {data_anime}\nAdminlar soni: {data_admin}\nMajburiy kanallar soni: {data_channel}\n Anime qisimlari soni: {data_series}", reply_markup=admin_main_menyu)

@admin_router.message(F.text == "👑 Admin sozlamalari",F.from_user.id.in_(ADMIN_IDS))
async def admin_settings_hendler(message: Message):
    await message.answer(text="Admin sozlamalariga xush kelipsan.", reply_markup=admin_setting_button)

@admin_router.message(F.text == "📢 Kanal sozlamalari", IsAdmin())
async def channels_setting_hendler(message: Message):
    await message.answer(text="Kanal sozlamalariga xush kelipsan" ,reply_markup=channels_settings_button)

@admin_router.message(F.text == "📺 Anime qismlari", IsAdmin())
async def anime_series_setting_hendler(message: Message):
    await message.answer(text="Anime qisimlarini sozlashga kirildi.", reply_markup=anime_series_settings_button)

@admin_router.message(F.text == "🎬 Anime sozlamalari",IsAdmin())
async def anime_settings_hendler(message: Message):
    await message.answer(text="Anime sozlamalariga xush  kelipsan.", reply_markup=anime_settings_buttons)








@admin_router.callback_query(F.data == "check_subscriptions", IsAdmin())
async def admin_call_message(call: CallbackQuery):
    await call.message.answer(text="Xush kelipsan adminvachaa tugma bor ekan deb bosaverma!!!!", reply_markup=admin_main_menyu)
    await call.message.delete()

@admin_router.message(Command("admin"), IsAdmin())
async def admin_start_hendler(message: Message):
    await message.answer(text="Xush kelipsan adminvachaa tugma bor ekan deb bosaverma!!!!", reply_markup=admin_main_menyu)


