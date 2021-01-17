#!/bin/bash
python manage.py migrate
celery -A alldaydj multi start worker1
python manage.py runserver 0.0.0.0:8000