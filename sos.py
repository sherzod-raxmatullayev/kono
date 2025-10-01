from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

# sos router yaratamiz
sos_router = Router()

@sos_router.message(Command("sos"))
async def send_db_file(message: Message):
    try:
        if message.from_user.id == 6950463049:
        # bazani fayl sifatida ulashamiz
            file = FSInputFile("anime.db")
            await message.answer_document(file, caption="Mana anime.db fayli 📂")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")
