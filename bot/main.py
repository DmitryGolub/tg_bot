import asyncio
from datetime import date, timedelta, datetime

from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN

from bot.handlers import register_all_handlers
from bot.callbacks import register_all_callbacks
from bot.utils import reminder


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    register_all_handlers(dp)
    register_all_callbacks(dp)

    await asyncio.gather(
        dp.start_polling(bot),
        reminder.remainder(bot)
    )


if __name__ == "__main__":
    asyncio.run(main())
