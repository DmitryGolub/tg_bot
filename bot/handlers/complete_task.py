from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.database import get_tasks_by_user_id, complete_task
from keyboards.keyboards import keyboard_complete


router = Router()


@router.message(Command("complete_task"))
async def command_update_task(message: Message) -> None:
    data = await get_tasks_by_user_id(message.from_user.id, status=False)
    if data:
        for task in data:
            await message.answer(f"<b>{task['task_title']}</b>\n"
                                 f"Начало: {datetime.strftime(task['task_start_date'], '%Y-%m-%d %H:%M')}\n"
                                 f"Конец: {datetime.strftime(task['task_end_date'], '%Y-%m-%d %H:%M')}\n"
                                 f"{'Выполнено' if task['status'] else 'Невыполнено'}",
                                 reply_markup=keyboard_complete(task['task_id'])
                                 )
    else:
        await message.answer("У Вас нет невыполненых задач. Вы большой молодец!")



