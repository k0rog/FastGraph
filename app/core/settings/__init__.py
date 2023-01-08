import os
from functools import lru_cache
from dotenv import load_dotenv


@lru_cache()
def get_settings():
    environment = os.environ.get('ENVIRONMENT')

    if environment == 'test':
        from app.core.settings.test import TestSettings
        return TestSettings()

    from app.core.settings.dev import DevSettings
    settings = DevSettings()
    print('--------------------------------')
    print(settings.DATABASE_URL)
    print('--------------------------------')
    return settings


settings = get_settings()
