from loader import dp, bot
import asyncio
import logging

from Router.mandatory import mandatory_router
from Router.user import user_router
from Router.admin import admin_router
from Admin.anime import anime_router
from Admin.qisim import qisimlar_router
from sos import sos_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp.include_router(sos_router)
dp.include_router(admin_router)
dp.include_router(mandatory_router)
dp.include_router(anime_router)
dp.include_router(qisimlar_router)
dp.include_router(user_router)


async def main():
    await dp.start_polling(bot)
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())