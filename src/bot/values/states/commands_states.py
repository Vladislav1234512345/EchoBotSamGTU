from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    set_name = State()
    set_surname = State()
    set_age = State()
    check = State()


class ConverterState(StatesGroup):
    how_much_convert_state = State()


class DigitGameState(StatesGroup):
    my_game = State()
    bot_game = State()
