from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import AddTask
from keyboards.keyboards import keyboard_choose_day, keyboard_reminder, keyboard_choose_time
from database.database import add_task

router = Router()


@router.message(Command("add_task"))
async def command_add_task(message: Message, state: FSMContext) -> None:
    await state.set_state(AddTask.title)
    await message.answer("Какое название?")


@router.message(AddTask.title)
async def process_title(message: Message, state: FSMContext) -> None:
    # запоминаем текст
    await state.update_data(title=message.text)
    # меняем состояние
    await state.set_state(AddTask.date)
    # отображаем кнопки для выбора даты
    await message.answer("На когда хотите запланировать задачу?",
                         reply_markup=keyboard_choose_day()
                         )


@router.message(AddTask.date, F.text == "Сегодня")
async def process_today_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date=datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
    await state.set_state(AddTask.start_time)
    await message.answer("Какое время?\nПрмер: 11:00",
                         reply_markup=ReplyKeyboardRemove())


@router.message(AddTask.date, F.text == "Завтра")
async def process_tomorrow_date(message: Message, state: FSMContext) -> None:
    await state.update_data(
        date=(datetime.today() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
    await state.set_state(AddTask.start_time)
    await message.answer("Какое время?\nПрмер: 11:00",
                         reply_markup=ReplyKeyboardRemove())


@router.message(AddTask.start_time)
async def process_start_time(message: Message, state: FSMContext) -> None:
    hours, minutes = map(int, message.text.split(":"))
    data = await state.update_data()
    await state.update_data(start_time=data['date'] + timedelta(hours=hours, minutes=minutes))
    await state.set_state(AddTask.end_time)
    await message.answer("Сколько вы планируете выполнять по времени?",
                         reply_markup=keyboard_choose_time()
                         )


@router.message(AddTask.end_time)
async def process_end_time(message: Message, state: FSMContext) -> None:
    data = await state.update_data()
    end_time = data['start_time']
    if message.text == "30 мин":
        end_time += timedelta(minutes=30)
    elif message.text == "1 час":
        end_time += timedelta(hours=1)
    elif message.text == "1 час 30 мин":
        end_time += timedelta(hours=1, minutes=30)

    await state.update_data(end_time=end_time)

    await state.set_state(AddTask.reminder)

    await message.answer("Когда вам напомнить о задаче?",
                         reply_markup=keyboard_reminder()
                         )


@router.message(AddTask.reminder)
async def process_end_time(message: Message, state: FSMContext) -> None:
    data = await state.update_data()

    minutes = int(message.text.split()[1])
    reminder = data['start_time'] - timedelta(minutes=minutes)

    await add_task(data['title'],
                   data['start_time'],
                   data['end_time'],
                   reminder,
                   message.from_user.id)

    await message.answer(f"Название: {data['title']}\n"
                         f"Начало: {datetime.strftime(data['start_time'], '%Y-%m-%d %H:%M')}\n"
                         f"Конец: {datetime.strftime(data['end_time'], '%Y-%m-%d %H:%M')}\n"
                         f"Статус: Невыполнено\n",
                         reply_markup=ReplyKeyboardRemove())

    await state.clear()
