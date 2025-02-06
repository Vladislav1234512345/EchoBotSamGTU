__all__ = ("router",)


from .register_callback_command import router as callback_command_register_router
from aiogram import Router


router = Router(name=__name__)
router.include_router(router=callback_command_register_router)
