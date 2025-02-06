__all__ = ("router",)


from .base_commands import router as base_commands_router
from .message_commands import router as message_commands_router
from .callback_commands import router as callback_commands_router
from aiogram import Router


router = Router(name=__name__)
router.include_routers(
    base_commands_router, message_commands_router, callback_commands_router
)
