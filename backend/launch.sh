#!/bin/bash
python manage.py migrate
celery -A alldaydj multi start worker1 --loglevel=INFO --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
#gunicorn -b 0.0.0.0:8000 alldaydj.wsgi --timeout 300 --workers 3 --log-level=debug
python manage.py runserver 0.0.0.0:8000