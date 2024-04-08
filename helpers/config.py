from motor.motor_asyncio import AsyncIOMotorClient

from common.const import MONGODB_CONNECTION_STRING, MONGODB_NAME

client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client[MONGODB_NAME]


user_collection = database.user_collection
post_collection = database.post_collection
comment_collection = database.comment_collection

