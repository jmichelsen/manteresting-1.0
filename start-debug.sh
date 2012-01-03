#!/bin/bash

umask 000
pkill -f 'manage\.py.*Manticore'
./manage.py runfcgi method=threaded daemonize=false socket=`pwd`/fastcgi.socket debug=true outlog=`pwd`/out.log errlog=`pwd`/err.log
