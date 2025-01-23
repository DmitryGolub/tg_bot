import asyncio
from datetime import datetime

from database.database import check_time_complete


async def remainder(bot) -> None:
    while True:
        time_now = datetime.today().replace(microsecond=0)

        data = await check_time_complete(time_now=time_now)
        for item in data:
            await bot.send_message(chat_id=int(item['user_id']),
                                   text=f"Напоминание !!\n"
                                        f"Название: {item['task_title']}\n"
                                        f"Начало: {datetime.strftime(item['task_start_date'], '%Y-%m-%d %H:%M')}\n"
                                        f"Конец: {datetime.strftime(item['task_end_date'], '%Y-%m-%d %H:%M')}\n"
                                        f"Статус: Невыполнено\n")

        await asyncio.sleep(3)
