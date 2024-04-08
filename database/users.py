from typing import Dict

from database.config import users_collection


async def add_user(user: Dict) -> Dict:
    document = await users_collection.insert_one(user)
    return await users_collection.find_one({"_id": document.inserted_id})


async def find_user(username: str) -> Dict:
    return await users_collection.find_one({"username": username})


async def update_user(username: str, user: Dict) -> bool:
    result = await users_collection.update_one({"username": username}, {"$set": user})
    return result.modified_count > 0
