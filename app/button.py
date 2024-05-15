from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="registration"), KeyboardButton(text="login")],
], one_time_keyboard=True, resize_keyboard=True)

dop_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="picture"), KeyboardButton(text="exit")],
], resize_keyboard=True)
