__all__ = ("router",)

from .text_message_commands import router as text_message_commands_router
from aiogram import Router


router = Router(name=__name__)
router.include_router(text_message_commands_router)
