from fastapi import APIRouter, HTTPException, Depends, status

from database.config import posts_collection
from database.posts import delete_post_db, get_post_db, add_post_db, update_post_db
from models.posts import PostCreate, PostResponse, PostUpdate
from datetime import datetime

from tools.generate import generate_unique_id
from tools.jwt import verify_token
from tools.serialize import serialize_mongo_document
from loguru import logger

router = APIRouter()


def get_current_username(token: dict = Depends(verify_token)):
    # Extract username from token payload. The payload is a dictionary.
    return token.get("sub")


@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, username: str = Depends(get_current_username)):
    try:
        post_id = generate_unique_id()
        post_data = {**post.dict(), "id": post_id, "author_name": username}
        new_post = await add_post_db(post_data)
        return serialize_mongo_document(new_post)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: str, post: PostUpdate, username: str = Depends(get_current_username)):
    existing_post = await get_post_db(post_id)
    if not existing_post or existing_post["author_name"] != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized or post not found")
    try:
        updated_post = await update_post_db(post_id, post.dict(exclude_unset=True))
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post not found")
        return serialize_mongo_document(updated_post)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="An error occurred during sign in")


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, username: str = Depends(get_current_username)):
    success = await delete_post_db(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
