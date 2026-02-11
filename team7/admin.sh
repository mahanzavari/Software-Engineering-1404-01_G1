#!/usr/bin/env bash
set -e

echo "Making migrations for team7..."
docker exec -i core python manage.py makemigrations team7

echo "--- FIX: Migrating on DEFAULT database (for Admin Panel compatibility) ---"
docker exec -i core python manage.py migrate team7

echo "--- Migrating on TEAM7 database (for Data storage) ---"
docker exec -i core python manage.py migrate team7 --database=team7

echo "Creating superuser..."
docker exec -i core python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
email = 'admin@example.com';
password = 'admin';
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password);
    print(f'Superuser {email} created.');
else:
    print(f'Superuser {email} already exists.');
"