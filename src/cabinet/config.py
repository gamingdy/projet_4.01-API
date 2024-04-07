import os
from os.path import dirname, join

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
AUTH_URL = os.getenv("AUTH_URL")


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
