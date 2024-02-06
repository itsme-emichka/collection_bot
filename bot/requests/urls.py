from enum import Enum


BASE: str = 'http://api.kinopoisk.dev/v1.4/'


class KinopoiskUrls(Enum):
    SEARCH: str = BASE + 'movie/search?query={}'
    GET_TITLE: str = BASE + 'movie/{}'
