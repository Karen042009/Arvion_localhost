import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Arvion.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="Admin_1").exists():
    User.objects.create_superuser(
        username="Admin_1",
        email="admin@example.com",
        password="Karen2009"
    )
    print("✅ Superuser Admin_1 created.")
else:
    print("⚠️ Admin_1 already exists.")
