"""
WSGI config for what2watch project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'what2watch.settings')

application = get_wsgi_application()
