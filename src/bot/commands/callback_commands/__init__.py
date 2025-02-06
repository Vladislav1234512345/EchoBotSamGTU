__all__ = ("router",)


from .register_callback_command import router as callback_command_register_router
from .bot_game_callback_command import router as bot_game_callback_command_router
from aiogram import Router


router = Router(name=__name__)
router.include_routers(
    callback_command_register_router, bot_game_callback_command_router
)
