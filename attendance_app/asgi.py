"""
ASGI config for attendance_app project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_app.settings')

application = get_asgi_application()
