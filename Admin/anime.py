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
    add_anime,
    get_all_admin_ids,
    delete_anime,
    add_admin,
    delete_admin,
    get_all_admin
)


def adminss():
    adi = get_all_admin_ids()
    return adi

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        adminss = get_all_admin_ids()  # faqat telegram_id lar ro'yxati
        return message.from_user.id in adminss

class addanimestate(StatesGroup):
    name = State()
    janr = State()
    yili = State()
    duber = State()
    qisimlari = State()
    file_id = State()

class delete_anime_state(StatesGroup):
    anime_id = State()

anime_router = Router()

@anime_router.message(addanimestate.file_id)
async def add_anime_file(message: Message, state: FSMContext):
    try: 
        file_id = message.photo[-1].file_id

        data = await state.get_data()
        name = data.get("name")
        janr = data.get("janr")
        yili = data.get("yili")
        duber = data.get("duber")
        qisimlar = data.get("qisimlari")

        if not all([name, janr, yili, duber, qisimlar, file_id]):
            await message.answer("Xatolik yuz berdi")
            await message.answer(f"{name, janr, yili, duber, qisimlar, file_id}")
            await state.clear()
            return
        id = add_anime(name, janr, yili, duber, int(qisimlar), file_id)
        if message.caption == None:
            await message.bot.send_photo(chat_id=-1002165160594, photo=file_id, caption=f"✅ Yangi anime qo'shildi: ID {id}\n\n📛 Nomi: {name}\n🎭 Janri: {janr}\n📅 Yili: {yili}\n🎙️ Duber: {duber}\n🎬 Qismlari: {qisimlar}"
                                        ,reply_markup=kanal_yuklash(id))
        
        await message.answer(f"Anime '{name}' muvaffaqiyatli qo'shildi! ID: {id}")
        await state.clear()
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@anime_router.message(addanimestate.qisimlari)
async def add_anime_series(message:Message, state:FSMContext):
    if message.text.isdigit():
        await state.update_data(qisimlari=message.text)
        await message.answer(text="Kanalga tashlash uchun rasimni yuboring faqat rasim!!!", reply_markup=back)
        await state.set_state(addanimestate.file_id)
    else:
        await message.answer("Faqat son kiriting!!!", reply_markup=back)
        await state.set_state(addanimestate.qisimlari)

@anime_router.message(addanimestate.duber)
async def add_anime_dubber_hendler(message:Message, state: FSMContext):
    await state.update_data(duber=message.text)
    await message.answer(text="Animeni barcha qisimlarini kiriting! Maslan(12)", reply_markup=back)
    await state.set_state(addanimestate.qisimlari)

@anime_router.message(addanimestate.yili)
async def add_anime_year(message:Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(yili=message.text)
        await message.answer(text="Animega ovoz berganlarni kiriting hammasini bitta xabarda!", reply_markup=back)
        await state.set_state(addanimestate.duber)
    else:
        await message.answer("Iltimos yilga faqat son kiriting!", reply_markup=back)
        await state.set_state(addanimestate.yili)

@anime_router.message(addanimestate.janr)
async def add_anime_janr(message: Message, state: FSMContext):
    await state.update_data(janr=message.text)
    await message.answer(text="Anime yilini kiriting: Masalan(2003)", reply_markup=back)
    await state.set_state(addanimestate.yili)

@anime_router.message(addanimestate.name)
async def anime_name_add(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Anime janrlarini kiriting hammasini bir xabarda!", reply_markup=back)
    await state.set_state(addanimestate.janr)

@anime_router.message(IsAdmin() ,F.text == "➕ 🎬 Anime qo'shish")
async def add_anime_hendler(message: Message, state: FSMContext):
    await message.answer(text="Qo'shmoqchi bo'lgan anime nomini yuboring.", reply_markup=back)
    await state.set_state(addanimestate.name)

@anime_router.message(IsAdmin(), delete_anime_state.anime_id)
async def delete_anime_states(message:Message, state: FSMContext):
    if message.text.isdigit():
        if delete_anime(int(message.text)):
            await message.answer("Anime o'chirildi.")
            await state.clear()
        else:
            await message.answer("Bunday ID da anime yo'q.")
    else:
        await message.answer("ID faqat son bo'ladi")
        await state.set_state(delete_anime_state.anime_id)


@anime_router.message(IsAdmin() ,F.text == "🗑 🎬 Anime o'chirish")
async def delete_anime_db(message: Message, state:FSMContext):
    await message.answer(text="O'chirmoqchi bo'lgan anime ID ni yuboring!", reply_markup=back)
    await state.set_state(delete_anime_state.anime_id)



ADMIN_IDS = [8153447771, 6950463049]

class add_admins(StatesGroup):
    id = State()

class del_admins(StatesGroup):
    id = State()

@anime_router.message(add_admins.id)
async def adminstate(message: Message, state:FSMContext):
    if message.text.isdigit():
        add_admin(int(message.text))
        await state.clear()
    else:
        await message.answer(text="ID faqat son bo'ladi.", reply_markup=back)
        await state.set_state(add_admins.id)

@anime_router.message(del_admins.id)
async def delstate(message: Message, state:FSMContext):
    if message.text.isdigit():
        delete_admin(int(message.text))
        await state.clear()
    else:
        await message.answer("Faqat son yubor!")
        await state.set_state(del_admins.id)


@anime_router.message(F.from_user.id.in_(ADMIN_IDS), F.text == "🗑 👑 Admin o'chirish")
async def delete_admin_blayt(message:Message, state:FSMContext):
    await message.answer(text="O'chirish uchun admin ID ni yubor ID ni ro'yxad tugmasidan olasan", reply_markup=back)
    await state.set_state(del_admins.id)

@anime_router.message(F.from_user.id.in_(ADMIN_IDS), F.text == "➕ 👑 Admin qo'shish")
async def admin_pilus(message:Message, state: FSMContext):
    await message.answer(text="Admin kiritish uchun admin ID raqamini yuboring", reply_markup=back)
    await state.set_state(add_admins.id)


@anime_router.message(F.from_user.id.in_(ADMIN_IDS), F.text == "📜 👑 Adminlar ro'yxati")
async def stat_admin(message:Message, state: FSMContext):
    admmin = get_all_admin()
    for i in admmin:
        await message.answer(f'{i}')
















