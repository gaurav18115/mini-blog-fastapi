from pydantic import BaseModel
from datetime import datetime, timedelta


class Session(BaseModel):
    username: str
    expiresAt: datetime
    accessToken: str

