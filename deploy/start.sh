#!/bin/bash

export LANG=en_GB.UTF-8
uwsgi --ini ./uwsgi_parasite.ini --wsgi-disable-file-wrapper
