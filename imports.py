import asyncio
import random
import os
import time
# import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import AdminFilter
from aiogram.dispatcher import filters

API_TOKEN = os.getenv('API_TOKEN')

# webhook settings
# WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_HOST = ''
WEBHOOK_PATH = f'/{API_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 8080

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig()

import json

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, )

import pyrogram
ubot = pyrogram.Client(
  ':memory:', 
  bot_token=API_TOKEN,
  api_id=94575,
  api_hash='a3406de8d171bb422bb6ddf3bbd800e2', 
  no_updates=True,
)

@ubot.on_message()
def update_rec(app, m):
	print('update! why?')

async def start_ubot(ubot):
	await ubot.start()
	print(await ubot.get_me())

asyncio.ensure_future(start_ubot(ubot))

from mongo import db

chats = db.bot_tag.chats
# querys = db.search_bot.querys

# links_store = db.rbrowse.links
