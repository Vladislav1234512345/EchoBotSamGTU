from contextlib import asynccontextmanager

from aiogram import Bot
from logging import getLogger

import uvicorn

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI, Request

from src.container import configure_logging
from src.config import bot_settings, web_settings, logging_settings
from src.v1 import router as v1_router
from src import dp
import sys
import os


sys.path.insert(1, os.path.join(sys.path[0], ".."))


logger = getLogger(__file__)
configure_logging(level=logging_settings.LOGGING_LEVEL)

bot = Bot(
    token=bot_settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await bot.set_webhook(f"{web_settings.WEBHOOK_URL}{web_settings.WEBHOOK_PATH}")
        logger.info("Webhook установлен!")
        yield
    finally:
        logger.info("Webhook удален!")
        await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)
app.include_router(router=v1_router)


@app.post(web_settings.WEBHOOK_PATH, tags=["HOOKS"])
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot=bot, update=update)


if __name__ == "__main__":
    uvicorn.run(app=app, host=web_settings.WEB_HOST, port=web_settings.WEB_PORT)
