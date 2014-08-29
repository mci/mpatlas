#!/bin/bash
VIRTUALENV=/home/mpatlas/virtualenvs/mpatlas_dev
PROJECTDIR=/home/mpatlas/projects/django_mpatlas
DJANGO_SETTINGS_MODULE=mpatlas.settings
DJANGO_WSGI_MODULE=mpatlas.wsgi

export PYTHONPATH=$PROJECTDIR:$PYTHONPATH

USER=mpatlas
GROUP=mpatlas

# Change to project dir so gunicorn can find mpatlas.wsgi on default python search path
cd $PROJECTDIR
source ~/.bashrc
source $VIRTUALENV/bin/activate

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
# exec $VIRTUALENV/bin/gunicorn_django -c $PROJECTDIR/deploy/gunicorn.conf $PROJECTDIR/settings.py
exec $VIRTUALENV/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  -c $PROJECTDIR/mpatlas/deploy/gunicorn.conf \
  --user=$USER --group=$GROUP
