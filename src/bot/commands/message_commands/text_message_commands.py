from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import random

from src.bot.values.states.commands_states import DigitGameState


router = Router(name=__name__)


@router.message(F.text.lower() == "игра")
async def digit_game_start_handler(message: Message, state: FSMContext):
    attempt = 5

    await message.answer(f'Игра "угадай число"!\nКоличество попыток: {attempt}')

    random_digit = random.randint(1, 10)

    await state.set_data({"attempt": attempt, "random_digit": random_digit})

    await message.answer("Готово! Загадано число от 1 до 10!")
    await message.answer("Введите число")

    await state.set_state(DigitGameState.start_game)


@router.message(DigitGameState.start_game, F.text)
async def digit_game_handler(message: Message, state: FSMContext):
    user_digit = message.text

    if not user_digit.isdigit():
        await message.answer(text="Вы ввели не цифры, введите пожалуйста цифры")
    else:
        data = await state.get_data()
        attempt = int(data.get("attempt"))
        random_digit = int(data.get("random_digit"))
        if int(user_digit) == random_digit:
            await message.answer(
                f"Ура! Ты угадал число! Это была цифра: {random_digit}"
            )
            await state.clear()
        elif attempt > 1:
            attempt -= 1
            await state.update_data(attempt=attempt)
            await message.answer(f"Неверно, осталось попыток: {attempt}")
        else:
            await message.answer("Вы проиграли!")
            await state.set_state()


@router.message(F.text)
async def echo_handler(message: Message):
    if message.text == "Привет":
        await message.reply(text="Привет создатель бота!")
    elif message.text == "hi":
        await message.reply(text="Hi again! The bot creator!")
