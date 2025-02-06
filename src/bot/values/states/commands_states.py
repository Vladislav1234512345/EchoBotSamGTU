from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    set_name = State()
    set_surname = State()
    set_age = State()
    check = State()


class DigitGameState(StatesGroup):
    start_game = State()
