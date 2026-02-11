#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🚀 Starting to seed the database with TOEFL questions..."
echo "--------------------------------------------------------"

# This line executes the Django management command inside the 'core' container.
# It also passes any arguments you give to this script (like --clear) to the command.
docker-compose exec core python manage.py seed_questions "$@"

echo "--------------------------------------------------------"
echo "✅ Seeding process finished successfully!"