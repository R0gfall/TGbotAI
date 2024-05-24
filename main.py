import asyncio

# from aiogram import Bot, Dispatcher

# from config import TOKEN_API, download_image_path
from app.handlers import router
from global_bot import bot, dp
from backend.server_flask import app, on_startup, setup_routers
from aiohttp import web
from config import TOKEN_API


# bot = Bot(token=TOKEN_API)
# dp = Dispatcher()


async def main():
    dp.include_router(router)
    # await dp.start_polling(bot)

# app.router.add_post(f'/{TOKEN_API}', handle_webhook)

if __name__ == '__main__':
    dp.include_router(router)
    # app.router.add_post(f'/{TOKEN_API}', handle_webhook)
    app.on_startup.append(on_startup)
    setup_routers()
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080
    )

    # asyncio.run(main())
    # start
