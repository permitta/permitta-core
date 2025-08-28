#!/bin/bash
set -e

export PYTHONPATH=/app/permitta-core/src
export FLASK_APP=permitta-core.src.app

if [ "$1" = "start-server" ]; then
    echo "Starting server on port 8000..."
    exec uwsgi --http 0.0.0.0:8000 --master -p 4 -w src.uwsgi:app
else
    # Default: Run the CLI command
    echo "Running CLI command: $@"
    exec python -m cli.src.cli "$@"
fi