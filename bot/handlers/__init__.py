from aiogram import Dispatcher

from .start import router as start_router
from .add_task import router as add_task_router
from .complete_task import router as complete_task_router
from .get_tasks import router as get_tasks_router


def register_all_handlers(dp: Dispatcher):
    dp.include_routers(
        start_router,
        add_task_router,
        complete_task_router,
        get_tasks_router,
    )

