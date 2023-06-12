#!/bin/bash
PROJECTDIR=/home/mpatlas/projects/django_mpatlas
DJANGO_WSGI_MODULE=ratemympa.wsgi
POETRY=/home/mpatlas/.local/bin/poetry
# VIRTUALENV=/home/mpatlas/.cache/pypoetry/virtualenvs/ratemympa-HT8bCPFt-py3.11
# export PATH="/home/mpatlas/.local/bin:$PATH"

# Change to project dir so gunicorn can find mpatlas.wsgi on default python search path
source ~/.bashrc
# source $VIRTUALENV/bin/activate
cd $PROJECTDIR

export DJANGO_SETTINGS_MODULE=ratemympa.settings
export PYTHONPATH=$PROJECTDIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
# exec poetry run $VIRTUALENV/bin/gunicorn ${DJANGO_WSGI_MODULE}:application -c $PROJECTDIR/ratemympa/deploy/gunicorn.conf.py
exec $POETRY run gunicorn ${DJANGO_WSGI_MODULE}:application -c $PROJECTDIR/mpatlas/deploy/gunicorn.conf.py
