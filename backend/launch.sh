#!/bin/bash
python manage.py migrate
celery -A alldaydj.celery multi start worker1 --loglevel=DEBUG --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
python manage.py runserver 0.0.0.0:8000