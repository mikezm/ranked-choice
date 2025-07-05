"""
ASGI config for ranked_choice project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranked_choice.settings')

application = get_asgi_application()