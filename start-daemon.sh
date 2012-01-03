#!/bin/bash

pkill -f 'manage\.py.*run_gunicorn'
pkill -f 'manage\.py.*Manticore'
./manage.py runfcgi umask=000 method=threaded daemonize=true socket=`pwd`/fastcgi.socket debug=true outlog=`pwd`/out.log errlog=`pwd`/err.log
#./manage.py run_gunicorn --umask=000 --daemon --bind=127.0.0.1:8001
