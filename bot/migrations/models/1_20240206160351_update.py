from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "title" ADD "rating" DECIMAL(2,1) NOT NULL;
        ALTER TABLE "title" ADD "genre" VARCHAR(256);
        ALTER TABLE "title" ADD "type_id" SMALLINT NOT NULL;
        ALTER TABLE "title" ADD "director" VARCHAR(256);
        ALTER TABLE "title" ADD "release_year" SMALLINT NOT NULL;
        ALTER TABLE "title" ADD "description" TEXT NOT NULL;
        CREATE TABLE IF NOT EXISTS "type" (
    "id" SMALLSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL UNIQUE,
    "slug" VARCHAR(256) NOT NULL
);
        ALTER TABLE "title" ADD CONSTRAINT "fk_title_type_c3876217" FOREIGN KEY ("type_id") REFERENCES "type" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "title" DROP CONSTRAINT "fk_title_type_c3876217";
        ALTER TABLE "title" DROP COLUMN "rating";
        ALTER TABLE "title" DROP COLUMN "genre";
        ALTER TABLE "title" DROP COLUMN "type_id";
        ALTER TABLE "title" DROP COLUMN "director";
        ALTER TABLE "title" DROP COLUMN "release_year";
        ALTER TABLE "title" DROP COLUMN "description";
        DROP TABLE IF EXISTS "type";"""
