#!/bin/bash

redis-cli flushall
dropdb lalookup
createdb lalookup
python manage.py migrate
python manage.py makemigrations
