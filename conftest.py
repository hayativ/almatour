import os

import pytest

# Configure Django settings for pytest before any imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.env.local')
os.environ.setdefault('PROJECT_ENV_ID', 'local')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-pytest')
os.environ.setdefault('DEBUG', 'True')
