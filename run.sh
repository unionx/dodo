#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
    echo "Running development server"
    exec python3 "dodo.py"
else
    echo "Running production server"
    exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/dodo.py --callable app --stats 0.0.0.0:9191
fi
