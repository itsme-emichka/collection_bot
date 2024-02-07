from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from utils import search_title as search
from services import add_title_to_collection, get_user, get_user_collection

from texts.messages import Text as t


collection_router: Router = Router(name=__name__)


@collection_router.message(Command('collection'))
async def my_collection(msg: Message) -> None:
    username = msg.chat.username
    user = await get_user(username)
    titles = await get_user_collection(user)
    for title in titles:
        answer_text: str = (
            f'{title.id}\n' +
            f'{title.name}\n' +
            f'{title.release_year}\n' +
            f'{title.description}...'
        )
        await msg.answer(answer_text)


@collection_router.message()
async def search_title(msg: Message) -> None:
    titles = await search(msg.text)
    for title in titles[:5]:
        answer_text: str = (
            f'{title.get('id')}\n' +
            f'{title.get('name')}\n' +
            f'{title.get('year')}\n' +
            f'{title.get('description')[:300]}...'
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text='Коллекционировать',
                callback_data=f'id_{title.get('id')}'
            )
        )
        await msg.answer(answer_text, reply_markup=builder.as_markup())


@collection_router.callback_query(F.data.startswith('id_'))
async def add_to_collection(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    username = callback.message.chat.username
    user = await get_user(username)
    title, is_created = await add_title_to_collection(id, user)
    if not is_created:
        await callback.message.answer(t.ALREADY_IN_COLLECTION.value)
    else:
        await callback.message.answer(
            t.ADD_TO_COLLECTION.value.format(title.name)
        )
    await callback.answer()
