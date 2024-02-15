from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usertitle" DROP COLUMN "is_watched";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "usertitle" ADD "is_watched" BOOL NOT NULL  DEFAULT False;"""
