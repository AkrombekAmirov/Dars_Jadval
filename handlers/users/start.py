from keyboards.inline.personal_keyboard import yonalish_nomi_keyboard
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from aiogram import types
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id == str(ADMINS):
        await message.answer(f"Salom, {message.from_user.full_name}!")
    else:
        await message.answer(f"Salom, {message.from_user.full_name}!\nYo'nalishingizni tanlang", reply_markup=yonalish_nomi_keyboard)
