from datetime import datetime, timedelta

from database.config import sessions_collection

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # or your specific expiration duration


async def add_session(username: str, access_token: str) -> dict:
    session_data = {
        "username": username,
        "expiresAt": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "accessToken": access_token
    }
    await sessions_collection.insert_one(session_data)
    return session_data
