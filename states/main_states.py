from aiogram.dispatcher.filters.state import State,StatesGroup

class Registration(StatesGroup):
    name:str = State()
    surname:str = State()
    age:int = State()