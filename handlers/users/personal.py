from keyboards.inline import faculty_file_map2, file_name_map, yonalish_nomi_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import TelegramAPIError, Throttled
from tenacity import retry, stop_after_attempt, wait_exponential
from file_service import get_file_path
from aiocache import cached
from functools import wraps
from aiogram import types
from loader import dp
import logging

# Yo'nalish va guruhlar sonini ko'rsatuvchi lug'at
yonalishlar = {
    "faculty0": 7,
    "faculty1": 1,
    "faculty2": 5,
    "faculty3": 2,
    "faculty4": 2,
    "faculty5": 2,
    "faculty6": 1,
    "faculty7": 2,
}

# Logging sozlamalari
logging.basicConfig(filename='bot.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Throttling uchun dekorator
def throttled_callback(rate_limit=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(call, *args, **kwargs):
            try:
                await dp.throttle(rate=rate_limit)
                return await func(call, *args, **kwargs)
            except Throttled as e:
                logging.warning(f"Throttling cheklovi: {e}")
                await call.answer("So‘rov tezligi cheklangan, qayta urinib ko‘ring.")

        return wrapper

    return decorator


# Yo'nalish keyboardi
def yonalish_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for yonalish in yonalishlar.keys():
        keyboard.add(InlineKeyboardButton(yonalish, callback_data=f"yonalish_{yonalish}"))
    return keyboard


# Guruh tanlash uchun keyboard
def guruh_keyboard(yonalish):
    keyboard = InlineKeyboardMarkup(row_width=3)
    guruh_soni = yonalishlar[yonalish]
    for i in range(1, guruh_soni + 1):
        keyboard.add(InlineKeyboardButton(f"{i} - guruh", callback_data=f"guruh_{yonalish}_{i}"))
    return keyboard


@dp.message_handler(commands=["start"])
async def bot_personal(message: types.Message):
    """Foydalanuvchini boshlash uchun yo'nalishlarni tanlashga yo'naltiradi"""
    await message.answer("Yo'nalishingizni tanlang!", reply_markup=yonalish_nomi_keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("yonalish_"))
@throttled_callback(rate_limit=2)
async def yonalish_tanlash(call: types.CallbackQuery):
    """Yo'nalishni tanlash"""
    try:
        yonalish = call.data.split("_")[1]
        await call.message.answer(
            f"{faculty_file_map2.get(yonalish)} yo'nalishi uchun guruhni tanlang:",
            reply_markup=guruh_keyboard(yonalish)
        )
    except TelegramAPIError as e:
        logging.error(f"Telegram API xatosi: {e}")
        await call.message.answer("Xatolik yuz berdi. Keyinroq urinib ko‘ring.")
    except Exception as e:
        logging.error(f"Yo'nalishni tanlashda xatolik: {e}")
        await call.message.answer("Xatolik yuz berdi, qayta urinib ko‘ring.")


# Fayl yo'lini keshlangan holda olish
@cached(ttl=60)
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
async def cached_get_file_path(file_name):
    """Keshlangan holda fayl yo‘lini olish"""
    logging.info(f"Fayl yo'lini olish: {file_name}")
    return await get_file_path(file_name)


@dp.callback_query_handler(lambda call: call.data.startswith("guruh_"))
@throttled_callback(rate_limit=2)
async def guruh_tanlash(call: types.CallbackQuery):
    """Guruhni tanlash"""
    try:
        _, yonalish, guruh = call.data.split("_")
        await call.message.answer(f"Siz {faculty_file_map2.get(yonalish)} yo'nalishi - {guruh}-guruh dars jadvallari!")

        file_path = await cached_get_file_path(file_name_map.get(f"{yonalish}_{guruh}"))
        await call.message.answer_document(document=open(file_path, "rb"))

    except FileNotFoundError:
        logging.error(f"Fayl topilmadi: {file_name_map.get(f'{yonalish}_{guruh}')}")
        await call.message.answer("Kechirasiz, fayl topilmadi. Qayta urinib ko‘ring.")
    except TelegramAPIError as e:
        logging.error(f"Telegram API xatosi: {e}")
        await call.message.answer("Xatolik yuz berdi. Keyinroq urinib ko‘ring.")
    except Exception as e:
        logging.error(f"Guruhni tanlashda xatolik: {e}")
        await call.message.answer("Xatolik yuz berdi, qayta urinib ko‘ring.")
