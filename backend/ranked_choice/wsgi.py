"""
WSGI config for ranked_choice project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ranked_choice.settings')

application = get_wsgi_application()