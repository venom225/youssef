from imports import bot, dp, types
from imports import filters
from imports import asyncio

from help import get_chat, save_chat, inuse_chats
from help import auth, get_mentions


@dp.message_handler(
  lambda m: m.chat.type in ['group', 'supergroup'],
  lambda m: bool(inuse_chats.get(m.chat.id, False)),
  commands = ['cancel', 'stop', 'стоп'], 
  run_task=True)
async def cancel(message: types.Message, regexp=None):
  command = inuse_chats[message.chat.id]

  if not await auth(command, message):
    return
  
  inuse_chats[message.chat.id] = False
  await message.reply(
    'Остановлено'
  )

def raiseit(e):
  raise e

chat_sets = {
  'all': lambda v: v if v in ['all', 'admin', 'noone'] else raiseit(ValueError()),
  'admin': lambda v: v if v in ['all', 'admin', 'noone'] else raiseit(ValueError()),
  'timeout': lambda v: int(v) if v.isdigit() else raiseit(ValueError()),
}
@dp.message_handler(
  lambda m: m.chat.type in ['group', 'supergroup'],
  filters.RegexpCommandsFilter(regexp_commands=['set_?([a-z0-9]+)_([a-z0-9]+)']),
  run_task=True)
async def settings(message: types.Message, regexp_command):
  key = regexp_command.group(1)
  value = regexp_command.group(2)

  try:
    value = chat_sets.get(
      key,
      lambda v: raiseit(ValueError()),
    )(value)
  except ValueError:
    err_alert = await message.reply('Неправильная команда. Может, /help?')
    await asyncio.sleep(3)
    await err_alert.delete()
    return
  
  if not await auth('set', message):
    err_notify = await message.answer('Эту команду могут использовать только админы')
    await asyncio.sleep(5)
    await err_notify.delete()
    return


  await save_chat({
    '_id': message.chat.id,
    key: value,
  })

  if key in ['all', 'admin']:
    await message.reply(f'''
Хорошо, теперь {
  {
  'all': f'команду @{key} смогут использовать все',
  'admin': f'команду @{key} смогут только админы',
  'noone': f'команда @{key} отключена',
  }[value]
}.''')
  elif key in ['timeout']:
    await message.reply(
      f'''
Хорошо, таймаут установлен в значение {value} минут.
      '''
    )
