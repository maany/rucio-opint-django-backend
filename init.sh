#!/bin/bash

# gunicorn
cp /code/config/gunicorn /etc/init.d/gunicorn
cp /code/config/gunicorn.socket /etc/systemd/system

# wait for postgres
if [ "$MODE" = "dev" ]
then
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#django
export PYTHONPATH=/code:${PYTHONPATH}
export DJANGO_SETTINGS_MODULE='rucio_opint_backend.apps.core.settings'
python manage.py makemigrations core
python manage.py migrate
python manage.py loaddata initial
# echo "yes" | python mannage.py collectstatic
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '${ADMIN_PASSWORD}')" | python manage.py shell

# cron
echo "0 * * * * root /usr/bin/python3 /code/manage.py rucio_loader_cron >> /code/rucio_loader_output" >> /etc/crontab

#services
service cron start
if [ $MODE = "prod" ]
then 
    gunicorn rucio_opint_backend.apps.core.wsgi:application --bind 0.0.0.0:8000
else
    python manage.py runserver 0.0.0.0:8000
fi


