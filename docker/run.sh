#!/bin/sh


flask db create
echo 'running uwsgi...'
exec uwsgi --ini /uwsgi.ini
