from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import faculty_file_map2, file_name_map
from keyboards.inline import yonalish_nomi_keyboard
from file_service import get_file_path
from aiogram import types
from loader import dp

# Yo'nalishlar va guruhlar soni ro'yxati
# Yo'nalish nomi va har bir yo'nalishda nechta guruh borligini ko'rsatadigan lug'at.
yonalishlar = {
    "faculty0": 6,  # 1-yo'nalishda 5 ta guruh
    "faculty1": 0,  # 2-yo'nalishda 3 ta guruh
    "faculty2": 5,  # 3-yo'nalishda 7 ta guruh
    "faculty3": 2,  # Shu tarzda har bir yo'nalish uchun guruhlar sonini kiriting
    "faculty4": 3,
    "faculty5": 2,
    "faculty6": 1,
    "faculty7": 1,
}

guruh_yunalish_map = {
    "faculty0_1": "faculty0",
}

# Yo'nalish nomlarini tanlash uchun keyboard
def yonalish_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for yonalish in yonalishlar.keys():
        keyboard.add(InlineKeyboardButton(yonalish, callback_data=f"yonalish_{yonalish}"))
    return keyboard

# Guruhlarni tanlash uchun keyboard
def guruh_keyboard(yonalish):
    keyboard = InlineKeyboardMarkup(row_width=3)
    guruh_soni = yonalishlar[yonalish]
    for i in range(1, guruh_soni + 1):
        keyboard.add(InlineKeyboardButton(f"{i} - guruh", callback_data=f"guruh_{yonalish}_{i}"))
    return keyboard

@dp.message_handler(commands=["start"])
async def bot_personal(message: types.Message):
    await message.answer("Yo'nalishingizni tanlang!", reply_markup=yonalish_nomi_keyboard)

@dp.callback_query_handler(lambda call: call.data in ["faculty0", "faculty1", "faculty2", "faculty3", "faculty4", "faculty5", "faculty6", "faculty7"])
async def yonalish_tanlash(call: types.CallbackQuery):
    yonalish = call.data
    await call.message.answer(f"{faculty_file_map2.get(yonalish)} yo'nalishi uchun guruhni tanlang:", reply_markup=guruh_keyboard(yonalish))

@dp.callback_query_handler(lambda call: call.data.startswith("guruh_"))
async def guruh_tanlash(call: types.CallbackQuery):
    _, yonalish, guruh = call.data.split("_")
    await call.message.answer(f"Siz {faculty_file_map2.get(yonalish)} yo'nalishi - {guruh}-guruh dars jadvallari!")
    await call.message.answer_document(document=open(f"{await get_file_path(file_name_map.get(f'{yonalish}_{guruh}'))}", "rb"))
