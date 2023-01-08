import os

from pydantic import BaseSettings


class DevSettings(BaseSettings):
    DATABASE_URL: str = os.environ.get('DATABASE_URL')
