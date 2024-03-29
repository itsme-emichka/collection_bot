from tortoise.query_utils import Prefetch

from models import User, UserTitle, Title, Type
from requests.kinopoisk import get_title_data
from requests.client_session import session
from utils import get_director_from_response


async def get_or_create_user(
        username: str,
        first_name: str = None,
        last_name: str = None) -> User:
    user, is_created = await User.get_or_create(
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    return user


async def get_or_create_type(slug: str) -> Type:
    title_type, is_created = await Type.get_or_create(slug=slug)
    return title_type


async def get_title(kinopoisk_id: int) -> Title:
    return await Title.all().prefetch_related(
        Prefetch(
            'type',
            queryset=Type.all().select_related(),
            to_attr='title_type',
        )
    ).get(kinopoisk_id=kinopoisk_id)


async def get_or_create_title(kinopoisk_id: int) -> Title:
    if await Title.filter(kinopoisk_id=kinopoisk_id).exists():
        return await get_title(kinopoisk_id)
    data = await get_title_data(kinopoisk_id, session())

    kinopoisk_id: int = data.get('id', None)
    name: str = data.get('name', None)
    title_type: Type = await get_or_create_type(data.get('type', None))
    description: str = data.get('description', None)
    rating: float = data.get('rating', dict()).get('imdb', None)
    director: str = await get_director_from_response(data.get('persons', None))
    release_year: int = data.get('year', None)
    genre: str = ''.join(
        (f'{genre.get('name')}, ' for genre in data.get('genres')))
    image_url: str = data.get('poster', dict()).get('url', None)

    title = await Title.create(
        kinopoisk_id=kinopoisk_id,
        name=name,
        type=title_type,
        description=description,
        rating=rating,
        director=director,
        release_year=release_year,
        genre=genre[:-2],
        image_url=image_url,
    )

    return await get_title(title.kinopoisk_id)


async def get_user(username: str) -> User:
    return await User.get(username=username)


async def add_title_to_collection(kinopoisk_id: int, user: User) -> Title:
    title = await get_or_create_title(kinopoisk_id)
    _, is_created = await UserTitle.get_or_create(
        user=user,
        title=title,
    )
    return title, is_created


async def get_user_collection(user: User, **filters) -> list[Title]:
    return await Title.filter(
        user_title__user=user,
        **filters
    ).prefetch_related(
        Prefetch(
            'type',
            queryset=Type.all().select_related(),
            to_attr='title_type',
        )
    )


async def remove_title_from_collection(user: User, title_id: int) -> None:
    await UserTitle.filter(user=user, title_id=title_id).delete()
