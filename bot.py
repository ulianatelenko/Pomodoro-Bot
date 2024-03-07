import asyncio
import configparser

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from answers import responses
import keyboards

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(
    token=config.get('default', 'TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

kb_lang = keyboards.kb_lang
kb_opt_en = keyboards.kb_opt_en
kb_opt_ua = keyboards.kb_opt_ua


lang = {}
timers = {}

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
   await message.reply("Choose your language:", reply_markup=kb_lang)


@dp.message(Command("english"))
async def cmd_eng(message: types.Message):
   lang[message.from_user.id] = "en"
   await message.reply(responses[lang[message.from_user.id]]["Start_Message"].format(user=message.from_user.full_name), reply_markup=kb_opt_en)


@dp.message(Command("українська"))
async def cmd_ukr(message: types.Message):
   lang[message.from_user.id] = "ua"
   await message.reply(responses[lang[message.from_user.id]]["Start_Message"].format(user=message.from_user.full_name), reply_markup=kb_opt_ua)


@dp.message(Command("lang", "мова"))
async def cmd_lang(message: types.Message):
   user_language = lang.get(message.from_user.id)
   if user_language:
       await message.reply(responses[lang[message.from_user.id]]["Change_language_Message"], reply_markup=kb_lang)
   else:
       await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)


@dp.message(Command("rules", "правила"))
async def cmd_rules(message: types.Message):
   user_language = lang.get(message.from_user.id)
   if user_language:
       await message.reply(responses[lang[message.from_user.id]]["Rules_Message"])
   else:
       await message.reply(responses["en"]["Choosse language"])


@dp.message(Command("help", "допомога"))
async def cmd_help(message: types.Message):
   user_language = lang.get(message.from_user.id)
   if user_language:
       await message.reply(responses[user_language]["Help_Message"])
   else:
       await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)


@dp.message(Command("5", "10", "15", "20"))
async def start_pomodoro(message: types.Message):
   user_id = message.from_user.id
   user_language = lang.get(message.from_user.id)
   if user_language:
      if user_id in timers:
         if not timers[user_id][0].done():
            await message.reply(responses[lang[message.from_user.id]]["Already_active"])
            return
      if message.text in ["/5", "/10", "/15", "/20"]:
         duration = int(message.text.replace("/", ""))
         timers[user_id] = (asyncio.create_task(run_pomodoro(duration, user_id, message)), duration)
         await message.reply(responses[lang[message.from_user.id]]["Start_timer_Message"].format(duration=duration))
   else:
      await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)


@dp.message(lambda message: message.text.isnumeric())
async def start_free_pomodoro(message: types.Message):
   user_id = message.from_user.id
   user_language = lang.get(message.from_user.id)
   if not user_language:
      await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)
      return
   time = int(message.text)
   if time <= 120 and time >= 5:
         if user_id in timers and not timers[user_id][0].done():
            await message.reply(responses[lang[message.from_user.id]]["Already_active"])
            return
         duration = int(message.text)
         timers[user_id] = (asyncio.create_task(run_pomodoro(duration, user_id, message)), duration)
         await message.reply(responses[lang[message.from_user.id]]["Start_free_timer_Message"].format(time=time))
   else:
      await message.reply(responses[lang[message.from_user.id]]["Error_Message"])


@dp.message(Command("stop", "зупинити"))
async def stop_pomodoro(message: types.Message):
   user_id = message.from_user.id
   user_language = lang.get(message.from_user.id)
   if user_language:
      if user_id in timers:
           timers[user_id][0].cancel()
           await message.reply(responses[lang[message.from_user.id]]["Stop_timer_Message"])

      else:
           await message.reply(responses[lang[message.from_user.id]]["Not_active"])
   else:
      await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)


@dp.message(Command("repeat", "повторити"))
async def repeat_pomodoro(message: types.Message):
   user_language = lang.get(message.from_user.id)
   user_id = message.from_user.id
   if user_language:
      if user_id in timers and not timers[user_id][0].done():
           await message.reply(responses[lang[message.from_user.id]]["Already_active"])
           return
      duration = timers.get(user_id, [5, 5])[1]
      timers[user_id] = (asyncio.create_task(run_pomodoro(duration, user_id, message)), duration)
      await message.answer(responses[lang[message.from_user.id]]["Repeat_timer_Message"].format(duration=duration))
   else:
      await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)


async def run_pomodoro(duration, user_id, message):
   user_language = lang.get(message.from_user.id)
   if user_language:
      await asyncio.sleep(duration * 60)
      await message.reply(responses[lang[user_id]]["Timer_finished_Message"])
      timers.pop(user_id, None)
   else:
      await message.reply(responses["en"]["Choosse language"], reply_markup=kb_lang)
      

async def main():
   await dp.start_polling(bot)


if __name__ == '__main__':
   asyncio.run(main())
