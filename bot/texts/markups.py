from enum import Enum


class Markup(Enum):
    DELETE_FROM_COLLECTION: str = 'Удалить из коллекции'
    DETAIL: str = 'Подробнее'
    DELETE: str = 'Удалить'
    COLLECT: str = 'Коллекционировать'
    MOVIE: str = 'Кино'
    SERIES: str = 'Сериалы'
    ANIME: str = 'Аниме'
    CARTOON: str = 'Мультфильмы'
