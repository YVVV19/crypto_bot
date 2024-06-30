from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class Answer(CallbackData, prefix="answer"):
    id: int
    name: str


def answer_keyboard_markup(
        answer_list: list[dict], offset: int | None = None, skip: int | None = None
                           ):
    builder = InlineKeyboardBuilder()
    builder.adjust(2)

    for index, film_data in enumerate(answer_list):
        callback_data = Answer(id=index, **film_data)
        builder.button(text=f"{callback_data.name}", callback_data=callback_data.pack())

    return builder.as_markup()