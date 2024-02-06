from aiohttp import ClientSession


def session() -> ClientSession:
    return ClientSession()
