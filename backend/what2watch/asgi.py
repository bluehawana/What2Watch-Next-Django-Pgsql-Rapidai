"""
ASGI config for what2watch project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'what2watch.settings')

application = get_asgi_application()
