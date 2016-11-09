#!/usr/bin/env bash
. venv/bin/activate
./manage.py shell <<EOF
from graph import g
g.delete_all()
EOF
