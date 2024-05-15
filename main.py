import asyncio

# from aiogram import Bot, Dispatcher

# from config import TOKEN_API, download_image_path
from app.handlers import router
from global_bot import bot, dp

# bot = Bot(token=TOKEN_API)
# dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    # start
