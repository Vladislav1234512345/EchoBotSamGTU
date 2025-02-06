from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.register_keyboard import register_keyboard
from src.bot.values.states.commands_states import RegisterState
from src.config import logging_settings
from src.container import configure_logging

from logging import getLogger

logger = getLogger(__file__)
configure_logging(level=logging_settings.LOGGING_LEVEL)

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Напиши: игра")


@router.message(Command("start", "help", prefix="/"))
async def start_and_help_commands_handler(message: Message):
    await message.reply(text="Howdy, how are you doing?")


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
