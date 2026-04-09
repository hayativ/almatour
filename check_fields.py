import os
import django

# Set PROJECT_ENV_ID so settings.conf can read it via decouple
os.environ['PROJECT_ENV_ID'] = 'local'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.env.local')
django.setup()

from apps.places.models import Place

print("Fields in Place model:")
for field in Place._meta.fields:
    print(f"- {field.name}")
