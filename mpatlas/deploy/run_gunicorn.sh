#!/bin/bash
VIRTUALENV=/home/mpatlas/virtualenvs/mpatlas_dev
PROJECTDIR=/home/mpatlas/projects/django_mpatlas/mpatlas
DJANGO_SETTINGS_MODULE=mpatlas.settings
DJANGO_WSGI_MODULE=mpatlas.wsgi

USER=mpatlas
GROUP=mpatlas

# Change to project dir so gunicorn can find mpatlas.wsgi on default python search path
cd $PROJECTDIR
source ~/.bashrc
source $VIRTUALENV/bin/activate

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VIRTUALENV/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  -c $PROJECTDIR/deploy/gunicorn.conf
  --user=$USER --group=$GROUP \
