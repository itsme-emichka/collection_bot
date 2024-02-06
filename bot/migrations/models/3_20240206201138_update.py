from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "first_name" VARCHAR(512);
        ALTER TABLE "user" ADD "last_name" VARCHAR(512);
        ALTER TABLE "user" ADD "username" VARCHAR(512) NOT NULL;
        CREATE TABLE IF NOT EXISTS "usertitle" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title_id" INT NOT NULL REFERENCES "title" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "first_name";
        ALTER TABLE "user" DROP COLUMN "last_name";
        ALTER TABLE "user" DROP COLUMN "username";
        DROP TABLE IF EXISTS "usertitle";"""
