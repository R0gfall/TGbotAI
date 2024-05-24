from urllib import request

from app.handlers import router
from aiohttp import web
from aiogram import types
from config import TOKEN_API, web_url
from global_bot import bot, dp
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# app = Flask(__name__)
app = web.Application()


async def set_webhook():    # Регистрация webhook
    print("1111")
    webhook_uri = f'{web_url}/{TOKEN_API}'
    await bot.set_webhook(webhook_uri)
    print(f"Webhook set to {webhook_uri}")


async def on_startup(_):
    await set_webhook()
    print("Webhook setup complete!")


# async def handle_webhook(request):
#     print('def handle_webhook(request):')
#     url = str(request.url)
#     index = url.rfind('/')
#     token = url[index+1:]
#     print("Received a webhook request")
#     if token == TOKEN_API:
#         request_data = await request.json()
#         update = types.Update(**request_data)
#
#         bot.set_current()
#
#         await dp.process_update(update)
#
#         return web.Response()
#
#     else:
#         return web.Response(status=403)

def setup_routers():
     webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
     webhook_requests_handler.register(app, path=f'/{TOKEN_API}')

     setup_application(app, dp, bot=bot)


# app.router.add_post(f'/{TOKEN_API}', handle_webhook)


# @app.route('/', methods=["GET", "POST"])
# def web_hook():
#     if request.method == "POST":
#         print(request.json)

# app.run(debug=True, host='127.0.0.1', port=8080)
