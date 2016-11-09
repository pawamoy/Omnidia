#!/usr/bin/env bash
. venv/bin/activate
. scripts/export_env.sh "$@"
./manage.py shell <<EOF
from graph import g
g.delete_all()
EOF
