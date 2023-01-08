import os

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    DATABASE_URL: str = os.environ.get('DATABASE_URL')
