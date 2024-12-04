#!/usr/bin/env bash
echo "Waiting for the DB server to start"
/docker_init/wait-for-it.sh "$POSTGRES_SERVER":"$POSTGRES_PORT" -t "$POSTGRES_TIMEOUT"

echo "Checking migrations"
cd /opt || exit

if /opt/app/env/bin/alembic check; then
    echo "Migrations are up to date. Applying upgrades."
    /opt/app/env/bin/alembic upgrade heads
else
    echo "Migrations are not up to date. Generating new migration."
    /opt/app/env/bin/alembic revision --autogenerate -m "Auto-generated migration"
    echo "Applying new migration."
    /opt/app/env/bin/alembic upgrade heads
fi

cd || exit
echo "Starting the server"
/opt/app/env/bin/gunicorn "$UVICORN_APP_NAME" --workers "$UVICORN_WORKERS" --worker-class uvicorn.workers.UvicornWorker --bind "$UVICORN_HOST":"$UVICORN_PORT" --timeout "$UVICORN_TIMEOUT"
