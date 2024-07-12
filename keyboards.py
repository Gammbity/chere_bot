from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Kontakt yuborish", request_contact=True)
    ]
],resize_keyboard=True, is_persistent=True)

location_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Joylashuvni yuborish", request_location=True)
    ]
],resize_keyboard=True)

lang_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="uz"),
    KeyboardButton(text="ru")]
],resize_keyboard=True)

water_button_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="1L"),
        KeyboardButton(text="2L"),
        KeyboardButton(text="5L"),
        KeyboardButton(text="19L")
    ]
],resize_keyboard=True)

yes_or_no_murkup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Tasdiqlash"),
        KeyboardButton(text="Bekor qilish")
    ]  
],resize_keyboard=True)