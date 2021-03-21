# AllDay DJ

Radio playout for the modern, cloud-driven world. This is the API for AllDay DJ, handing media storage, logs, VT, etc.

![Test and Build](https://github.com/steelegbr/alldaydj/workflows/alldaydj-actions/badge.svg)
[![DeepSource](https://deepsource.io/gh/steelegbr/alldaydj.svg/?label=active+issues&show_trend=true&token=GaOCuVhfpV_A47FO4RVupPrF)](https://deepsource.io/gh/steelegbr/alldaydj/?ref=repository-badge)

## Project Plan

The plan for delivering AllDay DJ in stages:

 - [X] JWT auth integration.
 - [ ] Audio library (can store and edit carts).
 - [ ] Search
 - [ ] Log editing.
 - [ ] VT.
 - [ ] Scheduling.
 - [ ] Audio playout.

Some of these are absolute beasts (i.e. not a simple feature). Nice to have some ambition though!

## virtualenv

For the virtual environment, run the following:

    pip3.9 install virtualenv
    python3.9 -m virtualenv addjvenv

Once activated, remember to:

    pip install -r requirements.txt

## Configuration

Environment variables are used to configure the application. For any deployment / test / whatever, you'll
need the following variables.

 - ADDJ_SECRET_KEY - The Django secret key.
 - ADDJ_DEBUG - Indicates if debug mode should be enabled. Defaults to False.
 - ADDJ_DB_NAME - Name of the database to connect to.
 - ADDJ_DB_USER - Username to connect to the database as.
 - ADDJ_DB_PASS - The password to connect to the database with.
 - ADDJ_DB_HOST - The host to connect to the database on.
 - ADDJ_DB_PORT - The port to connect to the database on. Defaults to 5432.
 - ADDJ_LANG_CODE - The language code we're installed with. Defaults to en-gb.
 - ADDJ_TIMEZONE - The server timezone. Defaults to UTC.
 - ADDJ_USERS_DOMAIN - The URL the application is installed on.
 - ADDJ_RABBIT_HOST - The host RabbitMQ is running on. Defaults to localhost.
 - ADDJ_RABBIT_PORT - The port RabbitMQ is running on. Defaults to 5672.
 - ADDJ_RABBIT_USER - The username to log into RabbitMQ with. Defaults to "guest".
 - ADDJ_RABBIT_PASS - The password to log into RabbitMQ with. Defaults to "".
 - ADDJ_CELERY_ALWAYS_EAGER - Indicates if Celery should run immediately (test environment).
 - ADDJ_S3_REGION - The S3 bucket region.
 - ADDJ_S3_ENDPOINT - The S3 endpoint to use.
 - ADDJ_S3_KEY_ID - The S3 key.
 - ADDJ_S3_KEY_SECRET - The S3 secret.
 - ADDJ_ELASTIC_SERVER - The elasticsearch server. Defaults to "elasticsearch".
 - ADDJ_ELASTIC_PORT - The elasticsearch server port. Defaults to 9200.
 - ADDJ_ELASTIC_INDEX - The elasticsearch index. Defaults to "alldaydj".

A simple shell script that exports the environment variables should be enough for dev work. Remember to execute it correctly inside the Python virtualenv:

    . set_params_dev.sh

Note the lack of forward slash!

## PostgreSQL on macOS

You'll need to install through homebrew:

    brew install postgresql

Same as for installing modern Python versions:

    brew install python@3.9

To start the database engine:

    brew services start postgresql

This creates a user with your username but no password.

## Rabbit... Rabbit, Rabbit, Rabbit!

RabbitMQ is required to make the Celery magic work. On macOS you can use homebrew:

    brew install rabbitmq
    brew services start rabbitmq

## Celery

Celery is used for async tasks. You need to have the running going for it to do anything. ;)

    celery -A alldaydj worker -l INFO

## Magic

On macOS, libmagic needs to be manually installed:

    brew install libmagic

## FFMPEG

FFMPEG is used to handle the odd and wonderous array of codecs out there. It needs to be installed as a binary we can call.

## Elasticsearch

To create the index:

    python manage.py search_index --create -f

To rebuild the index:

    python manage.py search_index --populate -f

An elasticsearch server (or cluster) is required for search functionality.

## Cypress on WSL

To make Cypress run on WSL, you'll need to re-point the DISPLAY variable. Add the following to your bashrc file:

    # set DISPLAY variable to the IP automatically assigned to WSL2
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
    sudo /etc/init.d/dbus start &> /dev/null

You will also need VcXsrv running on Windows and DBUS passwordless sudo access. Details can be found at https://nickymeuleman.netlify.app/blog/gui-on-wsl2-cypress
