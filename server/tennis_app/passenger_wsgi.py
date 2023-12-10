# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1390694/data/www/tennis57.ru/tennis')
sys.path.insert(1, '/var/www/u1390694/data/www/tennis57.ru/djangoenv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennis.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()