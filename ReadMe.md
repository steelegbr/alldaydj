# AllDay DJ

Radio playout for the modern, cloud-driven world. This is the API for AllDay DJ, handing media storage, logs, VT, etc.

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