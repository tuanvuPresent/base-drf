release: python manage.py migrate --no-input
release: python manage.py loaddata fixtures/*

web: gunicorn base_drf.wsgi:application
