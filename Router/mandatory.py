from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from baza import get_all_subscriptions
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

mandatory_router = Router()

async def check_call_data(message: CallbackQuery ) -> bool:
    user_id = message.from_user.id
    channels = get_all_subscriptions()
    if not channels:
        return False
    
    for channnel in channels:
        channnel_id = channnel[1]
        try:
            member = await message.bot.get_chat_member(channnel_id, user_id)
            if member.status in ("creator", "administrator", "member", "restricted"):
                continue
            else:
                return True
        except Exception:
            return False
    return False


async def check_message(message : Message) -> bool:
    user_id = message.from_user.id
    channels = get_all_subscriptions()
    if not channels:
        return False

    for ch in channels:
        channel_id = ch[1]
        try:
            member = await message.bot.get_chat_member(channel_id, user_id)
            if member.status in ("creator", "administrator", "member", "restricted"):
                continue
            else:
                return True  
        except Exception:
            return False  
    return False  

from loader import bot
async def build_subscribe_keyboard(user_id: int):
    channels = get_all_subscriptions()
    if not channels:
        return None

    builder = InlineKeyboardBuilder()
    for ch in channels:
        member = await bot.get_chat_member(ch[1], user_id)
        if member.status not in ("creator", "administrator", "member", "restricted") :
            username = ch[2].lstrip("@") if len(ch) > 2 else str(ch[1])
            builder.button(text=f"📢 {username}", url=f"https://t.me/{username}")

    builder.button(text="✅ Tekshirish", callback_data="check_subscriptions")
    builder.adjust(1)
    return builder.as_markup()



class SubscriptionFilteri(BaseFilter):
    async def __call__(self, query: CallbackQuery) -> bool:
        return await check_call_data(query)

class SubscriptionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await check_message(message)
    
@mandatory_router.message(SubscriptionFilter())
async def must_subscribe(message: Message):
    kb = await build_subscribe_keyboard(message.from_user.id)
    await message.answer(
        "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
        reply_markup=kb
    )

@mandatory_router.callback_query(SubscriptionFilteri())
async def must_subscribe(query: CallbackQuery):
    kb = await build_subscribe_keyboard(query.from_user.id)
    await query.answer(
        "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
        reply_markup=kb
    )