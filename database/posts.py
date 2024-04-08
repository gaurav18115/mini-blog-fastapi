from datetime import datetime
from database.config import posts_collection


async def add_post_db(post_data: dict) -> dict:
    post_data['created_at'] = datetime.utcnow()
    post_data['updated_at'] = datetime.utcnow()
    result = await posts_collection.insert_one(post_data)
    new_post = await posts_collection.find_one({'_id': result.inserted_id})
    return new_post


async def get_post_db(post_id: str) -> dict:
    return await posts_collection.find_one({'id': post_id})


async def update_post_db(post_id: str, update_data: dict) -> dict:
    update_data['updated_at'] = datetime.utcnow()
    await posts_collection.update_one({'id': post_id}, {'$set': update_data})
    updated_post = await posts_collection.find_one({'id': post_id})
    return updated_post if updated_post else None


async def delete_post_db(post_id: str) -> bool:
    result = await posts_collection.delete_one({'id': post_id})
    return result.deleted_count > 0
