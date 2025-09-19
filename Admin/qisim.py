from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from Button.admin_button import (
    back, 
    admin_main_menyu,
    kanal_yuklash
)
from baza import (
    add_qism,
    get_all_admin_ids,
    delete_qism,
    get_anime_by_id,
    add_subscription, 
    delete_subscription,
    get_all_subscriptions

    
    
)


def adminss():
    adi = get_all_admin_ids()
    return adi

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        adminss = get_all_admin_ids()  # faqat telegram_id lar ro'yxati
        return message.from_user.id in adminss
    
qisimlar_router = Router()


class add_series(StatesGroup):
    anime_id = State()
    qisim = State()
    file_id = State()

class delete_series(StatesGroup):
    qisim_id = State()



@qisimlar_router.message(add_series.file_id)
async def admin_series_3(message:Message, state:FSMContext):
    try:
        file_id = message.video.file_id
        data = await state.get_data()
        anime_id = data.get("anime_id")
        qisim = data.get("qisim")
        if not all([anime_id, qisim, file_id]):
            await message.answer("Xatolik yuz berdi")
        anime_data = add_qism(int(anime_id), file_id, int(qisim))
        if anime_data != None:
            anime = get_anime_by_id(int(anime_id))
            if message.caption == None:
                await message.bot.send_photo(chat_id=-1002165160594,photo=anime[8], caption=f"✅Yangi qisim qo'shildi: ID {anime_data}\n\n{qisim} - qisim\n📛 Nomi: {anime[1]}\n🎭 Janri: {anime[2]}\n📅 Yili: {anime[3]}\n🎙️ Duber: {anime[4]} ", reply_markup=kanal_yuklash(int(anime[0])))
            await message.answer("Anime qo'shildi Kanalga tashladim!")
            await state.clear()

    except:
        await message.answer("Nimadir xato ketgan!")
        await state.clear()


@qisimlar_router.message(add_series.qisim)
async def admin_series_2(message:Message, state:FSMContext):
    if message.text.isdigit():
        await state.update_data(qisim = message.text)
        await message.answer("Video file ni tashlang!", reply_markup=back)
        await state.set_state(add_series.file_id)


@qisimlar_router.message(add_series.anime_id)
async def admin_series(message:Message, state:FSMContext):
    if message.text.isdigit():
        anime = get_anime_by_id(int(message.text))
        if anime == None:
            await message.answer("Anime topilmadi ID ni aniq kiriting. ", reply_markup=back)
            await state.set_state(add_series.anime_id)
        else:
            await state.update_data(anime_id = message.text)
            await message.answer("Nechanchi qisimligini kirit!!")   
            await state.set_state(add_series.qisim)
    else:
        await message.answer("Anime ID si faqat son bo'ladi!")
        await state.set_state(add_series.anime_id)

@qisimlar_router.message(IsAdmin(), F.text == "➕ 📺 Qisim qo'shish")
async def qisim_hendler_s(message: Message, state:FSMContext):
    await message.answer("Qo'shmoqchi bo'lgan qisimni anime ID sini yuboring!", reply_markup=back)
    await state.set_state(add_series.anime_id)

@qisimlar_router.message(delete_series.qisim_id)
async def dlete_qsiim(message:Message, state:FSMContext):
    if message.text.isdigit():
        if delete_qism(int(message.text)):
            await message.answer("Qisim o'chirildi.")
            await state.clear()
        else:
            await message.answer("Xatolik *******")
            await state.clear()

@qisimlar_router.message(IsAdmin(), F.text == "🗑 📺 Qisimni o'chirish")
async def dlete(message: Message, state:FSMContext):
    await message.answer("Ochirmoqchi bo'lgan qisim ID sini yubor.", reply_markup=back)
    await state.set_state(delete_series.qisim_id)








class deletechannel(StatesGroup):
    sub_id = State()


class chennel_state(StatesGroup):
    channel_id = State()
    


from aiogram.methods.get_chat import GetChat


    
from loader import bot
async def get_channel_info(link: str):
    if link.startswith("https://t.me/"):
        link = link.split("/")[-1]
    chat = await bot.get_chat(f"@{link}")
    
    return {
        "id": chat.id,
        "username": chat.username,
        "title": chat.title
    }

@qisimlar_router.message(chennel_state.channel_id)
async def chennal_hendler_1(message: Message, state: FSMContext):
    if message.text:
        try: 
            info = await get_channel_info(message.text)
            if info:
                add_subscription(info["id"], info["username"])
                await message.answer("Kanl qo'shildi!")
                await state.clear()
        except Exception as e:
            print(e)
            await message.answer("Qayta urinib ko'r")
            await state.clear()


@qisimlar_router.message(deletechannel.sub_id)
async def deletechannelstatehendler(message:Message, state:FSMContext):
    try:
        if delete_subscription(int(message.text)):
            await message.answer("Kanal majburiy obunaadan o'chirildi")
            await state.clear()
        else:
            await message.answer("Kanalni o'chirib bo'lmadi")
            await state.clear()
    except:
        await message.answer("ID faqat son bo'ladi!", reply_markup=back)
        await state.set_state(deletechannel.sub_id)



@qisimlar_router.message(IsAdmin(), F.text == "🗑 📢 Kanal o'chirish")
async def delete_channel_hendler(message:Message, state: FSMContext):
    await message.answer(text="O'chirmoqchi bo'lgan kanal ID sini kiriting! ID ni ro'yxadlar bo'limidan oling.")
    await state.set_state(deletechannel.sub_id)

@qisimlar_router.message(IsAdmin(), F.text == "➕ 📢 Kanal qo'shish")
async def chennal_hendler(message:Message, state:FSMContext):
    await message.answer(text="Yangi kanla havolasini bering!", 
                         reply_markup=back)
    await state.set_state(chennel_state.channel_id)

@qisimlar_router.message(F.text == "📜 📢 Kanallar ro'yxati")
async def channels_aount(message: Message):
    ch = get_all_subscriptions()
    try: 
        for i in ch:
            await message.answer(f"ID: {i[0]}\nTelegram id: {i[1]}\nName: {i[2]}")
    except:
        await message.answer("Kanala yo'q")











