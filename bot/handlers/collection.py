from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from magic_filter import MagicFilter as F

from utils import search_title as search
from services import add_title_to_collection

# from texts.messages import Text as t


collection_router: Router = Router(name=__name__)


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
async def add_to_collection(callback: types.CallbackQuery):
    id = callback.data.split('_')[-1]
    username = callback.message.chat.username
    await add_title_to_collection(id, username)
    await callback.message.answer('Успешно добавлено в коллекцию')
    await callback.answer()
