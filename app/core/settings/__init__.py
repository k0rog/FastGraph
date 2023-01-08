import os
from functools import lru_cache


@lru_cache()
def get_settings():
    environment = os.environ.get('ENVIRONMENT')

    if environment == 'test':
        from app.core.settings.test import TestSettings
        return TestSettings()

    from app.core.settings.dev import DevSettings
    settings = DevSettings()
    return settings


settings = get_settings()
