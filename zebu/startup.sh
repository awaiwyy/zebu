#!/bin/bash
trap 'echo " killall -- forked thread done"; kill %1 %2 %3 %4 %5 %6 %7 %8 %9 2>/dev/null' TERM INT

# update database
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:2020

wait
