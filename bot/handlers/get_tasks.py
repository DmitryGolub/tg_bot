from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from bot.database.database import get_tasks_by_user_id


router = Router()


@router.message(Command("get_tasks"))
async def command_get_tasks(message: Message) -> None:
    data = await get_tasks_by_user_id(message.from_user.id, False)
    if data:
        for task in data:
            await message.answer(f"<b>{task['task_title']}</b>\n"
                                 f"Начало: {datetime.strftime(task['task_start_date'], '%Y-%m-%d %H:%M')}\n"
                                 f"Конец: {datetime.strftime(task['task_end_date'], '%Y-%m-%d %H:%M')}\n"
                                 f"{'Выполнено' if task['status'] else 'Невыполнено'}")
    else:
        await message.answer("У Вас нет невыполненых задач. Вы большой молодец!")

