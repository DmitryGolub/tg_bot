from aiogram import Dispatcher

from .complete_task import router as complete_task_router


def register_all_callbacks(dp: Dispatcher):
    dp.include_routers(
        complete_task_router,
    )
