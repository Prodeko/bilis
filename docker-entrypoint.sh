#!/bin/bash

set -e

echo $DATABASE_URL

function wait_for_db () {
	# Check if database is up and accepting connections.
  echo "Checking database connection"
  until psql $DATABASE_URL -c "select 1" 2>/dev/null; do
		>&2 echo "Database is unavailable - sleeping"
		sleep 1
	done
	>&2 echo "Database is up - continuing"
}

wait_for_db

# Create and run migrations
echo "Creating migrations..."
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

# Create a superuser for development
echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; \
	User = get_user_model(); User.objects.filter(email='webbitiimi@prodeko.org').exists() or \
	User.objects.create_superuser(username='webbitiimi', email='webbitiimi@prodeko.org', password='kananugetti')"

exec "$@"
