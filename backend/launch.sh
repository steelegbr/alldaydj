#!/bin/bash
python manage.py migrate
celery -A alldaydj multi start worker1 --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
python manage.py runserver 0.0.0.0:8000