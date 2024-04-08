from typing import Dict

from helpers.config import user_collection


async def add_user(user: Dict) -> Dict:
    document = await user_collection.insert_one(user)
    return await user_collection.find_one({"_id": document.inserted_id})


async def find_user(username: str) -> Dict:
    return await user_collection.find_one({"username": username})


async def update_user(username: str, user: Dict) -> bool:
    result = await user_collection.update_one({"username": username}, {"$set": user})
    return result.modified_count > 0
