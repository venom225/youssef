from imports import bot, dp, types
from imports import filters
from imports import asyncio

from help import get_chat, save_chat, inuse_chats
from help import auth, get_mentions


@dp.message_handler(
  lambda m: m.chat.type in ['group', 'supergroup'],
  commands = ['help', 'start', ], 
  run_task=True)
async def help(message: types.Message):
  chat_rec = await get_chat(message.chat.id)


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
Все: /set_all_all
Только админы: /set_all_admin
Отключить: /set_all_noone
<b>Сейчас {
  {
  'all': f'команду @all могут использовать все',
  'admin': f'команду @all могут только админы',
  'noone': f'команда @all отключена',
  }[chat_rec['all']]
}.</b>

Команда @admin:
Все: /set_admin_all
Только админы: /set_admin_admin
Отключить: /set_admin_noone
<b>Сейчас {
  {
  'all': f'команду @admin могут использовать все',
  'admin': f'команду @admin могут только админы',
  'noone': f'команда @admin отключена',
  }[chat_rec['admin']]
}.</b>

По всем вопросам: @dmmebot
  ''', reply_markup=kb)