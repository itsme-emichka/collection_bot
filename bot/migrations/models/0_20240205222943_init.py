from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "title" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "kinopoisk_id" INT NOT NULL,
    "name" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
