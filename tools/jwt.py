from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt import PyJWTError

from common.const import SECRET_KEY, ALGORITHM

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes if not specified
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(http_authorization_credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = http_authorization_credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if 'sub' not in payload:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        return payload
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
