from imports import bot, dp, types
from imports import filters
from imports import asyncio

from help import get_chat, save_chat, inuse_chats
from help import auth, get_mentions


@dp.message_handler(
  lambda m: m.chat.type in ['private'],
  commands = ['help', 'start', ], 
  run_task=True)
async def help(message: types.Message):
  kb = types.InlineKeyboardMarkup()
  kb.add(
    types.InlineKeyboardButton(
      'Добавить бота в чат',
      url = f't.me/{(await bot.me).username}?startgroup=1',
    )
  )
  
  await message.reply(f'''
Отправьте #admin (@admin) в группе с ботом, чтобы позвать всех админов или #all (@all), чтобы позвать всех.

Команды для настройки:
Команда @all:
Все: <code>/set_all_all</code>
Только админы: <code>/set_all_admin</code>
Отключить: <code>/set_all_noone</code>

Команда @admin:
Все: <code>/set_admin_all</code>
Только админы: <code>/set_admin_admin</code>
Отключить: <code>/set_admin_noone</code>

По всем вопросам: @dmmebot
  ''', reply_markup=kb)