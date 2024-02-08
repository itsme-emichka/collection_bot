from typing import Any

from requests.client_session import session
from requests.kinopoisk import search
from models import Title


async def clean_search_response(response: dict[str, dict[str, str]]) -> str:
    clean_response = {'titles': []}
    temp = dict()

    for title in response.get('docs'):
        temp['id'] = title.get('id')
        temp['name'] = title.get('name')
        temp['type'] = title.get('type')
        temp['year'] = title.get('year')
        temp['description'] = title.get('description')
        temp['image'] = title.get('poster').get('previewUrl')
        clean_response['titles'].append(temp)
        temp = dict()

    return clean_response


async def search_title(query: str) -> list[dict[str, str]]:
    response = await search(query, session())
    clean_response = await clean_search_response(response)
    return clean_response.get('titles')


async def get_director_from_response(persons):
    if not persons:
        return
    directors: str = ''
    for person in persons:
        if person.get('enProfession') == 'director':
            directors += f'{person.get('name')}, '
    return directors[:-1]


async def get_title_detail_info(title: Title) -> str:
    return f'''<strong>{title.name}</strong> ({title.release_year})

<strong>Рейтинг IMDB:</strong> {title.rating}
<strong>Жанр:</strong> {title.genre}
<strong>Тип произведения:</strong> {title.title_type.slug}
<strong>Режиссеры:</strong>
{title.director}

<strong>Описание:</strong>
{title.description}'''


async def get_text_for_collection(title: Title) -> str:
    return (
        f'<strong>{title.name}</strong> ({title.release_year})\n' +
        f'<strong>Жанр:</strong> {title.genre}\n' +
        f'<strong>Тип:</strong> {title.title_type.slug}\n' +
        f'<strong>Режиссеры:</strong> {title.director}'
    )


async def get_text_for_search(title: dict[str, Any]) -> str:
    return (
        f'<strong>{title.get('name')}</strong> ({title.get('year')})\n' +
        f'{title.get('description')[:300]}...'
    )
