from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "title" ALTER COLUMN "description" DROP NOT NULL;
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY
);
        CREATE UNIQUE INDEX "uid_title_kinopoi_10cbee" ON "title" ("kinopoisk_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_title_kinopoi_10cbee";
        ALTER TABLE "title" ALTER COLUMN "description" SET NOT NULL;
        DROP TABLE IF EXISTS "user";"""
