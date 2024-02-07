from aiohttp import ClientSession

from config import KINOPOISK_TOKEN
from requests.urls import KinopoiskUrls as k


HEADERS: dict[str, str] = {'X-API-KEY': KINOPOISK_TOKEN}


async def search(
        query: str, session: ClientSession) -> dict[str, dict[str, str]]:
    async with session.get(
        url=k.SEARCH.value.format(query),
        headers=HEADERS,
    ) as response:
        resp = await response.json()
        return resp


async def get_title_data(title_id: int, session: ClientSession) -> dict:
    async with session.get(
        url=k.GET_TITLE.value.format(title_id),
        headers=HEADERS,
    ) as response:
        resp = await response.json()
        return resp
