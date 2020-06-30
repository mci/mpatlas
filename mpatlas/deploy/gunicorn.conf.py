import sys, os
#GU_PATH = os.path.abspath(os.path.dirname(__file__))
GU_PATH = os.path.join(os.path.abspath(''), 'mpatlas/deploy/')
sys.path.append(GU_PATH)

sockfile = os.path.join(GU_PATH, 'gunicorn.sock')
pidfile = os.path.join(GU_PATH, 'gunicorn.pid')
#logfile = os.path.join(GU_PATH, 'gunicorn.log')
#loglevel = 'debug'

proc_name = "mpatlas"
user = "mpatlas"
group = "mpatlas"

bind = "unix:" + sockfile  # Use socket file in current dir
workers = 3
worker_class = "gevent"
max_requests = 500
timeout = 90

def post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
    worker.log.info("Made Psycopg Green")
