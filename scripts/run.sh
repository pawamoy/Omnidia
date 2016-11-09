#!/usr/bin/env bash
. venv/bin/activate
. scripts/export_env.sh "$@"
./manage.py runserver
