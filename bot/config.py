from os import getenv

from dotenv import load_dotenv


load_dotenv(override=True)

# DATABASE
POSTGRES_USER: str = getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD')
POSTGRES_PORT: str = getenv('POSTGRES_PORT', '5432')
POSTGRES_HOST: str = getenv('POSTGRES_HOST')
POSTGRES_DB: str = getenv('POSTGRES_DB')

# BOT
BOT_TOKEN: str = getenv('BOT_TOKEN')

# REQUESTS TOKENS
KINOPOISK_TOKEN: str = getenv('KINOPOISK_TOKEN')
