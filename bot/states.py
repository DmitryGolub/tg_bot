from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    title = State()
    date = State()
    start_time = State()
    end_time = State()
    reminder = State()


class Update(StatesGroup):
    task_id = State()
