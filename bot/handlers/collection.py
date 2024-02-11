from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command

from utils import (
    search_title as search,
    get_title_detail_info,
    get_text_for_collection,
    get_text_for_search,
    send_photo_if_exists,
)
from services import (
    add_title_to_collection,
    get_user,
    get_user_collection,
    remove_title_from_collection,
    get_or_create_title,
)

from texts.messages import Text as t
from markups.inline_markups import (
    get_collection_markup,
    get_filter_markup,
    get_search_markup,
)


collection_router: Router = Router(name=__name__)

TITLES_NUM_IN_SEARCH: int = 5


@collection_router.message(Command('collection'))
async def my_collection(msg: Message) -> None:
    username = msg.chat.username
    user = await get_user(username)
    titles = await get_user_collection(user)

    for title in titles:
        await send_photo_if_exists(msg, title.image_url)
        await msg.answer(
            await get_text_for_collection(title),
            reply_markup=get_collection_markup(title),
            disable_notification=True,
        )


@collection_router.message(Command('filter'))
async def filter_collection(msg: types.Message) -> None:
    await msg.answer(
        t.CHOOSE_TYPE.value,
        reply_markup=get_filter_markup()
    )


@collection_router.callback_query(F.data.startswith('filter_'))
async def get_filtered_collection(callback: types.CallbackQuery) -> None:
    username = callback.message.chat.username
    filters = {'type__slug': callback.data.split('_')[-1]}
    user = await get_user(username)
    titles = await get_user_collection(user, **filters)

    for title in titles:
        await send_photo_if_exists(callback.message, title.image_url)
        await callback.message.answer(
            await get_text_for_collection(title),
            reply_markup=get_collection_markup(title),
            disable_notification=True,
        )


@collection_router.message()
async def search_title(msg: Message) -> None:
    titles = await search(msg.text)
    for title in titles[:TITLES_NUM_IN_SEARCH]:
        await send_photo_if_exists(msg, title.get('image', None))
        await msg.answer(
            await get_text_for_search(title),
            reply_markup=get_search_markup(title.get('id')),
            disable_notification=True,
        )


@collection_router.callback_query(F.data.startswith('detail_'))
async def detail_title(callback: types.CallbackQuery) -> None:
    id = callback.data.split('_')[-1]
    title = await get_or_create_title(id)

    await send_photo_if_exists(callback.message, title.image_url)
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
