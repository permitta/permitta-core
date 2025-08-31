#!/bin/bash
set -e

if [ "$1" = "start-server" ]; then
    echo "Running database migrations"
    exec alembic upgrade head

    echo "Starting server on port 8000..."
    exec uwsgi --http 0.0.0.0:8000 --master -p 4 -w src.uwsgi:app

# tests
elif [ "$1" = "test" ]; then
  if [ "$2" = "opa" ]; then
    opa test /app/opa/trino -v
  elif [ $2 == 'unit' ]; then
    cd /app && python -m pytest
  fi

# Default: Run the CLI command
else
    echo "Running CLI command: $@"
    exec python -m cli.src.cli "$@"
fi