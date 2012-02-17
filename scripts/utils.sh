#!/bin/bash

function run_management_command
{
    # WARNING: this is a script to run management command from a crontab, it returns output only if there were errors

    COMMAND=$1
    # get absolute path to the parent dir
    BASE=$(cd $(dirname $0)/..; pwd)
    LOG=$BASE/log/$1.log
    TMP_LOG=$LOG.tmp

    trap "rm -f $TMP_LOG" EXIT
    date > $TMP_LOG

    # go to the /tmp to create lock files there
    cd /tmp

    # now run the command
    "$BASE/env/bin/python" "$BASE/manage.py" $COMMAND > $TMP_LOG 2>&1

    # copy this run's log into the full size log
    cat $TMP_LOG >> $LOG

    # check for errors and print them
    if grep -i -e traceback -e error $TMP_LOG; then
        cat $TMP_LOG
    fi
}
