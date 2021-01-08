from imports import chats
from imports import random, time
from imports import types
from imports import AdminFilter
from imports import ubot, bot


inuse_chats = {}

async def get_chat(chat_id):
  user_rec = await chats.find_one({'_id': chat_id})
  if user_rec: 
    user_rec['lang'] = user_rec.get('lang', 'ru')
    return user_rec

  # lang='en'
  # ask_lang=True
  # if hasattr(user, 'language_code') and user.language_code:
  #   user.language_code=user.language_code.lower()
  #   if 'ru' in user.language_code:
  #     lang='ru'
  #     ask_lang=False
  #   elif 'en' in user.language_code:
  #     lang='en'
  #     ask_lang=False
  # else:
  #   lang = 'en'

  user_rec = dict(
    _id=chat_id,
    lang='ru',
    all='admin',
    admin='all',
    jointime=time.time(),
    inuse='',
    # ask_lang=ask_lang,
    # first_name=user.first_name,
    # last_name=user.last_name,
    # full_name=f'{user.first_name} {user.last_name}' if user.last_name else user.first_name,
  )

  await chats.insert_one(user_rec)
  return user_rec

async def save_chat(chat_rec):
  await chats.update_one({'_id': chat_rec['_id']}, {'$set': chat_rec}, upsert=True)



async def auth(method, message):
  Filter = AdminFilter()

  if method == 'set':
    return await Filter.check(message)

  if method in ['all', 'admin']:
    chat_rec = await get_chat(message.chat.id)

    if chat_rec[method] == 'noone':
      return False
    if chat_rec[method] == 'all':
      return True

    return await Filter.check(message)

  raise ValueError('Invalid method')
  # return await Filter.check(message)    


def get_user_name(user):
  if user.last_name:
    return f'{user.first_name} {user.last_name}'
  return user.first_name

async def get_mentions(chat_id, command):
  members = ubot.iter_chat_members(
    chat_id,
    filter = 'administrators' if command == 'admin' else 'all',
  )

  chunk = []
  async for member in members:
    if member.user.is_deleted or member.user.is_bot:
      continue
    chunk.append(member)

    if len(chunk) == 5:
      yield ', '.join([f'<a href="tg://user?id={member.user.id}">{get_user_name(member.user)}</a>' for member in chunk])
      chunk = []

  if chunk:
    yield ', '.join([f'<a href="tg://user?id={member.user.id}">{get_user_name(member.user)}</a>'])


def field_to_dict(field):
  if isinstance(field, dict):
    return {k: field_to_dict(v) for k, v in field.items()}
  if isinstance(field, list):
    return [field_to_dict(v) for v in field]
  
  to_python = getattr(field, 'to_python', None)
  # print(f'{type(field)}: {bool(to_python)}')

  if not to_python:
    return field
  
  obj = to_python()
  
  if isinstance(obj, dict):
    return {k: field_to_dict(v) for k, v in obj.items()}
  if isinstance(obj, list):
    return [field_to_dict(v) for v in obj]
  return obj

def dict_to_message(conf):
  return types.Message(conf)
