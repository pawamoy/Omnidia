#!/usr/bin/env bash
. venv/bin/activate

export NEO4J_USER="${1:neo4j}"
export NEO4J_PASS="${2:admineo4j}"

./manage.py runserver
