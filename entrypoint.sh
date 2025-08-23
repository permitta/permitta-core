#!/bin/bash
set -e

# Set Python path
export PYTHONPATH=/app/permitta-core/src

if [ "$1" = "start-server" ]; then
    # Start the Flask app on port 8000
    echo "Starting Flask server on port 8000..."
    exec flask run --host=0.0.0.0 --port=8000
else
    # Default: Run the CLI command
    echo "Running CLI command: $@"
    exec python -m cli.src.cli "$@"
fi