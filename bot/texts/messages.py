from enum import Enum


class Text(Enum):
    START: str = '''Привет, я Коллекшн бот!
Я создан, чтобы коллекционировать все твои находки в интернете в красивом виде. Сейчас поддерживаются следуюшие типы произведений для добавления в коллецию:
- Кино
- Сериал
- Аниме

Чтобы начать работу, просто напиши название произведения и выбери из тех, что мне удалось найти.'''
    ADD_TO_COLLECTION: str = 'Произведение "{}" успешно добавлено в коллекцию!'
    ALREADY_IN_COLLECTION: str = 'Произведение уже было добавлено в коллекцию!'
    REMOVED: str = 'Произведение удалено из коллекции.'
