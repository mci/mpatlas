#!/bin/bash
VIRTUALENV=/home/mpatlas/virtualenvs/mpatlas_dev
PROJECTDIR=/home/mpatlas/projects/django_mpatlas/mpatlas
source ~/.bashrc
source $VIRTUALENV/bin/activate
exec $VIRTUALENV/bin/gunicorn_django -c $PROJECTDIR/deploy/gunicorn.conf $PROJECTDIR/settings.py

