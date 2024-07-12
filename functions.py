from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import NewMember
from keyboards import contact_markup, location_markup, lang_markup, water_button_markup, yes_or_no_murkup
import psycopg2
import datetime

now = datetime.datetime.now()
commands = f""" Buyruqlar:
        /new - Buyurtma qilish
        /orders - Buyurtmalarim
        /help - Qo'llab-quvvatlash
    """

db_name = "Chere"
db_user = "ChereAdmin"
db_password = "Qwerty123$"
db_host = "localhost"
db_port = "5432"
try:
    # PostgreSQL-ga ulanish
    connection= psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    cursor = connection.cursor()
    print("PostgreSQL-ga muvaffaqiyatli ulandik")

except (Exception, psycopg2.Error) as error:
    print("PostgreSQL-ga ulanishda xatolik:", error)


async def start_command_answer(message:Message, state:FSMContext):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM user_usermodel WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        await message.answer("Ismingizni kiriting")
        return await state.set_state(NewMember.name)
    await message.answer("Mahsulot turini kiriting", reply_markup=water_button_markup)
    return await state.set_state(NewMember.water)

async def new_command_answer(message:Message, state:FSMContext):
    await message.answer("Mahsulot turini kiriting")
    await state.set_state(NewMember.water)

async def get_name_answer(message:Message, state:FSMContext):
    if message.text.isalpha():
        await state.update_data(name = message.text)
        await message.answer("Ismingiz qabul qilindi!")
        await message.answer("Kantaktingizni tugma orqali kiriting", reply_markup=contact_markup)
        await state.set_state(NewMember.phone)
    else: await message.reply("Ismingiz faqatgina harflardan iborat bo'lishi kerak!")

async def get_phone_answer(message:Message, state:FSMContext):
    if message.contact.phone_number:
        await state.update_data(phone = message.contact.phone_number)
        await message.answer("Kantaktingiz qabul qilindi!", reply_markup=lang_markup)
        await message.answer("Tilni kiriting.")
        await state.set_state(NewMember.language)
    

async def get_language_answer(message:Message, state:FSMContext):
    data = await state.get_data()
    cursor.execute("INSERT INTO user_usermodel (telegram_id, full_name, phone, lang, password, last_login, is_superuser, is_staff, is_active, date_joined, created_at, updated_at, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
               (message.from_user.id, data.get('name'), data.get('phone'), message.text, "", now, False, False, False, now, now, now, None))
    connection.commit()
    await state.update_data(lang = message.text)
    await message.answer("Til qabul qilindi!", reply_markup=water_button_markup)
    await message.answer("Mahsulot turini kiriting")
    await state.set_state(NewMember.water)

async def get_water_type_answer(message:Message, state:FSMContext):
    await state.update_data(water = message.text)
    await message.answer("Mahsulot turi qabul qilindi")
    await message.answer("Miqdorini kiriting")
    await state.set_state(NewMember.much)

async def much_water(message:Message, state:FSMContext):
    data = await state.get_data()
    await message.answer("Buyurtma qabul qilindi", reply_markup=yes_or_no_murkup)
    if data.get('name'):
        await message.answer(f"Ma'lumotlaringiz:\n\t\tIsmingiz: {data.get('name')}\n\t\tTel: {data.get('phone')}\n\t\tTil: {data.get('lang')}\n\t\tWater: {data.get('water')}\n\t\tMuch: {message.text} ta")
        await message.answer("Buyurtma jo'natilsinimi?")
        await state.clear()
    await message.answer(f"Buyurtmangiz:\n\t\tMahsulot: {data.get('water')}\n\t\tSoni: {message.text} ta")
    
async def yes_or_no_answer(message:Message):
    if message.text == "Tasdiqlash":
        await message.answer("Tasdiqlandi")
    elif message.text == "Bekor qilish":
        await message.answer("Bekor qilindi")

async def get_location_answer(message:Message):
    await message.answer("Joylashuvingizni kiriting", reply_markup=location_markup)

async def orders_answer(message:Message):
    await message.answer("Orders:")

async def help_answer(message:Message):
    await message.answer("Operator tel: +998977777777")

async def location_answer(message:Message):
    await message.answer("Joylashuv qabul qilindi")