from imports import bot, dp, types
from imports import filters
from imports import asyncio

from help import get_chat, save_chat, inuse_chats
from help import auth, get_mentions


@dp.message_handler(
  lambda m: m.chat.type in ['private'],
  commands = ['cancel', 'stop', 'стоп'], 
  run_task=True)
@dp.message_handler(
  lambda m: m.chat.type in ['private'],
  filters.RegexpCommandsFilter(regexp_commands=['set_?([a-z0-9]+)_([a-z0-9]+)']),
  run_task=True)
async def settings(message: types.Message):
  kb = types.InlineKeyboardMarkup()
  kb.add(
    types.InlineKeyboardButton(
      'Добавить бота в чат',
      url = f't.me/{(await bot.me).username}?startgroup=1',
    )
  )
  
  await message.reply('Эту команду надо использовать в чате!', reply_markup=kb)
