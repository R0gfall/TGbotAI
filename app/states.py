from aiogram.fsm.state import StatesGroup, State
from enum import Enum


class Register(StatesGroup):
    login_R = State()
    password_R = State()
    login_L = State()
    password_L = State()


class OnOff(StatesGroup):
    online = State()
    offline = State()
    predict_image = State()


class TypeLog(Enum):
    REGISTRATION = 1
    LOGIN = 2
    LOGOUT = 3


command_list = ["This ID chat already exists!", "User registered successfully!", "Incorrect credentials!",
                "Login successful!", "Logout successful!"]

