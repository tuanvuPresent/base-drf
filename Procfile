release: python manage.py migrate --no-input
release: python manage.py loaddata fixtures/*
release: python manage.py collectstatic --no-input
web: gunicorn base_drf.wsgi:application
