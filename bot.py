from aiogram import F, Bot, Dispatcher
from aiogram.types import BotCommand
from asyncio import run
import functions
from aiogram.filters import CommandStart, Command, and_f
from states import NewMember
from config import BOT_TOKEN
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up the database connection
engine = create_engine('postgresql://ChereAdmin:Qwerty123$@localhost:5432/Chere')
Session = sessionmaker(bind=engine)
Base = declarative_base()


dp = Dispatcher()

# async def startup_answer(bot:Bot):
#     await bot.send_message(6089066974, "Bot ishga tushdi!")

# async def shutdown_answer(bot:Bot):
#     await bot.send_message(6089066974, "Bot ishdan to'xtadi!")

async def start():
    # dp.startup.register(startup_answer)
    dp.message.register(functions.start_command_answer, CommandStart())
    dp.message.register(functions.start_command_answer, Command('new'))
    dp.message.register(functions.orders_answer, Command('orders'))
    dp.message.register(functions.help_answer, Command('help'))
    dp.message.register(functions.get_name_answer, NewMember.name)
    dp.message.register(functions.get_phone_answer, NewMember.phone)
    dp.message.register(functions.get_language_answer, NewMember.language)
    dp.message.register(functions.get_water_type_answer, NewMember.water)
    dp.message.register(functions.much_water, NewMember.much)
    dp.message.register(functions.get_location_answer, F.location)
    # dp.shutdown.register(shutdown_answer)

    bot = Bot(BOT_TOKEN)

    await bot.set_my_commands([
        BotCommand(command='/new', description="Yangi buyurtmalar berish"),
        BotCommand(command='/orders', description="Buyurtmalarni ko'rish"),
        BotCommand(command='/help', description="Operator bilan bog'lanish")
    ])
    await dp.start_polling(bot)

run(start())