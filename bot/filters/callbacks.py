from aiogram.filters.callback_data import CallbackData


class CompleteTaskCallback(CallbackData, prefix="complete task"):
    task_id: int
