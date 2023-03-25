#!/bin/sh -e

exec gunicorn -b 0.0.0.0:9999 --chdir application app:app
