# AllDay DJ

Radio playout for the modern, cloud-driven world. This is the API for AllDay DJ, handing media storage, logs, VT, etc.

![Test and Build](https://github.com/steelegbr/alldaydj/workflows/alldaydj-actions/badge.svg)

## Project Plan

The plan for delivering AllDay DJ in stages:

 - [ ] JWT auth integration.
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
 - ADDJ_ALLOWED_HOSTS - The hosts we are permitted to make requests from. Default to an empty list.
 - ADDJ_LANG_CODE - The language code we're installed with. Defaults to en-gb.
 - ADDJ_TIMEZONE - The server timezone. Defaults to UTC.
 - ADDJ_USERS_DOMAIN - Base URL to match tenants on.

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