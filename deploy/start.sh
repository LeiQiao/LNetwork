#!/bin/bash

export LANG=en_GB.UTF-8
uwsgi --ini ./uwsgi_parasite.ini  --enable-threads --wsgi-disable-file-wrapper
