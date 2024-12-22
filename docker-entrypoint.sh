#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

export FLASK_APP=server.py
if [ ! -d "migrations" ]; then
    flask db init
fi

flask db migrate -m "Initial migration"
flask db upgrade

python server.py
