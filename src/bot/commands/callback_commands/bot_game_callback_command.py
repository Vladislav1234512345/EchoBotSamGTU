import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.bot_game_keyboard import bot_game_keyboard
from src.bot.values.callback.base_callbacks_values import bot_game_callback


router = Router(name=__name__)


@router.callback_query(F.data == bot_game_callback.yes)
async def yes_bot_game_callback_handler(
    callback_query: CallbackQuery, state: FSMContext
):
    await callback_query.message.answer(text="Ура! Я выиграл!")
    await state.clear()


@router.callback_query(F.data == bot_game_callback.no)
async def no_bot_game_callback_handler(
    callback_query: CallbackQuery, state: FSMContext
):

    if await state.get_value("attempt") is None:
        await callback_query.message.answer(text="Произошла ошибка.")
    else:
        attempt = int(await state.get_value("attempt"))
        if attempt > 1:
            attempt -= 1
            await state.update_data(attempt=attempt)
            await callback_query.message.answer(
                text=f"У меня осталось {attempt} попыток."
            )
            await callback_query.message.answer(
                text=f"У тебя число {random.randint(1, 10)}?",
                reply_markup=bot_game_keyboard(),
            )
        else:
            await callback_query.message.answer(text="Я проиграл.")
            await state.clear()
