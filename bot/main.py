import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN

from handlers import register_all_handlers
from callbacks import register_all_callbacks
from utils import reminder


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
