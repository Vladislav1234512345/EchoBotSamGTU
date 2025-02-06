from aiogram import Dispatcher
from src.bot import router as bot_router


dp = Dispatcher()
dp.include_router(bot_router)
