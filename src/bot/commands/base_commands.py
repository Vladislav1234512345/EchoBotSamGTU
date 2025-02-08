from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.bot_game_keyboard import bot_game_keyboard
from src.bot.keyboards.register_keyboard import register_keyboard
from src.bot.values.states.commands_states import RegisterState
from src.config import logging_settings
from src.container import configure_logging

from logging import getLogger
import random
import time

from src.utils import generate_password

logger = getLogger(__file__)
configure_logging(level=logging_settings.LOGGING_LEVEL)

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer(
        text="Привет! Я бот для напоминаний. Используй /remind [время] [текст] для установки таймера."
    )


@router.message(Command("remind", prefix="/"))
async def remind_command_handler(message: Message):
    words = message.text.split()

    if len(words) < 3:
        await message.answer(
            text="Пожалуйста, укажи желаемое время и текст для установки паузы после команды /remind. Например, /remind 10 Привет, мир!"
        )
        return None

    try:
        remind_time = float(words[1])
    except ValueError:
        await message.answer(
            text="Пожалуйста, укажи желаемое время для команды /generate_password в виде ЧИСЛА, и не забудьте про текст для установки паузы. Например, /remind 1234 Ветер северный"
        )
        return None

    remind_text = "".join(words[2:])
    await message.answer(
        text=f"Ок, Я напомню тебе через {remind_time} с  {remind_text}."
    )
    time.sleep(remind_time)
    await message.answer(text=f"Хэй, не забудь {remind_text}!")


@router.message(Command("generate_password", prefix="/"))
async def generate_password_command_handler(message: Message):
    words = message.text.split()

    if len(words) != 2:
        await message.reply(
            text="Пожалуйста, укажи желаемую длину пароля после команды /generate_password. Например, /generate_password 12"
        )
        return None
    try:
        length = int(words[1])
    except ValueError:
        await message.reply(
            text="Пожалуйста, укажи желаемую длину пароля после команды /generate_password в виде ЦЕЛОГО ЧИСЛА. Например, /generate_password 12"
        )
        return None

    password = generate_password(length=length)

    await message.answer(text=f"Вот твой новый пароль: {password}")


@router.message(Command("help", prefix="/"))
async def help_command_handler(message: Message):
    await message.reply(
        text="Используйте команду /convert [значение] [величина] [величина] для конвертации. Доступные величины: км, м, ми, яр, фут, кг, г, фнт, унц"
    )


@router.message(Command("convert", prefix="/"))
async def convert_command_handler(message: Message):
    args = message.text.split()[1:]
    if len(args) != 3:
        await message.reply(
            text="Неверное количество аргументов. Используйте команду следующим образом: /convert [значение] [величина] [величина]"
        )
        return None
    try:
        value = float(args[0])
    except ValueError:
        await message.reply(text="Неверное значение. Пожалуйста, введите число")
        return None

    unit_from = args[1]
    unit_to = args[2]
    ratios = {
        "км": 1,
        "м": 1000,
        "ми": 0.621371,
        "яр": 1093.61,
        "фут": 3280.84 / 1000,
        "кг": 1,
        "г": 1000,
        "фнт": 2.20462,
        "унц": 35.274,
    }

    if unit_from not in ratios or unit_to not in ratios:
        await message.reply(
            text="Неверная величина. Для получения списка доступных величин введите команду /help"
        )

    result = value * ratios[unit_to] / ratios[unit_from]

    await message.answer(text=f"{value} {unit_from} = {result:.2f} {unit_to}")


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
