from motor.motor_asyncio import AsyncIOMotorClient

from common.const import MONGODB_CONNECTION_STRING, MONGODB_NAME, ACCESS_TOKEN_EXPIRE_MINUTES

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client[MONGODB_NAME]

users_collection = database.users_collection
posts_collection = database.posts_collection
comments_collection = database.comments_collection

sessions_collection = database.sessions_collection


async def create_ttl_index():
    await sessions_collection.create_index([("expiresAt", 1)], expireAfterSeconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60)


