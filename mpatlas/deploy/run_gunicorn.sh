#!/bin/bash
VIRTUALENV=/home/mpatlas/virtualenvs/py3_mpatlas
PROJECTDIR=/home/mpatlas/projects/django_mpatlas
DJANGO_WSGI_MODULE=mpatlas.wsgi

# Change to project dir so gunicorn can find mpatlas.wsgi on default python search path
source ~/.bashrc
source $VIRTUALENV/bin/activate
cd $PROJECTDIR

export DJANGO_SETTINGS_MODULE=mpatlas.settings
export PYTHONPATH=$PROJECTDIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VIRTUALENV/bin/gunicorn ${DJANGO_WSGI_MODULE}:application -c $PROJECTDIR/mpatlas/deploy/gunicorn.conf.py
