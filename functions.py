from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import NewMember
from keyboards import contact_markup, location_markup, lang_markup, water_button_markup, yes_or_no_murkup
import psycopg2
import datetime
from datetime import datetime
import json

now = datetime.now()
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
    await message.answer("Joylashuvingizni kiriting", reply_markup=location_markup)
    await state.set_state(NewMember.location)

async def get_name_answer(message:Message, state:FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Ismingiz qabul qilindi!")
    await message.answer("Kantaktingizni tugma orqali kiriting", reply_markup=contact_markup)
    await state.set_state(NewMember.phone)

async def get_phone_answer(message:Message, state:FSMContext):
    if message.contact.phone_number:
        await state.update_data(phone = message.contact.phone_number)
        await message.answer("Kantaktingiz qabul qilindi!")
        await message.answer("Tilni kiriting", reply_markup=lang_markup)
        await state.set_state(NewMember.language)
    

async def get_language_answer(message:Message, state:FSMContext):
    data = await state.get_data()
    cursor.execute("INSERT INTO user_usermodel (telegram_id, full_name, phone, lang, password, last_login, is_superuser, is_staff, is_active, date_joined, created_at, updated_at, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
               (message.from_user.id, data.get('name'), data.get('phone'), message.text, "", now, False, False, False, now, now, now, None))
    connection.commit()
    await state.update_data(lang = message.text)
    await message.answer("Til qabul qilindi!")
    await message.answer("Joylashuvingizni kiriting", reply_markup=location_markup)
    await state.set_state(NewMember.location)

async def get_location_answer(message:Message, state:FSMContext):
    await state.update_data(location_latitude = message.location.latitude, location_longitude=message.location.longitude)
    await message.answer("Joylashuv qabul qilindi")
    await message.answer("Mahsulot turini kiriting", reply_markup=water_button_markup)
    await state.set_state(NewMember.water)

async def get_water_type_answer(message:Message, state:FSMContext):
    await state.update_data(water = message.text)
    await message.answer("Mahsulot turi qabul qilindi")
    await message.answer("Miqdorini kiriting")
    await state.set_state(NewMember.much)

async def much_water(message:Message, state:FSMContext):
    data = await state.get_data()
    cursor.execute("SELECT id, price FROM product_productmodel WHERE name = %s", (data.get('water'),))
    product = cursor.fetchall()
    cursor.execute("SELECT id FROM user_usermodel WHERE telegram_id = %s", (int(message.from_user.id),))
    user = cursor.fetchall()
    user_id = user[0][0]
    now = datetime.now()
    product_id = product[0][0]
    product_price = product[0][1]
    total_price = int(message.text ) * product_price
    
    cursor.execute("INSERT INTO order_ordermodel (product_id, count, free_count, customer_id, longitude, latitude, product_price, total_price, condition, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   (product_id, int(message.text), 0, user_id, data.get('location_latitude'), data.get('location_longitude'), product_price, total_price, "Yaratildi", now, now))
    connection.commit()
    await message.answer("Buyurtma qabul qilindi")
    

async def orders_answer(message:Message):
    cursor.execute("SELECT id FROM user_usermodel WHERE telegram_id = %s", (int(message.from_user.id),))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        cursor.execute("SELECT * FROM order_ordermodel WHERE %s = customer_id ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        created_at = rows[0][1]
        formatted_date_time = created_at.strftime("%Y-%m-%d")
        products = rows[0][3]
        free_products = rows[0][4]
        product_price = rows[0][7]
        total_price = rows[0][8]
        condition = rows[0][9]
        if rows:
            await message.answer(
                f'Orders:\n'
                f"created_at: {formatted_date_time}\n"
                f"products: {products}\n"
                f"free products: {free_products}\n"
                f"product price: {product_price}\n"
                f"total price: {str(total_price)}\n"
                f"condition: {condition}"
            )
        else:
            await message.an("No orders found")
    else:
        await message.answer("User not found")

async def help_answer(message:Message):
    await message.answer("Operator tel: +998977777777")
