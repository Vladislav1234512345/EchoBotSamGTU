from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.commands.base_commands import reg_command_handler
from src.bot.values.callback.base_callbacks_values import register_callback

router = Router(name=__name__)


@router.callback_query(F.data == register_callback.yes)
async def yes_register_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Приятно познакомится! Теперь запишу в БД!")


@router.callback_query(F.data == register_callback.no)
async def no_register_callback_handler(
    callback_query: CallbackQuery, state: FSMContext
):
    await callback_query.message.answer("Попробуем еще раз!")
    await reg_command_handler(message=callback_query.message, state=state)
