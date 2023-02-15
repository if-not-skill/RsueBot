import asyncio
import logging
from os import getenv

from telebot.async_telebot import AsyncTeleBot

log = logging.getLogger('TelegramBot')
bot = AsyncTeleBot(getenv('TOKEN'))
__name = "[TelegramBot]"


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    log.info(f"{__name} {message.chat.id} /start")
    await bot.send_message(message.chat.id, "Hello. I'm RsueBot.")


def start_bot():
    asyncio.run(bot.polling())
