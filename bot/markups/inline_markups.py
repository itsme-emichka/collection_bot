from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from texts.markups import Markup as m
from models import Title


def get_collection_markup(title: Title) -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(
        text=m.DELETE_FROM_COLLECTION.value,
        callback_data=f'delete_{title.id}'
    )
    btn2 = InlineKeyboardButton(
        text=m.DETAIL.value,
        callback_data=f'detail_{title.kinopoisk_id}'
    )
    return InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])


def get_filter_markup() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(
        text=m.MOVIE.value,
        callback_data='filter_movie',
    )
    btn2 = InlineKeyboardButton(
        text=m.SERIES.value,
        callback_data='filter_series',
    )
    btn3 = InlineKeyboardButton(
        text=m.CARTOON.value,
        callback_data='filter_cartoon',
    )
    btn4 = InlineKeyboardButton(
        text=m.ANIME.value,
        callback_data='filter_anime',
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[btn1, btn2], [btn3, btn4]]
    )


def get_search_markup(kinopoisk_id: int) -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(
        text=m.COLLECT.value,
        callback_data=f'id_{kinopoisk_id}'
    )
    btn2 = InlineKeyboardButton(
        text=m.DETAIL.value,
        callback_data=f'detail_{kinopoisk_id}'
    )
    return InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
