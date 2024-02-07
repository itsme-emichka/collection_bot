from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from texts.messages import Text as t
from services import get_or_create_user


start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start(msg: Message) -> None:
    username: str = msg.chat.username
    first_name: str = msg.chat.first_name
    last_name: str = msg.chat.last_name
    btn = KeyboardButton(text='/collection')
    markup = ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)
    await msg.answer(t.START, reply_markup=markup)
    await get_or_create_user(username, first_name, last_name)
