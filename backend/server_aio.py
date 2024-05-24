
from aiohttp import web

from config import TOKEN_API, web_url
from global_bot import bot, dp
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


app = web.Application()


async def set_webhook():    # Регистрация webhook
    print("1111")
    webhook_uri = f'{web_url}/{TOKEN_API}'
    await bot.set_webhook(webhook_uri)
    print(f"Webhook set to {webhook_uri}")


async def on_startup(_):
    await set_webhook()
    print("Webhook setup complete!")


def setup_routers():
     webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
     webhook_requests_handler.register(app, path=f'/{TOKEN_API}')

     setup_application(app, dp, bot=bot)

