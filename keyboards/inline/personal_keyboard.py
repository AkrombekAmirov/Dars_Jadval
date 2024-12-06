from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

yonalish_nomi_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Maktabgacha talim tashkiloti tarbiyachisi',
                                 callback_data="faculty0"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha talim tashkiloti psixologi",
                                 callback_data="faculty1"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha talim tashkiloti direktori", callback_data="faculty2"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha talim tashkiloti metodisti", callback_data="faculty3"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha talim tashkiloti musiqa rahbari", callback_data="faculty4"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha ta`lim tashkiloti tashkilot oshpazi",
                                 callback_data="faculty5"),
        ],
        [
            InlineKeyboardButton(text="Maktabgacha talim tashkiloti defektolog/logopedi", callback_data="faculty6"),
        ],
        [
            InlineKeyboardButton(text="Oilaviy nodavlat",
                                 callback_data="faculty7"),
        ]
    ])

faculty_group = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-guruh",
                                 callback_data="group0"),
        ],
        [
            InlineKeyboardButton(text="2-guruh",
                                 callback_data="group1"),
        ],
        [
            InlineKeyboardButton(text="3-guruh",
                                 callback_data="group2"),
        ],
        [
            InlineKeyboardButton(text="4-guruh",
                                 callback_data="group3"),
        ],
        [
            InlineKeyboardButton(text="5-guruh",
                                 callback_data="group4"),
        ]
])