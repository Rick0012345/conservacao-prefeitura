#!/bin/bash

# Wait for database
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

echo "Database is ready!"

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
"

# Start server
exec "$@" 