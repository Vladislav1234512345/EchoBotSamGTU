from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.bot_game_keyboard import bot_game_keyboard
from src.bot.keyboards.register_keyboard import register_keyboard
from src.bot.values.states.commands_states import RegisterState, ConverterState
from src.config import logging_settings
from src.container import configure_logging

from logging import getLogger
import random
import time
import datetime
from cbrf.models import DailyCurrenciesRates

from src.container import memes, jokes

from src.utils import generate_password

logger = getLogger(__file__)
configure_logging(level=logging_settings.LOGGING_LEVEL)

router = Router(name=__name__)

command_list = (
    "Напиши мне команду\n"
    "/send_meme - отправить мем\n"
    "/send_joke - отправить анекдот\n"
)

memes_sent_count = 0
jokes_sent_count = 0


@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer(
        text="Привет, это бот создан в качестве примера получения картинки и анекдотов!\n"
        + command_list
    )


@router.message(Command("send_meme", prefix="/"))
async def send_meme_command_handler(message: Message):
    global memes_sent_count
    memes_sent_count += 1
    await message.answer_photo(photo=random.choice(memes))


@router.message(Command("send_joke", prefix="/"))
async def send_joke_command_handler(message: Message):
    global jokes_sent_count
    jokes_sent_count += 1
    await message.answer(text=random.choice(jokes))


@router.message(Command("stats", prefix="/"))
async def stats_memes_and_jokes_handler(message: Message):
    global memes_sent_count, jokes_sent_count
    await message.answer(
        text=f"Количество отправленных мемов = {memes_sent_count}"
        f"\nКоличество отправленных шуток = {jokes_sent_count}"
    )


# command_list = "Полный список команд:\n" "/AUD \n" "/USD \n " "/EUR \n " "/converter \n"

convert_list = "Полный перечень валют:\nUSD,\nAUD,\nEUR,\nRUB"
today = datetime.date.today()
daily = DailyCurrenciesRates()
# daily.date
datetime.datetime(today.year, today.month, today.day, 0, 0)

CURRENCIES = {"EUR": "R01239", "USD": "R01235", "AUD": "R01010", "RUB": None}


@router.message(Command("AUD", prefix="/"))
async def get_aud_handler(message: Message):
    aud_object = daily.get_by_id(CURRENCIES[message.text[1:]])
    names = aud_object.name
    value = aud_object.value
    await message.answer(text=" " + names + " " + str(value))


@router.message(Command("USD", prefix="/"))
async def get_usd_handler(message: Message):
    usd_object = daily.get_by_id(CURRENCIES[message.text[1:]])
    names = usd_object.name
    value = usd_object.value
    await message.answer(text=" " + names + " " + str(value))


@router.message(Command("EUR", prefix="/"))
async def get_euro_handler(message: Message):
    euro_object = daily.get_by_id(CURRENCIES[message.text[1:]])
    names = euro_object.name
    value = euro_object.value
    await message.answer(text=" " + names + " " + str(value))


@router.message(Command("converter", prefix="/"))
async def convert_currencies_command_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Введите сообщение вида: [Число] [Валюта1] [Валюта2], где\n"
        "\nЧисло - количество денег для конвертами,"
        "\nВалюта1 - валюта из какой конвертировать,"
        "\nВалюта2 - валюта в какую конвертировать.\n\n" + convert_list
    )
    await state.set_state(ConverterState.how_much_convert_state)


@router.message(ConverterState.how_much_convert_state, F.text)
async def convert_currencies_handler(message: Message, state: FSMContext):
    words = message.text.split()
    if len(words) != 3:
        await message.reply(text="Введите сообщение вида: [Число] [Валюта1] [Валюта2]")
        return None

    try:
        amount = float(words[0])
    except ValueError:
        await message.reply(
            text="Введите ЧИСЛО денег в рублях, которые вы хотите конвертировать."
        )
        return None

    from_currency = words[1]
    to_currency = words[2]
    if from_currency == to_currency:
        await message.reply(text="Валюта 1 и валюта 2 не должны быть одинаковыми.")
        return None
    if from_currency in CURRENCIES.keys() and to_currency in CURRENCIES.keys():
        if from_currency == "RUB":
            to_currency_value = float(daily.get_by_id(CURRENCIES[to_currency]).value)
            answer_count = round(amount / to_currency_value, 2)
        elif to_currency == "RUB":
            from_currency_value = float(
                daily.get_by_id(CURRENCIES[from_currency]).value
            )
            answer_count = round(amount * from_currency_value, 2)
        else:
            from_currency_value = float(
                daily.get_by_id(CURRENCIES[from_currency]).value
            )
            to_currency_value = float(daily.get_by_id(CURRENCIES[to_currency]).value)
            answer_count = round(amount * from_currency_value / to_currency_value, 2)
        await message.answer(
            text=f"После конвертации денег из одной валюты в другую, мы получили число, которое равно {answer_count}"
        )
        await state.clear()
    else:
        if from_currency not in CURRENCIES.keys():
            await message.reply(
                text="Валюта которую необходимо конвертировать была введена неверна\n"
                + convert_list
            )
        else:
            await message.reply(
                text="Валюта в которую необходимо конвертировать была введена неверна\n"
                + convert_list
            )

    await state.set_data({"amount": amount})


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
