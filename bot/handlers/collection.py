from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from utils import search_title as search, get_title_detail_info
from services import (
    add_title_to_collection,
    get_user,
    get_user_collection,
    remove_title_from_collection,
    get_title,
)

from texts.messages import Text as t


collection_router: Router = Router(name=__name__)


@collection_router.message(Command('collection'))
async def my_collection(msg: Message) -> None:
    username = msg.chat.username
    user = await get_user(username)
    titles = await get_user_collection(user)
    for title in titles:
        answer_text: str = (
            f'<strong>{title.name}</strong> ({title.release_year})\n' +
            f'{title.description}'
        )
        btn1 = types.InlineKeyboardButton(
            text='Удалить из коллекции',
            callback_data=f'delete_{title.id}'
        )
        btn2 = types.InlineKeyboardButton(
            text='Подробнее',
            callback_data=f'detail_{title.id}'
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
        await msg.answer(answer_text, reply_markup=markup)


@collection_router.callback_query(F.data.startswith('delete_'))
async def delete_from_collection(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    username = callback.message.chat.username
    user = await get_user(username)
    await remove_title_from_collection(user, id)
    await callback.message.answer(t.REMOVED.value)
    await callback.answer()


@collection_router.callback_query(F.data.startswith('detail_'))
async def detail_title(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    title = await get_title(id)
    await callback.message.answer_photo(title.image_url)
    await callback.message.answer(await get_title_detail_info(title))


@collection_router.message()
async def search_title(msg: Message) -> None:
    titles = await search(msg.text)
    for title in titles[:5]:
        answer_text: str = (
            f'<strong>{title.get('name')}</strong> ({title.get('year')})\n' +
            # f'{title.get('')}'
            f'{title.get('description')[:300]}...'
        )
        btn1 = types.InlineKeyboardButton(
            text='Коллекционировать',
            callback_data=f'id_{title.get('id')}'
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
        await msg.answer(answer_text, reply_markup=markup)


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
