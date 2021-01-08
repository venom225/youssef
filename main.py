from imports import asyncio
from imports import dp, bot, start_webhook, executor, types
from imports import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT

import sys, traceback
# from imports import ubot, chats
from imports import *
@dp.message_handler(
  commands=['ping'],
  run_task=True)
async def ping(message: types.Message):
  try:
    all_vars = {**locals(), **globals()}
    all_vars_size = {k: sys.getsizeof(v) for k, v in all_vars.items()}
    sorted_size = [(k, all_vars_size[k]) for k in sorted(all_vars_size, key=all_vars_size.get, reverse=True)]
    text = '\n'.join([f'- {k}: {v}' for k, v in sorted_size[:10]])

    await message.reply(text)
  except Exception as e:
    print(e)
    traceback.format_exc()

import chats
import pm

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def after(message):
    pass

async def on_startup(dp):
    await dp.skip_updates()
    # await bot.set_webhook(WEBHOOK_URL)
    # await bot.get_me()
    print(await bot.me)
    # insert code here to run it after start

async def on_shutdown(dp):
    # logging.warning('Shutting down..')
    pass

# input(111)
# if __name__ == '__main__':
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )
print('HEERERERERERE')

loop = asyncio.get_event_loop()  
loop.run_until_complete(on_startup(dp))
executor.start_polling(dp, skip_updates=True)