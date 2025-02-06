from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.values.callback.base_callbacks_values import register_callback


def register_keyboard() -> InlineKeyboardMarkup:

    yes_button = InlineKeyboardButton(text="Да", callback_data=register_callback.yes)
    no_button = InlineKeyboardButton(text="Нет", callback_data=register_callback.no)

    inline_keyboard = [[yes_button], [no_button]]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)
