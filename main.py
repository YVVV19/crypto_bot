import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardRemove,
)

from parsing import Pair, get_symbol_keyboard, get_price
from data import get_answer
from keyboard import Answer, answer_keyboard_markup

class Form(StatesGroup):
    name = State()
    like_rate = State()


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
form_router = Router()
pair_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Form.name)
    await message.answer(
        "What is your name?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("Cancel"))
@form_router.message(F.text.casefold() == "Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.like_rate)
    await message.answer(
        f"Nice to meet you,{html.quote(message.text)}! \nDo you want to see the exchange rates?",
        )
    #MAKING KEYBOARD
    data = get_answer()
    markup = answer_keyboard_markup(answer_list=data)
    await message.answer(
        f"Click yes if you want and no if you don`t",
        reply_markup=markup,
    )
   

@form_router.callback_query(Answer.filter(F.name =="no"))
async def process_dont_want(query: CallbackQuery, callback_data: Answer, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await query.message.answer("See you later.", reply_markup=ReplyKeyboardRemove())


@form_router.callback_query(Answer.filter())
async def process_want(query:CallbackQuery, callback_data: Answer) -> None:
    await query.message.answer(
        "Click on the button of the selected currency",
        reply_markup=get_symbol_keyboard(),
    )


@pair_router.callback_query(Pair.filter())
async def pair_hanlder(callback: CallbackQuery, callback_data: Pair):

    await callback.message.answer(
        text=f"{get_price(str(callback_data))}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(form_router)
    dp.include_router(pair_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
