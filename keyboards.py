from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import psycopg2
from psycopg2 import Error

# PostgreSQL ulanish parametrlari
db_name = "Chere"
db_user = "ChereAdmin"
db_password = "Qwerty123$"
db_host = "localhost"
db_port = "5432"

try:
    # PostgreSQL-ga ulanish
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    cursor = connection.cursor()
    print("PostgreSQL-ga muvaffaqiyatli ulandik")

except (Exception, Error) as error:
    print("PostgreSQL-ga ulanishda xatolik:", error)

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

cursor.execute("SELECT name FROM product_productmodel")
rows = cursor.fetchall()

water_button_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=str(row[0])) for row in rows 
    ]
],resize_keyboard=True)

yes_or_no_murkup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Tasdiqlash"),
        KeyboardButton(text="Bekor qilish")
    ]  
],resize_keyboard=True)