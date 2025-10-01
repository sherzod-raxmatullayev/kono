from aiogram import Router , F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import asyncio

from baza import add_user, get_user_by_telegram, get_anime_json, update_anime_views, get_qism_by_id, get_anime_by_name
from Button.user_button import yuklash, qism, result

user_router = Router()

@user_router.callback_query(F.data == "check_subscriptions")
async def user_start_message(call: CallbackQuery):
    await call.message.answer(f"👋 Assalomu alaykum {call.from_user.full_name} botimizga xush kelibsiz.\n✍🏻 Kino kodini yuboring.")
    await call.message.delete()

@user_router.message(F.text.startswith("/start"))
async def handler_with_payload(message: Message):
    try:
        payload = message.text.split()
        payload = payload[1] if len(payload) > 1 else None
        user = get_user_by_telegram(message.from_user.id)
        if user is None:
            text = f"""🚨 Yangi foydalanuvchi qo‘shildi!

    👤 Ismi: {message.from_user.first_name or 'Noma’lum'}
    👥 Familyasi: {message.from_user.last_name or 'Noma’lum'}
    🔗 Username: @{message.from_user.username if message.from_user.username else 'Yo‘q'}
    🆔 ID: {message.from_user.id}
    🌍 Til kodi: {message.from_user.language_code}
    """

            # Adminlarga yuborish
            await message.bot.send_message(chat_id=8153447771, text=text)
            await message.bot.send_message(chat_id=6950463049, text=text)

            # Foydalanuvchini bazaga qo'shamiz
            add_user(message.from_user.id)
        
        anime = get_anime_json(int(payload))
        if anime:
            text = anime["text"]
            file_id = anime["file_id"]
            update_anime_views(int(payload))
            await message.answer_photo(photo=file_id, caption=text, reply_markup=qism(int(payload)))
        else:
            await message.answer("❌ Anime topilmadi.")
    except Exception:
        if not get_user_by_telegram(message.from_user.id):
            add_user(message.from_user.id)
        await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name} botimizga xush kelibsiz.\n✍🏻 Kino kodini yuboring.")

@user_router.message(CommandStart())
async def start_handler(message: Message):
    try:
        user = get_user_by_telegram(message.from_user.id)
        if user is None:
            text = f"""🚨 Yangi foydalanuvchi qo‘shildi!

    👤 Ismi: {message.from_user.first_name or 'Noma’lum'}
    👥 Familyasi: {message.from_user.last_name or 'Noma’lum'}
    🔗 Username: @{message.from_user.username if message.from_user.username else 'Yo‘q'}
    🆔 ID: {message.from_user.id}
    🌍 Til kodi: {message.from_user.language_code}
    """

            # Adminlarga yuborish
            await message.bot.send_message(chat_id=8153447771, text=text)
            await message.bot.send_message(chat_id=6950463049, text=text)

            # Foydalanuvchini bazaga qo'shamiz
            add_user(message.from_user.id)

        await message.answer(f"👋 Assalomu alaykum {message.from_user.full_name} botimizga xush kelibsiz.\n✍🏻 Kino kodini yuboring.")
    except:
        print("zaybal")

@user_router.callback_query(F.data.startswith("qism_"))
async def qism_callback(query: CallbackQuery):
    qism_id = int(query.data.split("_")[1])
    await query.answer(f"Qism ID: {qism_id}")
    qismii = get_qism_by_id(qism_id)
    if qismii:
        await query.message.answer_video(video=qismii[3], caption=f'{qismii[1]}', reply_markup=qism(qismii[2]))
    else:
        await query.message.answer("❌ Qism topilmadi.")


@user_router.callback_query(F.data.startswith("anime_"))
async def anime_callback(query: CallbackQuery):
    anime_id = int(query.data.split("_")[1])
    await query.answer(f"Anime ID: {anime_id}")
    anime = get_anime_json(anime_id)
    if anime:
        text = anime["text"]
        file_id = anime["file_id"]
        update_anime_views(anime_id)
        await query.message.answer_photo(photo=file_id, caption=text, reply_markup=qism(anime_id))
    else:
        await query.message.answer("❌ Anime topilmadi.")


@user_router.message(F.text)
async def skrech(message:Message):
    if message.text.isdigit():
        anime = get_anime_json(int(message.text))
        if anime:
            text = anime["text"]
            file_id = anime["file_id"]
            update_anime_views(int(message.text))
            await message.answer_photo(photo=file_id, caption=text, reply_markup=qism(int(message.text)))
        else:
            await message.answer("Anime topilmadi")
    else:
        if get_anime_by_name(message.text):
            await message.answer(
                text='Topilgan animelar: ',
                reply_markup= result(get_anime_by_name(message.text))

            )
