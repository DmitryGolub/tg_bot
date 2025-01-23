from aiogram import Router
from aiogram.types import CallbackQuery

from filters.callbacks import CompleteTaskCallback
from database.database import complete_task


router = Router()


@router.callback_query(CompleteTaskCallback.filter())
async def command_complete_task(callback: CallbackQuery, callback_data: CompleteTaskCallback):
    task_id = callback_data.task_id

    await complete_task(task_id)

    await callback.message.edit_text(text="Выполнено", reply_markup=None)
    await callback.answer()
