from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.values.callback.base_callbacks_values import bot_game_callback


def bot_game_keyboard() -> InlineKeyboardMarkup:

    yes_button = InlineKeyboardButton(text="Да", callback_data=bot_game_callback.yes)
    no_button = InlineKeyboardButton(text="Нет", callback_data=bot_game_callback.no)

    inline_keyboard = [[yes_button], [no_button]]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)
