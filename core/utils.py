from django.conf import settings


def is_dev_environment() -> bool:
    """Checks if currently working on dev."""
    return settings.ENVIRONMENT == 'dev'
