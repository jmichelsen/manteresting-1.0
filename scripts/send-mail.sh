#!/bin/bash

# get absolute path to the parent dir
BASE=$(cd $(dirname $0)/..; pwd)

# go to the /tmp to create lock files there
cd /tmp

# now run the command
"$BASE/env/bin/python" "$BASE/manage.py" send_mail
