from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from utils import (
    search_title as search,
    get_title_detail_info,
    get_text_for_collection,
    get_text_for_search
)
from services import (
    add_title_to_collection,
    get_user,
    get_user_collection,
    remove_title_from_collection,
    get_or_create_title,
)

from texts.messages import Text as t
from texts.markups import Markup as m


collection_router: Router = Router(name=__name__)


@collection_router.message(Command('collection'))
async def my_collection(msg: Message) -> None:
    username = msg.chat.username
    user = await get_user(username)
    titles = await get_user_collection(user)

    for title in titles:
        answer_text: str = await get_text_for_collection(title)
        btn1 = types.InlineKeyboardButton(
            text=m.DELETE_FROM_COLLECTION.value,
            callback_data=f'delete_{title.id}'
        )
        btn2 = types.InlineKeyboardButton(
            text=m.DETAIL.value,
            callback_data=f'detail_{title.kinopoisk_id}'
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])

        await msg.answer_photo(title.image_url, disable_notification=True,)
        await msg.answer(
            answer_text,
            reply_markup=markup,
            disable_notification=True,
        )


@collection_router.message()
async def search_title(msg: Message) -> None:
    titles = await search(msg.text)
    for title in titles[:5]:
        answer_text: str = await get_text_for_search(title)
        btn1 = types.InlineKeyboardButton(
            text=m.COLLECT.value,
            callback_data=f'id_{title.get('id')}'
        )
        btn2 = types.InlineKeyboardButton(
            text=m.DETAIL.value,
            callback_data=f'detail_{title.get('id')}'
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])

        await msg.answer_photo(title.get('image'), disable_notification=True,)
        await msg.answer(
            answer_text,
            reply_markup=markup,
            disable_notification=True,
        )


@collection_router.callback_query(F.data.startswith('detail_'))
async def detail_title(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    title = await get_or_create_title(id)

    await callback.message.answer_photo(title.image_url)
    await callback.message.answer(await get_title_detail_info(title),)
    await callback.answer()


@collection_router.callback_query(F.data.startswith('delete_'))
async def delete_from_collection(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    username = callback.message.chat.username
    user = await get_user(username)

    await remove_title_from_collection(user, id)
    await callback.message.answer(t.REMOVED.value)
    await callback.answer()


@collection_router.callback_query(F.data.startswith('id_'))
async def add_to_collection(callback: types.CallbackQuery) -> None:
    kinopoisk_id = callback.data.split('_')[-1]
    username = callback.message.chat.username
    user = await get_user(username)
    title, is_created = await add_title_to_collection(kinopoisk_id, user)

    if not is_created:
        await callback.message.answer(t.ALREADY_IN_COLLECTION.value)
    else:
        await callback.message.answer(
            t.ADD_TO_COLLECTION.value.format(title.name)
        )
    await callback.answer()
