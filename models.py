import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yaroslava.settings")
django.setup()

from menu import models

orm = models
