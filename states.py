from aiogram.fsm.state import State, StatesGroup

class NewMember(StatesGroup):
    name = State()
    phone = State()
    language = State()
    water = State()
    much = State()
    location = State()