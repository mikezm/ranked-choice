import os
import pytest
import django
from django.conf import settings

# This file is automatically loaded by pytest
# It configures pytest to work with Django

# Set up Django settings before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranked_choice.settings')

# Add 'testserver' to ALLOWED_HOSTS for testing
if 'ALLOWED_HOSTS' in os.environ:
    if 'testserver' not in os.environ['ALLOWED_HOSTS']:
        os.environ['ALLOWED_HOSTS'] += ',testserver'
else:
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'

# Initialize Django before pytest_configure is called
django.setup()

# Ensure database configuration exists and has ENGINE set
def pytest_configure():
    """Configure Django for testing before tests run."""
    # Ensure database configuration exists
    if not hasattr(settings, 'DATABASES') or not settings.DATABASES or 'default' not in settings.DATABASES:
        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'TEST': {
                    'NAME': ':memory:',
                },
            }
        }
    # Ensure ENGINE is set
    elif 'ENGINE' not in settings.DATABASES['default']:
        settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
        settings.DATABASES['default']['NAME'] = ':memory:'
        settings.DATABASES['default']['TEST'] = {
            'NAME': ':memory:',
        }

# This is used by pytest-django to configure Django for testing
# It's not necessary to call django.setup() in the test files when using pytest
