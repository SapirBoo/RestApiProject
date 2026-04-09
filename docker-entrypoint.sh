#!/bin/sh
echo "Waiting for DB..."

#until pg_isready -h db -p 5432 -U postgres
#do
#  echo "Postgres is unavailable - sleeping"
#  sleep 2
#done
sleep 5

echo "Postgres is up!"

echo "Running migrations..."
alembic upgrade head || exit 1

echo "Starting app..."
exec gunicorn -k uvicorn.workers.UvicornWorker app:app \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -