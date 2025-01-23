from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove


class CompleteTaskCallback(CallbackData, prefix="complete task"):
    task_id: int


def keyboard_reminder():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="за 5 минут"),
                KeyboardButton(text="за 1 минуту"),
                KeyboardButton(text="за 10 минут")
            ]
        ],
        resize_keyboard=True
    )

    return keyboard


def keyboard_complete(task_id):
    keyboard = InlineKeyboardMarkup(
                 inline_keyboard=[
                     [
                         InlineKeyboardButton(text="Вполнить",
                                              callback_data=CompleteTaskCallback(task_id=task_id).pack())
                     ]
                 ]
             )

    return keyboard


def keyboard_choose_day():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Сегодня"),
                KeyboardButton(text="Завтра")
            ]
        ],
        resize_keyboard=True,
    )

    return keyboard


def keyboard_choose_time():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="30 мин"),
                KeyboardButton(text="1 час"),
                KeyboardButton(text="1 час 30 мин")
            ]
        ],
        resize_keyboard=True,
    )

    return keyboard

