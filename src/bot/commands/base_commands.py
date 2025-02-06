from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.bot_game_keyboard import bot_game_keyboard
from src.bot.keyboards.register_keyboard import register_keyboard
from src.bot.values.states.commands_states import RegisterState, DigitGameState
from src.config import logging_settings
from src.container import configure_logging

from logging import getLogger
import random


logger = getLogger(__file__)
configure_logging(level=logging_settings.LOGGING_LEVEL)

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer("Напиши: игра")


@router.message(Command("help", prefix="/"))
async def help_command_handler(message: Message):
    await message.reply(text="Howdy, how are you doing?")


@router.message(Command("game", prefix="/"))
async def game_command_handler(message: Message, state: FSMContext):

    await message.answer(
        f'Давай сыграем в игру "угадай число"!\nТы загадываешь число, а я должен его угадать. У меня есть ограниченное кол-во попыток: 5'
    )

    attempt = 5
    await state.set_data({"attempt": attempt})
    await message.answer(
        f"У тебя число {random.randint(1, 10)}?", reply_markup=bot_game_keyboard()
    )


@router.message(Command("reg", prefix="/"))
async def reg_command_handler(message: Message, state: FSMContext):
    await message.reply(text="Привет, давай познакомимся! Как тебя зовут?")
    await state.set_state(RegisterState.set_name)


@router.message(RegisterState.set_name, F.text)
async def register_name_text_message_handler(message: Message, state: FSMContext):
    await state.set_data({"name": message.text})
    await state.set_state(RegisterState.set_surname)
    await message.answer("Какая у вас фамилия?")


@router.message(RegisterState.set_surname, F.text)
async def register_surname_text_message_handler(message: Message, state: FSMContext):
    logger.info(await state.get_data())
    await state.update_data(surname=message.text)
    await state.set_state(RegisterState.set_age)
    await message.answer("Сколько вам лет?")


@router.message(RegisterState.set_age, F.text)
async def register_age_text_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    logger.info(data)
    await state.clear()
    await message.answer(
        text=f"Тебе {message.text} лет? И тебя зовут: {data.get("name")} {data.get("surname")}?",
        reply_markup=register_keyboard(),
    )
    await state.set_state(RegisterState.check)
