from aiogram import types, filters, F, Router
from aiogram.fsm.context import FSMContext
from app.states import Register, OnOff, TypeLog, command_list
from machine_learn.well_model import predict_image
from config import image_path, model5_path, download_image_path

import app.button as button
from data.database import connect_to_database
from global_bot import bot

router = Router()


@router.message(filters.CommandStart())
async def start_command(message: types.Message):
    # connect_to_database(TypeLog.LOGIN, 1198984812)
    await message.reply(f"Hello {message.from_user.first_name}, welcome to TGbotAI\n"
                        f"I can determine what is depicted in the picture: a Human or a Penguin. "
                        f"if you want to use me, pls logging!", reply_markup=button.main_reply_keyboard)


@router.message(F.text == "registration")
@router.message(filters.Command('register'))
async def register_command(message: types.Message, state: FSMContext):
    await state.set_state(Register.login_R)
    await message.reply("Write new login")


@router.message(F.text == "login")
@router.message(filters.Command("login"))
async def login_command(message: types.Message, state: FSMContext):
    await state.set_state(Register.login_L)
    await message.reply("Write your login")


@router.message(Register.login_R)
async def register_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(Register.password_R)
    await message.answer("Add new password")


@router.message(Register.login_L)
async def login_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(Register.password_L)
    await message.answer("Add your password")


@router.message(Register.password_R)
async def register_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data_register = await state.get_data()
    data_register["ID_user"] = message.from_user.id
    print(message.from_user.id)
    data_register["stable_login"] = True
    print(data_register)

    answer_bd = connect_to_database(TypeLog.REGISTRATION, data_register["ID_user"], data_register["login"],
                                    data_register["password"])
    if answer_bd == command_list[0]:
        await state.clear()
        await message.answer(answer_bd)

    elif answer_bd == command_list[1]:
        await state.set_state(OnOff.online)
        await message.answer(answer_bd, reply_markup=button.dop_reply_keyboard)


@router.message(Register.password_L)
async def login_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data_register = await state.get_data()
    data_register["ID_user"] = message.from_user.id
    print(message.from_user.id)
    data_register["stable_login"] = True

    answer_bd = connect_to_database(TypeLog.LOGIN, data_register["ID_user"], data_register["login"],
                                    data_register["password"])
    if answer_bd == command_list[2]:
        await state.clear()
        await message.answer(answer_bd)

    elif answer_bd == command_list[3]:
        await state.set_state(OnOff.online)
        print('set_onlite_state'
        )
        await message.answer(answer_bd, reply_markup=button.dop_reply_keyboard)


@router.message(F.text == "exit")
@router.message(filters.Command("logout"))
async def logout_command(message: types.Message, state: FSMContext):
    if await state.get_state() == OnOff.online or await state.get_state() == OnOff.predict_image:
        # Изменить состояние пользователя в бд на False
        data_register = await state.get_data()
        data_register["ID_user"] = message.from_user.id
        answer_bd = connect_to_database(TypeLog.LOGOUT, data_register["ID_user"], data_register["login"],
                                        data_register["password"])
        await message.answer(answer_bd, reply_markup=button.main_reply_keyboard)
        await state.clear()
        return

    await message.answer(f"You have been logged out!")


@router.message(filters.Command("predict"))
@router.message(F.text == "picture")
async def predict_command(message: types.Message, state: FSMContext):

    # Дополнить машину состояния дополнительным критерий высылки фото, добавить новый обработчик-декоратор, добавить загрузку картинки под названием, и
    # ОБЯЗАТЕЛЬНО сделать удаление картинки после ее использования
    if await state.get_state() == OnOff.online:
        await state.set_state(OnOff.predict_image)
        await message.answer("Send your picture!")
        # msg_answer = predict_image(image_path, model5_path)
        # print(msg_answer)
        # await message.answer(msg_answer)


@router.message(F.photo)
async def predict_picture(message: types.Message, state: FSMContext):

    # await message.bot.download(file=message.photo[-1].file_id, destination=download_image_path)
    if await state.get_state() == OnOff.predict_image:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await bot.get_file(file_id)
        photo_path = file_info.file_path

        # Скачиваем файл
        await bot.download_file(photo_path, download_image_path)

        msg_answer = predict_image(image_path, model5_path)
        await message.answer(msg_answer)

        await state.set_state(OnOff.online)
