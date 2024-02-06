from models import User, UserTitle, Title, Type
from requests.kinopoisk import get_title_data
from utils import get_director_from_response
from requests.client_session import session


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


async def get_or_create_title(title_id: int) -> Title:
    if await Title.filter(kinopoisk_id=title_id).exists():
        return await Title.get(kinopoisk_id=title_id)
    data = await get_title_data(title_id, session())

    kinopoisk_id: int = data.get('id', None)
    name: str = data.get('name', None)
    title_type: Type = await get_or_create_type(data.get('type', None))
    description: str = data.get('description', None)
    rating: float = data.get('rating', dict()).get('imdb', None)
    director: str = await get_director_from_response(data.get('persons', None))
    release_year: int = data.get('year', None)
    genre: str = data.get('genres', [dict()])[0].get('name', None)
    image_url: str = data.get('poster', dict()).get('url', None)

    title = await Title.create(
        kinopoisk_id=kinopoisk_id,
        name=name,
        type=title_type,
        description=description,
        rating=rating,
        director=director,
        release_year=release_year,
        genre=genre,
        image_url=image_url,
    )

    return title


async def get_user(username: str) -> User:
    return await User.get(username=username)


async def add_title_to_collection(title_id: int, username: str) -> None:
    title = await get_or_create_title(title_id)
    user = await get_user(username)
    await UserTitle.get_or_create(
        user=user,
        title=title,
    )
