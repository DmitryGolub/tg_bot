from aiogram import Router
from aiogram.filters import Command
from aiogram.types.message import Message

from bot.database.database import add_user


router = Router()


@router.message(Command("start"))
async def command_start(message: Message) -> None:
    answer = await add_user(message.from_user.id, message.from_user.username, message.from_user.first_name,
                            message.from_user.last_name)

    if answer == "All ready exists":
        await message.answer(f"Я вижу Вы здесь не в первые. Напомню, что я умею. "
                             f"Я помогу тебе создать и помотерть список задач. Смотри меню")
    else:
        await message.answer(f"Привет! Я помогу тебе создать и помотерть список задач. Смотри меню")
