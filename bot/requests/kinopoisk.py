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
        return await response.json()
