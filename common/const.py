import os
from dotenv import load_dotenv

load_dotenv()

# MONGODB
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
MONGODB_NAME = os.getenv('MONGODB_NAME')

# JWT
SECRET_KEY = '#D08dsDS*&$@e280'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time
