from requests.client_session import session
from requests.kinopoisk import search


async def clean_search_response(response: dict[str, dict[str, str]]) -> str:
    clean_response = {'titles': []}
    temp = dict()

    for title in response.get('docs'):
        temp['id'] = title.get('id')
        temp['name'] = title.get('name')
        temp['type'] = title.get('type')
        temp['year'] = title.get('year')
        temp['description'] = title.get('description')
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
            directors += f'{person.get('name')},'
    return directors[:-1]
