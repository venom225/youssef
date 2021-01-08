from imports import bot, dp, types
from imports import asyncio

from help import get_chat, save_chat, inuse_chats
from help import auth, get_mentions

import chats_settings
import chats_help

@dp.message_handler(
  lambda m: m.chat.type in ['group', 'supergroup'],
  lambda m: not bool(inuse_chats.get(m.chat.id, False)), 
  regexp='[@#](all|admin)', 
  run_task=True)
async def cmd_start(message: types.Message, regexp=None, command=None):
  if not command:
    command = regexp.group(1)

  if not await auth(command, message):
    return
  
  
  inuse_chats[message.chat.id] = command
  try:
    async for mention_text in get_mentions(message.chat.id, command):
      if not bool(inuse_chats.get(message.chat.id, False)):
        break
      await message.answer(
        f'{message.text}\n{mention_text}'
      )
      await asyncio.sleep(60/20)
  finally:
    inuse_chats[message.chat.id] = False
