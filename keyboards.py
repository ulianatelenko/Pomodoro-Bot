from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_lang = ReplyKeyboardMarkup(
   keyboard=[
      [
         KeyboardButton(text="/english"),
         KeyboardButton(text="/українська"),
      ],
   ],
      resize_keyboard= True,
      one_time_keyboard= True,
      selective= True,
      input_field_placeholder= "Choose language/Виберіть мову"
)

kb_opt_en = ReplyKeyboardMarkup(
   keyboard=[
       [
         KeyboardButton(text="/rules"),
         KeyboardButton(text="/help"),
         KeyboardButton(text="/repeat"),
         KeyboardButton(text="/lang"),
      ],
      [
         KeyboardButton(text="/stop"),
         KeyboardButton(text="/5"),
         KeyboardButton(text="/10"),
      ],
      [
         KeyboardButton(text="/15"),
         KeyboardButton(text="/20"),
      ],
   ],
      resize_keyboard= True,
      one_time_keyboard= True,
      selective= True,
      input_field_placeholder= "Choose option"
)

kb_opt_ua = ReplyKeyboardMarkup(
   keyboard=[
       [
         KeyboardButton(text="/правила"),
         KeyboardButton(text="/допомога"),
         KeyboardButton(text="/мова"),
      ],
      [
         KeyboardButton(text="/зупинити"),
         KeyboardButton(text="/5"),
         KeyboardButton(text="/10"),
      ],
      [
         KeyboardButton(text="/повторити"),
         KeyboardButton(text="/15"),
         KeyboardButton(text="/20"),
      ],
   ],
      resize_keyboard= True,
      one_time_keyboard= True,
      selective= True,
      input_field_placeholder= "Виберіть опцію"
)