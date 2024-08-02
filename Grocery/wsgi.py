"""
WSGI config for Grocery project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

import environ
env = environ.Env()
environ.Env.read_env()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Grocery.settings')

application = get_wsgi_application()

project_folder = os.path.expanduser('~/Grocery')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))