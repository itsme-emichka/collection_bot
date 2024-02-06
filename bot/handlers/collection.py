from aiogram import Router
from aiogram.types import Message

from utils import search_title as search

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
        await msg.answer(answer_text)
